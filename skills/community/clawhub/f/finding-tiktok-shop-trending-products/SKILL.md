---
name: finding-tiktok-shop-trending-products
description: >
  Finds trending products on TikTok Shop using apidojo's TikTok scraper on Apify.
  Triggers when the user asks to: find trending TikTok Shop products, discover what products are
  selling on TikTok Shop right now, identify viral TikTok Shop items in a category, find trending
  items with TikTok affiliate links, research TikTok Shop bestsellers, discover products going
  viral on TikTok for e-commerce, find hot items being promoted by TikTok creators, or build a
  trending product list from TikTok Shop data.
  Returns product name, creator promotion count, engagement signals, price range, and trend momentum.
  Ideal for TikTok Shop sellers, dropshippers, and e-commerce trend researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-scraper
---

# Finding TikTok Shop Trending Products

Identifies products gaining momentum on TikTok Shop by analyzing creator promotion density and engagement. A product promoted by many creators simultaneously is a strong viral commerce signal.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | TikTok URLs — user profiles, hashtags, music pages, search, locations |
| `keywords` | array | Optional | `[]` | Search keywords/terms to find posts |
| `sortType` | string | Optional | `RELEVANCE` | Sort order for keyword results: `RELEVANCE`, `MOST_LIKED`, `DATE_POSTED` |
| `location` | string | Optional | — | ISO 3166-1 alpha-2 country code for regional filtering (e.g. `US`, `GB`) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return across the run |
| `includeSearchKeywords` | boolean | Optional | `false` | Add the matched search keyword field to each post |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search TikTok Shop hashtags for category
- [ ] Step 2: Extract products from promotional posts
- [ ] Step 3: Count creator promotion density per product
- [ ] Step 4: Score product trend momentum
- [ ] Step 5: Deliver trending product list
```

### Step 1: Search Posts


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input:
{
  "keywords": ["#tiktokshop[category]", "#[category]deals", "#tiktokmademebuyit"],
  "maxItems": 300
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["#tiktokmademebuyit", "#skincaretiktokshop"], "maxItems": 300}'
```

### Step 2: Score Products

Group posts by product name from captions. For each product:
```
promotion_density = count(unique creators promoting product)
total_reach = sum(playCount for all promoting posts)
engagement_rate = sum(diggCount) / total_reach * 100

trend_score = (promotion_density / 5, max 1) * 0.35
            + (total_reach / 1000000, max 1) * 0.35
            + (engagement_rate > 3 ? 1 : engagement_rate/3) * 0.30
```

**Trend window:** 70%+ promotions in last 7 days = `PEAKING`; spread evenly = `SUSTAINED`; mostly > 7 days = `FADING`

### Step 3: Edge Cases

- **Product name extraction unreliable**: Extract most specific noun phrase from caption alongside shop link
- **Same product different variants**: Group by product name similarity; sum reach across variants
- **Saturated trend** (> 50 creators): Window may be closing; flag as `LATE_STAGE`
- **Counterfeit signals**: Price far below market (e.g. < $5 for normally $30+ item) → flag

## Output Format

```
# TikTok Shop Trending Products: [CATEGORY]
Posts analyzed: [N] | Unique products: [N] | Date: [DATE]

## Trending Now (Peak Momentum)
| Product | Creators | Total Views | Avg Eng Rate | Stage | Score |
|---------|---------|------------|-------------|-------|-------|

## Sustained Performers
| Product | Creators | Total Views | Stage |
|---------|---------|-----------|-------|

## Saturation Alert
[Products with > 30 creators — difficult to enter profitably]
```

## Troubleshooting

**Few products identified**: Check bio links of top promoting creators for product page.
**Trend already peaked**: Run every 3-4 days to catch trends early.
**Suspicious pricing**: Flag and verify before sourcing.

