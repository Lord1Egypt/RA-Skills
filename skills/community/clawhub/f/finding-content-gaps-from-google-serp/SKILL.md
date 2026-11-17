---
name: finding-content-gaps-from-google-serp
description: >
  Finds content gaps and opportunities from Google SERP analysis using apidojo's Google Search
  scraper on Apify. Triggers when the user asks to: find content gaps in Google search results,
  identify topics that are poorly covered in Google SERPs, discover content opportunities where
  competitors are ranking but coverage is weak, analyze what is missing from the top search
  results for a keyword, find underserved topics in a niche from Google search, or identify
  where existing content could easily outrank weak competitors.
  Returns keyword opportunities, SERP quality scores, content gap analysis, and recommended topics.
  Ideal for SEO strategists, content marketers, and blog editors prioritizing content investments.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Finding Content Gaps from Google SERP

Analyzes Google SERP results to identify where existing content is weak, outdated, or missing key information — these are the gaps where new content can rank quickly.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Google search URLs |
| `searchTerms` | array | Optional | `[]` | Keywords to search on Google |
| `countryCode` | string | Optional | `US` | Country for Google search (e.g. `US`, `GB`, `TR`) |
| `languageCode` | string | Optional | — | Language for results (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum results to return across all queries |
| `maxPagesPerQuery` | integer | Optional | `1` | Maximum result pages per query |
| `mobileResults` | boolean | Optional | `false` | Fetch mobile SERP layout |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Run google-search-scraper for all keywords
- [ ] Step 2: Analyze SERP result quality signals
- [ ] Step 3: Score content gap opportunity per keyword
- [ ] Step 4: Cluster gaps by theme
- [ ] Step 5: Deliver prioritized content gap report
```

### Step 1: Scrape SERPs


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~google-search-scraper"
Input:
{
  "queries": ["[KEYWORD_1]", "[KEYWORD_2]", "..."],
  "maxPagesPerQuery": 1,
  "countryCode": "US",
  "includePeopleAlsoAsk": true
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"queries": ["[KEYWORD_1]", "[KEYWORD_2]"], "maxPagesPerQuery": 1}'
```

### Step 2: Score SERP Quality

For each keyword, assess the top 10 results:

**Weakness signals (from title + URL):**
```
stale_content = title or URL contains year < (current_year - 2)
low_authority_domain = not in [known authority list] (e.g. Wikipedia, Forbes, HubSpot, Moz, etc.)
thin_content_signal = page title is vague or generic (no specific angle)
forum_or_QA = result is from Reddit, Quora, AnswerThePublic (not editorial)
```

```
gap_score = (stale_content_count / 10) * 0.30
          + (low_authority_count / 10) * 0.25
          + (forum_qa_count / 10) * 0.20
          + (no_featured_snippet ? 1 : 0) * 0.25
```

Tier: HIGH OPPORTUNITY (score ≥ 0.60) | MODERATE (0.35–0.59) | LOW (< 0.35)

### Step 3: Edge Cases

- **All top 10 results are from major authorities**: Gap score will be low — this is accurate; don't recommend targeting this keyword without a unique angle
- **SERP dominated by one domain**: Note monopoly; this keyword may be unfairly dominated; consider long-tail variants
- **Keyword returns mixed intent** (informational + transactional): Separate the analysis — informational content has different gap criteria than product pages

## Output Format

```
# Content Gap Analysis: [KEYWORD_SET]
Keywords analyzed: [N] | High opportunity: [N] | Moderate: [N] | Low: [N] | Date: [DATE]

## High-Opportunity Keywords (Best Investment)
| Keyword | Gap Score | Stale Results | Low Auth | No Snippet | Recommended Angle |
|---------|----------|--------------|---------|-----------|------------------|
| [keyword] | [0.XX] | [N]/10 | [N]/10 | Yes | "[content angle]" |

## Content Brief Recommendations

### 1. "[Keyword]" (Gap Score: [X])
Current top result: [title] ([year if stale]) from [domain]
Gap: [stale/thin/no snippet/forum-dominated]
Recommended content: [format + angle + target length]
```

## Troubleshooting

**All gaps score low**: Target keywords may be well-served by existing content — pivot to long-tail variations or sub-topics.
**Stale content from authority domains still ranks well**: Google may not penalize age heavily for that topic; assess based on whether the content actually answers the user's question.
**Gap analysis is subjective**: The weakness signals are proxies; manually review the top 3 results for your top 5 keywords to validate before committing to content production.

