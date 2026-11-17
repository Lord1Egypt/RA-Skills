# Search Module Rules

## 1. Module Scope

All keyword-, image-, or query-style search requests should be routed through this module first. Typical examples include:

- searching creators by keyword
- searching products by keyword
- searching videos by keyword
- searching live sessions by keyword
- searching hashtags or music by keyword
- searching products from an image

## 2. Priority Rule

- When the user's intent is explicitly to search, prefer the dedicated realtime search endpoint for that entity.
- `Universal Search - EchoTik` is a fallback search endpoint only.
- Use the fallback search endpoint when:
  - the dedicated realtime search endpoint is unavailable for the target entity
  - the realtime search result is too sparse for broad discovery and a fallback is still useful
  - the user explicitly wants the EchoTik search-box style behavior
- All realtime keyword-search endpoints (creator, product, video, live, hashtag, music) paginate through `offset` unless an endpoint section below states otherwise.

## 3. Product Photo Search - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/product/photo-search.md`
- Purpose: search products from an input image encoded as base64

### Rules

- The image must be raw base64 without the `data:image/...;base64,` prefix.
- Supported formats are `png`, `jpg`, `jpeg`, and `webp`.
- Maximum size is `2 MB`.
- This endpoint does not paginate directly.
- It usually returns a random set of `6` products in `e_com_items`.
- Always pair this endpoint with `Product Photo Search Pagination - Realtime` when the user wants more results.
- Save the returned `image_uri` and `box_detection` values and pass them into the pagination endpoint for additional results.

## 4. Product Photo Search Pagination - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/product/photo-search/page.md`
- Purpose: paginate additional product results after the initial product photo-search response

### Rules

- This endpoint depends on `image_uri` and `box_detection` returned by the initial product photo-search request.

## 5. Hashtag Search - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/hashtag/search.md`
- Purpose: search hashtags by keyword in a target region

## 6. Creator Search - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/influencer/search.md`
- Purpose: search creators by keyword in realtime

## 7. Music Search - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/music/search.md`
- Purpose: search music tracks by keyword in realtime

## 8. Video Search - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/video/search.md`
- Purpose: search videos by keyword in realtime

## 9. Live Search - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/live/search.md`
- Purpose: search live sessions by keyword in realtime

## 10. Product Search - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/product/search.md`
- Purpose: search products by keyword in realtime

### Rules

- Product records are primarily returned under `data.body.sections[0].items`.
- The search endpoint does not return the full product detail shape.
- After retrieving `product_id`, use product detail when the user needs richer fields.

## 11. Universal Search - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/search/items.md`
- Purpose: fallback search across creators, products, shops, videos, and live sessions

### Rules

- Supports tokenized, fuzzy, and exact-match behavior.
- Returns at most `30` results.
- Does not return the same rich metric depth as list or detail endpoints.
- Use detail endpoints after search if the user needs richer fields.

## 12. Orchestration

For the full search priority order and entity mapping, see `orchestration-playbooks.md`.
