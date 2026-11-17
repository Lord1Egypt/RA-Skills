# auction-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## Bonhams (5)

### `bonhams_auction_detail`

- **HTTP:** `GET /bonhams/auctions/{id}`
- **What:** Get a Bonhams auction's normalized facts. Returns one Bonhams auction's facts by id: title, category, department, country, currency, sale dates, and lot count. Unlike the search endpoint, this is not restricted to upcoming/live auctions -- a historical/ended auction id resolves too.
- **Params:** `id` (string, **required**) — Bonhams auction id

### `bonhams_auction_lots`

- **HTTP:** `GET /bonhams/auctions/{id}/lots`
- **What:** List the lots in a Bonhams auction. Returns the lot listing for one Bonhams auction, optionally filtered by department and/or a free-text query.
- **Params:** `department` (string, optional) — Comma-separated department names (not a fixed enum -- varies per auction); `id` (string, **required**) — Bonhams auction id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 48, max 100; `q` (string, optional) — Free-text search across lot title, catalog description, and footnotes

### `bonhams_auction_search`

- **HTTP:** `GET /bonhams/auctions/search`
- **What:** Search Bonhams auctions. Searches and filters Bonhams' auctions. Default status "upcoming" excludes ended auctions, matching bonhams.com's own default; "past" browses Bonhams' full historical auction archive instead.
- **Params:** `auction_type` (string, optional) — Comma-separated auction types; `category` (string, optional) — Comma-separated categories. Allowed values: 20th & 21st Century Art, Asian Art, Books, History & Science, Classic Art, Decorative Arts & Furniture, Handbags, Jewels & Watches, Motoring, Popular Culture, Wine & Whisky.; `country` (string, optional) — Comma-separated country names (not a fixed enum -- live facet); `month` (string, optional) — Comma-separated month-and-year values, e.g. \; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 24, max 100; `q` (string, optional) — Free-text search across auction title and department names; `status` (string, optional) — Filters by bidding/completion status, default upcoming

### `bonhams_lot_detail`

- **HTTP:** `GET /bonhams/lots/{auctionId}/{lotNumber}`
- **What:** Get a Bonhams lot's normalized facts. Returns one Bonhams lot's facts: title, estimate range, hammer/realized price (once sold), sale date, category, department, and lot number. Full lot description prose, condition-report text, and additional images are not reproduced -- see the response fields.
- **Params:** `auctionId` (string, **required**) — Bonhams auction id; `lotNumber` (string, **required**) — Bonhams lot number

### `bonhams_lot_search`

- **HTTP:** `GET /bonhams/lots/search`
- **What:** Search Bonhams lots across every auction. Searches Bonhams lots across every auction, current and historical -- including sold/prices-realized lots -- optionally filtered by department, country, a GBP-normalized estimate price range, and/or a free-text query, in a caller-selected sort order. Without a query and without an explicit sort, results are ordered by most recently active sale date first.
- **Params:** `country` (string, optional) — Comma-separated country names (not a fixed enum -- live facet); `department` (string, optional) — Comma-separated department names (not a fixed enum -- large, changes over time); `max_price_gbp` (number, optional) — Maximum estimate, in GBP (converted from each lot's own sale currency), inclusive. Omit or 0 for no maximum.; `min_price_gbp` (number, optional) — Minimum estimate, in GBP (converted from each lot's own sale currency), inclusive. Omit or 0 for no minimum.; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 48, max 100; `q` (string, optional) — Free-text search across lot title, catalog description, and footnotes; `sort` (string, optional) — Result order. Default: Typesense relevance ranking when q is set, otherwise recency (most recently active sale date first).
