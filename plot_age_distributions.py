
# coding: utf-8

# # Interrogating building age distributions
# 
# This notebook is to explore the distribution of building ages in
# communities in Western Australia.

from os.path import join as pjoin
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import re
import seaborn as sns
sns.set_context("poster")
sns.set_style('darkgrid')


# Apply GA colour palette
palette = sns.blend_palette(["#5E6A71", "#006983", "#72C7E7",
                             "#A33F1F", "#CA7700", "#A5D867", 
                             "#6E7645"], 7)


# The source file `WA_Residential_Wind_Exposure_2018_TCRM.CSV` can be
# found in HPRM D2018-6256. Download a local version (by using the
# 'Supercopy' option when right-clicking on the record), and change
# the path to the appropriate folder.


inputFile = "C:/WorkSpace/data/derived/exposure/WA/WA_Residential_Wind_Exposure_2018_TCRM.CSV"

df = pd.read_csv(inputFile)

output_path = "C:/Workspace/data/derived/exposure/WA/"

SA2_names = sorted(list(pd.unique(df['SA2_NAME'])))
ages = sorted(list(pd.unique(df['YEAR_BUILT'])))

print(ages)
def plotAgeDist(df, locality):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    locdf = df[df['SA2_NAME'] == locality]
    sns.countplot(x="YEAR_BUILT", data=locdf, order=ages, ax=ax,
                 palette=palette)

    ax.set_xlabel("Year built")
    ax.set_ylabel("Number")
    plt.setp(ax.get_xticklabels(), rotation=90)
    ax.set_title("{0} - {1:,} residential buildings".format(locality, len(locdf.index)))
    """
    ax = fig.add_subplot(122)
    suburblist = locdf[locdf['SUBURB'].notnull()]['SUBURB']
    suburbs = sorted(list(pd.unique(suburblist)))
    sns.countplot(x='SUBURB', hue='YEAR_BUILT', data=locdf,
                  order=suburbs, hue_order=ages,
                  palette=palette,ax=ax)
    ax.set_xlabel("Suburb")
    ax.set_ylabel("Number")
    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels = [l.replace(' ', '\n').title() for l in labels]

    ax.set_xticklabels(labels)
    locs, labels = plt.xticks()

    plt.setp(labels, rotation=90)
    l = ax.legend(title="Year built", ncol=2)
    """
    fig.tight_layout()
    fig.savefig(pjoin(output_path, "{0}_SA2_AgeProfile.png".format(locality)))
    plt.clf()
    plt.close('all')


# There's two aspects to the age distribution - communities where
# there has been substantial growth since the last significant
# cyclone, and communities with a large proportion of older (pre-1980)
# era construction.

# TODO: 
# 1. Add a chart that ranks the localities by proportion of a
# selected age group. The list of age groups is already compiled
# (`ages`), just need to do the calculations to get proportions for
# the specified age group.  
# 2. Add another figure that plots the
# predominant age group for each suburb in the locality. If there's a
# spatial layer of the boundaries for `SUBURB_2015`, then one could
# plot up a categorised map of the suburbs based on predominant age
# group.

# In[26]:


def plotBySuburb(df, locality):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    locdf = df[df['SA2_NAME'] == locality]
    suburblist = locdf[locdf['SUBURB'].notnull()]['SUBURB']
    suburbs = sorted(list(pd.unique(suburblist)))
    sns.countplot(x='SUBURB', hue='YEAR_BUILT', data=locdf,
                  order=suburbs, hue_order=ages,
                  palette=palette,ax=ax)
    ax.set_xlabel("Suburb")
    ax.set_ylabel("Number")
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    l = ax.legend(title="Year built", ncol=2)
    ax.set_title("{0} - {1:,} residential buildings".format(locality, len(locdf.index)))
    fig.tight_layout()
    plt.savefig(pjoin(output_path, "{0}_SA2_SuburbAgeProfile.png".format(locality)))
    plt.close('all')

#for SA2 in SA2_names:
#    print(SA2)
#    plotAgeDist(df, SA2)
#    plotBySuburb(df, SA2)

# For the Perth region, we perform the analysis at a larger
# aggregation, due to the number of suburbs that make up the Greater
# Perth area.

# In[28]:


urbanareas = sorted(list(pd.unique(df['UCL_NAME'])))[1:]
cities = sorted(list(pd.unique(df['SA2_NAME'])))


# In[29]:


regex = re.compile(r"\([A-Z]\)")
def plotAgeDistCity(df, locality):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    locdf = df[df['UCL_NAME'] == locality]
    sns.countplot(x="YEAR_BUILT", data=locdf, order=ages, ax=ax,
                  palette=palette)

    ax.set_xlabel("Year built")
    ax.set_ylabel("Number")
    plt.setp(ax.get_xticklabels(), rotation=90)
    ax.set_title("{0} - {1:,} residential buildings".format(locality, len(locdf.index)))
    """
    suburblist = locdf[locdf['SA2_NAME'].notnull()]['SA2_NAME']
    suburbs = sorted(list(pd.unique(suburblist)))
    sns.countplot(x='SA2_NAME', hue='YEAR_BUILT', data=locdf,
                  order=suburbs, hue_order=ages,
                  palette=palette,ax=ax[1])
    ax[1].set_xlabel("Suburb")
    ax[1].set_ylabel("Number")
    labels = [item.get_text() for item in ax[1].get_xticklabels()]
    
    labels = [re.sub(regex, "", l) for l in labels]

    ax[1].set_xticklabels(labels)
    locs, labels = plt.xticks()

    plt.setp(labels, rotation=90)
    l = ax[1].legend(title="Year built", ncol=2)
    """
    fig.tight_layout()
    plt.savefig(pjoin(output_path, "{0}_UCL_AgeProfile.png".format(locality.replace('/','-'))))
    plt.close('all')



def plotByCity(df, locality):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    locdf = df[df['UCL_NAME'] == locality]
    #suburblist = locdf[locdf['LGA_NAME'].notnull()]['LGA_NAME']
    #suburbs = sorted(list(pd.unique(suburblist)))
    suburbs = locdf.groupby(['SUBURB', 'YEAR_BUILT']).size()
    ageprofile = suburbs.groupby(level=0).apply(lambda x: 100*x/float(x.sum()))
    cmap = ListedColormap(palette.as_hex())

    try:
        ageprofile.unstack().plot(kind='barh', stacked=True, ax=ax, cmap=cmap)
    except AttributeError:
        print("Skipping {0}".format(locality))
        
    else:
        ax.set_xlabel("Percentage")
        ax.set_xlim((0,100))
        ax.set_ylabel("Suburb")
        labels = [item.get_text() for item in ax.get_yticklabels()]
        ax.set_yticklabels([re.sub(regex, "", l).title() for l in labels])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                  fancybox=True, shadow=True, ncol=7)

        """
        sns.countplot(x='LGA_NAME', hue='YEAR_BUILT', data=locdf,
                      order=suburbs, hue_order=ages,
                      palette=palette,ax=ax)
        ax.set_xlabel("Local Government Area")
        ax.set_ylabel("Number")

        labels = [item.get_text() for item in ax.get_xticklabels()]
        labels = [re.sub(regex, "", l) for l in labels]
        ax.set_xticklabels(labels)
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=90)
        l = ax.legend(title="Year built", ncol=2)
        """
        ax.set_title("{0} - {1:,} residential buildings".format(locality, len(locdf.index)))
        fig.tight_layout()

        plt.savefig(pjoin(output_path, "{0}_UCL_LGAAgeProfile.png".format(locality.replace('/','-'))),bbox_inches="tight" )
        plt.close(fig)

for ua in urbanareas:
    print(ua)
    plotAgeDistCity(df, ua)
    plotByCity(df, ua)
    

locdf = df[df['UCL_NAME'] == 'Geraldton']
suburbs = locdf.groupby(['SUBURB', 'YEAR_BUILT']).size()
ageprofile = suburbs.groupby(level=0).apply(lambda x: 100*x/float(x.sum()))

f,ax = plt.subplots()
cmap = ListedColormap(palette.as_hex())
ageprofile.unstack().plot(kind='barh', stacked=True, ax=ax, cmap=cmap)
ax.set_xlabel("Percentage")
ax.set_ylabel("Suburb")
labels = [item.get_text() for item in ax.get_yticklabels()]
labels = [l.title() for l in labels]
ax.set_yticklabels(labels)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=7)


urbanareas = sorted(list(pd.unique(df['UCL_NAME'])))[1:]
cities = sorted(list(pd.unique(df['SA2_NAME'])))
def plotByCity(df, locality):
    locdf = df[df['UCL_NAME'] == locality]
    suburbs = locdf.groupby(['LGA_NAME', 'YEAR_BUILT']).size()
    try:
        ageprofile = suburbs.groupby(level=0).apply(lambda x: 100*x/float(x.sum()))
    except AttributeError:
        print("Skipping {0}".format(locality))
        
    else:
        nsuburbs=len(suburbs)
        fig = plt.figure()
        ax = plt.add_subplot(111) #figsize=(12, nsuburbs/12))
        cmap = ListedColormap(palette.as_hex())
        ageprofile.unstack().plot(kind='barh', stacked=True, ax=ax, cmap=cmap)
        ax.set_xlabel("Percentage")
        ax.set_xlim((0,100))
        ax.set_ylabel("Local Government Area")
        labels = [item.get_text() for item in ax.get_yticklabels()]
        ax.set_yticklabels([re.sub(regex, "", l).title() for l in labels])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                  fancybox=True, shadow=True, ncol=7)
        fig.tight_layout()
        plt.show()
    


# Calculate the proportion of pre-1980 construction in each Statistical Area:

sa2 = df.groupby(['SA2_CODE','YEAR_BUILT',]).size().unstack(level=1)
sa2['PROP_1980'] = sa2[ages[:5]].sum(axis=1)/sa2[ages].sum(axis=1)
sa2.fillna(0).to_csv(pjoin(output_path, "SA2_building_age.csv"))


sa1 = df.groupby(['SA1_CODE', 'YEAR_BUILT']).size().unstack(level=1)
sa1['PROP_1980'] = sa1[ages[:5]].sum(axis=1)/sa1[ages].sum(axis=1)
sa1.fillna(0).to_csv(pjoin(output_path, "SA1_building_age.csv"))

