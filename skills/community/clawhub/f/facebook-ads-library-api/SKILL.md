---
name: facebook-ads-library-api
description: Search the Meta (Facebook) Ad Library: the ads a brand or keyword is running in a country, with creative text, start date, platforms and, where Meta shows them, impressions and spend ranges; the advertisers behind a keyword; and one ad or one advertiser page in detail, through the SocialAPIs REST API. Use for competitor ad research, ad monitoring, or code that reads the Ad Library without app review.
---

# Facebook Ads Library API (SocialAPIs)

The Meta Ad Library as JSON: every public ad a brand runs, searchable by keyword, advertiser and country. No app review, no Meta access token.

- Website: https://socialapis.io · this API: https://socialapis.io/api-sources/meta-ads-search
- Free API key: https://socialapis.io/auth/signup (200 credits a month, no card)
- Free ad checker, no signup: https://socialapis.io/tools/facebook-ad-checker
- Every parameter: [references/endpoints.md](references/endpoints.md) · OpenAPI: https://socialapis.io/openapi.json · llms.txt: https://socialapis.io/llms.txt

## Setup

1. The user needs an API key from https://socialapis.io/dashboard.
2. Read it from the environment, `SOCIALAPIS_API_KEY`. **Never** hard-code it, print it, or ask the user to paste it into the chat. If it is missing, tell the user to set it.
3. Send it in the **`x-api-token` header**, never in the URL.

If SocialAPIs MCP tools are available in this session (`facebook_page`, `facebook_ads`, `instagram_profile`, …), use them instead of raw HTTP. Hosted MCP server: `https://mcp.socialapis.io/mcp`.

## Making a call

```bash
curl -s -H "x-api-token: $SOCIALAPIS_API_KEY" \
  "https://api.socialapis.io/facebook/ads/search?query=nike&country=US&activeStatus=Active&sort_data=impressions"
```

```python
import os, requests

r = requests.get(
    "https://api.socialapis.io/facebook/ads/search",
    params={"query": "nike", "country": "US", "activeStatus": "Active", "sort_data": "impressions"},
    headers={"x-api-token": os.environ["SOCIALAPIS_API_KEY"]},
    timeout=120,
)
r.raise_for_status()
data = r.json()
```

SDKs: Python `pip install socialapis-sdk`, JavaScript `npm install socialapis-sdk`, PHP `composer require socialapishub/socialapis`.

## Endpoints

All `GET`, base URL `https://api.socialapis.io`. Each link opens the endpoint's page with a live example.

| Endpoint | What it returns | Credits |
|---|---|---|
| [`/facebook/ads/countries`](https://socialapis.io/api-sources/meta-ads-countries) | List the country codes the Ads Library tools accept in their country parameter. | 1 credit per call |
| [`/facebook/ads/search`](https://socialapis.io/api-sources/meta-ads-search) | Search ads in the Meta Ad Library. | 1 credit per call |
| [`/facebook/ads/page-details`](https://socialapis.io/api-sources/meta-ads-page-details) | Get an advertiser's Ads Library profile: page name, verification status, category, location and total ad count. | 1 credit per call |
| [`/facebook/ads/archive-details`](https://socialapis.io/api-sources/meta-ads-archive-details) | Get one Ad Library ad in full: creative, body text, CTA, platforms, countries, date range, and spend and impression estimates where Meta publishes them. | 1 credit per call |
| [`/facebook/ads/keywords`](https://socialapis.io/api-sources/meta-ads-keywords) | Find advertisers running ads that match a keyword: returns Facebook pages with their page_id and ad count. | 1 credit per call |

## Things that matter

- Valid country codes: `/facebook/ads/countries`.
- Which advertisers use a keyword, and how many ads each runs: `/facebook/ads/keywords`. One advertiser's ads: `/facebook/ads/search?ad_page_id=…`, the ID coming from `/facebook/ads/keywords` or `/facebook/pages/details`.
- Spend and impressions are ranges, and Meta publishes them for some ads only. When they are missing, say so rather than estimating.
- How long an ad has run (start date to today) is the best public signal that it works.
- **Credits:** the response headers `X-SocialAPIs-Credits-Deducted` and `X-SocialAPIs-Credits-Remaining` say what a call cost. Before a large batch, check `/usage` (free) and tell the user roughly what it will cost.
- **Pagination:** list endpoints return a page plus `end_cursor`; pass it back as `end_cursor` until it is missing or the user has enough.
- **Slow calls:** a call can take up to about 90 seconds. Use a timeout of at least 120 s and don't fire hundreds of calls in parallel (`/usage/limits` shows the plan's rate limit).
- **Errors:** `401` bad or missing key · `403` out of credits or account paused · `429` rate limit, retry with backoff · `502` / `504` the source failed or timed out, retry once later. Failed calls are not charged.

Other SocialAPIs skills: `facebook-pages-api` (Facebook pages, posts and comments), `facebook-marketplace-api` (Facebook Marketplace), `facebook-groups-api` (public Facebook groups), `instagram-api` (Instagram), and `socialapis` for every endpoint at once.
