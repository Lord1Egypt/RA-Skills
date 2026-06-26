---
name: best-shopify-stores
description: Discover the best Shopify stores with PPSPY by filtering stores by traffic, revenue, language, region, theme, and single-product characteristics.
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

# Best Shopify Stores

Find and compare top Shopify stores using revenue, traffic, theme, region, and store structure signals.

Keywords: Best Shopify Stores.

## Setup

1. Visit the official website at [ppspy.com](https://www.ppspy.com/) to view real-time dashboard data and product UI.
2. Visit the direct API site at [api.ppspy.com](https://api.ppspy.com/) to get your API key and manage billing/recharge.
3. Set the environment variable: `PPSPY_API_KEY`

## Available Tools (6 total)

### Shopify Store Discovery (6 tools)
- `ppspy_shopify_store_list` — Search and filter Shopify stores by region, language, revenue, traffic, theme
- `ppspy_shopify_store_details` — Get detailed information for a specific Shopify store
- `ppspy_shopify_store_traffic_list` — Search Shopify stores with traffic data
- `ppspy_shopify_single_product_store_list` — Search single-product Shopify stores
- `ppspy_shopify_theme_store_list` — Search Shopify stores by theme
- `ppspy_shopify_theme_list` — Get Shopify themes

## Usage Examples

- "Find the best Shopify stores by monthly revenue"
- "Show top Shopify stores in the US beauty niche"
- "List Shopify stores with strong traffic using this theme"
- "Find single-product Shopify stores worth studying"
- "Get details for this top-performing Shopify store"

## Credits

Each API call consumes credits from your PPSPY account:
- **Shopify Store Search**: 1 credit per record
- **Detail/Supplement APIs**: Free
