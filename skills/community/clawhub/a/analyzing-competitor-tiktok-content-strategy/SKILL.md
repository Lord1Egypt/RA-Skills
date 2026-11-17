---
name: analyzing-competitor-tiktok-content-strategy
description: >
  Analyzes a competitor's TikTok content strategy and top-performing videos using apidojo's scrapers on Apify.
  Triggers when the user asks to: see what content a competitor posts on TikTok, analyze which TikTok
  videos perform best for a brand, reverse-engineer a competitor's TikTok strategy, find out how often
  a competitor posts and what gets the most engagement, study a brand's TikTok presence, compare TikTok
  content strategies across competing brands, or find out what topics a competitor covers on TikTok.
  Returns video topics, post frequency, avg views, top hooks, hashtags used, and engagement patterns.
  Ideal for social media strategists, content teams, and competitive intelligence analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tiktok-scraper, apidojo/tiktok-profile-scraper
---

# Analyzing Competitor TikTok Content Strategy

Scrapes a competitor's TikTok profile to pull their recent videos, engagement data, posting patterns, and hashtag usage. Reverse-engineers what's working for them so you can learn from it or differentiate against it.

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
- [ ] Step 1: Get competitor TikTok handle(s)
- [ ] Step 2: Pull profile stats with tiktok-profile-scraper
- [ ] Step 3: Pull recent videos with tiktok-scraper
- [ ] Step 4: Identify top-performing content patterns
- [ ] Step 5: Deliver content strategy analysis
```

### Step 1: Clarify Parameters

Ask the user for:
- **Competitor TikTok handle(s)** — up to 5 accounts (without @)
- **Number of recent videos** to analyze (default: 50 — last 2-3 months of content)
- **Analysis focus** — top content, posting cadence, hashtag strategy, or all three

### Step 2: Pull Profile Stats


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
Actor: "apidojo~tiktok-profile-scraper"
Input:
{
  "usernames": ["[handle1]", "[handle2]"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-profile-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["[handle1]", "[handle2]"]}'
```

Extract: `fans`, `heart` (total likes), `video` count, `following`, bio text.

### Step 3: Pull Recent Videos

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input:
{
  "profiles": ["https://www.tiktok.com/@[handle1]", "https://www.tiktok.com/@[handle2]"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profiles": ["https://www.tiktok.com/@[handle1]"]
  }'
```

### Step 4: Analyze Content Patterns

From the video dataset, extract:

**Top 10 videos by play count:**
- Title/caption, views, likes, comments, shares, date, hashtags

**Posting frequency:**
```
dates = [video.createTimeISO for each video]
days_covered = max(dates) - min(dates)
posting_rate = total_videos / days_covered (posts per day)
```

**Hashtag analysis:**
Extract all hashtags across videos. Count frequency. Top 10 = their core hashtag strategy.

**Content format patterns:**
From captions, classify videos into buckets:
- Educational/Tutorial (contains: "how to", "tips", "learn", numbers like "5 ways")
- Entertainment/Humor (reactions, trends, dances)
- Promotional (product mentions, CTAs, "link in bio")
- Behind-the-scenes (BTS, day-in-life, founder story)
- UGC/Response (reply to comment format)

**Hook patterns in top videos:**
Look at the first line of captions in the top 10 videos. What do they have in common?

### Step 5: Format Analysis

## Output Format

```
# TikTok Content Strategy Analysis: @[COMPETITOR]
Videos analyzed: [N] | Period: [start]–[end] | Date: [DATE]

## Account Overview
Followers: [N] | Total likes: [N] | Videos posted: [N] | Avg likes per video: [N]
Overall engagement rate: [X.X%]

## Posting Pattern
- Frequency: [X] videos per week
- Best-performing days: [day], [day] (based on publish date of top videos)
- Average video length: [X] seconds (if available)

## Top 5 Videos (by Views)
| # | Caption Excerpt | Views | Likes | Comments | Hashtags | Date |
|---|----------------|-------|-------|----------|----------|------|
| 1 | "[caption]"   | [N]   | [N]   | [N]      | [tags]   | [date] |

## Content Mix
| Format | % of Videos | Avg Views |
|--------|-------------|-----------|
| Educational | [X%] | [N] |
| Entertainment | [X%] | [N] |
| Promotional | [X%] | [N] |
| BTS/Story | [X%] | [N] |

## Top Hashtags Used
1. #[tag] — used in [N] of [total] videos
2. #[tag] — [N] videos
3. #[tag] — [N] videos

## Hook Patterns in Top Content
- Top performing hooks start with: [pattern — e.g., questions, numbers, bold claims]
- Example: "[first line of top video]"

## What's Working for Them
1. [Insight 1 — specific, actionable]
2. [Insight 2]
3. [Insight 3]

## Gap / Differentiation Opportunity
[What they're NOT doing that could be a strategic opening]
```

## Troubleshooting

**Profile scraper returns no videos:** The account may have few posts or have gone inactive. Check the handle.
**Top videos all very old:** Account may have slowed down. Note this in the analysis.
**Hashtags missing from results:** Some captions don't use hashtags. Analyze caption text for topic signals instead.

