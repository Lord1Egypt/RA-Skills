---
name: finding-speaking-opportunities-on-twitter
description: >
  Finds speaking opportunities and event organizer contacts on Twitter using apidojo's Twitter scrapers. Triggers when the user asks to: find speaking opportunities on Twitter, discover conferences looking for speakers on X, find event organizers calling for speaker submissions, identify call-for-speakers announcements in an industry on Twitter, find podcast or summit hosts looking for guests, discover virtual event opportunities for thought leadership, or build a speaking opportunity pipeline from Twitter.
  Returns event name, organizer handle, topic focus, deadline signals, event size, and submission URL.
  Ideal for startup founders, executives, coaches, and consultants building thought leadership through speaking.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tweet-scraper
---

# Finding Speaking Opportunities On Twitter

Executes finding speaking opportunities on twitter using apidojo scrapers. Part of the apidojo intelligence skills library.

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
- [ ] Step 1: Define parameters
- [ ] Step 2: Run tweet-scraper
- [ ] Step 3: Filter and classify results
- [ ] Step 4: Score by quality and relevance
- [ ] Step 5: Deliver output
```

### Step 2: Run the Actor


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
  "searchTerms": ["call for speakers [TOPIC]", "looking for speakers [TOPIC]", "CFP [TOPIC]", "speaker applications [TOPIC]"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["call for speakers [TOPIC]", "looking for speakers [TOPIC]", "CFP [TOPIC]", "speaker applications [TOPIC]"], "maxItems": 100}'
```

Wait for `SUCCEEDED`. Fetch dataset:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN"
```

### Step 3: Classify Results

```
classification: KEYNOTE (large event, competitive) | PANEL (group format) | PODCAST_GUEST (audio interview) | VIRTUAL_SUMMIT (online event) | WORKSHOP (hands-on, smaller)
```

### Step 4: Score Each Result

```
score = opportunity_score = (event_audience_size_signal: large=1, mid=0.6, small=0.3) * 0.40 + (deadline_is_future ? 1 : 0) * 0.35 + (topic_alignment ? 1 : 0.5) * 0.25
```

### Step 5: Edge Cases

- **CFP deadlines are time-sensitive; flag any opportunity with a deadline in the past as EXPIRED; prioritize by days until deadline**

Additional fallbacks:
- **< 20 results**: Broaden search terms; remove secondary filters
- **No results**: Verify the search terms are correct; try alternate phrasings
- **Data quality issues**: Remove entries with missing key fields; note count in output

## Output Format

```
# Finding Speaking Opportunities On Twitter
Results: [N] | Date: [DATE]

| # | [Key Field] | [Metric 1] | [Metric 2] | [Classification] | [Score] |
|---|------------|-----------|-----------|-----------------|---------|
| 1 | [value] | [value] | [value] | [type] | [0.XX] |

## Summary
Top result: [description]
Key finding: [insight]
```

## Troubleshooting

**Too few results:** Broaden the primary search term; remove restrictive filters.
**Low quality results:** Apply minimum score threshold (≥ 0.50) to filter noise.
**Actor fails to run:** Verify API key; check actor status at apify.com/apidojo.

