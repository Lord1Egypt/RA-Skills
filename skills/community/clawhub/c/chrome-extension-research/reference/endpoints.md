# chrome-extension-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**19 endpoints across 2 platform group(s).**

## ChromeWebStore (12)

### `chromewebstore_categories`

- **HTTP:** `GET /chromewebstore/categories`
- **What:** List Chrome Web Store categories and collections. Returns the reference taxonomy for the list endpoints: extension category groups and their subcategory slugs, the top-chart identifiers, and known curated collection slugs.
- **Params:** _none_

### `chromewebstore_category`

- **HTTP:** `GET /chromewebstore/category`
- **What:** List items in a Chrome Web Store category. Returns the item cards listed under an extensions category slug (e.g. `productivity/tools`, `lifestyle/shopping`, `make_chrome_yours/privacy`). Use /chromewebstore/categories for the reference taxonomy. Defaults: `num=50`, `country=us`, `lang=en`.
- **Params:** `category` (string, **required**) — Category slug under extensions; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_charts`

- **HTTP:** `GET /chromewebstore/charts`
- **What:** List a Chrome Web Store top chart. Returns the item cards in a store top chart. `chart` accepts `trending`, `popular`, or `notable`. Defaults: `chart=popular`, `num=50`, `country=us`, `lang=en`.
- **Params:** `chart` (string, optional) — Top chart to list; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_collection`

- **HTTP:** `GET /chromewebstore/collection`
- **What:** List items in a curated Chrome Web Store collection. Returns the item cards in a curated store collection slug (e.g. `editors_picks_extensions`, `dark_mode`, `ai_productivity`). Use /chromewebstore/categories for known collection slugs. Defaults: `num=50`, `country=us`, `lang=en`.
- **Params:** `collection` (string, **required**) — Curated collection slug; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_developer`

- **HTTP:** `GET /chromewebstore/developer`
- **What:** Retrieve a Chrome Web Store publisher and their items. Returns a Chrome Web Store publisher (developer) by publisher id, including the disclosed trader details — legal name, email, phone, address, website, and D-U-N-S number — plus the publisher's listed items ("More from ..."). Trader fields are only present for publishers that identify as EU traders. Defaults: `num=50`, `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store publisher id (u + 32 hex chars); `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_item`

- **HTTP:** `GET /chromewebstore/item`
- **What:** Retrieve Chrome Web Store item details. Returns detail for a Chrome Web Store extension or theme, including name, rating, rating count, user count, version, last-updated date, size, supported languages, developer, category, screenshots, and privacy links. Defaults: `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_permissions`

- **HTTP:** `GET /chromewebstore/permissions`
- **What:** Retrieve a Chrome Web Store item's declared permissions. Returns the permissions a Chrome Web Store extension declares in its manifest: `permissions`, `optional_permissions`, `host_permissions`, `optional_host_permissions`, plus `manifest_version` and `min_browser_version`. Useful for security and supply-chain review. Defaults: `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_privacy`

- **HTTP:** `GET /chromewebstore/privacy`
- **What:** Retrieve a Chrome Web Store item's privacy disclosures. Returns an extension's privacy disclosures as the store renders them: the developer's data-use statement, whether it collects data, the standard data-handling declarations, and the privacy-policy link. Defaults: `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_reviews`

- **HTTP:** `GET /chromewebstore/reviews`
- **What:** Retrieve Chrome Web Store item reviews. Returns the reviews the store renders on an item's reviews page, each with author, star rating, text, posted/edited dates and reviewed version. Defaults: `num=20`, `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of reviews; `sort` (string, optional) — Review sort order

### `chromewebstore_search`

- **HTTP:** `GET /chromewebstore/search`
- **What:** Search Chrome Web Store items. Returns Chrome Web Store search result cards for a keyword, each with id, name, rating, user count, publisher and detail URL. Defaults: `num=30`, `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of results; `term` (string, **required**) — Search keyword

### `chromewebstore_similar`

- **HTTP:** `GET /chromewebstore/similar`
- **What:** Retrieve related Chrome Web Store items. Returns the related-items shelf shown on a Chrome Web Store item's page. `id` is the required 32-character item id; `country` and `lang` default to `us` and `en`. Each card has name, publisher, category, rating, rating count, users, summary, icon and URL. An unknown or removed id returns 404.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_suggest`

- **HTTP:** `GET /chromewebstore/suggest`
- **What:** Suggest Chrome Web Store search terms. Returns search-term suggestions for a Chrome Web Store prefix given in `term`, up to `num` (default 8), with `country` and `lang` defaulting to `us` and `en`. Suggestions are the distinct item names of the top store-search results for that prefix, each returned as a `term`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of suggestions; `term` (string, **required**) — Search prefix to autocomplete

## Datasets (7)

### `datasets_chrome_extensions_changes`

- **HTTP:** `GET /datasets/chrome-extensions/changes`
- **What:** Get recent Chrome Web Store item changes. Lists recent change observations across Chrome Web Store items in the dataset, optionally for one `change_type`: `users`, `rating`, `rating_count`, `version`, `developer`, `permissions`, `privacy` or `status`. Returns up to `limit` (default 100, max 500), each with the item's name, category, developer, observed time and the figures that changed.
- **Params:** `change_type` (string, optional) — Change type enum: users, rating, rating_count, version, developer, permissions, privacy, status; `limit` (integer, optional) — Maximum observations, default 100, max 500

### `datasets_chrome_extensions_facets`

- **HTTP:** `GET /datasets/chrome-extensions/facets`
- **What:** Facet the Chrome Web Store dataset. Returns aggregation buckets. Facet enum: `item_type`, `category`, `developer`, `developer_email`, `manifest_version`, `permission`, `status`, `collects_data`, `has_broad_host_access`. Item type enum: `extension`, `theme`, `app`, `unknown`. Search sort, status and manifest-version enums match the search endpoint.
- **Params:** `category` (string, optional) — Exact category; `collects_data` (boolean, optional) — Data-collection filter; `developer` (string, optional) — Exact developer; `developer_email` (string, optional) — Exact developer email; `facet` (string, **required**) — Facet enum: item_type, category, developer, developer_email, manifest_version, permission, status, collects_data, has_broad_host_access; `has_broad_host_access` (boolean, optional) — Broad-host-access filter; `item_type` (string, optional) — Item type enum: extension, theme, app, unknown; `manifest_version` (integer, optional) — Manifest version enum: 2, 3; `min_rating` (number, optional) — Minimum rating; `min_rating_count` (integer, optional) — Minimum rating count; `min_users` (integer, optional) — Minimum users; `permission` (string, optional) — Exact permission; `q` (string, optional) — Full-text query; `sort` (string, optional) — Sort enum: relevance, users_desc, rating_desc, reviews_desc, updated_desc, trending_desc; `status` (string, optional) — Status enum: active, removed

### `datasets_chrome_extensions_history`

- **HTTP:** `GET /datasets/chrome-extensions/history/{id}`
- **What:** Get Chrome Web Store item history. Returns the change history of one Chrome Web Store item by `id`. A point is recorded only when a tracked field changed, with users, rating, version, permissions and the list of `change_types`. Narrow with `from` and `to` (YYYY-MM-DD); `limit` defaults to 365, max 1000.
- **Params:** `from` (string, optional) — Inclusive start date, YYYY-MM-DD; `id` (string, **required**) — Chrome Web Store item id; `limit` (integer, optional) — Maximum points, default 365, max 1000; `to` (string, optional) — Inclusive end date, YYYY-MM-DD

### `datasets_chrome_extensions_item`

- **HTTP:** `GET /datasets/chrome-extensions/items/{id}`
- **What:** Get a Chrome Web Store dataset item. Returns the stored record of one Chrome Web Store extension, theme or app by its 32-character `id`. It has name, `item_type`, category, users, rating, version, developer and disclosed email, declared permissions, host access flags, privacy disclosures and screenshots, taken from the latest observation.
- **Params:** `id` (string, **required**) — Chrome Web Store item id

### `datasets_chrome_extensions_metrics`

- **HTTP:** `GET /datasets/chrome-extensions/metrics`
- **What:** Get Chrome Web Store dataset metrics. Returns chart-ready coverage, adoption, rating, permission, privacy and recent-change aggregates for the stored Chrome Web Store dataset. Days enum: `7`, `30`, `90`.
- **Params:** `days` (integer, optional) — Recent-change window enum: 7, 30, 90; default 30; `limit` (integer, optional) — Top category and permission buckets, default 10, min 5, max 25

### `datasets_chrome_extensions_search`

- **HTTP:** `GET /datasets/chrome-extensions/search`
- **What:** Search the Chrome Web Store dataset. Searches stored Chrome Web Store item snapshots. Item type enum: `extension`, `theme`, `app`, `unknown`. Sort enum: `relevance`, `users_desc`, `rating_desc`, `reviews_desc`, `updated_desc`, `trending_desc`. Status enum: `active`, `removed`. Manifest version enum: `2`, `3`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `category` (string, optional) — Exact Chrome Web Store category; `collects_data` (boolean, optional) — Filter by public data-collection disclosure; `developer` (string, optional) — Exact displayed developer name; `developer_email` (string, optional) — Exact disclosed developer email; `has_broad_host_access` (boolean, optional) — Filter by broad host access; `item_type` (string, optional) — Item type enum: extension, theme, app, unknown; `manifest_version` (integer, optional) — Manifest version enum: 2, 3; `min_rating` (number, optional) — Minimum rating, 0 through 5; `min_rating_count` (integer, optional) — Minimum rating count; `min_users` (integer, optional) — Minimum displayed user count; `page` (integer, optional) — Page number, default 1; `page_size` (integer, optional) — Page size, default 20, max 100; `permission` (string, optional) — Exact declared permission; `q` (string, optional) — Full-text query, max 256 characters; `sort` (string, optional) — Sort enum: relevance, users_desc, rating_desc, reviews_desc, updated_desc, trending_desc; `status` (string, optional) — Status enum: active, removed

### `datasets_chrome_extensions_trending`

- **HTTP:** `GET /datasets/chrome-extensions/trending`
- **What:** Get trending Chrome Web Store items. Returns stored Chrome Web Store items ranked by the latest observed user and rating-count movement. Filters match the search endpoint; sort is fixed to `trending_desc`. Billing: this endpoint costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `category` (string, optional) — Exact category; `collects_data` (boolean, optional) — Data-collection filter; `developer` (string, optional) — Exact developer; `developer_email` (string, optional) — Exact developer email; `has_broad_host_access` (boolean, optional) — Broad-host-access filter; `item_type` (string, optional) — Item type enum: extension, theme, app, unknown; `manifest_version` (integer, optional) — Manifest version enum: 2, 3; `min_rating` (number, optional) — Minimum rating; `min_rating_count` (integer, optional) — Minimum rating count; `min_users` (integer, optional) — Minimum users; `page` (integer, optional) — Page number; `page_size` (integer, optional) — Page size, max 100; `permission` (string, optional) — Exact permission; `q` (string, optional) — Full-text query; `status` (string, optional) — Status enum: active, removed
