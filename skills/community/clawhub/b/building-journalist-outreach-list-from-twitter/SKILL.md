---
name: building-journalist-outreach-list-from-twitter
description: >
  Builds targeted journalist and media contact lists from Twitter/X using apidojo's Twitter scrapers on Apify.
  Triggers when the user asks to: find journalists covering a specific beat or topic on Twitter, build a
  media outreach list from Twitter, identify reporters writing about an industry, find editors or writers
  at specific publications on X, create a PR contact list from Twitter, discover freelance journalists in
  a niche, or compile a list of media contacts for a press release or story pitch.
  Returns name, handle, publication affiliation from bio, follower count, and recent article topics.
  Ideal for PR agencies, startup communications teams, and founders doing press outreach.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Building a Journalist Outreach List from Twitter

Finds journalists and media professionals on Twitter/X who cover a specific beat, industry, or topic. Journalists are the heaviest users of Twitter for professional networking — it's the best platform to build a media contact list.

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
- [ ] Step 1: Define beat, industry, and target publications
- [ ] Step 2: Search for journalists tweeting about the beat
- [ ] Step 3: Enrich profiles to extract publication affiliation
- [ ] Step 4: Filter and verify journalist signals
- [ ] Step 5: Deliver press contact list
```

### Step 1: Clarify Parameters

Ask the user for:
- **Beat/topic** (e.g., "artificial intelligence", "climate tech", "fintech", "B2B SaaS")
- **Target publications** (optional — e.g., "TechCrunch", "Forbes", "Wired", "any tier-1 tech media")
- **Type** — staff writers, freelancers, or both
- **Geography** (optional — US, UK, global)
- **List size** (default: 30 contacts)

### Step 2: Search for Beat-Relevant Tweets

Find journalists actively tweeting about the beat — recency of coverage matters for outreach.


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
  "searchTerms": [
    "[TOPIC] journalist",
    "[TOPIC] reporter",
    "writing about [TOPIC]",
    "[TOPIC] story [current year]"
  ],
  "maxItems": 300,
  "tweetLanguage": "en"
}
```

Also run a second query for article link tweets (journalists tweet their published work):
```
Input:
{
  "searchTerms": ["[TOPIC] [publication_domain OR article link signal]"],
  "maxItems": 200
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchTerms": ["[TOPIC] journalist", "[TOPIC] reporter", "writing about [TOPIC]"],
    "maxItems": 300
  }'
```

Collect unique author usernames from all results.

### Step 3: Enrich Profiles

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input:
{
  "usernames": ["[username1]", "...", "up to 150 usernames"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["[username1]", "[username2]"]}'
```

### Step 4: Filter for Journalist Signals

Keep accounts where bio contains ANY of:
- Publication names (e.g., "TechCrunch", "@Forbes", "Bloomberg", "@Wired")
- Journalist titles: "reporter", "journalist", "editor", "correspondent", "writer at", "staff writer", "freelance writer", "contributing editor"
- Byline signals: "bylines at", "writes for", "covering"
- Press credentials: "press", "media"

**Follower range:** 1,000–500,000 (removes complete unknowns and major TV anchors who don't respond to pitches)

**Remove:** PR/comms people (bio says "PR", "communications", "agency"), brand accounts, academics without journalist credentials.

### Step 5: Format Output

## Output Format

```
# Journalist Outreach List: [BEAT/TOPIC]
Contacts found: [N] | Publication filter: [if any] | Date: [DATE]

## Contact List

| # | Name | @Handle | Publication | Beat | Followers | Recent Coverage |
|---|------|---------|-------------|------|-----------|-----------------|
| 1 | [name] | @[handle] | [pub] | [beat] | [N] | [recent tweet/article topic] |

## By Publication

### [Publication Name] ([N] contacts)
1. **[Name]** (@[handle]) — [title from bio] | [N] followers
   Recent tweet: "[excerpt showing beat relevance]"

2. **[Name]** (@[handle]) — [title] | [N] followers

### Freelancers / Independent ([N] contacts)
1. **[Name]** (@[handle]) — writes for [pubs mentioned in bio] | [N] followers

## Pitch Angle Notes
Based on recent tweets, the top 5 contacts are actively covering:
1. @[handle]: recently tweeted about [specific topic] — pitch angle: [suggestion]
2. @[handle]: covering [topic] — pitch angle: [suggestion]
```

## Personalization Tip

Before pitching, read the journalist's last 3 tweets and their most recent published article. Reference something specific. Generic pitches fail. The recent tweet data in this output enables that personalization without additional research.

## Troubleshooting

**Too many non-journalists in results:** Strengthen bio filter — require "reporter" OR "journalist" OR "editor" as exact words, not just a publication name.
**Can't find journalists for obscure beats:** Widen the search to adjacent beats or try the publication name directly as a search term.
**Follower counts seem stale:** For final outreach list, spot-check the top 10 contacts directly on Twitter.

