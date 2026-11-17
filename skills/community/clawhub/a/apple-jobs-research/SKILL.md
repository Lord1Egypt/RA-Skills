---
name: apple-jobs-research
description: Researches Apple job postings via the Crawlora API — searches jobs.apple.com and pulls full posting detail (description, qualifications, location, team) — returning clean JSON. Use when the user wants to search Apple careers listings, check what a specific Apple team/location is hiring for, or pull the full detail of a specific Apple requisition or pipeline role.
---

# Apple Jobs search

Search Apple's public careers site and pull full posting detail — all as
normalized JSON from the Crawlora API, no scraping jobs.apple.com by hand.

## When to use this skill

- "Search for <role> jobs at Apple in <location>."
- "What is Apple currently hiring for on the <team> team?"
- "Pull the full description and qualifications for Apple job <id>."
- "Is Apple hiring for retail / evergreen roles in <location>?"

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search** — `/apple-jobs/search` (`q` required, `location` and `page`
   optional) searches jobs.apple.com's server-rendered search page. Page size
   is fixed by Apple at 20 results per page; results carry identity/location/
   team metadata only, not the full description.
2. **Job detail** — `/apple-jobs/job` (`id` required) fetches one posting's
   full description and qualifications by the `id` field returned from
   search (a specific requisition like `200674676-0836`, or an evergreen/
   pipeline retail role like `PIPE-200314122`).

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search:
scripts/crawlora.sh /apple-jobs/search q="software engineer" location="united-states-USA" | jq '.'

# Job detail:
scripts/crawlora.sh /apple-jobs/job id="200674676-0836" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for both Apple Jobs
endpoints this skill uses.

## Examples

- **"What is Apple hiring for in Cupertino?"** — `/apple-jobs/search`
  `q="engineer" location="united-states-USA"`, page through with `page`,
  then `/apple-jobs/job` on the ids you care about for full qualifications.
- **"Pull the full posting for req 200674676-0836."** — `/apple-jobs/job
  id=200674676-0836` directly, no search needed if you already have the id.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public postings; respect jobs.apple.com's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Search page size is fixed at 20** by Apple — walk multiple pages via `page` to cover more results.
- **`location` uses Apple's own slug format** (e.g. `united-states-USA`, `singapore-SGP`), not a free-text city/country string.
- **Search results are metadata-only** — call `/apple-jobs/job` for the full description and qualifications of a specific posting.
