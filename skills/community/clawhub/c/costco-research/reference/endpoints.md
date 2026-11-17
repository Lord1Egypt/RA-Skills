# costco-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 1 platform group(s).**

## Costco (6)

### `costco_categories`

- **HTTP:** `GET /costco/categories`
- **What:** Get Costco category facets. Returns Costco category slugs and product counts relevant to an optional search term, each slug usable directly with GET /costco/search's category filter. Public data sourced from Costco's own search backend.
- **Params:** `query` (string, optional) — Search text to scope the returned categories to, e.g. \

### `costco_product`

- **HTTP:** `GET /costco/product/{id}`
- **What:** Get a Costco product's detail. Returns a Costco product's detail: title, description, manufacturer, image, price, stock status, and rating. Public data sourced from Costco's own product backend.
- **Params:** `id` (string, **required**) — Costco product id, e.g. from a search result's id field or a product page URL's \

### `costco_product_availability`

- **HTTP:** `GET /costco/product/{id}/availability`
- **What:** Get a Costco product's delivery estimate. Returns a Costco product's stock and estimated-delivery status for a delivery destination. Public data sourced from Costco's own fulfillment backend.
- **Params:** `id` (string, **required**) — Costco product id; `postal_code` (string, **required**) — US destination ZIP code; `state` (string, **required**) — US destination two-letter state code

### `costco_product_reviews`

- **HTTP:** `GET /costco/product/{id}/reviews`
- **What:** Get a Costco product's reviews. Returns a page of a Costco product's reviews: title, text, rating, author, and recommendation for each. Public data sourced from Costco's own review platform.
- **Params:** `id` (string, **required**) — Costco product id, e.g. from a search result's id field

### `costco_search`

- **HTTP:** `GET /costco/search`
- **What:** Search Costco products. Returns public Costco products matching a text query and/or a category slug: title, brand, model, image, and rating for each result. GDX is primary; if GDX is blocked, query-only searches may return explicitly partial product-sitemap results.
- **Params:** `category` (string, optional) — Costco category slug, e.g. the last path segment of a category page URL; `query` (string, optional) — Search text

### `costco_warehouses`

- **HTTP:** `GET /costco/warehouses`
- **What:** Find nearby Costco warehouses. Returns Costco warehouses near a latitude/longitude, sorted by distance: name, address, and distance for each. Public data sourced from Costco's own warehouse locator backend.
- **Params:** `latitude` (number, **required**) — Latitude; `longitude` (number, **required**) — Longitude
