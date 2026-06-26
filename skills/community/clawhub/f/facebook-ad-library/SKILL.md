---
name: facebook-ad-library
description: Search Facebook Ad Library and Meta Ad Library data with PPSPY. Analyze ads, advertiser stores, landing pages, and ad products from one focused skill.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PPSPY_API_KEY
      bins:
        - npm
    install:
      command: npm
      args:
        - install
        - -g
        - "ppspy-mcp-server@1.0.1"
    primaryEnv: PPSPY_API_KEY
    emoji: "🔍"
    homepage: https://www.ppspy.com
    mcpServers:
      ppspy:
        command: ppspy-mcp-server
        env:
          PPSPY_API_KEY: "{{PPSPY_API_KEY}}"
---

# Facebook Ad Library

Search Facebook Ad Library and Meta Ad Library data across ads, ad-linked stores, and ad products.

Keywords: Facebook Ad Library, Meta Ad Library, FB library, FB library product, FB library store.

## Setup

1. Visit the official website at [ppspy.com](https://www.ppspy.com/) to view real-time dashboard data and product UI.
2. Visit the direct API site at [api.ppspy.com](https://api.ppspy.com/) to get your API key and manage billing/recharge.
3. Set the environment variable: `PPSPY_API_KEY`

## Available Tools (13 total)

### Ad Library - Ads (2 tools)
- `ppspy_advertisement_list` — Search Facebook ads with advanced filters: keyword, audience reach, spend, status
- `ppspy_advertisement_details` — Get detailed information for a specific advertisement

### Ad Library - Stores (8 tools)
- `ppspy_ad_store_list` — Search ad library stores with advanced filters
- `ppspy_ad_store_details` — Get detailed information for a specific ad store
- `ppspy_ad_store_landing_page_stats` — Get landing page statistics
- `ppspy_ad_store_advertising_trends` — Get advertising trends over time
- `ppspy_ad_store_placement_analysis` — Get ad placement analysis (day/time breakdown)
- `ppspy_ad_store_content_most_used` — Get most used ad copy content
- `ppspy_ad_store_content_longest_run` — Get longest running ad content
- `ppspy_ad_store_advertiser_list` — Get advertisers associated with a store

### Ad Library - Products (2 tools)
- `ppspy_ad_product_list` — Search ad library products with advanced filters
- `ppspy_ad_product_details` — Get detailed information for a specific ad product

### Supplement (1 tool)
- `ppspy_ad_filter_options` — Get ad filter options (button types/texts)

## Usage Examples

- "Search Facebook Ad Library for pet ads running over 30 days"
- "Show me Meta Ad Library stores in beauty"
- "Find FB library products with high audience reach"
- "Get landing page stats for this ad store"
- "List the advertisers associated with this store"

## Credits

Each API call consumes credits from your PPSPY account:
- **Ad Library Search (Ads/Stores/Products)**: 2 credits per record
- **Detail/Analysis/Supplement APIs**: Free
