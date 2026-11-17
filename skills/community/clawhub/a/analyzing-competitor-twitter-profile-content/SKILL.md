---
name: analyzing-competitor-twitter-profile-content
description: >
  Extracts and analyzes tweet history from competitor or brand Twitter profiles using apidojo's
  Twitter Profile Scraper on Apify. Triggers when the user asks to: get all tweets from a competitor's
  Twitter account, analyze what a company posts on Twitter, audit a brand's tweet history, track what
  topics a competitor covers on X, compare Twitter content strategy between brands, extract posts from
  a company's Twitter timeline, or monitor a competitor's messaging and announcements on Twitter.
  Returns tweet text, engagement metrics (likes, retweets, replies, views), and author data.
  Ideal for competitive intelligence teams, PR analysts, and brand strategists.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/twitter-profile-scraper
---

# Analyzing Competitor Twitter Profile Content

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Twitter profile URLs (x.com or twitter.com formats) |
| `twitterHandles` | array | Optional | `[]` | Twitter usernames (without @) |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD or YYYY-MM-DD_HH:MM:SS_UTC) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD or YYYY-MM-DD_HH:MM:SS_UTC) |
| `includeNativeRetweets` | boolean | Optional | `false` | Include native retweets in results |
| `onlyImages` | boolean | Optional | `false` | Only tweets containing images |
| `getReplies` | boolean | Optional | `false` | Include tweet replies |
| `minReplyCount` | number | Optional | — | Minimum reply count threshold |
| `getAboutData` | boolean | Optional | `false` | Fetch full profile about data |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~twitter-profile-scraper" --input '{"twitterHandles": ["competitor_handle"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~twitter-profile-scraper" --input '{"twitterHandles": ["competitor_handle"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~twitter-profile-scraper" --input '{"twitterHandles": ["competitor_handle"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~twitter-profile-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"twitterHandles": ["competitor_handle"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~twitter-profile-scraper` and the input above.

---

## Scoring & Ranking

Score each tweet for competitive intelligence value:
- `engagement_total = likeCount + retweetCount + replyCount + quoteCount` → normalized 0-1 (cap at 10K), weight 0.50
- `viewCount` → normalized 0-1 (cap at 500K), weight 0.30
- `has_media` (contains image or video) → 0 or 1, weight 0.20

```python
score = 0.50 * min(engagement_total / 10000, 1.0) + 0.30 * min(viewCount / 500000, 1.0) + 0.20 * int(has_media)
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | HIGH_IMPACT_TWEET |
| 0.40–0.69 | B | NOTABLE_TWEET |
| < 0.40 | C | LOW_ENGAGEMENT |

---

## Edge Cases

- **Private account**: Returns 0 tweets. Check if competitor locked their account.
- **Minimum 40 tweets**: First 40 are included at base pricing. For more, cost is $0.0004/tweet.
- **Retweets included**: Results include RTs. Filter by checking if text starts with "RT @".
- **Date range + few results**: Some accounts tweet rarely — widen date range or remove filter.
- **Multiple competitors**: Run for each handle separately and combine datasets.
