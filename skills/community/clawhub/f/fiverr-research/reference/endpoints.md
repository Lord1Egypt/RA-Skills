# fiverr-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## Fiverr (3)

### `fiverr_gig`

- **HTTP:** `GET /fiverr/gig/{username}/{slug}`
- **What:** Get Fiverr gig detail. Returns a Fiverr gig detail page: title, description, category, pricing packages (basic/standard/premium tiers with price and delivery time), rating, review count, orders in queue, tags, gallery images, and a seller summary (level, rating, response time, languages). Seller level uses the same values on the search, seller and gig endpoints: level_one_seller, level_two_seller, top_rated_seller, or new_seller.
- **Params:** `slug` (string, **required**) — Fiverr gig URL slug, the trailing path segment after the username in a gig URL; `username` (string, **required**) — Fiverr seller username, e.g. from a search result's seller_username field

### `fiverr_search`

- **HTTP:** `GET /fiverr/search`
- **What:** Search Fiverr gigs. Searches Fiverr's public gig listings by free-text keyword, returning gig summaries (title, seller username, seller level, rating, review count, starting price, category, thumbnail image). Seller level uses the same values on the search, seller and gig endpoints: level_one_seller, level_two_seller, top_rated_seller, or new_seller.
- **Params:** `page` (integer, optional) — 1-based result page. Defaults to 1.; `q` (string, **required**) — Free-text gig search keyword

### `fiverr_seller`

- **HTTP:** `GET /fiverr/seller/{username}`
- **What:** Get Fiverr seller profile. Returns a Fiverr seller profile: display name, one-liner title, description, country, seller level, verification status, hourly rate, spoken languages, join date, and the seller's gig ids. Seller level uses the same values on the search, seller and gig endpoints: level_one_seller, level_two_seller, top_rated_seller, or new_seller.
- **Params:** `username` (string, **required**) — Fiverr seller username, e.g. from a search result's seller_username field
