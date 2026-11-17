---
name: discovering-viral-tiktok-content-trends
description: >
  Discovers viral content trends and trending formats on TikTok using apidojo's TikTok scraper
  on Apify. Triggers when the user asks to: find trending content formats on TikTok, discover
  what is going viral on TikTok in a niche, identify viral TikTok hooks or video styles to
  adapt, research TikTok trends for a product category, find what content formats are performing
  best on TikTok right now, discover trending sounds or concepts in a niche on TikTok, or
  analyze what drives viral TikTok engagement in a specific category.
  Returns trending hashtags, view counts, engagement metrics, content format patterns, and hook analysis.
  Ideal for TikTok content creators, brand social teams, and video content strategists.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-scraper
---

# Discovering Viral TikTok Content Trends

Identifies what's going viral on TikTok in a niche by analyzing high-performing posts. Extracts repeatable content formats, hooks, and structural patterns — the inputs needed to create content that rides existing momentum.

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
- [ ] Step 1: Search niche hashtags
- [ ] Step 2: Filter for high-performing posts
- [ ] Step 3: Analyze content formats and hooks
- [ ] Step 4: Score trend viability for replication
- [ ] Step 5: Deliver trend brief
```

### Step 1: Search Hashtags


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
  "keywords": ["#[niche]", "#[niche]tiktok", "#[niche]foryou"],
  "maxItems": 200
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"keywords": ["#skincaretips", "#skincaretiktok"], "maxItems": 200}'
```

Filter: `playCount >= min_views`

### Step 2: Analyze Content Patterns

From caption and available metadata, classify:

```
hook_type:
  QUESTION = caption starts with or contains "?", "have you", "do you", "did you know"
  LIST = "X things", "here are the", "number [N]"
  BEFORE_AFTER = "I did X for 30 days", "watch the transformation"
  STORY = first-person narrative opener ("I was struggling with...")
  CONTROVERSY = "unpopular opinion", "no one talks about", "this is controversial"
  TUTORIAL = "how to", "step by step", "the only guide you need"

content_length_tier:
  SHORT = video duration < 15 seconds
  MEDIUM = 15-60 seconds
  LONG = > 60 seconds
```

### Step 3: Score Trend Replicability

```
trend_score = (playCount / 1000000, max 1) * 0.30
            + (diggCount / playCount * 100 > 3 ? 1 : ratio/3) * 0.25
            + (commentCount / playCount * 100 > 0.5 ? 1 : ratio/0.5) * 0.25
            + (format_is_replicable: TUTORIAL/LIST/QUESTION = 1, BEFORE_AFTER = 0.8, STORY = 0.6) * 0.20
```

**Trend window:** posts all from the same 7-day period = `TRENDING NOW`; spread over 30 days = `ESTABLISHED FORMAT`

### Step 4: Edge Cases

- **Trend driven by a single mega-creator**: If top 3 posts are from same creator, it's a creator trend not a format trend — flag as `CREATOR_DRIVEN`; harder to replicate without their audience
- **Trend requires specific audio**: Note if posts share the same sound; audio trends are TikTok-specific and may expire quickly
- **Niche too small** (< 50 posts above threshold): Lower `min_views` to 25K; or report the top posts available with a note on data volume
- **International content dominates**: Filter by caption language; use English-language posts if targeting English-speaking audience

## Output Format

```
# TikTok Viral Trend Report: [NICHE]
Period: [DATE_RANGE] | Posts analyzed: [N] | Viral posts (>[MIN_VIEWS] views): [N] | Date: [DATE]

## Top Performing Formats
| Format | # Posts | Avg Views | Avg Like Rate | Best Example |
|--------|---------|-----------|--------------|-------------|
| Tutorial | [N] | [N] | [X%] | @[handle]: "[caption excerpt]" |
| List | [N] | [N] | [X%] | |

## Top Viral Posts
| Creator | Views | Likes | Comments | Hook Type | Caption Preview |
|---------|-------|-------|----------|----------|----------------|

## Hook Patterns Worth Replicating
1. "[Hook structure]" — used in [N] viral posts, avg [N] views
   Example: "[verbatim hook from top post]"

## Trend Window Assessment
- TRENDING NOW (< 7 days): [N] posts in format
- ESTABLISHED FORMAT (7-30 days): [N] posts
- FADING (> 30 days): [N] posts

## Recommended Content Angles for [NICHE]
1. [Format + hook recommendation with rationale]
2. [Format + hook recommendation]
```

## Troubleshooting

**All viral posts are from mega-creators**: Add filter `follower_count < 500K` to surface format trends from creators of all sizes.
**Format analysis is inconsistent**: Caption text is the only metadata available without video analysis; use it as a proxy and note this limitation.
**Trend is already declining**: TikTok trends typically peak and decline within 2-3 weeks; if freshness is low, recommend adapting the format with a new angle rather than copying directly.

