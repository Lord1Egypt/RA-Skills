---
name: finding-ecommerce-brands-for-outreach
description: >
  Discovers e-commerce and DTC brands on Instagram and TikTok using apidojo's scrapers on Apify.
  Triggers when the user asks to: find DTC brands on Instagram for outreach, discover Shopify brands
  on social media, identify e-commerce companies running TikTok shops, build an outreach list of
  online brands, find brands selling in a specific product category on social media, identify
  fast-growing DTC companies for partnerships or sales, or compile a list of online retailers
  active on Instagram or TikTok.
  Returns brand handle, follower count, bio, product category, and engagement rate.
  Ideal for wholesale suppliers, SaaS vendors targeting e-commerce, and B2B partnership teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/instagram-scraper, apidojo/tiktok-scraper
---

# Finding E-commerce Brands for Outreach

Finds DTC and e-commerce brands active on Instagram and/or TikTok by searching product-category hashtags and filtering accounts whose bios signal commercial activity (shop links, product keywords, "DTC", "founder", etc.).

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Define product category and target platform(s)
- [ ] Step 2: Build hashtag and keyword list
- [ ] Step 3: Scrape accounts from product hashtags
- [ ] Step 4: Filter for brand signals in bio
- [ ] Step 5: Rank and deliver outreach list
```

### Step 1: Clarify Parameters

Ask the user for:
- **Product category** (e.g., "skincare", "dog accessories", "home gym equipment")
- **Platform** — Instagram, TikTok, or both
- **Brand signals to look for** (e.g., shop links, "founder", "official", product-related keywords in bio)
- **Min followers** (default: 1,000 — filters out personal accounts)
- **Max followers** (optional — e.g., 500,000 to focus on emerging brands)
- **Number of brands** (default: 50)

### Step 2: Build Hashtag List

Generate product-category hashtags. Bias toward brand/seller hashtags, not consumer hashtags:
- Skincare → `#skincarebrand`, `#skincarefounder`, `#cleanbeauty`, `#skincareproducts`
- Dog accessories → `#dogbrand`, `#petbusiness`, `#dogaccessories`, `#handmadedogtoys`
- Home gym → `#homegymequipment`, `#fitnessbrand`, `#gymequipment`, `#fitnessproducts`

### Step 3: Scrape Platform(s)

**Instagram — If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "keywords": ["[hashtag1]", "[hashtag2]", "[hashtag3]"],
  "maxItems": 100
}
```

**TikTok — If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input:
{
  "keywords": ["[hashtag1]", "[hashtag2]"]
}
```

**REST API fallback (Instagram):**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["[hashtag1]", "[hashtag2]"], "maxItems": 100}'
```

**REST API fallback (TikTok):**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["[hashtag1]", "[hashtag2]"]}'
```

Collect unique account handles from results. Wait for `SUCCEEDED` before fetching dataset.

### Step 4: Filter for Brand Signals

From profile bios, keep accounts where ANY of the following are true:
- Bio contains a link (Linktree, Shopify store, website)
- Bio contains keywords: "shop", "founder", "CEO", "official", "buy", "available at", "®", "™"
- Bio contains product-specific language matching the category
- Profile is a business account (Instagram only: `businessCategoryName` field present)
- Follower count within specified range

Remove: personal accounts without shop signals, celebrity/influencer accounts (unless user wants these), accounts with 0 posts.

### Step 5: Rank and Format

Rank by engagement rate (likes + comments / followers) within follower range.

## Output Format

```
# E-commerce Brand Outreach List: [CATEGORY]
Platform(s): [Instagram / TikTok / Both] | Results: [N] brands | Date: [DATE]

| # | Handle | Platform | Followers | Category | Bio Excerpt | Website | Eng. Rate |
|---|--------|----------|-----------|----------|-------------|---------|-----------|
| 1 | @[name] | [IG/TT] | [N]       | [cat]    | [bio]       | [url]   | [X.X%]    |

## Highlights
- Fastest growing: @[handle] — [N] followers, [X.X%] engagement
- Most established: @[handle] — [N] followers, [N] posts
- Most active: @[handle] — posts [X]x per week

## Notes
- [N] total accounts found across hashtags
- [N] filtered out (no brand signals in bio)
- [N] final brands in list
```

## Troubleshooting

**Mostly personal accounts in results:** Use more brand-specific hashtags (e.g., `#[category]brand` instead of `#[category]`).
**Too few results:** Expand hashtag list or lower minimum follower count.
**Results from large established brands only:** Add `#small[category]brand`, `#indie[category]`, or `#handmade[category]` hashtags.



**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

