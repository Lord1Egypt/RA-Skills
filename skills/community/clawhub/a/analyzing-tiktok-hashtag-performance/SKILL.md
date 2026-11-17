---
name: analyzing-tiktok-hashtag-performance
description: >
  Analyzes TikTok hashtag performance, reach, and trending content using apidojo's TikTok scraper on Apify.
  Triggers when the user asks to: analyze a TikTok hashtag, find trending hashtags on TikTok in a niche,
  see which hashtags perform best for a content type, compare hashtag reach and total view counts on
  TikTok, identify viral content under a hashtag, research TikTok hashtag strategy for a campaign,
  find which hashtags a competitor uses most, or determine the best hashtags to use for a TikTok post.
  Returns hashtag name, total views, top video stats, top creators, and engagement benchmarks.
  Ideal for social media managers, content strategists, and TikTok growth consultants.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-scraper
---

# Analyzing TikTok Hashtag Performance

Scrapes TikTok hashtag pages to pull top-performing videos, engagement data, and creator information. Compares multiple hashtags side-by-side to identify which ones deliver the best reach for a given content category.

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
- [ ] Step 1: Define hashtags to analyze
- [ ] Step 2: Run tiktok-scraper for each hashtag
- [ ] Step 3: Calculate hashtag-level metrics
- [ ] Step 4: Identify top content and creators
- [ ] Step 5: Deliver strategy recommendations
```

### Step 1: Clarify Parameters

Ask the user for:
- **Hashtags to analyze** — up to 10 (without #)
- **Posts per hashtag** (default: 30 — enough for reliable stats)
- **Goal** — choosing hashtags for a post, auditing a competitor's hashtag strategy, or general research

If the user hasn't provided hashtags yet and wants recommendations, ask for:
- **Content niche** (e.g., "fitness", "cooking", "personal finance")
- Then generate a mix of: 2 mega hashtags (100M+ views), 3 mid-tier (10M–100M), 3 niche (1M–10M), 2 micro (<1M)

### Step 2: Run the Actor Per Hashtag


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
  "keywords": ["[hashtag1]", "[hashtag2]", "[hashtag3]"],
  "shouldDownloadCovers": false
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["[hashtag1]", "[hashtag2]", "[hashtag3]"]
  }'
```

Wait for `SUCCEEDED`. Fetch dataset.

### Step 3: Calculate Hashtag Metrics

For each hashtag, from its video results:

```
total_views_sampled = sum(video.playCount)
avg_views_per_video = total_views_sampled / num_videos
avg_likes_per_video = sum(video.diggCount) / num_videos
avg_comments_per_video = sum(video.commentCount) / num_videos
engagement_rate = (avg_likes + avg_comments) / avg_views * 100
competition_level = num_videos_per_day (estimate from timestamps)
```

Use `challengeInfo.stats.videoCount` (if available) as total hashtag size proxy.

### Step 4: Identify Top Content and Creators

For each hashtag, surface:
- Top 3 videos by play count (with creator handle and video URL)
- Top 3 creators by frequency in the hashtag's top content
- Common content formats in top videos (based on descriptions/captions)

### Step 5: Format Output

## Output Format

```
# TikTok Hashtag Performance Analysis
Hashtags analyzed: [N] | Posts sampled per hashtag: [30] | Date: [DATE]

## Hashtag Comparison Table

| Hashtag | Avg Views | Avg Likes | Eng. Rate | Competition | Verdict |
|---------|-----------|-----------|-----------|-------------|---------|
| #[name] | [N]       | [N]       | [X.X%]    | [Low/Med/High] | [Use / Test / Avoid] |

## Detailed Breakdown

### #[hashtag1]
- Avg views per post: [N]
- Engagement rate: [X.X%]
- Competition level: [Low / Medium / High] — approx [N] new posts/day
- Top video: "[creator]" — [N] views | [url]
- Dominant content format: [e.g., tutorial, reaction, storytelling]
- **Recommendation:** [Use as primary / Layer with broader tags / Avoid — too saturated]

### #[hashtag2]
[same structure]

## Recommended Hashtag Strategy
For maximum reach on [CONTENT NICHE], use this combination:
- Primary (1-2 hashtags): [#hashtag] — broad reach driver
- Secondary (2-3 hashtags): [#hashtag] — niche relevance
- Micro (1-2 hashtags): [#hashtag] — community engagement

## Top Creators in These Hashtags
[Creators who appear most in top-performing content across all analyzed hashtags]
1. @[handle] — [N] top videos found | [N] followers
```

## Troubleshooting

**Very low view counts:** Hashtag may be misspelled or very new. Verify spelling and try alternate versions.
**All results look the same:** Mega-hashtags (#fyp, #foryou) surface algorithmically promoted content, not organic. Use niche hashtags for better signal.
**Engagement rate seems too high or low:** Engagement rate varies heavily by content type — compare within the same content format for fair benchmarking.

