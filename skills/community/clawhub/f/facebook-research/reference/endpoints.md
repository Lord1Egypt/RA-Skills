# facebook-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**2 endpoints across 1 platform group(s).**

## Facebook (2)

### `facebook_marketplace_search`

- **HTTP:** `GET /facebook/marketplace/search`
- **What:** Search Facebook Marketplace. Fetches Facebook Marketplace search or browse results for a location: listing id, title, price, city/state, and a thumbnail image per result. Only the first page Facebook's own server-rendered results page returns is available — Facebook's own further pagination requires a logged-in session and is out of scope. Omit both query and category to get the location's browse feed instead of running a search. minPrice, maxPrice, sortBy, daysSinceListed, and condition only take effect alongside a query or category (Facebook itself ignores them on the plain browse feed), except for the property_rentals category, which has its own always-filtered listing page. This endpoint can take noticeably longer than other search endpoints (up to roughly a minute in the slowest case) as it retries to get past an intermittent upstream condition; priced accordingly.
- **Params:** `category` (string, optional) — Marketplace category; `condition` (string, optional) — Comma-separated listing conditions; requires query or category; `days_since_listed` (integer, optional) — Restrict to listings posted within this many days; requires query or category; `location` (string, **required**) — Facebook Marketplace location vanity slug; `max_price` (integer, optional) — Maximum price in whole currency units; requires query or category; `min_price` (integer, optional) — Minimum price in whole currency units; requires query or category; `query` (string, optional) — Free-text search terms; omit (with category) for the location's browse feed; `sort_by` (string, optional) — Result order; requires query or category

### `facebook_page`

- **HTTP:** `GET /facebook/{page}`
- **What:** Get Facebook page details. Fetches public data about a Facebook Page given its page ID, vanity name, or full page URL: name, follower/like counts, intro, category, business hours/price range, review count, and any public contact details (email, phone, address, website, WhatsApp number) exposed on the Page's About tab.
- **Params:** `page` (string, **required**) — Facebook Page reference: vanity name, handle, profile.php id, or full Facebook URL
