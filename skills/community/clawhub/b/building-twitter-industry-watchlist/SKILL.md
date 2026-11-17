---
name: building-twitter-industry-watchlist
description: >
  Builds a curated Twitter industry watchlist of key voices using apidojo's Twitter scrapers on Apify.
  Triggers when the user asks to: build a Twitter watchlist for an industry, find key Twitter accounts
  to follow in a niche, create a curated list of thought leaders in a sector on X, identify the most
  influential Twitter accounts in a business category, build a Twitter list for industry monitoring,
  find the signal-to-noise accounts in a topic area, or compile the must-follow accounts for staying
  current in an industry.
  Returns account list with handle, follower count, engagement rate, topic focus, and influence score.
  Ideal for business analysts, investors, executives, and professionals doing industry intelligence.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Building a Twitter Industry Watchlist

Identifies highest-signal Twitter accounts in an industry — people whose tweets consistently generate discussion, surface new information, or shape thinking in the space.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Twitter profile or tweet URLs |
| `twitterHandles` | array | Optional | `[]` | Twitter usernames (without @) |
| `twitterUserIds` | array | Optional | `[]` | Twitter user IDs |
| `getFollowers` | boolean | Optional | `false` | Extract follower lists |
| `getFollowing` | boolean | Optional | `false` | Extract following lists |
| `getRetweeters` | boolean | Optional | `false` | Extract retweeters of a tweet URL |
| `includeUnavailableUsers` | boolean | Optional | `false` | Include unavailable/suspended users |
| `maxItems` | number | Optional | Unlimited | Maximum users to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search for high-engagement industry tweets
- [ ] Step 2: Collect influential account handles
- [ ] Step 3: Enrich and score
- [ ] Step 4: Classify by account type
- [ ] Step 5: Deliver curated watchlist
```

### Step 1: Search Industry Conversations


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
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
  "searchTerms": ["[INDUSTRY]", "#[industry]", "[INDUSTRY] trends", "[INDUSTRY] analysis"],
  "maxItems": 500
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["venture capital", "#vc", "VC trends 2026"], "maxItems": 500}'
```

Collect authors with `likeCount + replyCount >= 10` on their industry tweets.

### Step 2: Score Influence

```
signal_score = (retweets / followers * 1000) * 0.35
             + (replies / followers * 1000) * 0.30
             + min(followers / 100000, 1) * 0.20
             + (tweeted_industry_content >= 3 in 30 days ? 1 : 0) * 0.15
```

**Account type from bio:**
- FOUNDER: "founder", "CEO", "built"
- INVESTOR: "partner", "VC", "investor"
- ANALYST: "analyst", "researcher", "writer"
- JOURNALIST: known pub or "reporter", "journalist"
- PRACTITIONER: role title at company

### Step 3: Edge Cases

- **Bot accounts**: `retweetCount >> likeCount` → flag if retweets > 5× likes
- **Ambiguous type**: Use `PRACTITIONER` as default when unclear
- **Multiple accounts from same company**: Keep the most influential one

## Output Format

```
# [INDUSTRY] Twitter Watchlist
Accounts: [N] | Date: [DATE]

## Founders & Operators
| Name | @Handle | Role | Followers | Avg Likes | Signal Score |
|------|---------|------|-----------|----------|-------------|

## Investors & Analysts
| Name | @Handle | Role | Followers | Signal Score |
|------|---------|------|-----------|-------------|

## Press & Media
| Name | @Handle | Publication | Followers | Signal Score |
|------|---------|------------|-----------|-------------|

## How to Create Twitter List
Go to Twitter → Lists → Create List → Add members by username
```

## Troubleshooting

**Results are news not insiders**: Use `#[industry]` hashtag to find community members vs. general readers.
**Too many promotional accounts**: Filter accounts where > 50% of tweets include external links.
**Watchlist too large**: Apply score cutoff ≥ 0.60; keep ≤ 40 accounts for daily readability.

