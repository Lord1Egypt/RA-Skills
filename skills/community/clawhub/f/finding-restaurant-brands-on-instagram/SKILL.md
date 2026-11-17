---
name: finding-restaurant-brands-on-instagram
description: >
  Discovers restaurant brands, food businesses, and hospitality accounts on Instagram using
  apidojo's Instagram Scraper on Apify. Triggers when the user asks to: find restaurant brands
  on Instagram, discover food businesses for outreach on Instagram, build a list of restaurant
  Instagram accounts, find cafes or food chains active on Instagram, identify local restaurant
  brands by hashtag or location on Instagram, or prospect food and beverage businesses via their
  Instagram presence. Returns account handle, follower count, bio, post count, and engagement data.
  Ideal for food tech SaaS vendors, beverage distributors, and B2B service providers targeting restaurants.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Finding Restaurant Brands On Instagram

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~instagram-scraper" --input '{"startUrls": ["https://www.instagram.com/explore/tags/restaurantowner/"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~instagram-scraper" --input '{"startUrls": ["https://www.instagram.com/explore/tags/restaurantowner/"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~instagram-scraper" --input '{"startUrls": ["https://www.instagram.com/explore/tags/restaurantowner/"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.instagram.com/explore/tags/restaurantowner/"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~instagram-scraper` and the input above.

---

## Scoring & Ranking

Score each account by:
- `engagement_rate = (likeCount + commentCount) / followerCount` → weight 0.4
- `followerCount` → normalized 0-1, weight 0.3
- `has_business_bio` (bio contains phone/website/address keywords) → weight 0.3

```python
score = 0.4 * min(engagement_rate / 0.05, 1.0) + 0.3 * min(followerCount / 50000, 1.0) + 0.3 * int(has_business_bio)
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

- **Hashtag too broad**: `#food` returns millions of posts from consumers, not businesses. Use niche tags like `#restaurantowner` or `#foodbiz`.
- **No business in bio**: Filter by accounts that have website links or phone in bio.
- **Consumer accounts mixed in**: Filter by followerCount > 500 and postCount > 20.
- **Private account**: No post data — skip.
- **Duplicate accounts**: Same brand may post under multiple hashtags — deduplicate by username.
