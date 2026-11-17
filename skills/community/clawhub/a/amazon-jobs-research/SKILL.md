---
name: amazon-jobs-research
description: Researches Amazon.jobs postings via the Crawlora API — search Amazon's public careers site by keyword and/or job category, then pull any single posting's full description and qualifications by job id — returning clean JSON. Use when the user wants to search Amazon job openings, browse a specific Amazon job category, or fetch the detail for one Amazon job posting.
---

# Amazon Jobs search

Search Amazon's public careers site (amazon.jobs) and pull individual job
postings as normalized JSON from the Crawlora API, no scraping amazon.jobs
by hand.

## When to use this skill

- "Search Amazon for <role> jobs in <country>." — keyword/category search on amazon.jobs.
- "What is Amazon hiring for in <category>?" — filter by Amazon's own job-category taxonomy.
- "Show me the full listing for Amazon job id <id>." — pull one posting's description and qualifications.
- "What are the newest Amazon job postings for <role>?" — sort by most recently posted.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search** — `/amazon-jobs/search` queries amazon.jobs's credential-free
   search JSON. Either `q` (text query) or `category` (Amazon's own
   job-category taxonomy slug) is required — pass both to narrow further.
   Optional `country` (ISO 3166-1 alpha-3) filters by location, `sort` picks
   `relevant` (default) or `recent`, and `limit`/`page` paginate results.
   Each result already includes the full description and qualifications
   inline, so a detail call is only needed to re-fetch one posting later.
2. **Job detail** — `/amazon-jobs/job` returns one posting by its numeric
   Amazon job `id` (the `id` field from a search result). Parsed from
   amazon.jobs's stable server-rendered job page — there is no separate
   JSON detail endpoint upstream.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search by keyword + country, newest first:
scripts/crawlora.sh /amazon-jobs/search q="software development engineer" country=USA sort=recent | jq '.'

# Fetch one posting by id:
scripts/crawlora.sh /amazon-jobs/job id=2612345 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for both Amazon Jobs
endpoints this skill uses.

## Examples

- **Category browse:** `/amazon-jobs/search category=hr-and-recruiting` with
  no text query to list every open role in a category, then page through with
  `page`/`limit`.
- **Track one posting over time:** save the `id` from a search hit, then poll
  `/amazon-jobs/job id=<id>` on a schedule to detect edits or removal
  (a missing/changed result signals the role closed or was updated).

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Amazon.jobs postings; respect Amazon's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Either `q` or `category` is required** on `/amazon-jobs/search` — a call
  with neither will fail.
- Results are paginated — pass `page`/`limit` (max 100 per page) to walk the
  full list.
