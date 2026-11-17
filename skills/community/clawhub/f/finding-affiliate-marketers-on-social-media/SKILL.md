---
name: finding-affiliate-marketers-on-social-media
description: >
  Finds affiliate marketers and performance marketing creators on Instagram and TikTok using apidojo's scrapers. Triggers when the user asks to: find affiliate marketers for a product category, discover creators running affiliate campaigns on social media, identify performance marketers promoting products in a niche, find social media affiliates for a brand program, discover who is promoting competitor affiliate links, build an affiliate creator recruitment list, or find content creators with affiliate marketing experience.
  Returns creator handle, platform, affiliate signal strength, niche focus, engagement rate, and promo code count.
  Ideal for affiliate program managers, e-commerce brands launching affiliate programs, and network managers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/instagram-scraper, apidojo/tiktok-scraper
---

# Finding Affiliate Marketers On Social Media

Executes finding affiliate marketers on social media using apidojo scrapers. Part of the apidojo intelligence skills library.

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
- [ ] Step 1: Define parameters
- [ ] Step 2: Run instagram-scraper
- [ ] Step 3: Filter and classify results
- [ ] Step 4: Score by quality and relevance
- [ ] Step 5: Deliver output
```

### Step 2: Run the Actor


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

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "searchTerms": ["#affiliate[niche]", "#[niche]code", "use code [NICHE]", "#commissioned"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["#affiliate[niche]", "#[niche]code", "use code [NICHE]", "#commissioned"], "maxItems": 100}'
```

Wait for `SUCCEEDED`. Fetch dataset:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN"
```

### Step 3: Classify Results

```
classification: ACTIVE_AFFILIATE (> 3 promo posts in 30 days) | OCCASIONAL_PROMOTER (1-3 posts) | AFFILIATE_AUDIENCE (uses affiliate content but doesn't produce it)
```

### Step 4: Score Each Result

```
score = affiliate_signal = (promo_code_post_count / total_posts * 100) * (avg_views_on_affiliate_posts / 1000)
```

### Step 5: Edge Cases

- **Distinguish genuine affiliates from brand employees — employees promote brand without code; affiliates promote with a trackable code or unique URL**

Additional fallbacks:
- **< 20 results**: Broaden search terms; remove secondary filters
- **No results**: Verify the search terms are correct; try alternate phrasings
- **Data quality issues**: Remove entries with missing key fields; note count in output

## Output Format

```
# Finding Affiliate Marketers On Social Media
Results: [N] | Date: [DATE]

| # | [Key Field] | [Metric 1] | [Metric 2] | [Classification] | [Score] |
|---|------------|-----------|-----------|-----------------|---------|
| 1 | [value] | [value] | [value] | [type] | [0.XX] |

## Summary
Top result: [description]
Key finding: [insight]
```

## Troubleshooting

**Too few results:** Broaden the primary search term; remove restrictive filters.
**Low quality results:** Apply minimum score threshold (≥ 0.50) to filter noise.
**Actor fails to run:** Verify API key; check actor status at apify.com/apidojo.

