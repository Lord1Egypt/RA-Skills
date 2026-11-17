---
name: finding-software-engineers-on-twitter
description: >
  Finds software engineers and developers to recruit using apidojo's Twitter scrapers on Apify.
  Triggers when the user asks to: find software engineers on Twitter for recruiting, discover
  developers to hire from their Twitter profile, find backend frontend or full-stack engineers
  on X for talent sourcing, identify programmers by tech stack on Twitter, find software
  engineers who are open to work on Twitter, build a developer recruiting pipeline from social,
  or find engineers tweeting about job search or career changes.
  Returns handle, name, tech stack (from bio/tweets), follower count, and open-to-work signals.
  Ideal for technical recruiters, startup hiring managers, and engineering talent acquisition teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Finding Software Engineers on Twitter

Discovers software engineers on Twitter/X via tech stack keywords, open-to-work signals, and engineering community activity. Twitter surfaces engineers who are active in their tech community — a strong passive candidate signal.

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
- [ ] Step 1: Search tweets by tech stack + role signals
- [ ] Step 2: Collect unique handles
- [ ] Step 3: Enrich profiles via twitter-user-scraper
- [ ] Step 4: Score candidate fit
- [ ] Step 5: Deliver candidate list
```

### Step 1: Search Queries

```
Queries: ["[TECH_STACK] engineer", "[TECH_STACK] developer", "senior [TECH_STACK]",
          "built with [TECH_STACK]", "[TECH_STACK] open to work", "[TECH_STACK] job search"]
```

For open-to-work pass: add `"looking for [TECH_STACK] role"`, `"[TECH_STACK] available"`


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
  "searchTerms": ["[TECH_STACK] engineer", "senior [TECH_STACK] developer", "built with [TECH_STACK]"],
  "maxItems": 300,
  "tweetLanguage": "en"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["Python engineer", "senior Python developer", "built with Python"], "maxItems": 300}'
```

Collect unique `author.username` from results.

### Step 2: Enrich Profiles

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input: {"usernames": ["[username1]", "[username2]", "..."]}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["handle1", "handle2"]}'
```

### Step 3: Score Candidate Quality

**Tech stack confirmation:** bio or recent tweets mention the target tech stack → `stack_confirmed = true`

**Role level proxy from bio:**
- "senior", "staff", "principal", "lead", "CTO", "VP Eng" → senior+
- "mid", "3+ years", "5 years" → mid
- "junior", "new grad", "bootcamp" → junior

**Open-to-work score:**
```
candidate_score = (stack_confirmed ? 1 : 0) * 0.35
                + (open_to_work_signal ? 1 : 0) * 0.30
                + (followerCount in 200..20000 ? 1 : 0.6) * 0.20
                + (tweeted_in_last_30_days ? 1 : 0) * 0.15
```

**Active** = tweeted in last 30 days; **Passive** = 30–90 days; **Dormant** = > 90 days

### Step 4: Edge Cases

- **Results dominated by developer tools companies**: Filter out accounts where `followerCount > 50K` and bio mentions company/brand — these are likely dev tool marketing accounts
- **Location filtering**: Twitter bio location is free text — use `contains` match; filter out profiles with ambiguous or non-geographic location entries
- **< 20 results for niche stack**: Broaden to language family (e.g. "Rust" → "systems programming") or remove role level filter
- **Bot accounts**: Flag profiles where `follower/following ratio < 0.05` AND `tweetsCount < 10` as likely bots

## Output Format

```
# Software Engineer Candidates: [TECH_STACK]
Profiles found: [N] | Open-to-work: [N] | Senior: [N] | Mid: [N] | Active: [N] | Date: [DATE]

## Priority: Open-to-Work Candidates
| Name | @Handle | Role Level | Location | Stack Confirmed | Followers | Last Active | Score |
|------|---------|-----------|---------|----------------|-----------|------------|-------|
| [name] | @[handle] | Senior | [city] | ✓ | [N] | [X days ago] | [0.XX] |

## Passive Candidates (Not Actively Searching)
| Name | @Handle | Role Level | Location | Stack | Followers | Score |
|------|---------|-----------|---------|-------|-----------|-------|

## Bio Highlights
Top 5 candidates — summarized bios:
1. @[handle]: "[bio excerpt]" — [tech signals]
```

## Troubleshooting

**Results are all companies not individuals**: Add `"-company -official -team -agency"` as negative search terms, or filter bio for first-person pronouns.
**Tech stack too common returns too many results**: Add a second filter — location OR seniority level — to reduce to a manageable size.
**Few open-to-work signals**: Most passive candidates don't signal openly; focus outreach on the `passive` tier with personalized messages referencing their recent tweets.

