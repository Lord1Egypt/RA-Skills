---
name: finding-instagram-creators-by-location
description: >
  Finds Instagram content creators and influencers posting from a specific location using
  apidojo's Instagram location scraper on Apify. Triggers when the user asks to: find Instagram
  creators based in a city, discover local influencers in a geographic market, find content
  creators who post from a specific venue or neighborhood, identify local Instagram micro-influencers
  for geo-targeted campaigns, find creators in a country for regional brand partnerships, or
  discover influencers who have visited or are based in a specific location.
  Returns creator handle, post count at location, follower estimate, engagement, and recent content.
  Ideal for regional brand campaigns, local business marketing, and geo-targeted influencer programs.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-location-scraper
---

# Finding Instagram Creators by Location

Identifies Instagram creators who actively post from a specific location — city, venue, or region. Creators with repeated location posts have genuine local presence and authentic ties to the place.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Instagram location page URLs |
| `locationIds` | array | Optional | `[]` | Instagram location IDs |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `until` | string | Optional | — | Date filter (YYYY-MM-DD) |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Resolve location ID
- [ ] Step 2: Run instagram-location-scraper
- [ ] Step 3: Identify repeat creators
- [ ] Step 4: Score creator quality
- [ ] Step 5: Deliver local creator list
```

### Step 1: Resolve Location ID

Instagram uses numeric location IDs. To find the ID:
1. Search for the location on Instagram (mobile or desktop)
2. Open the location page — URL format: `instagram.com/explore/locations/[LOCATION_ID]/[name]/`
3. Extract the numeric ID

If the user only provides a name, run a Google search:
`site:instagram.com/explore/locations "[LOCATION_NAME]"`

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-location-scraper"
Input:
{
  "locationIds": ["[LOCATION_ID]"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~instagram-location-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"locationIds": ["[LOCATION_ID]"], "maxItems": 100}'
```

### Step 3: Score Creator Quality

From location posts, group by `ownerUsername`. For each creator:

```
local_score = min(post_count_at_location / 5, 1) * 0.30  # repeat presence
            + (avg_likes / 100) * 0.25  # engagement quality
            + (avg_comments / 10) * 0.20  # comment depth
            + (has_website ? 1 : 0) * 0.15  # professional creator signal
            + (follower_count > 1000 ? 1 : 0) * 0.10
```

Clamp to [0, 1]. Tier: A ≥ 0.70 | B 0.40–0.69 | C < 0.40

### Step 4: Edge Cases

- **Location ID not found for small venue**: Try the city or neighborhood instead; scrape and filter by caption mentioning venue name
- **Tourist accounts dominate results** (one-time visitors): Filter by `post_count_at_location = 1` being lower priority than repeat posters
- **Business accounts posting from location**: If `is_business_account = true`, flag separately — these are brand accounts, not creator UGC
- **< 30 posts at location**: Small or new venue — lower `min_followers` threshold to 500; include more results

## Output Format

```
# Instagram Local Creators: [LOCATION_NAME]
Posts scraped: [N] | Unique creators: [N] | Repeat locals (2+ posts): [N] | Date: [DATE]

## TIER A — Established Local Creators (2+ Location Posts)
| Creator | @Handle | Location Posts | Avg Likes | Avg Comments | Content Theme | Score |
|---------|---------|---------------|-----------|--------------|---------------|-------|
| [name] | @[handle] | [N] | [N] | [N] | [food/lifestyle/travel] | [0.XX] |

## TIER B — Active Local Voices
| Creator | @Handle | Location Posts | Avg Likes | Last Post |
|---------|---------|---------------|-----------|----------|

## Niche Breakdown at [LOCATION]
| Content Theme | # Posts | Top Creator |
|--------------|---------|------------|
| [food] | [N] | @[handle] |
| [travel] | [N] | @[handle] |
```

## Troubleshooting

**Very few results for city**: City-level location IDs return general "in [city]" tags. Look for neighborhood or landmark IDs for denser results.
**Results are mostly tourist accounts**: Focus on the `post_count_at_location >= 3` tier — locals post from the same location repeatedly.
**Wrong city matches location name**: Some city names are duplicated globally. Verify the location page on Instagram before running.

