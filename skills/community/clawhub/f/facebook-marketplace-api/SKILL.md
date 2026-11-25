---
name: facebook-marketplace-api
description: Search Facebook Marketplace near any city: listings with price, photos, location and seller, plus one listing or one seller in detail, vehicles (make, model, year, mileage) and rentals (price, bedrooms), through the SocialAPIs REST API. Use for price checks, deal hunting, used-car or rental research, resale monitoring, or code that reads Marketplace.
---

# Facebook Marketplace API (SocialAPIs)

Public Facebook Marketplace listings as JSON, for any city: search, listing details, sellers, vehicles and rentals.

- Website: https://socialapis.io · this API: https://socialapis.io/api-sources/marketplace-search
- Free API key: https://socialapis.io/auth/signup (200 credits a month, no card)
- Every parameter: [references/endpoints.md](references/endpoints.md) · OpenAPI: https://socialapis.io/openapi.json · llms.txt: https://socialapis.io/llms.txt

## Setup

1. The user needs an API key from https://socialapis.io/dashboard.
2. Read it from the environment, `SOCIALAPIS_API_KEY`. **Never** hard-code it, print it, or ask the user to paste it into the chat. If it is missing, tell the user to set it.
3. Send it in the **`x-api-token` header**, never in the URL.

If SocialAPIs MCP tools are available in this session (`facebook_page`, `facebook_ads`, `instagram_profile`, …), use them instead of raw HTTP. Hosted MCP server: `https://mcp.socialapis.io/mcp`.

## Making a call

```bash
curl -s -H "x-api-token: $SOCIALAPIS_API_KEY" \
  "https://api.socialapis.io/facebook/marketplace/city-coordinates?city=Austin"
```

```python
import os, requests

r = requests.get(
    "https://api.socialapis.io/facebook/marketplace/city-coordinates",
    params={"city": "Austin"},
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
| [`/facebook/marketplace/search`](https://socialapis.io/api-sources/marketplace-search) | Search general Facebook Marketplace listings (items for sale) by keyword or category near a location, with price, condition, radius and sort filters. | 1 credit per call |
| [`/facebook/marketplace/listing`](https://socialapis.io/api-sources/marketplace-listing-details) | Get one Marketplace listing in full: title, price, description, condition, all photos, location and seller. | 1 credit per call |
| [`/facebook/marketplace/seller`](https://socialapis.io/api-sources/marketplace-seller-details) | Get a Marketplace seller's profile: name, join date, rating, review count and badges. | 1 credit per call |
| [`/facebook/marketplace/categories`](https://socialapis.io/api-sources/marketplace-categories) | List Marketplace categories with their IDs and category_url values. | 1 credit per call |
| [`/facebook/marketplace/city-coordinates`](https://socialapis.io/api-sources/marketplace-city-coordinates) | Convert a city name to the latitude and longitude that the Marketplace search tools expect in filter_location_latitude / filter_location_longitude. | 1 credit per call |
| [`/facebook/marketplace/vehicles`](https://socialapis.io/api-sources/marketplace-vehicles) | Search Facebook Marketplace vehicle listings (cars, trucks, motorcycles) near a location, with price, radius and seller-type filters. | 1 credit per call |
| [`/facebook/marketplace/rentals`](https://socialapis.io/api-sources/marketplace-rentals) | Search Facebook Marketplace rental listings (apartments, houses, rooms) near a location, with price, bedroom, bathroom and radius filters. | 1 credit per call |

## Things that matter

- Searches take coordinates: get them once with `/facebook/marketplace/city-coordinates?city=<city>`, then pass `latitude` / `longitude` to the search, vehicles or rentals endpoint.
- Category IDs: `/facebook/marketplace/categories`.
- Listings include accessories, placeholder prices ($1, $123) and duplicates: clean them before computing a price, and use the median, not the average.
- **Credits:** the response headers `X-SocialAPIs-Credits-Deducted` and `X-SocialAPIs-Credits-Remaining` say what a call cost. Before a large batch, check `/usage` (free) and tell the user roughly what it will cost.
- **Pagination:** list endpoints return a page plus `end_cursor`; pass it back as `end_cursor` until it is missing or the user has enough.
- **Slow calls:** a call can take up to about 90 seconds. Use a timeout of at least 120 s and don't fire hundreds of calls in parallel (`/usage/limits` shows the plan's rate limit).
- **Errors:** `401` bad or missing key · `403` out of credits or account paused · `429` rate limit, retry with backoff · `502` / `504` the source failed or timed out, retry once later. Failed calls are not charged.

Other SocialAPIs skills: `facebook-pages-api` (Facebook pages, posts and comments), `facebook-ads-library-api` (Meta Ads Library), `facebook-groups-api` (public Facebook groups), `instagram-api` (Instagram), and `socialapis` for every endpoint at once.
