# Search Method

## Source

- Entry: `https://www.douyin.com/jingxuan/search/<keyword>?type=general`
- Browser transport: Easy WebBridge local HTTP API
- Browser context: an authorized connected Chromium profile
- Cost: no paid data API

## Automated sequence

1. Read online browsers from `GET /v1/browsers`.
2. Resolve one exact display name or `browserId`.
3. Create one unique task session and human-readable group title.
4. Navigate to the encoded keyword URL in one background tab.
5. Wait for `[data-e2e="searchbar-input"]` and `.search-result-card`.
6. Verify that the search input contains the requested keyword.
7. Scroll the same tab only until the requested limit is available or the page stops adding cards.
8. Extract cards from `.search-result-card`; derive the work ID from the closest `waterfall_item_*` container.
9. Close the task session unless `--keep-tab` was explicitly requested.

The visible interface path is equivalent: open Douyin Selected, fill `[data-e2e="searchbar-input"]`, then activate `[data-e2e="searchbar-button"]`. Prefer the encoded search URL for deterministic automation and use the visible controls when demonstrating the interaction itself.

## Extracted fields

- Search result order, not popularity rank
- Work ID and video/image type
- Duration for videos
- Visible like count text
- Title, author, visible publication text
- Cover URL and constructed Douyin work URL

Prefer semantic attributes and `.search-result-card` over hashed CSS classes. Fail clearly when the page contract changes.

## Boundaries

- This is a current webpage snapshot, not an official public API.
- Results vary by account, region, experiment, and time.
- “综合” search order is not a verified popularity ranking.
- Stop on login, CAPTCHA, access control, or risk-control pages.
- Never persist Easy WebBridge tokens, cookies, browser IDs, or session data.
