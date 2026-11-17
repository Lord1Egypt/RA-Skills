---
name: finding-trending-twitter-topics-for-content
description: >
  Finds trending Twitter topics and conversations for content ideation using apidojo's Twitter
  scrapers on Apify. Triggers when the user asks to: find trending topics on Twitter for content,
  discover what is being discussed in a niche on X right now, identify Twitter conversations to
  join with content, find trending hashtags in an industry on Twitter, research what topics are
  generating engagement in a space on X, discover viral tweet themes for blog or video content,
  or find what your target audience is talking about on Twitter this week.
  Returns trending topics, tweet volume signals, top engagement posts, and content angle suggestions.
  Ideal for content marketers, social media managers, newsletter writers, and real-time content teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tweet-scraper
---

# Finding Trending Twitter Topics for Content

Identifies trending conversations in a niche on Twitter to inform timely content. Twitter trends are 48–72 hour windows — act fast or pivot to the evergreen angle.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `searchTerms` | array | ✅ | `[]` | Twitter advanced search queries (e.g. `["#AI lang:en", "from:NASA"]`) |
| `sort` | string | Optional | `Top` | Sort order: `Latest`, `Top`, or `Latest+Top` |
| `tweetLanguage` | string | Optional | — | ISO 639-1 language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `onlyVerifiedUsers` | boolean | Optional | `false` | Only tweets from verified users |
| `onlyTwitterBlue` | boolean | Optional | `false` | Only Twitter Blue subscribers |
| `onlyImage` | boolean | Optional | `false` | Only tweets with images |
| `onlyVideo` | boolean | Optional | `false` | Only tweets with videos |
| `onlyQuote` | boolean | Optional | `false` | Only quote tweets |
| `author` | string | Optional | — | Filter to a specific author handle |
| `inReplyTo` | string | Optional | — | Tweets replying to a specific handle |
| `mentioning` | string | Optional | — | Tweets mentioning a specific handle |
| `geotaggedNear` | string | Optional | — | Tweets near a location |
| `withinRadius` | string | Optional | — | Radius around geotaggedNear |
| `geocode` | string | Optional | — | Lat/lng + radius string |
| `placeObjectId` | string | Optional | — | Tweets tagged with a place |
| `minimumRetweets` | number | Optional | — | Minimum retweet count |
| `minimumFavorites` | number | Optional | — | Minimum like count |
| `minimumReplies` | number | Optional | — | Minimum reply count |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD) |
| `includeSearchTerms` | boolean | Optional | `false` | Add the matched search term to each tweet |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search niche keywords + trending signals
- [ ] Step 2: Extract high-engagement tweet clusters
- [ ] Step 3: Identify topic themes and their velocity
- [ ] Step 4: Score content opportunity per topic
- [ ] Step 5: Deliver trending topic brief
```

### Step 1: Search Tweets


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tweet-scraper"
Input:
{
  "searchTerms": ["[NICHE]", "#[niche]", "[NICHE] [current_year]"],
  "maxItems": 500,
  "tweetLanguage": "en",
  "since": "[7 days ago]"
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "searchTerms": ["B2B SaaS", "#saas", "B2B SaaS 2026"],
    "maxItems": 500,
    "tweetLanguage": "en"
  }'
```

### Step 2: Identify Trending Topics

Group tweets by topic cluster using keyword co-occurrence. For each cluster:
```
topic_velocity = count_of_tweets_in_cluster
topic_engagement = sum(likeCount + replyCount * 3 + retweetCount * 2) / topic_velocity
```

**Topic freshness:**
```
freshness = proportion of cluster tweets from last 48 hours
```

### Step 3: Score Content Opportunity

```
opportunity_score = (topic_velocity / 50, max 1) * 0.30
                  + (topic_engagement / 100, max 1) * 0.30
                  + freshness * 0.20
                  + (top_tweet_by_influencer ? 1 : 0) * 0.20
```

**Content angle recommendation by freshness:**
- Freshness > 0.7 → "Timely reaction piece / hot take"; publish within 24h
- Freshness 0.3–0.7 → "Analysis / deep dive"; publish within 72h
- Freshness < 0.3 → "Evergreen explainer"; no urgency

### Step 4: Edge Cases

- **Topic is news event, not evergreen**: Flag as `NEWS_REACTIVE` — good for social media posts but risky for long-form content investment
- **Trending topic is negative controversy**: Flag as `RISK_TOPIC`; joining controversy can be brand-damaging; present option to "inform from a distance"
- **Niche too broad** (returns unrelated topics): Add second qualifier — "B2B SaaS growth" not just "SaaS"
- **Trending terms are abbreviations or jargon**: Define them in output for non-native audience clarity

## Output Format

```
# Trending Twitter Topics: [NICHE]
Period: [DATE_RANGE] | Tweets analyzed: [N] | Topic clusters identified: [N] | Date: [DATE]

## Top Trending Topics
| # | Topic | Tweets | Avg Engagement | Freshness | Type | Score |
|---|-------|--------|---------------|---------|------|-------|
| 1 | [topic] | [N] | [N] | [X%] | [TRENDING/NEWS/EVERGREEN] | [0.XX] |

## Content Opportunities

### 1. [Topic Name] (Score: [X])
Volume: [N] tweets | Avg engagement: [N] | Freshness: [X%]
Angle: [recommended content format and angle]
Top tweet: @[handle] ([N] likes): "[excerpt]"

### 2. [Topic Name] ...

## Hashtag Map
| Hashtag | Usage Count | Avg Likes | Co-used With |
|---------|------------|-----------|-------------|
```

## Troubleshooting

**No trending topics** (flat distribution): Niche may not be particularly active on Twitter; try extending to 14-day window or switching to Reddit for content research in this niche.
**All topics are political/news**: Add niche qualifier more aggressively in search terms; most general news topics will surface on any broad search.
**Content idea doesn't fit your format**: Trending topics are inputs, not prescriptions — adapt the angle to your format (e.g. a Twitter controversy about pricing → a blog post "How to Communicate Pricing Changes").

