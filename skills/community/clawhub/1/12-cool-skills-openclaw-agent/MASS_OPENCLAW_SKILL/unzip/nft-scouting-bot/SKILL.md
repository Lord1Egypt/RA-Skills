---
name: nft-scouting-bot
description: Identifies trending NFT collections on specified platforms based on user-defined metrics. Use this when a user wants to scout for promising NFT projects or collections.
---

# NFT Scouting Bot

This skill enables the agent to act as an NFT scout, identifying trending and potentially profitable NFT collections on various platforms. It leverages key performance indicators (KPIs) and user-specified platforms to provide timely insights.

## Prerequisites

No specific prerequisites other than the user being able to specify their preferred NFT platform and desired scouting metrics.

## Workflow

When a user requests to scout for NFT collections, follow these steps:

### 1. Gather User Preferences

- **Ask for Platform**: Prompt the user to specify which NFT platform they want to scout (e.g., OpenSea, Magic Eden, Blur, Tensor). If no platform is specified, ask the user to choose from the popular platforms listed in `references/nft_scouting_guide.md`.
- **Ask for Indicators**: Inquire about the specific metrics or indicators the user is most interested in (e.g., "highest 24h volume," "fastest floor price growth," "collections with low listing percentage"). If no specific indicators are given, use a general approach focusing on a combination of volume, floor price growth, and sales count as outlined in `references/nft_scouting_guide.md`.

### 2. Navigate and Analyze Platform Data

- **Open Platform in Browser**: Use your browser tool to navigate to the specified NFT platform. Refer to `references/nft_scouting_guide.md` for direct links to the statistics or rankings pages of popular platforms.
- **Locate Trending Collections**: On the chosen platform, navigate to the "Trending," "Rankings," or "Stats" section. This usually provides an overview of top-performing collections.
- **Extract Key Data**: Visually inspect and extract data for collections that show significant positive movement based on the user's preferred indicators (or general KPIs). Focus on:
    - **Floor Price**: Current lowest price of an NFT in the collection.
    - **Volume**: Trading volume over the last 24 hours or 7 days.
    - **Sales Count**: Number of individual NFT sales.
    - **Unique Holders**: Growth in the number of distinct owners.
    - **Listing Rate**: Percentage of the collection listed for sale.

### 3. Identify Promising Collections

Based on the extracted data and the user's criteria, identify 3-5 collections that exhibit strong upward trends or meet the specified indicators for a promising investment.

### 4. Report Findings to User

Present your findings to the user in a clear and concise report. For each identified collection, include:

- **Collection Name**
- **Key Metrics**: Floor price, 24h/7d volume, sales count, and any other relevant indicators.
- **Reason for Recommendation**: Briefly explain why this collection is considered promising based on the scouting criteria.
- **Platform Link**: Provide a direct link to the collection on the respective platform for the user to conduct further due diligence.

## References

- `references/nft_scouting_guide.md`: Contains a detailed guide on key NFT performance indicators and a list of popular NFT platforms with their respective URLs for scouting.
