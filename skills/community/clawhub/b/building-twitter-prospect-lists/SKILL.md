---
name: building-twitter-prospect-lists
description: >
  Builds targeted B2B prospect lists from Twitter/X profiles and posts using apidojo's Twitter scrapers on Apify.
  Triggers when the user asks to: find Twitter users with a specific job title or keyword in bio,
  build a list of founders or executives on Twitter, find people tweeting about a topic for outreach,
  identify potential customers on X, scrape Twitter profiles matching an ICP description,
  find decision-makers in a specific industry on Twitter, or export a list of leads from Twitter bios.
  Returns name, username, bio, follower count, location, and recent tweet samples per prospect.
  Ideal for B2B SDRs, growth hackers, founder-led sales teams, and partnership managers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tweet-scraper, apidojo/twitter-user-scraper
---

# Building Twitter Prospect Lists

Searches Twitter/X for profiles matching a target ICP (Ideal Customer Profile) using bio keywords and topic-based tweet search. Delivers a contact-ready list with engagement signals and bio context.

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
- [ ] Step 1: Define ICP and search strategy
- [ ] Step 2: Run tweet-scraper for keyword/topic tweets
- [ ] Step 3: Extract unique authors from results
- [ ] Step 4: Enrich with twitter-user-scraper for bio + follower data
- [ ] Step 5: Filter, rank, and deliver prospect list
```

### Step 1: Define ICP and Strategy

Ask the user:
- **Job title keywords** for Twitter bio search (e.g., "Head of Growth", "Founder", "CTO")
- **Topic keywords** — what topics does the ICP tweet about? (e.g., "SaaS metrics", "PLG", "RevOps")
- **Industry signals** — keywords that suggest the right industry in bio (e.g., "SaaS", "fintech", "healthcare")
- **Follower range** (optional) — e.g., 1,000–50,000 (avoids both nobodies and celebrities)
- **Location** (optional) — e.g., "San Francisco", "London"
- **List size** — how many prospects needed?

### Step 2: Search for Topic-Based Tweets

Search Twitter for tweets about topics your ICP cares about. People who actively tweet about a topic are warmer prospects.


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
  "searchTerms": ["[TOPIC_KEYWORD_1]", "[TOPIC_KEYWORD_2]"],
  "maxItems": 200,
  "tweetLanguage": "en"
}
```

**If Apify MCP is not available:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchTerms": ["[TOPIC_KEYWORD]"],
    "maxItems": 200
  }'
```

Run for each topic keyword. Collect all `author.username` values. Deduplicate. This gives you a candidate pool.

### Step 3: Enrich Candidates with Profile Data

Take the top 100-200 unique usernames from Step 2. Fetch full profile data to filter by bio keywords and follower count.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input:
{
  "usernames": ["[username1]", "[username2]", "..."],
  "maxItems": 100
}
```

**If Apify MCP is not available:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["[username1]", "[username2]"]
  }'
```

### Step 4: Filter Against ICP Criteria

From profile data, keep only users where ALL of these are true:
1. Bio contains at least one job title keyword OR industry signal keyword
2. Follower count is within the specified range (if given)
3. Location matches (if specified) — check `location` field
4. Account is not a bot (has profile picture, has >10 tweets, account age >6 months)

Remove:
- Accounts with default profile images
- Accounts with 0 tweets
- Verified mega-influencers (follower count above range)
- Obviously automated accounts

### Step 5: Rank and Format

Rank filtered prospects by:
1. Relevance score = number of ICP keywords matched in bio
2. Engagement proxy = (likes + retweets on recent tweets) / follower count

## Output Format

```
# Twitter Prospect List: [ICP DESCRIPTION]
Generated: [N] prospects | Filters applied: [summary] | Date: [DATE]

| # | Name | Handle | Followers | Job / Bio | Location | Last Active | Profile |
|---|------|--------|-----------|-----------|----------|-------------|---------|
| 1 | [name] | @[handle] | [N] | [bio excerpt] | [city] | [date] | [url] |
| 2 | [name] | @[handle] | [N] | [bio excerpt] | [city] | [date] | [url] |

## Top 10 Highest-Priority Prospects
1. **@[handle]** — "[bio]" | [N] followers | Recently tweeted about: [topic]
2. **@[handle]** — "[bio]" | [N] followers | Recently tweeted about: [topic]
...

## Notes
- [N] candidates found in topic search
- [N] filtered out (didn't match ICP criteria)
- [N] final prospects delivered
- Engagement signals are 24-48h delayed
```

## Personalizing Outreach

For each top prospect, the recent tweet sample can be used to personalize outreach. Note their recent topics to reference in a first message.

## Troubleshooting

**Too few results after filtering:** Broaden bio keywords (use OR logic, not AND). Try more topic keywords in Step 2.
**Too many irrelevant accounts:** Add industry-specific keywords to bio filter (e.g., require "SaaS" or "B2B" in bio).
**Location filter not working:** Twitter location is self-reported and inconsistent — treat it as a soft signal, not a hard filter.

