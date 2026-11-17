---
name: finding-digital-agencies-via-google-search
description: >
  Finds digital marketing agencies, creative studios, and web design firms via Google Search
  using apidojo's Google Search Scraper on Apify. Triggers when the user asks to: find digital
  agencies for outreach or partnership, discover marketing agencies in a specific city, build a
  list of SEO agencies or web design studios via Google, find creative agencies that might need
  your software, prospect marketing firms by searching Google, identify agencies by specialty
  and location, or compile an agency contact list from Google search results. Returns agency name,
  website URL, and Google snippet per result. Ideal for SaaS vendors, white-label providers, and
  B2B service companies targeting marketing agencies.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Finding Digital Agencies Via Google Search

---

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

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["digital marketing agency NYC"], "countryCode": "US", "maxPagesPerQuery": 3}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["digital marketing agency NYC"], "countryCode": "US", "maxPagesPerQuery": 3}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["digital marketing agency NYC"], "countryCode": "US", "maxPagesPerQuery": 3}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["digital marketing agency NYC"], "countryCode": "US", "maxPagesPerQuery": 3}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~google-search-scraper` and the input above.

---

## Scoring & Ranking

Score each result by:
- `snippet_has_agency_signals` (contains: agency, studio, services, clients, marketing, SEO) → weight 0.50
- `is_agency_domain` (not .gov, .edu, .wikipedia, .youtube) → weight 0.30
- `position` → score = 1 - (position / total_results), weight 0.20

```python
score = 0.50 * int(agency_signals) + 0.30 * int(valid_domain) + 0.20 * (1 - position/total)
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | PRIME_PROSPECT |
| 0.40–0.69 | B | WARM_LEAD |
| < 0.40 | C | LOW_PRIORITY |

---

## Edge Cases

- **Directory sites in results**: Clutch, Yelp, Upwork listings are not agencies. Filter by checking if domain matches snippet.
- **Wikipedia/news results**: Skip results with domains like wikipedia.org, bbc.com.
- **Limited contact data**: SERP only returns title, URL, snippet — no phone/email. Use results as a starting list for manual outreach.
- **Duplicate agencies**: Same agency may appear for multiple search terms — deduplicate by domain.
- **Local vs global**: Use city-specific search terms for local results.
