# Facebook Marketplace API endpoint reference (SocialAPIs)

Base URL: `https://api.socialapis.io` · Auth: header `x-api-token: $SOCIALAPIS_API_KEY` · All endpoints are `GET` with query parameters.

Generated from the full reference in the `socialapis` skill. Machine-readable: https://socialapis.io/openapi.json

### `GET /facebook/marketplace/search`

Docs and live example: https://socialapis.io/api-sources/marketplace-search

Search general Facebook Marketplace listings (items for sale) by keyword or category near a location, with price, condition, radius and sort filters. Returns listings with their listing_id, plus an end_cursor. For cars and other vehicles use `/facebook/marketplace/vehicles`; for homes and rooms to rent use `/facebook/marketplace/rentals`. Get coordinates from `/facebook/marketplace/city-coordinates`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | no | Keyword to search listings for, e.g. iphone 15 |
| `category_url` | no | Category URL slug |
| `proxy_country` | no | Optional premium proxy country |
| `commerce_search_sort_by` | no | Sort: BEST_MATCH, CREATION_TIME_DESCEND, PRICE_ASCEND, etc. |
| `commerce_search_and_rp_condition` | no | Condition: new, used_like_new, used_good, used_fair |
| `filter_location_latitude` | no | Latitude of the search center, e.g. 30.2672 (from `/facebook/marketplace/city-coordinates`) |
| `filter_location_longitude` | no | Longitude of the search center, e.g. -97.7431 (from `/facebook/marketplace/city-coordinates`) |
| `filter_price_lower_bound` | no | Minimum price in the local currency, whole number, e.g. 100 |
| `filter_price_upper_bound` | no | Maximum price in the local currency, whole number, e.g. 2000 |
| `filter_radius_km` | no | Search radius around the center in kilometres, e.g. 40 |
| `posted_today` | no | When "true", limit to items posted today |
| `exact_match` | no | When "true", exact match search |
| `end_cursor` | no | Pagination cursor |
| `fields` | no | Comma-separated keys to include (e.g. 'items.id,items.title,page_info.end_cursor'). Invalid keys are ignored. |

### `GET /facebook/marketplace/listing`

Docs and live example: https://socialapis.io/api-sources/marketplace-listing-details

Get one Marketplace listing in full: title, price, description, condition, all photos, location and seller. Needs the listing_id from a Marketplace search result. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `listing_id` | yes | Marketplace listing ID, from a Marketplace search result |

### `GET /facebook/marketplace/seller`

Docs and live example: https://socialapis.io/api-sources/marketplace-seller-details

Get a Marketplace seller's profile: name, join date, rating, review count and badges. Needs the seller_id from `/facebook/marketplace/listing`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `seller_id` | yes | Seller ID, from the seller field of `/facebook/marketplace/listing` |

### `GET /facebook/marketplace/categories`

Docs and live example: https://socialapis.io/api-sources/marketplace-categories

List Marketplace categories with their IDs and category_url values. Use a category_url to filter `/facebook/marketplace/search`. Pricing: 1 credit per call.

No parameters.

### `GET /facebook/marketplace/city-coordinates`

Docs and live example: https://socialapis.io/api-sources/marketplace-city-coordinates

Convert a city name to the latitude and longitude that the Marketplace search tools expect in filter_location_latitude / filter_location_longitude. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `city` | yes | City name, e.g. Austin |
| `country` | no | Country name or code |
| `exactly_one` | no | When "true", return exactly one result |

### `GET /facebook/marketplace/vehicles`

Docs and live example: https://socialapis.io/api-sources/marketplace-vehicles

Search Facebook Marketplace vehicle listings (cars, trucks, motorcycles) near a location, with price, radius and seller-type filters. Returns listings with title, price, mileage, year and listing_id, plus an end_cursor. For non-vehicle items, use `/facebook/marketplace/search`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `sort_by` | no | Sort: CREATION_TIME_DESCEND, PRICE_ASCEND, VEHICLE_MILEAGE_ASCEND, etc. |
| `filter_location_latitude` | no | Latitude of the search center, e.g. 30.2672 (from `/facebook/marketplace/city-coordinates`) |
| `filter_location_longitude` | no | Longitude of the search center, e.g. -97.7431 (from `/facebook/marketplace/city-coordinates`) |
| `filter_price_lower_bound` | no | Minimum price in the local currency, whole number, e.g. 100 |
| `filter_price_upper_bound` | no | Maximum price in the local currency, whole number, e.g. 2000 |
| `filter_radius_km` | no | Search radius around the center in kilometres, e.g. 40 |
| `is_c2c_listing_only` | no | Individual sellers only |
| `exact_match` | no | Exact match search |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/marketplace/rentals`

Docs and live example: https://socialapis.io/api-sources/marketplace-rentals

Search Facebook Marketplace rental listings (apartments, houses, rooms) near a location, with price, bedroom, bathroom and radius filters. Returns rental listings with their listing_id, plus an end_cursor. For items for sale, use `/facebook/marketplace/search`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `sort_by` | no | Sort: CREATION_TIME_DESCEND, PRICE_ASCEND, BEST_MATCH |
| `filter_location_latitude` | no | Latitude of the search center, e.g. 30.2672 (from `/facebook/marketplace/city-coordinates`) |
| `filter_location_longitude` | no | Longitude of the search center, e.g. -97.7431 (from `/facebook/marketplace/city-coordinates`) |
| `filter_price_lower_bound` | no | Minimum price in the local currency, whole number, e.g. 100 |
| `filter_price_upper_bound` | no | Maximum price in the local currency, whole number, e.g. 2000 |
| `filter_radius_km` | no | Search radius around the center in kilometres, e.g. 40 |
| `filter_bedrooms_min` | no | Minimum number of bedrooms, e.g. 2 |
| `filter_bedrooms_max` | no | Maximum number of bedrooms |
| `filter_bathrooms_min` | no | Minimum number of bathrooms, e.g. 1 |
| `filter_bathrooms_max` | no | Maximum number of bathrooms |
| `is_c2c_listing_only` | no | Individual sellers only |
| `end_cursor` | no | Pagination cursor |
