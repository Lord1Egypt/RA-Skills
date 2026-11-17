---
name: finding-healthcare-practices-via-google-search
description: >
  Finds medical practices, clinics, dental offices, and healthcare providers via Google Search
  using apidojo's Google Search Scraper on Apify. Triggers when the user asks to: find medical
  practices for outreach, discover dental offices or clinics via Google, build a list of healthcare
  providers in a specific city, find doctors or medical groups for vendor sales, prospect healthcare
  practices for software or supply sales, identify hospitals or urgent care centers by location,
  or compile a healthcare provider list from Google results. Returns practice name, website URL,
  and Google snippet per result. Ideal for HealthTech SaaS vendors, medical suppliers, and B2B
  service companies targeting healthcare practices.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Finding Healthcare Practices Via Google Search

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
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["dental practice Chicago"], "countryCode": "US", "maxPagesPerQuery": 3}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["dental practice Chicago"], "countryCode": "US", "maxPagesPerQuery": 3}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["dental practice Chicago"], "countryCode": "US", "maxPagesPerQuery": 3}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["dental practice Chicago"], "countryCode": "US", "maxPagesPerQuery": 3}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~google-search-scraper` and the input above.

---

## Scoring & Ranking

Score each result by:
- `snippet_has_health_signals` (contains: clinic, practice, dental, medical, healthcare, patients, MD, DDS) → weight 0.50
- `valid_domain` (not .gov, .edu, .wikipedia, .yelp) → weight 0.30
- `position_score` → 1 - (position / total), weight 0.20

```python
score = 0.50 * int(health_signals) + 0.30 * int(valid_domain) + 0.20 * position_score
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

- **Directory sites**: Healthgrades, Zocdoc, WebMD listings — not practices. Filter by checking domain.
- **Hospital systems**: Large hospital networks are hard to reach. Focus on independent practices.
- **No contact data**: SERP returns URL and snippet only — no phone/email. Use as a starting list.
- **Duplicate practices**: Same clinic may appear for multiple search terms — deduplicate by domain.
- **Specialty filter**: Add specialty to search term: "orthopedic clinic Denver", "dermatology practice Miami".
