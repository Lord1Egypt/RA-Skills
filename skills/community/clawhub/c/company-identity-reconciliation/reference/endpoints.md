# company-identity-reconciliation — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 7 platform group(s).**

## Brand (1)

### `brand_retrieve`

- **HTTP:** `GET /brand/retrieve`
- **What:** Retrieve brand data by domain. Returns a brand profile for a domain (title, description, brand colors as hex, logos and icons ranked best-first, backdrops, socials, links, and any schema.org organization data). Enrichment-only fields that are not present in the page markup are returned as null.
- **Params:** `domain` (string, **required**) — Domain to retrieve brand data for, e.g. context.dev; `force_language` (string, optional) — Accepted for compatibility; not applied in HTML-only mode; `maxAgeMs` (integer, optional) — Cache freshness window in milliseconds, clamps to 1 day..1 year; `maxSpeed` (boolean, optional) — Optimize for speed by skipping schema.org and footer-link extraction; `timeoutMS` (integer, optional) — Upstream fetch timeout in milliseconds, clamps to 1000..300000

## LinkedIn (1)

### `linkedin_company`

- **HTTP:** `GET /linkedin/company/{id}`
- **What:** Get LinkedIn Company info by ID. Returns a LinkedIn company page by its company `id`. The response has the name, headline, about text, industry, company size, employee count on LinkedIn, follower count, founding year, headquarters, locations, specialties, website, logo, Products section cards, affiliated and similar pages, and recent updates with reactions and comment counts.
- **Params:** `id` (string, **required**) — LinkedIn Company ID

## SEC EDGAR (3)

### `sec_company_search`

- **HTTP:** `GET /sec/company/search`
- **What:** Resolve a ticker or company name to EDGAR companies. Resolves a ticker symbol or company-name query to SEC EDGAR companies (CIK, ticker, name).
- **Params:** `limit` (integer, optional) — Max matches, default 10, max 100; `q` (string, **required**) — Ticker symbol or company name

### `sec_company_submissions`

- **HTTP:** `GET /sec/company/submissions`
- **What:** List a company's EDGAR filings. Returns a company's recent SEC filings (form, dates, primary document URL) filtered by form type and date range, plus company profile fields as reported by EDGAR: entity_type, former_names, exchanges, category, fiscal_year_end, state_of_incorporation. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `form` (string, optional) — Filter by form type, e.g. 10-K, 10-Q, 8-K; `from` (string, optional) — Earliest filing date (YYYY-MM-DD); `limit` (integer, optional) — Max filings, default 50, max 500; `ticker` (string, optional) — Ticker symbol (alternative to cik); `to` (string, optional) — Latest filing date (YYYY-MM-DD)

### `sec_filing`

- **HTTP:** `GET /sec/filing`
- **What:** Get a single filing by accession number. Returns a single SEC filing's metadata and primary document URL. Provide accession plus cik or ticker.
- **Params:** `accession` (string, **required**) — Accession number; `cik` (string, optional) — SEC CIK (numeric or zero-padded); `ticker` (string, optional) — Ticker symbol (alternative to cik)

## Datasets (2)

### `datasets_jobs_companies`

- **HTTP:** `GET /datasets/jobs/companies`
- **What:** Find which companies are hiring. Searches the discovered company board registry — which companies are hiring, on which ATS (or, for the 5 single-company big-tech providers, which platform), with how many open roles. Set sponsors_visa=true to keep companies with certified employer filings in recent public U.S. Department of Labor LCA disclosure data. This is company-level historical evidence, not a guarantee for a specific role or candidate. provider enum: `greenhouse`, `lever`, `ashby`, `workday`, `smartrecruiters`, `workable`, `recruitee`, `rippling`, `personio`, `teamtailor`, `oracle`, `ukg`, `icims`, `eightfold`, `gem`, `pinpoint`, `amazon-jobs`, `apple-jobs`, `google-jobs`, `meta-jobs`, `tesla-jobs`. status enum: `active`, `empty`, `gone`, `blocked`, `pending`, `invalid`. sort enum: `open_desc`, `company_asc`, `crawled_desc`. Billing: this endpoint costs 1 credit per 10 records returned, rounded up, with a minimum of 1 (up to 10 records cost 1, a full page of 100 costs 10).
- **Params:** `min_open_roles` (integer, optional) — Minimum open roles; `page` (integer, optional) — Page number, default 1; `page_size` (integer, optional) — Page size, default 20, max 100; `provider` (string, optional) — Provider filter; `q` (string, optional) — Match on company name / domain; `sort` (string, optional) — Sort enum: open_desc, company_asc, crawled_desc; `sponsors_visa` (boolean, optional) — Keep companies with recent certified DOL LCA filings (default false); `status` (string, optional) — Board status. Enum: active, empty, gone, blocked, pending, invalid

### `datasets_jobs_company_item`

- **HTTP:** `GET /datasets/jobs/companies/{id}`
- **What:** Get a single company by board id. Returns one discovered company board by its dataset board id. When the company name matches recent public U.S. Department of Labor LCA disclosure data, the response includes `lca_sponsorship` with filing counts and observed fiscal-quarter range; this is company-level historical evidence, not a guarantee for a specific role or candidate. When the board carries a known domain, the response also includes a `tech_stack` firmographic hint. Returns 404 when the board id is not in the registry.
- **Params:** `id` (string, **required**) — Dataset board id

## Jobs (1)

### `jobs_company_search`

- **HTTP:** `GET /jobs/company-search`
- **What:** Find which ATS a company uses by slug. Probes Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee, Rippling, Teamtailor, and Pinpoint in parallel for a slug and reports the providers where it resolves to a non-empty board (with the open-role count and board URL). Workday is excluded (its board needs tenant + datacenter + site).
- **Params:** `slug` (string, **required**) — Company careers slug to probe

## Bing (1)

### `bing_search`

- **HTTP:** `GET /bing/search`
- **What:** Search Bing web results. Returns Bing web search results for a query string, including organic results, optional context panel data, related queries, people-also-ask questions, news modules, video modules, and page-based pagination. Empty optional blocks are omitted from the JSON response. Locale defaults to country=us and lang=en-us. Returns 503 on a genuine transport failure or challenge page. Bing occasionally serves a well-formed page whose results share no significant term with the query; when every attempt hits this, the response is still returned as 200 with data.low_confidence set to true (and the X-Low-Confidence header) instead of being withheld, so callers get Bing's real answer plus an honest signal to double-check it rather than nothing. Queries that use the site: operator (for example site:gov.hu) are not supported: Bing serves a bot-verification challenge for them, so they are rejected with 400 before any request is made. Use the DuckDuckGo (/api/v1/duckduckgo/search), Brave (/api/v1/brave/search), or Yahoo (/api/v1/yahoo-search/search) search endpoints for domain-restricted searches instead.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.
