---
name: distributor-product-selection
description: Cross-platform product selection and sourcing analysis for distributors and dropshippers. Uses opencli plugins (aliexpress, alibaba-api buyer API, amazon) to cross-analyze supply channels (Alibaba distribution + AliExpress dropshipping) against retail channels (Amazon) and generate structured product research reports with margin calculations. Use this skill whenever the user mentions product selection, product research, finding products to sell, sourcing analysis, cross-border e-commerce sourcing, dropshipping product research, "what should I sell", "find winning products", comparing Alibaba vs AliExpress pricing, analyzing Amazon competition for sourcing decisions, or any task involving evaluating products across supply and retail platforms.
requires:
  bins:
    - opencli
  env:
    - ALI_APP_KEY
    - ALI_APP_SECRET
    - ALI_ACCESS_TOKEN
primaryEnv: ALI_ACCESS_TOKEN
homepage: https://github.com/lcturing0/skills
---

# Distributor Cross-Platform Product Selection

## Business Model

```
Supply / Dropship Channels                Retail Channels
┌─────────────┐                    ┌──────────────────┐
│ Alibaba     │  Distribution      │ Amazon           │
│ buyer API   │  (preferred)       │ (pricing & demand │
│ tiered/MOQ  │ ──────────────────→│  reference)       │
├─────────────┤                    ├──────────────────┤
│ AliExpress  │  Dropship          │ Shopify / TikTok │
│ search/prod │  (test products)   │ Shop / Wix       │
│ zero stock  │ ──────────────────→│ (profit channels) │
└─────────────┘                    └──────────────────┘
```

**Core principles:**
- Alibaba buyer API returns **distribution products** (most with MOQ of 1) — always use this first
- AliExpress serves as a comparison supply channel (price benchmarking + dropship fallback)
- Amazon is used only as a retail reference (competitor pricing, market demand, trend validation)

---

## Prerequisites

### Environment Variables

The Alibaba buyer API requires these environment variables:

```
ALI_APP_KEY=<your_app_key>
ALI_APP_SECRET=<your_app_secret>
ALI_ACCESS_TOKEN=<your_access_token>
```

If `ALI_ACCESS_TOKEN` is not set or has expired, run the authorization flow:

```bash
# 1. Generate OAuth authorization URL
opencli alibaba-api auth-url "https://localhost/callback"
# 2. User authorizes in browser, obtains the code
# 3. Exchange code for token
opencli alibaba-api token-create "<code>"
# 4. Refresh expired token
opencli alibaba-api token-refresh "<refresh_token>"
```

### Plugin Check

Before starting, verify all three plugins are installed:

```bash
opencli plugin list
```

Required plugins: `aliexpress`, `alibaba-api`, `amazon`. Install any missing plugin with `opencli plugin install <name>`.

---

## Product Selection Workflow (5 Steps)

### Step 1: Define Selection Criteria

Confirm the following with the user (use reasonable defaults if not specified, and inform the user):

| Parameter | Description | Default |
|-----------|-------------|---------|
| Category keywords | Product types to research | Driven by trend discovery |
| Target market | Country/region for retail | US |
| Retail channel | Amazon / Shopify / TikTok Shop, etc. | All channels |
| Budget range | Expected per-unit sourcing cost | No limit |
| Result count | Number of categories to recommend | 5 |

If the user has no specific category in mind, use **trend discovery** first:

```bash
# Amazon Movers & Shakers — short-term growth signals
opencli amazon movers-shakers --limit 50 -f json

# Amazon New Releases — early momentum
opencli amazon new-releases --limit 50 -f json

# Amazon Best Sellers — specific category
opencli amazon bestsellers "<category_url>" --limit 50 -f json

# Alibaba distribution trend lists
opencli alibaba-api buyer-list US_GGS_Trendy --size 50 -f json
opencli alibaba-api buyer-list US_GGS_Hotselling --size 50 -f json
opencli alibaba-api buyer-list alibaba_picks --size 50 -f json
```

Extract 3–5 high-potential category keywords from the results, then proceed to Step 2.

---

### Step 2: Supply Channel Data Collection

For each target category keyword, **search Alibaba distribution products first, then AliExpress as a comparison**.

#### 2a. Alibaba Distribution Search (Priority)

```bash
# Keyword search for distribution products
opencli alibaba-api buyer-search "<keyword>" --size 20 -f json
```

Returns: `product_id`, `title`, `price`, `permalink`

For products with suitable pricing, get details:

```bash
# Product details — tiered pricing, SKUs, images
opencli alibaba-api buyer-desc <product_id> -f json

# Product attributes — material, dimensions, certifications
opencli alibaba-api buyer-attrs <product_id> -f json

# Product certifications — FCC/CE/UL, etc.
opencli alibaba-api buyer-cert <product_id> -f json

# Inventory check — by ship-from location
opencli alibaba-api buyer-inventory <product_id> --ship_from US -f json
opencli alibaba-api buyer-inventory <product_id> --ship_from CN -f json
```

#### 2b. Special Inventory Channels (Fast Delivery)

```bash
# Cross-border warehouse products (overseas warehouse, faster delivery)
opencli alibaba-api buyer-crossborder --size 30 -f json

# Overseas local warehouse products (US warehouse, 2–5 day delivery)
opencli alibaba-api buyer-local --size 30 -f json

# Local warehouse regular fulfillment
opencli alibaba-api buyer-local-regular --size 30 -f json

# Specific distribution product lists
opencli alibaba-api buyer-list US_CGS_48H --size 50 -f json    # US 48-hour delivery
opencli alibaba-api buyer-list US_GGS_48H --size 50 -f json    # US GGS 48-hour
opencli alibaba-api buyer-list US_GGS_POD --size 50 -f json    # Print on Demand
opencli alibaba-api buyer-list US_GGS_Branded --size 50 -f json # Branded distribution
```

Use `buyer-desc` to get details for returned product IDs.

#### 2c. Similar Product Discovery

After finding a strong product, expand the selection pool with recommendations and image search:

```bash
# Similar product recommendations
opencli alibaba-api buyer-rec <item_id> --type 2 --size 20 -f json

# Frequently bought together
opencli alibaba-api buyer-rec <item_id> --type 3 --size 20 -f json

# Image search — find same product from different suppliers
opencli alibaba-api buyer-image-search <item_id> --size 20 -f json
```

#### 2d. AliExpress Dropship Data (Comparison)

```bash
# Keyword search
opencli aliexpress search "<keyword>" --limit 20 -f json
```

Returns: `product_id`, `title`, `price_text`, `discount_text`, `orders_count`, `rating`

Get details for high-volume products:

```bash
opencli aliexpress product <product_id> -f json
```

Returns: `product_id`, `title`, `price_text`, `discount_text`, `orders_count`, `rating`, `store_name`

---

### Step 3: Retail Channel Data Collection (Amazon)

Use the Amazon plugin to get retail pricing, competitive landscape, and customer feedback.

#### 3a. Search Competitors

```bash
# Keyword search — understand competition and price ranges
opencli amazon search "<keyword>" --limit 20 -f json
```

Returns: `asin`, `title`, `price_text`, `rating_value`, `review_count`

#### 3b. Validate Top Competitors

For the top 3–5 ASINs from search results, get details:

```bash
# Product details
opencli amazon product <asin> -f json

# Seller and fulfillment info — FBA status, Amazon-sold check
opencli amazon offer <asin> -f json

# Review analysis — identify pain points and opportunities
opencli amazon discussion <asin> --limit 10 -f json
```

#### 3c. Category Rankings

```bash
# Category best sellers
opencli amazon bestsellers "<category_url>" --limit 30 -f json

# Movers & Shakers — growth signals
opencli amazon movers-shakers "<category_url>" --limit 30 -f json

# New Releases — new entrants
opencli amazon new-releases "<category_url>" --limit 30 -f json
```

---

### Step 4: Cross-Platform Analysis & Scoring

Aggregate data from all three platforms and score each candidate product on these dimensions:

#### Scoring Model (100 points max)

| Dimension | Weight | Data Source | Scoring Criteria |
|-----------|--------|-------------|------------------|
| **Profit margin** | 30% | Alibaba buyer-desc tiered price vs Amazon retail price | Gross margin >70% = full score, 50–70% = medium, <50% = low |
| **Market demand** | 25% | Amazon search review_count + bestseller rank | Reviews >5000 = full, 1000–5000 = medium |
| **Competition intensity** | 15% | Amazon search result count + Amazon-sold ratio from offers | Fewer Amazon-sold, more fragmented sellers = higher score |
| **Supply advantage** | 15% | Alibaba MOQ + inventory + overseas warehouse availability | MOQ ≤5 with US warehouse = full score |
| **Differentiation potential** | 10% | Amazon discussion pain points + Alibaba buyer-attrs | Clear improvement opportunities = higher score |
| **Trend direction** | 5% | Amazon movers-shakers rank changes | Upward trend = higher score |

#### Profit Calculation Formula

```
Wholesale cost = Tiered price from Alibaba buyer-desc (MOQ 1 price)
Dropship cost  = price_text from AliExpress product
Retail reference = Median price of top 10 results from Amazon search
Shipping estimate = By category weight (light $2–3 / medium $4–6 / heavy $8+)

Gross margin (distribution) = (Retail ref - Wholesale cost - Shipping) / Retail ref × 100%
Gross margin (dropship)     = (Retail ref - Dropship cost) / Retail ref × 100%
```

---

### Step 5: Generate Report

Write the analysis results to a Markdown file with the following structure:

```markdown
# Distributor Product Selection Report

**Date**: YYYY-MM-DD
**Target market**: <market>
**Categories**: <keyword list>
**Data sources**: opencli aliexpress / alibaba-api (buyer) / amazon

## 1. Category Recommendations Overview
<!-- Summary table: Rank, Category, Rating(★), Alibaba price, AliExpress price, Amazon retail price, Margin, Recommendation reason -->

## 2. Detailed Analysis by Category
### N. <Category> — <Rating>
#### Alibaba Distribution Data
<!-- Table: Product, Supplier, Tiered price, MOQ, SKU count, Overseas warehouse -->
#### AliExpress Dropship Comparison
<!-- Table: Product, Dropship price, Rating, Sales volume -->
#### Amazon Retail Competition
<!-- Table: ASIN, Product, Price, Rating, Reviews, FBA status -->
#### Profit Calculation
<!-- Table: Supply mode, Cost breakdown, Retail price, Gross profit, Margin -->
#### Customer Pain Points & Differentiation Opportunities
<!-- From Amazon discussion negative review analysis -->

## 3. Supply Mode Recommendations
<!-- AliExpress dropship vs Alibaba distribution: when to use which at each stage -->

## 4. Retail Channel Strategy
<!-- Analysis of which categories suit Amazon / Shopify / TikTok Shop -->

## 5. Action Items
<!-- This week / next week / ongoing: specific steps with product_ids -->
```

Save the report to `product-research/product-selection-report.md` in the working directory.

---

## Command Quick Reference

### AliExpress (Supply / Dropship)

| Command | Purpose | Key Parameters |
|---------|---------|----------------|
| `opencli aliexpress search "<kw>" --limit N -f json` | Search products | keyword, limit |
| `opencli aliexpress product <id> -f json` | Product details | product_id or URL |

### Alibaba Buyer API (Distribution Products — Use First)

| Command | Purpose | Key Parameters |
|---------|---------|----------------|
| `opencli alibaba-api buyer-search "<kw>" --size N -f json` | Search distribution products | keyword, size |
| `opencli alibaba-api buyer-desc <id> -f json` | Product details (tiered pricing/SKU) | product_id |
| `opencli alibaba-api buyer-attrs <id> -f json` | Product attributes | product_id |
| `opencli alibaba-api buyer-cert <id> -f json` | Product certifications | product_id |
| `opencli alibaba-api buyer-inventory <id> --ship_from US -f json` | Inventory check | product_id, ship_from |
| `opencli alibaba-api buyer-list <type> --size N -f json` | List by type | product_type, size |
| `opencli alibaba-api buyer-crossborder --size N -f json` | Cross-border warehouse products | size |
| `opencli alibaba-api buyer-local --size N -f json` | Overseas local warehouse | size |
| `opencli alibaba-api buyer-local-regular --size N -f json` | Local warehouse regular fulfillment | size |
| `opencli alibaba-api buyer-rec <id> --type 2 -f json` | Similar product recommendations | item_id, type |
| `opencli alibaba-api buyer-image-search <id> -f json` | Image search | item_id |
| `opencli alibaba-api buyer-channel-import "<ids>" --ecology_type SHOPIFY -f json` | Import products to channel | product_ids, ecology_type |
| `opencli alibaba-api buyer-events <id> --event_type PRODUCT_LISTED --channel AMAZON -f json` | Listing event notification | product_id, event_type, channel |

**buyer-list product_type values:**
`US_CGS_48H`, `US_GGS_48H`, `US_TOTAL_48H`, `US_GGS_Hotselling`, `US_GGS_POD`, `US_GGS_Branded`, `US_GGS_Trendy`, `MX_GGS_48H`, `EU_GGS_48H`, `crossborder`, `alibaba_picks`

**buyer-rec type values:** `1` = image search, `2` = similar products, `3` = frequently bought together

**buyer-inventory ship_from values:** `CN`, `US`, `UK`, `CA`, `AU`, `DE`, `FR`, `VN`, `TR`

### Alibaba Authorization

| Command | Purpose |
|---------|---------|
| `opencli alibaba-api auth-url "<redirect_uri>"` | Generate OAuth authorization URL |
| `opencli alibaba-api token-create "<code>"` | Exchange auth code for access_token |
| `opencli alibaba-api token-refresh "<refresh_token>"` | Refresh expired token |

### Amazon (Retail Channel)

| Command | Purpose | Key Parameters |
|---------|---------|----------------|
| `opencli amazon search "<query>" --limit N -f json` | Search products | query, limit |
| `opencli amazon product <asin> -f json` | Product details | ASIN or URL |
| `opencli amazon offer <asin> -f json` | Seller / fulfillment info | ASIN |
| `opencli amazon discussion <asin> --limit N -f json` | Review analysis | ASIN, limit |
| `opencli amazon bestsellers [url] --limit N -f json` | Best sellers | category URL, limit |
| `opencli amazon new-releases [url] --limit N -f json` | New releases | category URL, limit |
| `opencli amazon movers-shakers [url] --limit N -f json` | Movers & Shakers | category URL, limit |

---

## Execution Notes

1. **Always use `-f json` for all opencli commands** for easy parsing and aggregation.
2. **Alibaba buyer API commands require `ALI_ACCESS_TOKEN`**. Check before execution; if not set or if an auth error is returned, guide the user through the OAuth flow.
3. **The alibaba-api buyer commands are the core** — always use `buyer-search` for distribution products, not `product-search` or `product-list` (those are seller-perspective, not distribution).
4. **Get `buyer-desc` details for at least 3 Alibaba distribution products per category** to ensure tiered pricing data is available for margin calculations.
5. **Amazon data determines the retail price band** — use the median price of the top 10 `amazon search` results as the pricing reference.
6. **AliExpress data serves as a dropship cost benchmark** — compare against Alibaba distribution pricing to quantify the cost advantage of distribution.
7. **Timeout handling**: opencli commands using browser scraping can be slow; set a 60-second timeout per command. Alibaba buyer API commands (Strategy: public) do not use browser scraping and are faster.
8. **Pagination**: use the `--index` parameter to paginate (starting from 0) when more data is needed.

## Post-Selection Actions

After product selection is complete, use the Alibaba buyer API channel import feature to push distribution products directly to your store:

```bash
# Bulk import selected products to Shopify
opencli alibaba-api buyer-channel-import "product_id1,product_id2,product_id3" \
  --ecology_type SHOPIFY -f json

# Notify Alibaba that a product has been listed on Amazon
opencli alibaba-api buyer-events <product_id> \
  --event_type PRODUCT_LISTED --channel AMAZON -f json
```

Supported channels (`ecology_type`): `SHOPIFY`, `WIX`, `MERCADO`, etc.
Supported event notification channels (`channel`): `SHOPIFY`, `AMAZON`, `TEMU`, `WALMART`, `SHEIN`, `MERCADO`, etc.
