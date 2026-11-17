---
name: finding-fitness-brands-on-tiktok
description: >
  Discovers fitness studios, wellness brands, and gym businesses on TikTok using apidojo's
  TikTok Scraper on Apify. Triggers when the user asks to: find fitness businesses on TikTok,
  discover gym brands for B2B outreach, build a list of wellness brands active on TikTok, find
  personal trainers or fitness studios by hashtag on TikTok, prospect health and fitness companies
  via TikTok content, or identify growing fitness brands for partnership or vendor sales.
  Returns video data, channel info (username, followers, verified), hashtags, and engagement metrics.
  Ideal for fitness SaaS vendors, equipment suppliers, and health brand partnership teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-scraper
---

# Finding Fitness Brands On Tiktok

---

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

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~tiktok-scraper" --input '{"keywords": ["fitness studio", "gym owner"], "sortType": "MOST_LIKED", "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~tiktok-scraper" --input '{"keywords": ["fitness studio", "gym owner"], "sortType": "MOST_LIKED", "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~tiktok-scraper" --input '{"keywords": ["fitness studio", "gym owner"], "sortType": "MOST_LIKED", "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["fitness studio", "gym owner"], "sortType": "MOST_LIKED", "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~tiktok-scraper` and the input above.

---

## Scoring & Ranking

Score each channel by:
- `followers` → normalized 0-1 (cap at 500K), weight 0.35
- `avg_engagement = (likes + comments + shares) / views` → weight 0.35
- `verified` → 0 or 1, weight 0.30

```python
score = 0.35 * min(followers / 500000, 1.0) + 0.35 * min(avg_engagement / 0.10, 1.0) + 0.30 * int(verified)
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | PRIME_PROSPECT |
| 0.40–0.69 | B | WARM_LEAD |
| < 0.40 | C | LOW_PRIORITY |

---

## Edge Cases

- **Mixed results with consumers**: Filter by channel.followers > 1000 to focus on established brands.
- **Keyword too broad**: "fitness" returns individual users. Use "fitness business", "gym owner", "fitness studio" instead.
- **No contact info in TikTok**: Cross-reference with Instagram or website links in bio.
- **Duplicate channels**: Same brand may appear multiple times — deduplicate by channel.username.
- **Inflated views**: TikTok can have high views but low followers for viral one-offs — balance both metrics.
