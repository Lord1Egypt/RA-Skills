---
name: finding-instagram-ugc-creators-for-brands
description: >
  Finds Instagram UGC creators for brand campaigns using apidojo's Instagram scraper on Apify.
  Triggers when the user asks to: find Instagram UGC creators for product campaigns, discover
  micro-influencers posting organic product reviews on Instagram, identify creators for paid
  partnership posts or product seeding on Instagram, find authentic lifestyle creators in beauty
  food fitness or home decor, build an Instagram UGC creator list for a DTC brand, or find
  creators posting about a product category with strong engagement.
  Returns creator handle, follower count, avg likes, engagement rate, niche hashtags, and bio link.
  Ideal for DTC brands, e-commerce companies, and influencer campaign managers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Finding Instagram UGC Creators for Brands

Discovers Instagram micro-creators who produce authentic product content. Nano (1K–10K) and micro (10K–100K) creators on Instagram drive 3–5× higher engagement than macro-influencers on sponsored content.

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
- [ ] Step 1: Search niche hashtags on Instagram
- [ ] Step 2: Collect and deduplicate creator handles
- [ ] Step 3: Enrich profiles
- [ ] Step 4: Score UGC fit
- [ ] Step 5: Deliver creator list
```

### Step 1: Search Niche Hashtags

Target hashtags that UGC creators use (not brand accounts):
```
Primary: #[niche]review, #[niche]recommendations, #honest[niche]review
Supporting: #[niche]community, #[niche]lover, #[niche]obsessed
Broad: #[niche], #[niche]gram, #my[niche]
```


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
  "keywords": ["#[niche]review", "#[niche]recommendations", "#[niche]community"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "keywords": ["#skincarereviews", "#skincareobsessed", "#honestskincarereviews"],
    "maxItems": 100
  }'
```

Collect unique `ownerUsername` values from results.

### Step 2: Profile Enrichment

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "usernames": ["[username1]", "[username2]", "..."],
  "maxItems": 12
}
```

### Step 3: Score UGC Fit

```
engagement_rate = (avg_likes + avg_comments) / follower_count * 100

authenticity_signal = (is_not_verified ? 1 : 0) * 0.20
                    + (follower_count < 100000 ? 1 : 0.5) * 0.20
                    + (posts_with_product_content >= 3 ? 1 : posts/3) * 0.30
                    + (engagement_rate >= min_engagement_rate ? 1 : engagement_rate/min_engagement_rate) * 0.30
```

**Tier:** TIER 1 ≥ 0.75 | TIER 2 0.50–0.74 | TIER 3 < 0.50

### Step 4: Edge Cases

- **Brand ambassador accounts appear** (always using product): Check for `#ad` or `#sponsored` in every recent post — flag as `ALREADY_CONTRACTED`
- **Private accounts appear**: Skip — cannot assess content quality
- **Follower count doesn't match scrape**: If `follower_count = 0` in scrape output, retry profile fetch; Instagram sometimes throttles profile data
- **Location filter not matching**: Instagram bio location field is free-text — use contains match: bio.lower() contains country/city name

## Output Format

```
# Instagram UGC Creator List: [NICHE]
Creators evaluated: [N] | TIER 1: [N] | TIER 2: [N] | Date: [DATE]

## TIER 1 — Prime UGC Creators
| Creator | Handle | Followers | Avg Likes | Avg Comments | Eng Rate | Authenticity Score |
|---------|--------|-----------|-----------|--------------|----------|-------------------|
| [name] | @[handle] | [N] | [N] | [N] | [X%] | [0.XX] |

## TIER 2 — Worth Testing
| Creator | Followers | Avg Likes | Eng Rate | Location |
|---------|-----------|-----------|----------|---------|

## Top Performing Hashtags for This Niche
| Hashtag | Posts Found | Avg Likes per Post | Creator Quality (High/Med/Low) |
|---------|------------|-------------------|-------------------------------|
```

## Troubleshooting

**Hashtag returns only brand posts**: Add "review" or "honest" to hashtags to anchor on consumer voice.
**All creators already contracted**: Common in saturated niches — search adjacent sub-niches.
**Engagement rate < 3% across results**: Hashtag may be too popular and dominated by low-engagement accounts. Switch to long-tail hashtags like `#[niche][city]` or `#[brand]community`.

