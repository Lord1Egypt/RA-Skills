---
name: extracting-youtube-comments-for-research
description: >
  Extracts and analyzes YouTube comments for audience research using apidojo's YouTube scraper on Apify.
  Triggers when the user asks to: extract YouTube comments for research, analyze what viewers say
  in YouTube comments, scrape comments from a YouTube video for sentiment analysis, find common
  questions in YouTube comments, research audience feedback from YouTube video comments, extract
  top comments from a YouTube channel for audience insights, or analyze viewer reactions from
  YouTube comment sections.
  Returns comment text, likes on comment, reply count, commenter username, and timestamp.
  Ideal for content creators, brand researchers, product teams, and audience insight analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Extracting YouTube Comments for Research

Pulls YouTube video comments for sentiment analysis, question mining, and product feedback. YouTube comments are more considered than TikTok — viewers invest more time before commenting.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | YouTube URLs — channels, playlists, Shorts, search results |
| `youtubeHandles` | array | Optional | `[]` | YouTube channel handles (e.g. `@kurzgesagt`) |
| `getTrending` | boolean | Optional | `false` | Retrieve trending videos |
| `keywords` | array | Optional | `[]` | Search keywords |
| `gl` | string | Optional | `us` | Country code for results (e.g. `US`, `GB`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`, `de`) |
| `uploadDate` | string | Optional | `all` | Upload date filter: `any`, `hour`, `today`, `week`, `month`, `year` |
| `duration` | string | Optional | `all` | Duration filter: `any`, `short`, `long` |
| `features` | string | Optional | `all` | Feature filter: `4k`, `hd`, `live`, `cc`, `3d`, `hdr`, etc. |
| `sort` | string | Optional | `r` | Sort order for search results |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Scrape comments from target videos
- [ ] Step 2: Filter and clean dataset
- [ ] Step 3: Analyze by research goal
- [ ] Step 4: Extract top themes and insights
- [ ] Step 5: Deliver comment research report
```

### Step 1: Scrape Comments


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~youtube-comments-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~youtube-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~youtube-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-comments-scraper"
Input:
{
  "startUrls": [{"url": "[VIDEO_URL_1]"}, {"url": "[VIDEO_URL_2]"}],
  "type": "comments",
  "maxComments": 500
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~youtube-comments-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": [{"url": "[VIDEO_URL]"}], "type": "comments", "maxComments": 500}'
```

### Step 2: Clean Dataset

- Remove comments < 8 words (usually emoji-only or "great video!")
- Remove self-promotional comments (contain external links)
- Remove creator's own replies (match `authorName` to channel name)
- Apply `min_likes_on_comment` filter if set

### Step 3: Analyze by Goal

**Questions:** Contains "?", "how do you", "what is", "can you"
**Pain points:** "I struggle", "I can't", "problem is", "doesn't work"
**Product feedback:** Product mentions + opinion signals
**Sentiment:** Standard lexical classifier (positive/negative/neutral)

```
comment_importance = likeCount * 0.60 + replyCount * 10 * 0.40
```

### Step 4: Edge Cases

- **Comments disabled**: Note; try different video from same channel
- **Mostly non-English**: Report language distribution; filter to English if needed
- **Spam invasion**: Filter where same username appears > 3 times
- **Brigaded comment section**: > 50% share coordinated theme → flag as BRIGADED

## Output Format

```
# YouTube Comment Analysis
Videos: [N] | Comments analyzed: [N] | After filtering: [N] | Date: [DATE]

## Sentiment (if goal = sentiment)
Positive: [X%] | Negative: [X%] | Neutral: [X%]

## Top 10 Most-Liked Comments
| # | Comment (excerpt) | Likes | Replies |
|---|------------------|-------|---------|

## Key Themes
| Theme | Frequency | Avg Likes | Example |
|-------|-----------|-----------|---------|

## Most Asked Questions
1. "[question]" — [N] viewers
```

## Troubleshooting

**Few comments returned**: YouTube limits access for some videos; try high-comment video from same channel.
**Mostly surface-level praise**: Use `min_likes_on_comment = 5` to filter for substantive comments.
**Research goal not present**: Audience may not engage that way on YouTube; try Reddit or TikTok for this niche.

