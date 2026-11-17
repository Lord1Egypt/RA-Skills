---
name: finding-brand-collaborations-on-tiktok
description: >
  Discovers brand collaboration patterns and sponsored content on TikTok using apidojo's TikTok
  scrapers on Apify. Triggers when the user asks to: find which brands are running TikTok
  influencer campaigns, discover creator-brand partnerships in a product category, identify
  which influencers are working with competitor brands on TikTok, see what sponsorship deals
  are active in a niche, find brands that sponsor TikTok creators, analyze competitor influencer
  marketing strategy on TikTok, or track paid partnership posts by category.
  Returns creator handle, brand name, post performance, estimated reach, and collaboration frequency.
  Ideal for influencer marketing teams, competitive intelligence analysts, and brand partnership managers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tiktok-scraper, apidojo/tiktok-profile-scraper
---

# Finding Brand Collaborations on TikTok

Maps active brand-creator partnerships in a product category. Identifies which brands are investing in TikTok influencer marketing, which creators they're working with, and the performance benchmarks for sponsored content.

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
- [ ] Step 1: Search sponsored content hashtags for category
- [ ] Step 2: Filter for sponsored signals
- [ ] Step 3: Extract brand and creator pairs
- [ ] Step 4: Analyze collaboration patterns
- [ ] Step 5: Deliver brand-creator map
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
  "keywords": ["#ad", "#sponsored", "#[category]partner", "#[category]collab"],
  "keywords": ["[BRAND_NAME] sent", "use code", "thanks to [CATEGORY] brand"],
  "maxItems": 300
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "keywords": ["#ad", "#sponsored", "#fitnesspartner"],
    "maxItems": 300
  }'
```

### Step 2: Extract Brand-Creator Pairs

From each sponsored post, extract:
- `brand_name`: From caption mention (`@[brand]`, `[Brand] sent me`, `thanks to [Brand]`)
- `creator_handle`: `authorMeta.name`
- `post_views`: `playCount`
- `post_date`: `createTime`
- `collaboration_type`: `#gifted` (product seeding) vs. `#ad`/`#sponsored` (paid)

### Step 3: Score Campaign Performance

```
sponsored_performance = playCount / 1000 (views in thousands)
creator_roi_proxy = playCount / followerCount  (view-to-follower ratio for sponsored post)
```

Brand collaboration frequency per creator:
```
collab_depth = count(posts where same brand appears) / total_posts_in_date_range
```

### Step 4: Edge Cases

- **No #ad hashtag but clearly sponsored**: Also scan for `"gifted"`, `"c/o"`, `"partnership"` in caption; TikTok disclosure is inconsistently applied
- **Brand name ambiguous** (e.g. "Nike" in sports context): Verify by checking if creator's bio mentions brand partnership or if post has dedicated product showcase format
- **< 20 sponsored posts found**: Category may be under-sponsored on TikTok; check if brands are using darker patterns (no disclosure) — widen search to product names alone

## Output Format

```
# TikTok Brand Collaboration Map: [CATEGORY]
Posts analyzed: [N] | Sponsored posts identified: [N] | Unique brands: [N] | Date: [DATE]

## Brands Running Active TikTok Campaigns
| Brand | # Creators Used | # Posts | Avg Views/Post | Collaboration Type |
|-------|----------------|---------|----------------|-------------------|
| [brand] | [N] | [N] | [N] | [Gifted/Paid/Mixed] |

## Creator-Brand Pairs
| Creator | @Handle | Brand | Posts | Avg Views | Collab Type | Est. Reach |
|---------|---------|-------|-------|-----------|-------------|-----------|
| [name] | @[handle] | [brand] | [N] | [N] | [Gifted/Paid] | [N] |

## Benchmark: Sponsored Post Performance in [CATEGORY]
- Median views for sponsored posts: [N]
- Top-performing brand campaign: [brand] — [N] avg views
- Most-used creator tier: [micro/macro/mega]
```

## Troubleshooting

**Disclosure data sparse**: TikTok doesn't always surface `#ad` in scraped captions. Check for brand mentions in text and product codes.
**Results outside the category**: Refine search by combining `#ad` with a niche keyword: `"#ad #fitness"` or `"#sponsored #skincare"`.
**Can't find competitor campaigns**: If competitor avoids disclosure, search for their brand @mention directly in TikTok search.

