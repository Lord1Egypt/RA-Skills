# apple-jobs-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## Apple Jobs (3)

### `apple_jobs_job`

- **HTTP:** `GET /apple-jobs/job`
- **What:** Apple Jobs single posting. Returns one Apple Careers posting by its job id (the `id` field returned by search, e.g. `200674676-0836` for a specific requisition or `PIPE-200314122` for an evergreen/pipeline retail role).
- **Params:** `id` (string, **required**) — Apple job id

### `apple_jobs_locations`

- **HTTP:** `GET /apple-jobs/locations`
- **What:** Apple Jobs location discovery. Discovery endpoint for apple-jobs-search's `location` parameter, whose accepted values are a closed set Apple itself defines (its own `<slug>-<CODE>` location ids -- free-text location names are rejected). Apple exposes no bulk "list everything" option for this; the only lookup is a fuzzy search capped at 10 results per call covering four granularities (country, state/province, metro area, city) with no empty-input listing mode. With no `q`, this returns the full country-level value space (206 values, live-verified) as a static list -- the granularity apple-jobs-search's own examples use and nearly every caller needs. With `q` supplied, this instead looks up Apple's own location filter live so callers can discover state/metro/city-level values for finer filtering; results at those deeper levels may include more than one candidate and are ranked by Apple's own relevance, not alphabetically.
- **Params:** `q` (string, optional) — Optional free-text location search. Omit to get the full country-level list; supply to live-search state/metro/city-level values too (e.g. a city name).

### `apple_jobs_search`

- **HTTP:** `GET /apple-jobs/search`
- **What:** Apple Jobs search. Searches Apple's public careers site (jobs.apple.com) via its server-rendered search page's embedded job data. Page size is fixed by Apple at 20 results. Search results carry identity/location/team metadata only — call the job endpoint for the full description and qualifications.
- **Params:** `location` (string, optional) — Location filter in Apple's own slug format, e.g. united-states-USA or singapore-SGP. Free-text location names are not accepted -- call apple-jobs-locations to discover valid values.; `page` (integer, optional) — Page number, 1-based; `q` (string, **required**) — Search query
