# crowdfunding-campaign-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 2 platform group(s).**

## Kickstarter (4)

### `kickstarter_comments`

- **HTTP:** `GET /kickstarter/comments`
- **What:** Get a Kickstarter campaign's comments. Returns the first page of one Kickstarter campaign's comments feed (Kickstarter's own server-rendered initial batch, typically 40-60 comments; total_count reports the feed's real total). Each comment includes the author, whether the author is the creator (a reply), the posted timestamp, and the comment text. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

### `kickstarter_discover`

- **HTTP:** `GET /kickstarter/discover`
- **What:** Browse or search Kickstarter's Discover surface. Returns one page of Kickstarter's own Discover results -- browse by category id and/or a free-text search term, sorted by magic/popularity/newest/end_date/most_funded, optionally filtered by campaign state and/or restricted to staff picks. Each result includes the campaign's funding snapshot (goal, pledged, percent funded, backers), category, location, creator, and cover photo.
- **Params:** `category_id` (integer, optional) — Kickstarter's own numeric category id (top-level or sub-category), e.g. 16 for Technology; `page` (integer, optional) — 1-based page number; `sort` (string, optional) — Result order; `staff_pick_only` (boolean, optional) — Restrict results to Kickstarter's own \; `state` (array, optional) — Repeatable campaign state filter; `term` (string, optional) — Free-text search query

### `kickstarter_project`

- **HTTP:** `GET /kickstarter/project`
- **What:** Get a Kickstarter campaign's detail. Returns one Kickstarter campaign's detail: funding snapshot (goal, pledged, percent funded, backers, state, dates), category, creator, cover photo, story text, risks & challenges, update/comment/FAQ counts, and reward/pledge tiers. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi. Reward tiers are best-effort -- see the endpoint's documentation for when they may be omitted.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

### `kickstarter_updates`

- **HTTP:** `GET /kickstarter/updates`
- **What:** Get a Kickstarter campaign's updates feed. Returns one Kickstarter campaign's full updates feed: for each update, its number, title, author, whether the author is the creator, publish date, body text, and comment count. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.
