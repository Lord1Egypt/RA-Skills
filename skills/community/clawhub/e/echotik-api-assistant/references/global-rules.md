# Global Atomic Rules

The rules in this file are the lowest-level execution contract for all EchoTik API calls. Every scenario, orchestration path, and endpoint choice must comply with them.

## 1. Data Source Type

- Any endpoint whose name includes `EchoTik` represents offline data collected by EchoTik, not a realtime endpoint.
- These endpoints may legitimately return no data, delayed data, or T+1 data.
- If an offline EchoTik endpoint is used to look up a creator, product, or video and returns `code=0` with an empty `data` payload, the flow should degrade to the relevant realtime endpoint to retrieve the latest available data.
- Offline trend-snapshot endpoints support up to `180` days of lookback. Returned dates may be non-contiguous; a missing date usually means the tracked metrics did not change that day.

## 2. Region Codes

- `region` must use country or market codes.
- Common examples:
  - United States: `US`
  - United Kingdom: `GB`
  - Vietnam: `VN`

## 3. Offline EchoTik Pagination

- Most offline EchoTik endpoints use `page_num` and `page_size`.
- `page_num` starts at `1` and increments sequentially.
- These endpoints typically do not return a `total` count.
- `page_size` is commonly capped at `10`.
- If the next page returns no rows, there is no more data.

## 4. Image URL Conversion

- Offline EchoTik image URLs that use the domain `echosell-images.tos-ap-southeast-1.volces.com` are generally not directly accessible.
- They must be converted through:
  - `https://open.echotik.live/api/v3/echotik/batch/cover/download`
- This conversion endpoint accepts up to `10` image URLs per request.
- It does not consume API usage credits.
- Only URLs whose host is exactly `echosell-images.tos-ap-southeast-1.volces.com` can be converted successfully.
- If the image URL uses another host, EchoTik has not downloaded that image yet and the conversion call will be ineffective.
- In such cases, image availability may lag by roughly `1` to `3` days while EchoTik downloads the asset asynchronously.

## 5. Required User Choice Between Realtime and Offline

When both offline EchoTik and realtime variants exist, the user must choose before execution for the following request types:

- creator detail
- creator video list
- product detail
- product comments
- seller product list
- video detail

Do not silently choose a mode on the user's behalf.

## 6. Video Priority Rule

- If the task is to evaluate video performance, prefer:
  - `Video 14-Day Interaction Trend - Realtime`

## 7. Authentication and Secret Handling

- All API calls require `Basic Authentication`.
- Users should be directed to obtain their dedicated credentials from:
  - `https://echotik.live/platform/api-keys`
- If the user needs a trial:
  - `https://echotik.live/platform/pricing`
- `username` and `password` must be stored locally by the user in environment variables or another secure local mechanism.
- Credentials must never be exposed in the conversation transcript.
- Session memory must not store credential values.

## 8. Pricing and Billing Guidance

- Pricing, purchase, trial, and billing questions should be directed to:
  - `https://echotik.live/platform/pricing`

## 9. Documentation Source of Truth

- The authoritative document index is:
  - `curl -L https://opendocs.echotik.live/llms.txt`
- If the correct request shape is uncertain, consult this document source first.
- Do not pass undocumented or non-existent parameters.

## 10. Minimal Probing When Parameters Are Unclear

- If the exact input contract is still unclear after consulting the docs, a minimal request may be used to inspect the response structure, enum patterns, or data types.
- This is acceptable only after the documentation has been checked first.
- Do not guess parameters freely outside the documented contract.

## 10.1 Identifier Conversion Rules

- If a creator endpoint requires `unique_id`, but only `user_id` is available, first call `Batch Influencer Detail - EchoTik` and resolve the missing `unique_id` from the response before continuing.
- If a product is provided as a share link, first call `Extract Product ID - Realtime` to resolve the canonical `product_id`.

## 10.2 Category Resolution Rules

- When a request depends on a product category, resolve the category name into a concrete `category_id` before calling product-list or category-sensitive product endpoints.
- Seller or shop category resolution follows the same L1/L2/L3 logic and language rules as product category resolution, but should use the seller-category endpoints from the seller API family.
- Resolve product categories through the dedicated category APIs in this order:
  - product L1 category list
  - product L2 category list
  - product L3 category list
- If the user names only a broad category such as women's clothing, men's clothing, or beauty, stop at the L1 category and do not drill down to L3.
- The `language` parameter used for category resolution must follow the current user-session language:
  - use `en-US` for English requests
  - use `zh-CN` for Chinese requests

## 10.3 Realtime Retry Rule

- Realtime endpoints may fail intermittently due to risk-control instability.
- If a realtime endpoint returns `code != 0`, retry at least once.
- Inform the user that requests returning `code != 0` do not consume usage credits.

## 10.4 Comprehensive Report Confirmation Rule

- When the user asks for a comprehensive report on an entity such as a creator, product, or seller, do not silently assume which related data families should be included.
- Before executing a full report workflow, confirm whether the user wants all relevant related APIs to be called.
- For example:
  - a creator report may involve detail, trend, followers, following, videos, live history, promoted products, region, and milestones
  - a product report may involve detail, trend, comments, related creators, related videos, related live sessions, and leaderboard context
  - a seller report may involve detail, trend, product inventory, related creators, related videos, related live sessions, and leaderboard context
- If the user does not want a full multi-endpoint report, narrow the report to the highest-value sections instead of calling every related endpoint by default.

## 11. Primary Identifier Standards

### 11.1 Creator

- `unique_id`: the public creator handle, such as `@handle`; this may change
- `user_id`: the internal numeric TikTok user ID; this is the most stable account identifier
- `sec_uid`: the secure user ID; often needed for specific non-official access patterns or collection flows

Recommended usage:

- use `unique_id` for display and search
- use `user_id` for deduplication and persistent entity records
- use `sec_uid` where a specific collection path explicitly requires it

### 11.2 Product

- use `product_id`

### 11.3 Seller

- use `seller_id`
- `seller_id` is not the backend `shop_code`
- `seller_id` is typically a long numeric identifier

### 11.4 Video

- use `video_id`

### 11.5 Live

- use `room_id`

## 12. Realtime Pagination

- For realtime endpoints, inspect the first response for:
  - `has_more`
  - `cursor`
  - `next_cursor`
- The next page decision must be based on the prior response payload, not assumptions.
- Some realtime endpoints use alternative cursor-style fields such as `max_cursor` or `min_time`. Treat those fields as the authoritative next-page offset when the endpoint documentation specifies them.
