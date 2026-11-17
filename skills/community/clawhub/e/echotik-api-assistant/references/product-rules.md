# Product Module Rules

## 1. Module Scope

All product-related questions should be routed through this module first. Typical examples include:

- identifying winning products
- retrieving product detail records
- analyzing product comments
- tracing product-related creators, videos, and live sessions
- reading product trend or leaderboard data

## 2. Product Category Resolution

- Documentation:
  - `https://opendocs.echotik.live/echotik/category/l1.md`
  - `https://opendocs.echotik.live/echotik/category/l2.md`
  - `https://opendocs.echotik.live/echotik/category/l3.md`
- Purpose: resolve category names into concrete `category_id` values before category-sensitive product queries

### Rules

- Use L1 first when the user only provides a broad category such as beauty, women's clothing, or men's clothing.
- Use L2 only after the correct L1 parent is known.
- Use L3 only after the correct L2 parent is known.
- `parent_id` for L2 is the selected L1 category ID.
- `parent_id` for L3 is the selected L2 category ID.
- The `language` parameter must match the current session language:
  - `en-US` for English requests
  - `zh-CN` for Chinese requests

## 3. Product List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/list.md`
- Purpose: advanced filtering and bulk discovery over the offline product database

### Best Suited For

- winning-product research
- breakout-product screening
- category-driven product sourcing
- high-dimensional product filtering

### Rules

- Unless the user explicitly requests off-shelf products, always pass `off_mark=0` to focus on products currently on sale.
- This dataset is always `T+1`.
- If the user wants recent breakout products, this endpoint is still valid because the freshest available state is yesterday's snapshot.
- Use category resolution first whenever a category filter is needed.

### Supported Filtering Directions

- product category
- total sales range
- last 30-day sales range
- average SKU price range
- commission-rate range
- creator-count range
- commerce-video-count range
- commerce-video-view range
- rating-score range
- review-count range
- full-managed shop flag
- free-shipping flag
- total GMV range
- last 30-day GMV range
- first-captured date range
- live versus video commerce mode
- shop type
- hot-product flag
- branded-shop flag

## 4. Product Trend Snapshot - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/trend.md`
- Purpose: offline daily trend snapshots for product sales and GMV metrics
- Follows the offline trend-snapshot behavior in `global-rules.md` (180-day lookback, non-contiguous dates).

## 5. Product Comment List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/comment.md`
- Purpose: retrieve collected offline comments for a product through `product_id`

### Rules

- This dataset may not contain the latest comments.
- If the user wants fresher or more complete comments, ask whether to switch to the realtime product-comment endpoint before execution.

## 6. Batch Product Detail - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/detail.md`
- Purpose: batch-retrieve product detail records through `product_id`

### Rules

- Supports up to `10` product IDs per request.
- Multiple product IDs must be comma-separated.
- This endpoint returns rich relationship data including associated videos, creators, live sessions, and summary metrics.
- If a requested `product_id` returns no offline data, ask whether the user wants to switch to the realtime product-detail endpoint.
- The realtime replacement requires an explicit `region`.

## 7. Product-Related Creator List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/influencer/list.md`
- Purpose: retrieve creator relationships for a product

### Rules

- This endpoint returns product-to-creator relationships, not the full creator detail record.
- Commerce relationships may come from video, live, or showcase attribution.
- If the user wants richer creator fields, enrich the results through creator-detail endpoints.

## 8. Product-Related Video List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/video/list.md`
- Purpose: retrieve videos associated with a product

### Rules

- Supports filtering by publish time.
- Supports filtering by creator `user_id`.
- Supports filtering by `product_id`.

## 9. Product-Related Live List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/live/list.md`
- Purpose: retrieve live sessions associated with a product

## 10. Product Rank List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/product/ranklist.md`
- Purpose: retrieve periodic product leaderboards

### Rules

- Supported ranking families are sales ranking and creator-promotion ranking.
- The output reflects periodic deltas calculated by EchoTik.
- All such ranking data is `T+1`.
- Daily, weekly, and monthly leaderboard requests must use a `date` value aligned to the correct prior period.

#### Time Window Interpretation

- weekly leaderboard: anchored to Monday
- monthly leaderboard: anchored to the first day of the month

For example:

- the monthly leaderboard for `2026-06` will only be available after `2026-07` begins

## 11. Extract Product ID - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/extract_product_id.md`
- Purpose: resolve `product_id` and current product region from a product share link

### Rules

- Use this first whenever the user provides a product share link instead of a canonical `product_id`.

## 12. Realtime Product Comment List

- Documentation: `https://opendocs.echotik.live/realtime/product/comment.md`
- Purpose: retrieve product comments in realtime

### Rules

- Respect the documented supported `region` values.
- Pagination starts from `offset=1`.
- If `has_more=true`, use `next_cursor` as the next `offset`.

## 13. Orchestration

For multi-step product workflows (discovery, reports), see `orchestration-playbooks.md`.
