# competitor-intelligence — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**17 endpoints across 7 platform group(s).**

## Bing (1)

### `bing_search`

- **HTTP:** `GET /bing/search`
- **What:** Search Bing web results. Returns Bing web search results for a query string, including organic results, optional context panel data, related queries, people-also-ask questions, news modules, video modules, and page-based pagination. Empty optional blocks are omitted from the JSON response. Locale defaults to country=us and lang=en-us. Returns 503 on a genuine transport failure or challenge page. Bing occasionally serves a well-formed page whose results share no significant term with the query; when every attempt hits this, the response is still returned as 200 with data.low_confidence set to true (and the X-Low-Confidence header) instead of being withheld, so callers get Bing's real answer plus an honest signal to double-check it rather than nothing. Queries that use the site: operator (for example site:gov.hu) are not supported: Bing serves a bot-verification challenge for them, so they are rejected with 400 before any request is made. Use the DuckDuckGo (/api/v1/duckduckgo/search), Brave (/api/v1/brave/search), or Yahoo (/api/v1/yahoo-search/search) search endpoints for domain-restricted searches instead.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

## Web (2)

### `extract`

- **HTTP:** `POST /extract`
- **What:** Extract schema-conforming JSON from a URL. Reads a public URL as clean Markdown, then returns data that strictly conforms to the supplied bounded JSON Schema. The response includes `truncated`, which is true when the page was too long and only its first part was used.
- **Params:** `extractOption` (object, **required**) — Extraction options
- **REST body:** Send the value of the MCP argument `extractOption` directly as the JSON body; do not wrap it in a `extractOption` property.

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.

## SimilarWeb (2)

### `similarweb_search`

- **HTTP:** `GET /similarweb/search`
- **What:** Search SimilarWeb Info. Looks up a domain or keyword on SimilarWeb and returns the matching websites, companies (name, domain and logo) and apps on the App Store and Google Play.
- **Params:** `q` (string, **required**) — Domain or keyword to search

### `similarweb_web`

- **HTTP:** `GET /similarweb/web/{domain}`
- **What:** Get SimilarWeb Web Info. Returns SimilarWeb's traffic profile for one domain: global, country and category rank, estimated monthly visits, engagement (bounce rate, pages per visit, time on site), top countries, traffic sources, top keywords and similar sites. `DataSource` shows whether the full source or the narrower public-page fallback answered; the fallback omits several fields.
- **Params:** `domain` (string, **required**) — Domain to fetch SimilarWeb data for

## ProductHunt (4)

### `producthunt_alternatives`

- **HTTP:** `GET /producthunt/product/{id}/alternatives`
- **What:** Retrieve Product Hunt product alternatives. Lists alternatives to a Product Hunt product, looked up by its slug in `id`. `first` sets the page size (default 10), `order` defaults to `most_relevant`, and `tags` takes comma-separated tag slugs. Returns alternative items with ratings, badges and scores, alternative tags with counts, and related discussions. Use `end_cursor` as `cursor` for the next page.
- **Params:** `cursor` (string, optional) — Pagination cursor; `first` (integer, optional) — Page size; `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Sort order; `tags` (string, optional) — Comma-separated tag slugs

### `producthunt_launches`

- **HTTP:** `GET /producthunt/product/{id}/launches`
- **What:** Retrieve Product Hunt product launches. Lists the launch posts of a Product Hunt product, looked up by its slug in `id`. `order` defaults to `DATE`; pass the returned `end_cursor` as `cursor` for the next page. Each launch has its name, tagline, ranks, scores, comment count, badges and dates. An unknown slug returns 404.
- **Params:** `cursor` (string, optional) — Pagination cursor; `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Product Hunt launch order

### `producthunt_product`

- **HTTP:** `GET /producthunt/product/{id}`
- **What:** Retrieve Product Hunt product details. Returns the core Product Hunt product details. The path takes an exact Product Hunt slug; if you only know the product name, look the slug up first with `/producthunt/search` (live) or `/datasets/producthunt-products/search` (indexed). Unknown slugs return 404, and that 404 is cached for 24 hours.
- **Params:** `id` (string, **required**) — Product Hunt slug or numeric ID

### `producthunt_search`

- **HTTP:** `GET /producthunt/search`
- **What:** Search for products, users, or launches on Product Hunt. Searches Product Hunt for the required `query`. `type` is `product` (default), `user` or `launch`, and `page` starts at 1. `featured` and `topics` apply to launch search only. Results come as `edges` with `pageInfo` and `pagesCount`; launch search also returns topic aggregations.
- **Params:** `featured` (boolean, optional) — Launch search only: featured launches only; `page` (integer, optional) — Page number (1-based); `query` (string, **required**) — Search keywords; `topics` (string, optional) — Launch search only: comma-separated topic slugs; `type` (string, optional) — Result type: **product** (default), **user**, or **launch**

## Trustpilot (3)

### `trustpilot_business`

- **HTTP:** `GET /trustpilot/business/{slug}`
- **What:** Get Trustpilot business profile. Returns a Trustpilot business profile by `slug`, such as `openai.com`. The profile has the name, `trust_score`, `review_count`, rating histogram, review summary and topics, categories, claimed status, website URL, reply metrics, company activity and verification flags, and an about section with description and contact details.
- **Params:** `slug` (string, **required**) — Trustpilot business slug

### `trustpilot_business_reviews`

- **HTTP:** `GET /trustpilot/business/{slug}/reviews`
- **What:** Get Trustpilot business reviews. Returns one page of Trustpilot reviews for a business slug such as `openai.com`, with filters for star rating, verified reviews, reviews with a company reply, language and text search. Each review has its rating, title, body, author name, country and review count, dates, and any company reply; the response also carries the business summary and pagination totals.
- **Params:** `date_from` (string, optional) — Date range start in YYYY-MM-DD; currently rejected by upstream; `date_to` (string, optional) — Date range end in YYYY-MM-DD; currently rejected by upstream; `language` (string, optional) — Review language code used by Trustpilot; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, optional) — Text search within reviews; `replied` (boolean, optional) — Filter to reviews with business replies; `slug` (string, **required**) — Trustpilot business slug; `stars` (integer, optional) — Filter by star rating from 1 to 5; `verified` (boolean, optional) — Filter to verified reviews

### `trustpilot_business_search`

- **HTTP:** `GET /trustpilot/business-units/search`
- **What:** Search Trustpilot business units. Searches Trustpilot for businesses matching a query, for a country (default `US`), with `page` and `page_size` (default 20, max 100). Each result has the display name, identifying name, TrustScore, star rating, review count, categories, website, email, phone, address and Trustpilot URL; `total_hits` gives the full match count.
- **Params:** `country` (string, optional) — Two-letter country code; defaults to US; `page` (integer, optional) — 1-based page number; defaults to 1; `page_size` (integer, optional) — Results per page; defaults to 20, maximum 100; `q` (string, **required**) — Search query

## Capterra (3)

### `capterra_product`

- **HTTP:** `GET /capterra/product`
- **What:** Get a Capterra product. Returns a Capterra product profile: name, description, category, and aggregate rating.
- **Params:** `product_id` (string, **required**) — Capterra product id (the numeric id in a /p/{id}/{slug}/ URL)

### `capterra_reviews`

- **HTTP:** `GET /capterra/product/reviews`
- **What:** Get Capterra product reviews. Returns a page of Capterra reviews (author, headline, rating) plus the product's aggregate rating.
- **Params:** `page` (integer, optional) — Page number (default 1); `product_id` (string, **required**) — Capterra product id (the numeric id in a /p/{id}/{slug}/ URL)

### `capterra_search`

- **HTTP:** `GET /capterra/search`
- **What:** Search Capterra products. Returns Capterra search-result products (id, name, url, description, rating). Note: Capterra renders a fallback product list even for queries with no genuine match, rather than a distinct empty-results page, so callers should treat low-relevance results as an upstream characteristic, not a bug.
- **Params:** `q` (string, **required**) — Search query

## Datasets (2)

### `datasets_jobs_companies`

- **HTTP:** `GET /datasets/jobs/companies`
- **What:** Find which companies are hiring. Searches the discovered company board registry — which companies are hiring, on which ATS (or, for the 5 single-company big-tech providers, which platform), with how many open roles. Set sponsors_visa=true to keep companies with certified employer filings in recent public U.S. Department of Labor LCA disclosure data. This is company-level historical evidence, not a guarantee for a specific role or candidate. provider enum: `greenhouse`, `lever`, `ashby`, `workday`, `smartrecruiters`, `workable`, `recruitee`, `rippling`, `personio`, `teamtailor`, `oracle`, `ukg`, `icims`, `eightfold`, `gem`, `pinpoint`, `amazon-jobs`, `apple-jobs`, `google-jobs`, `meta-jobs`, `tesla-jobs`. status enum: `active`, `empty`, `gone`, `blocked`, `pending`, `invalid`. sort enum: `open_desc`, `company_asc`, `crawled_desc`. Billing: this endpoint costs 1 credit per 10 records returned, rounded up, with a minimum of 1 (up to 10 records cost 1, a full page of 100 costs 10).
- **Params:** `min_open_roles` (integer, optional) — Minimum open roles; `page` (integer, optional) — Page number, default 1; `page_size` (integer, optional) — Page size, default 20, max 100; `provider` (string, optional) — Provider filter; `q` (string, optional) — Match on company name / domain; `sort` (string, optional) — Sort enum: open_desc, company_asc, crawled_desc; `sponsors_visa` (boolean, optional) — Keep companies with recent certified DOL LCA filings (default false); `status` (string, optional) — Board status. Enum: active, empty, gone, blocked, pending, invalid

### `datasets_jobs_search`

- **HTTP:** `GET /datasets/jobs/search`
- **What:** Search the jobs dataset (all companies' live postings). Full-text + faceted search over every job posting crawled from every discovered company ATS board (Greenhouse, Lever, Ashby, Workday, SmartRecruiters, Workable, Recruitee, Rippling, Personio, Teamtailor, Oracle, UKG, iCIMS, Eightfold, Gem, Pinpoint) plus 5 single-company big-tech careers platforms (Amazon, Apple, Google, Meta, Tesla). Open roles only by default (set include_closed=true for historical/filled roles). Salary is parsed from a structured field when the provider has one, or from an explicit pay figure stated in the description otherwise, so coverage varies by posting rather than by provider; min_salary/max_salary filter on it and require salary_currency, since comparing raw compensation numbers across currencies is meaningless. Location is also exposed as structured city/state/country fields alongside the free-text location string, so city/state/country filter on an exact match of those parsed components rather than substring-matching the display string. job_family is an exact level-2 ISCO family label assigned from ESCO occupation evidence; ambiguous postings remain unclassified and do not match that filter. employment_type is never populated for google-jobs/meta-jobs, and posted_at (so sort=posted_desc) is never populated for meta-jobs/tesla-jobs -- their upstream APIs expose no such field. provider enum: `greenhouse`, `lever`, `ashby`, `workday`, `smartrecruiters`, `workable`, `recruitee`, `rippling`, `personio`, `teamtailor`, `oracle`, `ukg`, `icims`, `eightfold`, `gem`, `pinpoint`, `amazon-jobs`, `apple-jobs`, `google-jobs`, `meta-jobs`, `tesla-jobs`. workplace_type enum: `onsite`, `hybrid`, `remote`. sort enum: `relevance`, `posted_desc`, `company_asc`. Billing: this search costs 1 credit per 10 records returned, rounded up, with a minimum of 1 (up to 10 records cost 1, a full page of 100 costs 10).
- **Params:** `city` (string, optional) — Exact city filter (parsed location component); `company` (string, optional) — Company name match; `country` (string, optional) — Exact country filter (parsed location component); ISO country code or name, matched case-insensitively; `department` (string, optional) — Exact department filter; `employment_type` (string, optional) — Exact employment-type filter; `include_closed` (boolean, optional) — Include closed/filled roles (default false = open only); `job_family` (string, optional) — Exact ESCO/ISCO job-family label filter; `location` (string, optional) — Location match; `max_salary` (number, optional) — Maximum salary (matches postings whose range starts at or below this); requires salary_currency; `min_salary` (number, optional) — Minimum salary (matches postings whose range reaches at least this); requires salary_currency; `page` (integer, optional) — Page number, default 1; `page_size` (integer, optional) — Page size, default 20, max 100; page*page_size must be <= 10000; `provider` (string, optional) — Provider filter; `q` (string, optional) — Full-text over title, company, description; `remote` (boolean, optional) — Filter by remote (true or false); `salary_currency` (string, optional) — 3-letter ISO currency code (e.g. USD) the min_salary/max_salary bounds are in; required when either bound is set; `sort` (string, optional) — Sort enum: relevance, posted_desc, company_asc; `state` (string, optional) — Exact state/region filter (parsed location component); `workplace_type` (string, optional) — Workplace type filter
