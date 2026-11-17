---
name: finding-tiktok-creators-using-trending-sounds
description: >
  Finds TikTok creators using trending sounds or viral audio tracks using apidojo's TikTok Music
  Scraper on Apify. Triggers when the user asks to: find creators using a specific TikTok sound, discover
  influencers using a trending audio clip, identify creators participating in a sound-based trend, find
  TikTok accounts using a viral music track, build a list of creators who made content with a specific
  sound, or find early adopters of a trending TikTok audio for brand placement.
  Returns creator username, follower count, views, likes, hashtags, and song metadata per post.
  Ideal for music labels, brand trend spotters, and influencer marketing teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-music-scraper
---

# Finding Tiktok Creators Using Trending Sounds

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | TikTok music/sound page URLs |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~tiktok-music-scraper" --input '{"startUrls": ["https://www.tiktok.com/music/Trending-Sound-Title-123456"], "maxItems": 200}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~tiktok-music-scraper" --input '{"startUrls": ["https://www.tiktok.com/music/Trending-Sound-Title-123456"], "maxItems": 200}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~tiktok-music-scraper" --input '{"startUrls": ["https://www.tiktok.com/music/Trending-Sound-Title-123456"], "maxItems": 200}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~tiktok-music-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.tiktok.com/music/Trending-Sound-Title-123456"], "maxItems": 200}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~tiktok-music-scraper` and the input above.

---

## Scoring & Ranking

Score each creator by:
- `followers` → normalized 0-1 (cap at 1M), weight 0.35
- `engagement_rate = (likes + comments) / views` → weight 0.35
- `video_views` → normalized 0-1 (cap at 1M), weight 0.30

```python
score = 0.35 * min(followers / 1000000, 1.0) + 0.35 * min(engagement_rate / 0.10, 1.0) + 0.30 * min(views / 1000000, 1.0)
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | PRIME_CREATOR |
| 0.40–0.69 | B | GOOD_FIT |
| < 0.40 | C | LOW_PRIORITY |

---

## Edge Cases

- **No music URL**: Requires TikTok sound page URL. Tell user to find the sound on TikTok and copy the URL from the "sounds" page.
- **Sound removed**: If sound was taken down for copyright, URL returns empty. Try alternative sound.
- **Trending sound has too many creators**: Use maxItems cap and sort by engagement.
- **Duplicate creators**: Same creator may use the sound multiple times — deduplicate by channel.username.
- **Regional sound**: Some sounds trend in specific countries — results may reflect that audience.
