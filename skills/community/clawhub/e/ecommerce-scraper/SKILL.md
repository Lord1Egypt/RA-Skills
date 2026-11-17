---
name: ecommerce-scraper
description: Scrape product pages and search marketplace listings through ToolRouter's MCP server - product title, price, variants, images and specs from any store URL (Shopify detected automatically), plus listings from eBay, Facebook Marketplace, Vinted, Gumtree, Craigslist, Mercado Libre, OLX, Rakuten, Carousell, Trade Me and Google Shopping. Use for competitor pricing, product research, resale price checks and listing monitoring.
metadata: {"homepage":"https://toolrouter.com/tools/product-scraper","openclaw":{"emoji":"🛒","requires":{"bins":[],"env":[]}}}
---

# E-commerce Scraper

Turn store pages and marketplace searches into structured product data from one MCP connection. No scraper to host and no marketplace developer accounts.

## Installation

Install with `pnpm dlx skills add Humanleap/agent-skills --skill ecommerce-scraper`. Connect the client's remote MCP server to `https://api.toolrouter.com/mcp` (Claude: Customize → Connectors → Add custom connector; Claude Code: `claude mcp add toolrouter -- npx -y toolrouter-mcp`). Setup: https://toolrouter.com/docs/markdown/quickstart.

## Hard Rules

1. **One URL, one product.** `scrape_product` takes a direct product page, not a category or search page. Use `web-scraper` for anything else.
2. **Use the exact operation.** Pick the `tool` and `skill` below, or call `discover`. Never invent an input field.
3. **Prices are a snapshot.** Report the currency and when you pulled it. Marketplace prices come from indexed listing text and can be stale; open the listing before relying on a price.
4. **Respect site terms.** Marketplace search uses search-engine indexes, not logins. Do not try to bypass sign-in walls.

## Authentication and Cost

The server provisions an anonymous account on first use. Paid calls need credits: if `use_tool` returns a claim link, give it to the user so they can sign in and add credits. `discover` shows the live price for each operation; `listing_details` and `source_coverage` are free.

## Core Workflow

1. **Search the market.** `marketplace-search/search_listings` with the item, region and condition.
2. **Inspect listings.** `marketplace-search/listing_details` on the URLs worth a closer look (free).
3. **Scrape the stores.** `product-scraper/scrape_product` on competitor product pages for price, variants, specs and images.
4. **Read the rest of the site.** `web-scraper/scrape_page` for pricing pages, shipping and returns policies or category pages.
5. **Summarise.** Table of source, title, price, currency, condition and URL, with the low, median and high price.

## Essential Operations

| Job | `tool` | `skill` | Input |
|---|---|---|---|
| Full product details from a store page | `product-scraper` | `scrape_product` | `{"url":"https://store.example.com/products/item","include_images":false}` |
| Search marketplaces for an item | `marketplace-search` | `search_listings` | `{"query":"sony wh-1000xm5","regions":["UK"],"condition":"used","limit":10}` |
| One marketplace only | `marketplace-search` | `search_listings` | `{"query":"herman miller aeron","source":"ebay","country":"gb"}` |
| Preview one listing | `marketplace-search` | `listing_details` | `{"url":"<listing url>"}` |
| Compact price snapshot to track over time | `marketplace-search` | `watchlist_snapshot` | `{"query":"steam deck oled","regions":["UK"]}` |
| Which marketplaces cover a region | `marketplace-search` | `source_coverage` | `{"regions":["EU"]}` |
| Any other page as markdown | `web-scraper` | `scrape_page` | `{"url":"https://example.com/pricing"}` |

Call these through `use_tool` with `tool`, `skill` and `input`. Sources: `shopping_index`, `ebay`, `facebook_marketplace`, `craigslist`, `gumtree`, `trademe`, `mercadolibre`, `olx`, `rakuten`, `vinted`, `carousell`.

## Common Patterns

- **Competitor price check:** scrape the same product on 3 to 5 competitor stores and line up price, variants and stock.
- **Resale value:** `search_listings` with `condition:"used"` across eBay, Vinted and Facebook Marketplace; quote the price range, not one listing.
- **Sourcing:** search by model number across regions, then open the cheapest listings with `listing_details`.
- **Monitoring:** run `watchlist_snapshot` on a schedule and diff against the last snapshot the user saved; the tool does not store state.
- **Ad + product research:** pair with `ad-library-scraper` to see which products a competitor advertises, then scrape those product pages.

## Gotchas

- Shopify stores are detected automatically. Other stores use AI extraction, so check odd fields against the page.
- `scrape_product` saves images to the user's file space by default; set `include_images:false` when only data is needed.
- Marketplace coverage depends on the search index for that market. Run `source_coverage` before promising a country.
- Results can include search or category pages and other regions. Keep rows whose `source_region` matches the user's market and whose snippet names the exact item.
- Listing prices may be missing or in local currency; never convert currencies without saying so.

## Quick Reference

**Connect → search listings → inspect → scrape product pages → price table with sources and dates.**

More: https://toolrouter.com/tools/product-scraper · https://toolrouter.com/tools/marketplace-search · https://toolrouter.com/tools/web-scraper
