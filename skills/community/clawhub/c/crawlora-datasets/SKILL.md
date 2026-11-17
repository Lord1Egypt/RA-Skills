---
name: crawlora-datasets
description: Queries Crawlora's pre-built hosted datasets — Airbnb markets, App Store/Google Play apps, GitHub/Instagram/X users, job postings, US housing markets, Google Maps businesses, Goodreads, PitchBook, Steam, TrustMRR, Product Hunt, SEC companies, tech-stack, and more — via search/facets/item/nearby endpoints, returning clean JSON without live-crawling each platform. Use when the user wants bulk or aggregate analysis, to search a pre-indexed corpus, to facet/filter a large population, or to look up one record by its dataset id, instead of scraping pages one at a time.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Crawlora hosted datasets

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Query Crawlora's own **pre-crawled, pre-indexed datasets** — search, facet, and
fetch-by-id over corpora Crawlora already built and refreshes on a schedule.
This is different from the other skills in this repo: those hit a live
per-platform endpoint (one request, one page); this skill hits a **search
index** over millions of already-collected records, so it's the right tool
for population-level questions ("how many", "top N by X", "everything
matching Y") rather than one-off lookups.

## When to use this skill

- "How many / what share of X match Y?" — facet/aggregate questions.
- "Find all X with property Y" (e.g. jobs paying > $150k, apps with 4.5+
  rating, GitHub users near a city, houses in a metro).
- "Give me the full list of Z" instead of one record — bulk/list research.
- Any of: Airbnb markets, app-store apps/reviews/charts, GitHub/Instagram/X
  users, job postings + which companies are hiring, US housing markets
  (Redfin-sourced), Google Maps businesses, Goodreads authors/books, Apple
  Podcasts shows, Chrome Web Store extensions, PitchBook companies/funds/
  investors/advisors/LPs, PlayStation games, Product Hunt makers/products/
  trends, Reddit trending, SEC companies + institutional positions, Steam
  games/prices/playercounts/reviews/news/achievements/charts, TrustMRR
  startups, journalists, Numbeo cost-of-living cities/countries, website
  tech-stack.
- Prefer the platform-specific skill instead when the job is "look up this
  one profile/listing right now" (e.g. `youtube-research`, `movie-tv-research`)
  — datasets are refreshed periodically, not real-time.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Every dataset follows the same shape under `/datasets/<dataset-id>/...`:

1. **Discover** — `GET /datasets` lists every available dataset id and its
   capabilities (search / facets / item / nearby).
2. **Search** — `GET /datasets/<id>/search` full-text + filtered search;
   paginate with `page`/`size` (see `reference/endpoints.md` per dataset).
3. **Facet** — `GET /datasets/<id>/facets` returns aggregate breakdowns
   across a dataset's facetable fields at once (e.g. the jobs dataset
   returns top companies, department, location, seniority, remote share,
   and more in one call) — use for "how many / breakdown by X" questions.
4. **Item** — `GET /datasets/<id>/items/{id}` fetches one record by its
   dataset key (varies per dataset: `login`, `username`, `slug`, `cik`,
   `appid`, `domain`, `region_type/table_id`, …).
5. **Nearby** — where supported (`airbnb-markets`, `github-users`,
   `google-map-businesses`, `jobs`) — `GET /datasets/<id>/nearby` finds
   records near a `lat`/`lon` within `radius_km`.

Full endpoint list, per-dataset ids, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# List every dataset id and what it supports:
scripts/crawlora.sh /datasets | jq '.'

# Search the jobs dataset (all companies' live postings):
scripts/crawlora.sh /datasets/jobs/search q="staff engineer" location="remote" | jq '.'

# Facet: hiring-market breakdown (top companies, seniority, remote share, ...):
scripts/crawlora.sh /datasets/jobs/facets | jq '.'

# Item: one GitHub user by login:
scripts/crawlora.sh /datasets/github-users/items/torvalds | jq '.'

# Nearby: GitHub users within 50km of a coordinate (radius in meters):
scripts/crawlora.sh /datasets/github-users/nearby lat=37.7749 lon=-122.4194 radius_m=50000 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every dataset id,
its search/facets/item/nearby endpoints, and params.

## Examples

- **Hiring-market pulse:** `/datasets/jobs/facets` for the aggregate
  breakdown (top companies, seniority, remote share), then
  `/datasets/jobs/companies` to see which employers are actively posting.
- **App-store landscape scan:** `/datasets/apps/search` filtered by category
  and rating, then `/datasets/apps-reviews/search` for the sentiment behind
  the top results.
- **Startup revenue leaderboard:** `/datasets/trustmrr/search` sorted by
  MRR, then `/datasets/trustmrr/history/{slug}` for one company's trend line.
- **Housing-market snapshot:** `/datasets/housing-markets/search` for a
  metro, then `/datasets/housing-markets/items/{region_type}/{table_id}` for
  the full monthly series.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — every dataset is built from public sources.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Datasets refresh on a schedule (daily/weekly depending on source) — not
  real-time. For a live single-record lookup, prefer the matching
  platform-specific skill in this repo (e.g. `job-market-research`,
  `movie-tv-research`) instead.
- Results are paginated (`page`/`size`) — walk pages for full coverage.
