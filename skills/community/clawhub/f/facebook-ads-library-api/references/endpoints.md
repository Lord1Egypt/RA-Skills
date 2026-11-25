# Facebook Ads Library API endpoint reference (SocialAPIs)

Base URL: `https://api.socialapis.io` · Auth: header `x-api-token: $SOCIALAPIS_API_KEY` · All endpoints are `GET` with query parameters.

Generated from the full reference in the `socialapis` skill. Machine-readable: https://socialapis.io/openapi.json

### `GET /facebook/ads/countries`

Docs and live example: https://socialapis.io/api-sources/meta-ads-countries

List the country codes the Ads Library tools accept in their country parameter. Pricing: 1 credit per call.

No parameters.

### `GET /facebook/ads/search`

Docs and live example: https://socialapis.io/api-sources/meta-ads-search

Search ads in the Meta Ad Library. Pass a keyword (query) to find ads about a topic, or ad_page_id to list one advertiser's ads; filter by country, active status and date range, sort by impressions or recency. Returns ads with creative, body text, dates, platforms and snapshot URL, plus an end_cursor. Get an advertiser's ad_page_id from `/facebook/ads/keywords` or `/facebook/pages/details`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | no | Search keyword for ads |
| `ad_page_id` | no | Facebook AD Page ID (alternative to query) |
| `country` | no | ISO country code or "ALL" |
| `activeStatus` | no | Filter: ALL, Active, or Inactive |
| `after_time` | no | Filter ads after this date (YYYY-MM-DD) |
| `before_time` | no | Filter ads before this date (YYYY-MM-DD) |
| `sort_data` | no | Sort by "impressions" or "recent" |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/ads/page-details`

Docs and live example: https://socialapis.io/api-sources/meta-ads-page-details

Get an advertiser's Ads Library profile: page name, verification status, category, location and total ad count. Needs the page ID (ad_page_id from `/facebook/pages/details` or page_id from `/facebook/ads/keywords`). To list the ads themselves, use `/facebook/ads/search` with ad_page_id. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `page_id` | yes | Advertiser page ID: ad_page_id from `/facebook/pages/details`, or page_id from `/facebook/ads/keywords` |

### `GET /facebook/ads/archive-details`

Docs and live example: https://socialapis.io/api-sources/meta-ads-archive-details

Get one Ad Library ad in full: creative, body text, CTA, platforms, countries, date range, and spend and impression estimates where Meta publishes them. Needs the ad_archive_id from a `/facebook/ads/search` result. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `ad_archive_id` | yes | Ad Library archive ID of the ad (ad_archive_id from a `/facebook/ads/search` result) |
| `page_id` | no | Facebook Page ID |
| `country` | no | ISO country code or "ALL" |
| `is_ad_non_political` | no | Filter non-political ads |
| `is_ad_not_aaa_eligible` | no | Filter AAA eligibility |

### `GET /facebook/ads/keywords`

Docs and live example: https://socialapis.io/api-sources/meta-ads-keywords

Find advertisers running ads that match a keyword: returns Facebook pages with their page_id and ad count. Use it to discover who advertises on a topic, then pass a page_id to `/facebook/ads/search` (as ad_page_id) or `/facebook/ads/page-details`. To get the ads for a keyword directly, use `/facebook/ads/search`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword to find advertisers for, e.g. running shoes |
| `country` | no | ISO country code or "ALL" |
