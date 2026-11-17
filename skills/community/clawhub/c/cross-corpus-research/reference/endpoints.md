# cross-corpus-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**19 endpoints across 3 platform group(s).**

## Research Jobs (5)

### `research_cancel`

- **HTTP:** `POST /research/jobs/{job_id}/cancel`
- **What:** Cancel a research job. Requests cancellation of the caller's own research job, given by `job_id`. Returns the job's current state (such as `cancelling`), `cancel_requested`, `partial`, progress counts, research progress and usage. Results already retained stay readable and are marked partial where appropriate.
- **Params:** `job_id` (string, **required**) — Research job ID

### `research_events`

- **HTTP:** `GET /research/jobs/{job_id}/events`
- **What:** Read research job events. Reads a page of events for one of the caller's research jobs, by `job_id`. `limit` is 1 to 100 (default 50); pass `next_cursor` back as `cursor` to continue, with `has_more` showing whether more remain. Each event has `sequence`, `type` (such as `source_fetched` or `round_completed`), `timestamp`, `message` and `source_id`.
- **Params:** `cursor` (string, optional) — Signed event cursor; `job_id` (string, **required**) — Research job ID; `limit` (integer, optional) — Page size from 1 through 100; default 50

### `research_results`

- **HTTP:** `GET /research/jobs/{job_id}/results`
- **What:** Read all retained research results. Returns the complete owner-scoped retained result prefix up to a consistent manifest sequence. Before a valid report or structured result exists, returns `ready=false` with `partial=true` and any retained evidence.
- **Params:** `job_id` (string, **required**) — Research job ID

### `research_start`

- **HTTP:** `POST /research/jobs`
- **What:** Start a durable cross-corpus research job. Submits bounded research over the selected web, arXiv paper, and developer-document sources. Repeated owner-scoped idempotency requests return the original job.
- **Params:** `request` (object, **required**) — Research request; `scope` is `web`, `papers`, `developer`, or `mixed`; `output_format` is `report` or `json`.
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `research_status`

- **HTTP:** `GET /research/jobs/{job_id}`
- **What:** Read a research job status. Returns the state of a research job by `job_id`: queued, running, cancelling, succeeded, failed or cancelled. The response carries `progress` counts, `research` progress (round, searches completed, sources read, questions answered), usage, warnings, `partial`, `deadline_at` and any error. A job not started within 30 minutes fails with `timeout`.
- **Params:** `job_id` (string, **required**) — Research job ID

## Research (5)

### `research_inspect_paper`

- **HTTP:** `GET /research/papers/metadata`
- **What:** Inspect paper metadata. Return paper records including titles, abstracts when available, authors, publication dates and verified identifier aliases. Europe PMC resolution is limited to MED-backed PMID, PMCID and DOI records; no full-text body is fetched.
- **Params:** `paper_id` (string, **required**) — arXiv identifier, PMID, PMCID, DOI, Europe PMC primary ID or canonical paper ID

### `research_read_paper`

- **HTTP:** `POST /research/papers/read`
- **What:** Read a research paper. Return licensed Europe PMC body prose, question-ranked passages, byte locators, license and content provenance. Restricted or unavailable bodies return metadata-only availability; arXiv does not fetch PDFs. Full text costs 5 credits, metadata-only reads 1.
- **Params:** `request` (object, **required**) — Paper read request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `research_related_papers`

- **HTTP:** `POST /research/papers/related`
- **What:** Get paper references or citing papers. Return one-hop Europe PMC citation edges, canonical seed IDs, source provenance and a frozen owner-bound cursor. Modes are references and citers; intent is unsupported. Partial results explicitly report indexed-source and candidate-window limits.
- **Params:** `request` (object, **required**) — Seed IDs and graph direction, or cursor and optional limit
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `research_search_papers`

- **HTTP:** `GET /research/papers/search`
- **What:** Search research papers. Search arXiv papers with an owner-bound frozen result window and cursor-only continuation. When arXiv is rate limited or unavailable, an undated search is answered from OpenAlex's index of arXiv papers and the response says so in coverage and warnings.
- **Params:** `authors` (array, optional) — Author names (up to five; 256 characters each); `cursor` (string, optional) — Owner-bound continuation cursor (cursor-only with optional limit); `limit` (integer, optional) — Page size (1–50; default 10); `published_from` (string, optional) — Inclusive publication date (YYYY-MM-DD); `published_to` (string, optional) — Inclusive publication date (YYYY-MM-DD); `q` (string, optional) — Required for initial search; omit on cursor continuation; `sources` (array, optional) — Enabled paper sources

### `research_sources`

- **HTTP:** `GET /research/sources`
- **What:** List paper sources. Return the stable authenticated paper source registry, including arXiv search and MED-backed Europe PMC metadata, licensed text and citation operations.
- **Params:** _none_

## Retrieval (9)

### `developer_search`

- **HTTP:** `POST /developer/search`
- **What:** Search indexed developer documentation. Searches indexed sources only; this operation never starts ingestion or contacts upstream sources. The current ready source is `go:docs` and it covers only the 18 selected verified pages documented by `developer-sources`. Search matches Unicode-aware lexical terms and punctuation-bearing identifiers such as `context.Context`; passages retain byte/line locators into the indexed document. `types` accepts `doc`, `readme`, `issue`, and `pull_request`, but the current source supports only `doc`; unsupported values return 400. The `version` filter is not supported by the current unversioned source and returns 400. Continuation bodies contain only `cursor` and optional `limit`; their pages come from the frozen snapshot and do not repeat the search.
- **Params:** `request` (object, **required**) — Search query or cursor-only continuation
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `developer_sources`

- **HTTP:** `GET /developer/sources`
- **What:** Discover indexed developer sources. Returns the registered developer source catalog and each source's exact supported operations, filters, artifact types, and index state. The current catalog contains only `go:docs`, a selected set of 18 parser-verified Go documentation/specification pages. A source is `not_indexed` until a complete generation is promoted. The catalog does not accept a cursor; `limit` may be 1–100.
- **Params:** `limit` (integer, optional) — Maximum sources to return (1–100; defaults to 100)

### `web_capabilities`

- **HTTP:** `GET /web/capabilities`
- **What:** Get web retrieval capabilities and limits. Returns the account's effective web retrieval limits and options: `available_operations`, `crawl_available`, `research_available`, `search_max_results`, `map_max_urls`, `crawl_max_pages`, `max_active_jobs`, and the accepted `render_modes`, `sitemap_modes` and `query_policies`. The operations list is empty while retrieval setup is incomplete.
- **Params:** _none_

### `web_crawl`

- **HTTP:** `POST /web/crawl`
- **What:** Submit a bounded resumable web crawl. Accepts an owner-scoped durable crawl job. `max_credits` is required; the accepted request and active reader/source revisions are frozen for idempotent replay. A repeated matching idempotency key returns the original job without preparing another reservation.
- **Params:** `request` (object, **required**) — Bounded crawl request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `web_crawl_cancel`

- **HTTP:** `POST /web/crawl/{job_id}/cancel`
- **What:** Request cooperative crawl cancellation. Requests cancellation of an owned crawl job. This control call does not reserve, charge, or settle credits; retained successful work is reconciled by the job settlement worker.
- **Params:** `job_id` (string, **required**) — Owned crawl job ID

### `web_crawl_results`

- **HTTP:** `GET /web/crawl/{job_id}/results`
- **What:** Read committed crawl outcomes. Reads committed outcomes in stable publication order. While running, `has_more=false` only means the job is currently drained; poll again with `next_cursor` to observe later outcomes. Each response is bounded to 1 MiB.
- **Params:** `cursor` (string, optional) — Opaque owner-bound cursor; `job_id` (string, **required**) — Owned crawl job ID; `limit` (integer, optional) — Outcomes per page

### `web_crawl_status`

- **HTTP:** `GET /web/crawl/{job_id}`
- **What:** Read crawl job status and cumulative accounting. Returns status for a crawl job owned by the authenticated principal. This control call does not reserve or settle credits.
- **Params:** `job_id` (string, **required**) — Owned crawl job ID

### `web_map`

- **HTTP:** `POST /web/map`
- **What:** Map a public site. Maps a public site into a bounded, approximate URL list from its sitemaps and the seed page's links. The first request needs `url`; options are `scope`, `sitemap` (`include`, `only`, `skip`), `max_urls` (1 to 5000, default 1000) and `page_size` (1 to 500, default 100). Continue with `cursor`, optionally with `page_size`; the first page's snapshot lasts 30 minutes.
- **Params:** `request` (object, **required**) — Map request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `web_search`

- **HTTP:** `POST /web/search`
- **What:** Search the public web. Search Brave's public web results. limit (1-50, default 10) is honoured by reading up to 3 result pages; each successful result page read costs 3 credits, and optional page reads (5 credits each) remain scoped to each result host. country and language select the result locale (defaults us and en-us).
- **Params:** `request` (object, **required**) — Search request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.
