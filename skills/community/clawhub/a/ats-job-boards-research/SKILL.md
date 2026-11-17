---
name: ats-job-boards-research
description: Fetches any company's job openings straight from its Applicant Tracking System (ATS) via the Crawlora API — Greenhouse, Lever, Workday, Ashby, SmartRecruiters, Workable, Personio, Recruitee, iCIMS, Oracle Recruiting, Rippling, Pinpoint, Eightfold, Gem, UKG, and Teamtailor — returning clean JSON. Use when the user wants every open role from a specific company's ATS-hosted career page, a single job posting's full detail, or a hiring-velocity snapshot for a company, given its ATS platform and company/board slug.
---

# ATS job board research

Pull a company's live openings directly from its ATS-hosted career page —
Greenhouse, Lever, Workday, Ashby, and 12 more platforms — as normalized JSON
from the Crawlora API, no scraping career pages by hand. This is for
companies that host their own ATS-backed careers site, not aggregator search
(see the `job-market-research` skill for Indeed/Google Jobs) and not the
handful of big-tech-specific skills (Google/Amazon/Apple/Meta/Tesla Jobs).

## When to use this skill

- "Pull every open role from `<company>`'s Greenhouse/Lever/Workday board."
- "What is `<startup>` currently hiring for on Ashby / SmartRecruiters / Workable?"
- "Get the full description for this one job posting I found on `<company>`'s careers page."
- "Is `<company>` scaling headcount?" — hiring-velocity snapshot from their ATS board.
- "Which ATS does `<company>` use, and what's their board slug?"
- "Diff new postings on `<company>`'s board week over week."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Every platform follows the same two-call shape: a **board/list** endpoint
(all open postings, often with detail inline) and a **job-detail** endpoint
(one posting's full HTML/text description), both keyed by the company's own
slug from its careers URL — not its public brand name. `jobs/company-search`
probes the slug-only platforms for you when you don't already know which ATS
a company uses.

| Platform | Slug param(s) | List | Detail |
|---|---|---|---|
| Greenhouse | `token` | `/jobs/greenhouse/board` | `/jobs/greenhouse/job` |
| Lever | `company` | `/jobs/lever/postings` | `/jobs/lever/posting` |
| Ashby | `org` | `/jobs/ashby/board` | *(inline)* |
| Workday | `tenant` + `datacenter` + `site` | `/jobs/workday/board` | `/jobs/workday/job` |
| SmartRecruiters | `company` | `/jobs/smartrecruiters/postings` | `/jobs/smartrecruiters/posting` |
| Workable | `company` | `/jobs/workable/postings` | `/jobs/workable/posting` |
| Personio | `company` | `/jobs/personio/feed` | *(inline)* |
| Recruitee | `company` | `/jobs/recruitee/offers` | `/jobs/recruitee/offer` |
| iCIMS | `domain` | `/jobs/icims/board` | `/jobs/icims/job` |
| Oracle Recruiting | `host` + `site` | `/jobs/oracle/board` | `/jobs/oracle/job` |
| Rippling | `company` | `/jobs/rippling/board` | `/jobs/rippling/job` |
| Pinpoint | `company` | `/jobs/pinpoint/board` | *(inline)* |
| Eightfold | `tenant` + `domain` | `/jobs/eightfold/board` | `/jobs/eightfold/job` |
| Gem | `company` | `/jobs/gem/board` | *(inline)* |
| UKG (Pro Recruiting) | `tenant` + `board` | `/jobs/ukg/board` | *(inline, brief)* |
| Teamtailor | `company` | `/jobs/teamtailor/jobs` | *(inline)* |

Cross-cutting endpoints:

- `/jobs/company-search` — probe a `slug` across Greenhouse, Lever, Ashby,
  SmartRecruiters, Workable, Recruitee, Rippling, Teamtailor, and Pinpoint at
  once and report where it resolves (Workday excluded — needs
  tenant+datacenter+site, not a plain slug).
- `/jobs/hiring-signals` — aggregate any one platform's board into a
  headcount-growth snapshot (open-role total, department/location/title
  breakdowns, remote share, roles new in the last 7/30 days) in one call.
  Pass `provider` (the ATS name) plus that provider's own slug params.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Greenhouse — list a board, then pull one job's full description:
scripts/crawlora.sh /jobs/greenhouse/board token=stripe | jq '.data'
scripts/crawlora.sh /jobs/greenhouse/job token=stripe id=1234567 | jq '.'

# Lever — list postings filtered by department:
scripts/crawlora.sh /jobs/lever/postings company=netflix department=Engineering | jq '.'

# Workday — needs tenant + datacenter + site from the careers URL:
scripts/crawlora.sh /jobs/workday/board tenant=nike datacenter=wd5 site=nikeinc | jq '.'

# Hiring-velocity snapshot for an Ashby-hosted board:
scripts/crawlora.sh /jobs/hiring-signals provider=ashby org=ramp | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for all endpoints, their HTTP methods, and full param lists.

## Examples

- **"What is `<company>` hiring for right now?"** — if the platform is
  known, call its board endpoint directly (e.g.
  `/jobs/greenhouse/board token=<slug>`); otherwise resolve it first with
  `/jobs/company-search slug=<slug>`.
- **"Is `<company>` scaling?"** — `/jobs/hiring-signals` with the right
  `provider` + slug params for a velocity summary (new roles in last
  7/30 days, department mix), then the raw board endpoint for the
  role-by-role detail behind it.
- **Competitor hiring watch across ATS platforms:** pull the ATS boards of
  3-4 competitors (mixing Greenhouse, Lever, Workday, whichever each uses)
  on a schedule and diff new postings between runs.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public postings/boards; respect each source's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **You need to already know which ATS a company uses and its board slug**
  (not its public brand name) before calling a platform-specific endpoint —
  use `/jobs/company-search` to resolve it when you don't. This skill does
  not do fuzzy company-name lookup or cross-platform discovery beyond that
  one probe endpoint.
- Results are paginated on most board/list endpoints (`limit`/`offset` or
  `page`) — walk the full list for a complete pull.
