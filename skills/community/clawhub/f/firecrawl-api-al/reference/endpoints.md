# Reference: Endpoints

Base URL (direct HTTP): `https://api.firecrawl.dev/v2`. Auth header on every call: `Authorization: Bearer <FIRECRAWL_API_KEY>`. MCP equivalents: `firecrawl_scrape`, `firecrawl_crawl`, `firecrawl_map`, `firecrawl_search`.

All responses report `creditsUsed` (on the operation or inside `metadata`).

---

## scrape — `POST /v2/scrape`

- **Purpose:** Fetch a single URL and return clean content (Markdown/HTML/links/screenshot/summary) and/or structured JSON.
- **Sync/async:** Synchronous — returns content in the response.
- **Key params:** `url` (required); `formats` (array; default `["markdown"]`); `onlyMainContent`; `waitFor`; `actions`; `proxy`; `maxAge`. For structured data, include a format object `{type:"json", prompt, schema}`.
- **Response shape:** `{ success, data: { markdown?, html?, links?, screenshot?, summary?, json?, metadata: { sourceURL, statusCode, creditsUsed, title?, description?, ... } } }`.
- **Credit note:** Reported in `data.metadata.creditsUsed`. Cost rises with the number/kind of formats (screenshot, json, summary cost more than plain markdown).
  > Verification needed: confirm exact per-format credit costs at https://docs.firecrawl.dev.

---

## crawl — `POST /v2/crawl` (start) + `GET /v2/crawl/{id}` (poll)

- **Purpose:** Scrape many pages across a site/section with path filters and a bounded limit.
- **Sync/async:** **Asynchronous.** The start call returns a job id; you poll for results.
- **Key params (start):** `url` (required); `limit` (always set); `includePaths`; `excludePaths`; `scrapeOptions` (same shape as scrape options, applied to every page).
- **Start response:** `{ success, id, url }`.
- **Poll response (`GET /v2/crawl/{id}`):** `{ status, completed, total, data: [ <scrape-data objects> ], next? }`. `status` is `scraping` (in progress) or `completed`; follow `next` to paginate remaining results.
- **Credit note:** Cost scales with pages scraped and formats per page. Bound it with `limit` and minimal `scrapeOptions.formats`.
  > Verification needed: confirm crawl status values and pagination semantics at https://docs.firecrawl.dev.

---

## map — `POST /v2/map`

- **Purpose:** Quickly discover the URLs that exist on a site, optionally filtered.
- **Sync/async:** Synchronous.
- **Key params:** `url` (required); `search` (filter URLs by keyword/relevance); `limit`.
- **Response shape:** `{ success, links: [ { url, ... } ] }`.
- **Credit note:** Cheap relative to crawling. Use it to plan targeted scrapes/crawls.

---

## search — `POST /v2/search`

- **Purpose:** Run a web search and return ranked results; optionally scrape each result.
- **Sync/async:** Synchronous.
- **Key params:** `query` (required); `limit`; `scrapeOptions` (when present, each result is also scraped).
- **Response shape:** `{ success, data: { web: [ { url, title, description, position } ], news?, images? }, creditsUsed }`. With `scrapeOptions`, results also carry scraped content (markdown/metadata).
- **Credit note:** Search without `scrapeOptions` is cheaper; adding `scrapeOptions` adds scrape cost per result.

---

## Structured extraction (not a separate endpoint)

- Done via `scrape` with a `{type:"json", prompt, schema}` entry in `formats`. Read the result from `data.json`.
- The standalone `/v2/extract` endpoint is **deprecated** — do not use it.
