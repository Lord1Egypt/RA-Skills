# Influencer Module Rules

## 1. Module Scope

All creator- or influencer-related questions should be routed through this module first. Typical examples include:

- identifying creators with the fastest follower growth
- finding creators who perform well in a specific category
- retrieving detailed creator profiles
- evaluating creator video performance
- analyzing creator follower-growth trends

## 2. Influencer Category Data

- Documentation: `https://opendocs.echotik.live/echotik/influencer/category_name.md`
- Purpose: provides the creator-category enumeration set
- Use it only when category filtering is required for:
  - `Influencer List - EchoTik`
  - `Influencer Rank List - EchoTik`

## 3. Influencer List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/influencer/list.md`
- Purpose: advanced filtering and bulk discovery over the offline creator database
- Best suited for:
  - discovering commerce-enabled creators
  - multi-condition creator screening
  - large-scale creator research

### Rules

- Use this endpoint first when the user wants to discover creators with delivery or commerce attributes.
- When the request specifies a concrete product L1 category, filter with `product_category_id`.
- When sorting is required, use:
  - `influencer_sort_field_v2`
  - `sort_type`
- Prefer `sort_type=1` for descending order.

### Supported Advanced Filters

- follower count
- like count
- engagement rate
- total views
- last 7-day views
- average commerce-video views
- average commerce-video views in the last 7 days
- gender
- creator language
- whether the storefront is enabled
- whether the creator is commerce-active

## 4. Influencer Trend Snapshot - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/influencer/trend.md`
- Purpose: offline daily trend snapshots for creator interaction and growth metrics

### Rules

- Supports up to `180` days of lookback.
- Returned dates may be non-contiguous.
- If the response includes dates such as:
  - `2026-06-01`
  - `2026-06-03`
  - `2026-06-07`
- the missing dates typically indicate that the creator's metrics did not change on those days.

## 5. Batch Influencer Detail - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/influencer/detail.md`
- Purpose: retrieve one or multiple creator detail records when `user_id` or `unique_id` is known

### Rules

- `user_ids` and `unique_ids` may each contain multiple values
- multiple values must be comma-separated
- this is the standard enrichment endpoint after list, rank, or search retrieval

## 6. Influencer Video List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/influencer/video/list.md`
- Purpose: retrieve the offline creator video inventory collected by EchoTik

### Rules

- Unlike the realtime video-list endpoint, this version includes enhanced commercial metrics such as:
  - video sales
  - GMV
  - recent interaction trend changes
- It also supports filtering by commerce product via `product_id`.
- When the user asks for a creator's video list, the system must ask whether they want offline EchoTik data or realtime data before execution.

## 7. Influencer Live List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/influencer/live/list.md`
- Purpose: retrieve the creator's historical live-stream sessions collected by EchoTik

## 8. Influencer Product List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/influencer/product/list.md`
- Purpose: retrieve the historical products promoted by a creator

### Rules

- Supports product-category filtering.
- This endpoint is primarily used to represent the relationship between creators and products.

## 9. Influencer Rank List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/influencer/ranklist.md`
- Purpose: retrieve periodic creator rankings such as follower-growth and sales leaderboards

### Rules

- Rank-list data is based on periodic deltas calculated by EchoTik.
- All such ranking data is `T+1`.
- Daily, weekly, and monthly leaderboard requests must use a `date` value that aligns with the correct prior period.

#### Time Window Interpretation

- weekly leaderboard: anchored to Monday
- monthly leaderboard: anchored to the first day of the month

For example:

- the monthly leaderboard for `2026-06` will only be available after `2026-07` begins

### Field Interpretation

- fields labeled `history` describe the creator's historical state
- they are not the current leaderboard period deltas

## 10. Orchestration

For multi-step creator workflows (discovery shortlists, health reports), see `orchestration-playbooks.md`. For creator video-performance analysis the offline list is preferred when the user needs sales/GMV/enhanced-trend fields, but the user must still choose realtime or offline mode first.

## 11. Realtime Influencer Detail

- Documentation: `https://opendocs.echotik.live/realtime/influencer/detail.md`
- Purpose: retrieve the creator's public web-facing data in realtime using `unique_id`

## 12. Realtime Influencer Video List

- Documentation: `https://opendocs.echotik.live/realtime/influencer/video/list.md`
- Purpose: retrieve a creator's realtime video list using `unique_id`

### Rules

- Supports pagination through an offset-style cursor.
- Use `max_cursor` as the next-page value.
- The default order is reverse chronological by publish time, excluding pinned-video behavior.

## 13. Realtime Influencer Follower List

- Documentation: `https://opendocs.echotik.live/realtime/influencer/follower/list.md`
- Purpose: retrieve a creator's follower list using `user_id`

### Rules

- Supports pagination through `offset`.
- Use `min_time` as the next offset.

## 14. Realtime Influencer Following List

- Documentation: `https://opendocs.echotik.live/realtime/influencer/following/list.md`
- Purpose: retrieve a creator's following list using `user_id`

### Rules

- Supports pagination through `offset`.
- Use `min_time` as the next offset.

## 15. Realtime Influencer Region

- Documentation: `https://opendocs.echotik.live/realtime/influencer/region`
- Purpose: retrieve a creator's region in realtime using `unique_id`

### Rules

- This endpoint is not guaranteed to succeed consistently.
- If it fails to return the creator region, call `Realtime Influencer Video List` once and use the region from the first returned video as a fallback approximation.

## 16. Creator Homepage QR Code

- Documentation: `https://opendocs.echotik.live/realtime/influencer/generate/qrcode.md`
- Purpose: generate a QR code for the creator homepage using `user_id`

## 17. Creator Milestones - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/influencer/milestones_insight.md`
- Purpose: retrieve creator milestone data through `user_id`

### Rules

- Use this endpoint when the user asks about milestone events such as follower or view thresholds reached over time.
