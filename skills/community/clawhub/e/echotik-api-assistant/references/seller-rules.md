# Seller And Shop Module Rules

## 1. Module Scope

All seller-, shop-, or store-related questions should be routed through this module first. Typical examples include:

- discovering target shops by category or commerce mode
- retrieving shop detail records
- analyzing shop product inventories
- tracing shop-related creators, videos, and live sessions
- reading shop trend or leaderboard data

## 2. Seller Category Resolution

- Uses the same L1/L2/L3 progressive logic and `en-US`/`zh-CN` language rules as product category resolution (see `product-rules.md` §2), but with the seller-category endpoints:
  - `https://opendocs.echotik.live/echotik/seller/category/l1.md`
  - `https://opendocs.echotik.live/echotik/seller/category/l2.md`
  - `https://opendocs.echotik.live/echotik/seller/category/l3.md`

## 3. Seller List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/list.md`
- Purpose: advanced filtering and bulk discovery over the offline seller database

### Best Suited For

- target-shop discovery
- local versus cross-border seller screening
- shop filtering by category
- filtering by main commerce mode such as live or video

### Rules

- This dataset is always `T+1`.
- The freshest available state is yesterday's snapshot.
- Use category resolution first whenever a category filter is needed.

## 4. Seller Trend Snapshot - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/trend.md`
- Purpose: offline daily trend snapshots for seller sales metrics
- Follows the offline trend-snapshot behavior in `global-rules.md` (180-day lookback, non-contiguous dates).

## 5. Seller Detail - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/detail.md`
- Purpose: retrieve seller detail through `seller_id`

### Rules

- If this endpoint returns `code=0` with empty `data`, EchoTik has not collected this shop in the offline dataset.

## 6. Seller Product List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/product/list.md`
- Purpose: retrieve all products collected by EchoTik for a seller

### Rules

- The offline EchoTik product inventory may differ from the realtime seller product inventory.
- The offline list may include products that were historically listed and later taken down.
- When the user asks for a seller product list, ask whether they want offline EchoTik data or realtime data before execution.

## 7. Seller-Related Creator List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/influencer/list.md`
- Purpose: retrieve creator relationships for a seller

### Rules

- This endpoint returns seller-to-creator relationships, not full creator detail records.
- If the user wants richer creator fields, enrich the results through creator-detail endpoints.

## 8. Seller-Related Video List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/video/list.md`
- Purpose: retrieve videos associated with a seller

## 9. Seller-Related Live List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/live/list.md`
- Purpose: retrieve live sessions associated with a seller

## 10. Seller Rank List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/seller/ranklist.md`
- Purpose: retrieve seller leaderboards for local versus cross-border sellers and hot-sale versus hot-promotion ranking

### Rules

- Ranking behavior follows the same date and `T+1` logic as the product leaderboard family.
- Daily, weekly, and monthly leaderboard requests must use a `date` value aligned to the correct prior period.
- The endpoint supports local versus cross-border seller selection.

## 11. Realtime Seller Product List

- Documentation: `https://opendocs.echotik.live/realtime/seller/product/list.md`
- Purpose: retrieve the current seller product list in realtime

### Rules

- Respect the documented supported `region` values.
- The first request may omit the pagination token.
- If `has_more=true`, use `next_scroll_param` for the next page.

## 12. Orchestration

For multi-step seller workflows (discovery, performance reports), see `orchestration-playbooks.md`.
