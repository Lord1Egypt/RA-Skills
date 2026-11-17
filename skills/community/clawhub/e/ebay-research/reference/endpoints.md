# ebay-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 1 platform group(s).**

## eBay (10)

### `ebay_item`

- **HTTP:** `GET /ebay/item/{item_id}`
- **What:** Get eBay item details. Returns the details of one eBay listing by `item_id`: title, link, images, price and price text, condition, availability, item specifics, description, location and shipping. It also carries the seller's name, store, feedback score, followers and items sold, along with the listing's rating and rating count.
- **Params:** `item_id` (string, **required**) — eBay item ID

### `ebay_live_stream`

- **HTTP:** `GET /ebay/live/streams/{id}`
- **What:** Get an eBay Live stream. Returns one eBay Live stream or event by `id`, taken from the `streams[].id` of the stream list. The response has title, description, state, start and end times, viewer, watch and like counts, tags, channels and the live, preview and replay URLs. Each host carries a 365-day feedback summary and four average ratings. An unknown id returns `404`.
- **Params:** `id` (string, **required**) — eBay Live stream/event id

### `ebay_live_stream_items`

- **HTTP:** `GET /ebay/live/streams/{id}/items`
- **What:** List an eBay Live stream's featured items. Lists the items currently featured in an eBay Live stream, identified by the required event `id`. Each item has its listing id, title, price and currency, bid count, sale type, leader and winner usernames, and `auction_status` (`READY`, `LIVE` or `ENDED`). A stream with no featured items, or an unknown id, returns an empty `items` array.
- **Params:** `id` (string, **required**) — eBay Live stream/event id

### `ebay_live_streams`

- **HTTP:** `GET /ebay/live/streams`
- **What:** List eBay Live streams. Lists live and upcoming eBay Live streams for one category channel, set with `category` (default `explore`; other values are channel ids such as `IPqZx79LNuwFcSVt` for Sports Singles). Each stream has its title, state, start time, watch count, hosts, tags and preview media. Host feedback is not included. Page on with `next_request_number` and `session_id`, passed back as `request_number` and `session_id`.
- **Params:** `category` (string, optional) — eBay Live category channel, defaults to explore; `request_number` (integer, optional) — Pagination cursor from a previous response's next_request_number, defaults to 0; `session_id` (string, optional) — Pagination session id from a previous response's session_id

### `ebay_live_streams_batch`

- **HTTP:** `GET /ebay/live/streams/batch`
- **What:** Get multiple eBay Live streams. Returns summaries for several eBay Live streams in one call. `ids` is required and takes up to 9 stream ids, comma-separated or repeated. Each stream has its title, state, watch count, hosts, tags and preview media, without the per-host feedback summary. Ids that do not resolve are silently omitted, and the order may differ from the request.
- **Params:** `ids` (string, **required**) — One or more eBay Live stream/event ids, up to 9. Comma-separated or repeated query values are both accepted.

### `ebay_search`

- **HTTP:** `POST /ebay/search`
- **What:** Search eBay listings. Searches eBay listings by keyword from a JSON body, with page, page size (60, 120 or 240) and a listing-status filter (`active`, `sold`, `completed` or `sold_completed`). Each result has the item id, title, link, image, price or price range, bid count, seller and rating, location, shipping information, and sold and watcher counts.
- **Params:** `option` (object, **required**) — eBay search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `ebay_seller`

- **HTTP:** `GET /ebay/seller/{seller}`
- **What:** Get eBay seller profile. Returns the public profile of an eBay seller by the required `seller` username: display name, store name and URL, profile URL, description, location, member-since date, positive feedback percentage, feedback count, items sold, followers, and detailed seller ratings. Feedback details are included when eBay provides them.
- **Params:** `seller` (string, **required**) — eBay seller username

### `ebay_seller_about`

- **HTTP:** `GET /ebay/seller/{seller}/about`
- **What:** Get eBay seller about details. Returns seller about information from the eBay store about tab, including seller stats, top-rated status, optional location/member-since fields, and cleaned store categories.
- **Params:** `seller` (string, **required**) — eBay seller username

### `ebay_seller_feedback`

- **HTTP:** `GET /ebay/seller/{seller}/feedback`
- **What:** Get eBay seller feedback. Returns the feedback eBay shows for a seller, identified by the required `seller` username. The response has the total feedback count, positive feedback percentage, overall rating summary, detailed seller ratings, and review cards with buyer, comment, rating, period and verified-purchase flag. Page with `page` (default 1) and `per_page` (24, 48 or 72; default 48), using `has_more` and `next_page`.
- **Params:** `page` (integer, optional) — Feedback page number; `per_page` (integer, optional) — Reviews per page; `seller` (string, **required**) — eBay seller username

### `ebay_seller_shop`

- **HTTP:** `GET /ebay/seller/{seller}/shop`
- **What:** Get eBay seller shop listings. Lists the items in an eBay seller's shop, identified by the required `seller` username, one page at a time with `page` (default 1). Each result has its item id, title, link, image, price or price range, shipping note, location, bid count and watcher count. The response gives the `total` and a `has_more` flag.
- **Params:** `page` (integer, optional) — Shop page number; `seller` (string, **required**) — eBay seller username
