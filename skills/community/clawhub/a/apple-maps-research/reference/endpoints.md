# apple-maps-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**19 endpoints across 1 platform group(s).**

## Apple Maps (19)

### `apple_maps_autocomplete`

- **HTTP:** `GET /apple-maps/autocomplete`
- **What:** Get Apple Maps search suggestions for a partial query. Returns Apple Maps typeahead suggestions for a partial query near a coordinate: query completions, matching businesses (resolved to the same place summary the search endpoint returns, with the place ID the place endpoint takes), and addresses.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag. Defaults to en-US.; `latitude` (number, **required**) — Center latitude the suggestions are biased to; `longitude` (number, **required**) — Center longitude the suggestions are biased to; `query` (string, **required**) — Partial search text to complete; `span` (number, optional) — Viewport size in degrees around the center. Defaults to 0.05; minimum 0.001, maximum 5.

### `apple_maps_categories`

- **HTTP:** `GET /apple-maps/categories`
- **What:** List Apple Maps browse categories for an area. Returns the "Find Nearby" browse categories Apple Maps offers for an area (for example Restaurants, Coffee Shops, Gas Stations, Hotels, Parking, Grocery Stores), each with the key and name the category-search endpoint takes. The set is location-aware.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag. Defaults to en-US.; `latitude` (number, **required**) — Center latitude; `longitude` (number, **required**) — Center longitude; `span` (number, optional) — Viewport size in degrees around the center. Defaults to 0.05; minimum 0.001, maximum 5.

### `apple_maps_category_search`

- **HTTP:** `GET /apple-maps/category-search`
- **What:** Browse one Apple Maps category near a coordinate. Returns places in one browse category near a coordinate without a keyword, in the same shape as the search endpoint (place summaries, region, relocation flag, and the refinement filters block). The category is a name from the categories endpoint for the same area (case-insensitive) or its key; an unknown name returns 400 listing the categories available there. Filters and sort work exactly as on the search endpoint.
- **Params:** `category` (string, **required**) — Category name (e.g. Coffee Shops, Restaurants) or key from /apple-maps/categories for the same area; `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `filters` (string, optional) — Comma-separated filter keys from the filters block of an unfiltered category search for the same category and area. Unknown keys return 400 listing the available keys. Costs a second upstream call.; `lang` (string, optional) — Display language as a BCP 47 tag. Defaults to en-US.; `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Max places returned. Defaults to 25, maximum 100.; `longitude` (number, **required**) — Search center longitude; `sort` (string, optional) — Result order. Costs a second upstream call.; `span` (number, optional) — Search viewport size in degrees around the center. Defaults to 0.05; minimum 0.001, maximum 5.

### `apple_maps_directions`

- **HTTP:** `GET /apple-maps/directions`
- **What:** Get Apple Maps driving, walking, or cycling directions. Returns Apple Maps routes between an origin and a destination, with optional intermediate stops, for driving, walking, or cycling. Each route carries its name, whether it is Apple's main or an alternate route, distance, live/historic/free-flow durations, toll and highway flags, Apple's route description and traffic note, and per-leg turn-by-turn steps (maneuver, road, shield, instruction text, distance, duration); detail=full adds each leg's path as coordinates. Departure time and avoid-tolls/highways/stairs preferences are supported. Transit routing is not available.
- **Params:** `avoid_highways` (boolean, optional) — Driving only: prefer routes without highways; `avoid_stairs` (boolean, optional) — Walking only: prefer routes without stairs; `avoid_tolls` (boolean, optional) — Driving only: prefer routes without tolls; `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `depart_at` (string, optional) — Departure time as RFC 3339 for traffic-aware estimates. Defaults to now.; `destination_latitude` (number, **required**) — Destination latitude; `destination_longitude` (number, **required**) — Destination longitude; `detail` (string, optional) — How much of each route to return. Defaults to steps.; `lang` (string, optional) — Language for road names and instructions as a BCP 47 tag. Defaults to en-US.; `mode` (string, optional) — Travel mode. Defaults to driving.; `origin_latitude` (number, **required**) — Origin latitude; `origin_longitude` (number, **required**) — Origin longitude; `via` (string, optional) — Intermediate stops as lat,lng pairs separated by |, at most 8

### `apple_maps_eta`

- **HTTP:** `GET /apple-maps/eta`
- **What:** Get Apple Maps travel-time estimates between two points. Returns Apple Maps travel-time estimates between an origin and a destination: for each transport type Apple reports (driving always; walking when requested), the live best estimate, the historic and free-flow durations, and the route distance. Cheaper than the directions endpoint when only the time and distance are needed. Apple has no cycling ETA; use the directions endpoint for cycling.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `destination_latitude` (number, **required**) — Destination latitude; `destination_longitude` (number, **required**) — Destination longitude; `mode` (string, optional) — Travel mode. Defaults to driving.; `origin_latitude` (number, **required**) — Origin latitude; `origin_longitude` (number, **required**) — Origin longitude

### `apple_maps_guide`

- **HTTP:** `GET /apple-maps/guides/guide`
- **What:** Get one Apple Guide with its places. Returns one Apple Guide (curated collection) by id: title, description, last-modified time, cover photos, source link, publisher, and every place in the guide with the publisher's blurb for it plus the place's Apple place ID, name, category, coordinates, address, phone, website, rating, price level, hours, and photo.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `guide_id` (string, **required**) — Guide id: from the guides home, a publisher page, a place's guide_ids, or the curated= value in a maps.apple.com/guides URL; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, fr-FR. Defaults to en-US.

### `apple_maps_guides`

- **HTTP:** `GET /apple-maps/guides`
- **What:** Browse the Apple Guides home page worldwide or for one city. Returns the Apple Guides home page for the Worldwide scope or one city: the featured guide, the guide carousels (expert recommendations, latest, and similar rows), the city shortcut list, and the browse-by-publisher list. Each guide carries its id (the value the guide endpoint takes), title, description, last-modified time, place count, cover photo, source link, and publisher; each publisher carries its id, name, subtitle, website, and guide count.
- **Params:** `city_id` (string, optional) — City id from /apple-maps/guides/cities. Omit for the Worldwide guides home.; `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, fr-FR. Defaults to en-US.

### `apple_maps_guides_cities`

- **HTTP:** `GET /apple-maps/guides/cities`
- **What:** List the regions and cities Apple Guides cover. Returns the Apple Guides city picker: every region (North America, Europe, Australia, and any Apple adds) with the cities it publishes guides for, each with its id, country, coordinates, and cover photo. Pass a city id to the guides home, publishers, or publisher endpoints to scope them to that city; omit it for the Worldwide scope.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, fr-FR. Region and city names follow it. Defaults to en-US.

### `apple_maps_guides_lookup`

- **HTTP:** `GET /apple-maps/guides/lookup`
- **What:** Resolve up to 20 Apple Guide ids to guide summaries. Returns guide summaries (id, title, description, last-modified time, place count, cover photo, source link) for up to 20 guide ids in one call, for example the guide_ids a place carries. Ids Apple does not return are listed in not_found. Publisher details are not part of this lookup; use the guide endpoint for a single guide's publisher and places.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `guide_ids` (string, **required**) — Comma-separated Apple guide ids, 1 to 20; `lang` (string, optional) — Display language as a BCP 47 tag. Defaults to en-US.

### `apple_maps_guides_nearby`

- **HTTP:** `GET /apple-maps/guides/nearby`
- **What:** Get the Apple Guides curated for the area around a coordinate. Returns the guides Apple suggests for the area around a coordinate ("Guides We Love" for that location) as guide summaries, plus the Apple Guides city the area belongs to (with the city id the guides home endpoint takes). A coordinate outside any guides city returns an empty list.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag. Defaults to en-US.; `latitude` (number, **required**) — Latitude of the area; `longitude` (number, **required**) — Longitude of the area; `span` (number, optional) — Viewport size in degrees around the center. Defaults to 0.05; minimum 0.001, maximum 5.

### `apple_maps_guides_publisher`

- **HTTP:** `GET /apple-maps/guides/publisher`
- **What:** Get one Apple Guides publisher and its guides. Returns one Apple Guides publisher by id: name, subtitle, website, guide count, the cities the publisher offers as filters, and its guides (each with id, title, description, last-modified time, place count, cover photo, and source link). Pass one of the publisher's own city ids as city_id to return only the guides for that city.
- **Params:** `city_id` (string, optional) — Restrict to one city: an id from this publisher's own cities list; `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, fr-FR. Defaults to en-US.; `publisher_id` (string, **required**) — Publisher id: from the guides home or publishers list, a guide's publisher.id, or the publisher= value in a maps.apple.com/guides URL

### `apple_maps_guides_publishers`

- **HTTP:** `GET /apple-maps/guides/publishers`
- **What:** List Apple Guides publishers worldwide or for one city. Returns the Apple Guides "Browse by Publisher" list for the Worldwide scope or one city, sorted by name: each publisher's id (the value the publisher endpoint takes), name, subtitle, website, and number of guides. With no city_id this is the complete enumeration of every publisher Apple lists, usable as the id lookup table for the publisher endpoint.
- **Params:** `city_id` (string, optional) — City id from /apple-maps/guides/cities. Omit for the Worldwide publisher list.; `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, fr-FR. Defaults to en-US.

### `apple_maps_place`

- **HTTP:** `GET /apple-maps/place`
- **What:** Get one Apple Maps place's full detail. Returns one Apple Maps place by its place ID: name, type, category taxonomy, coordinates, formatted and structured address, phone numbers, website, rating and review count, price level, weekly opening hours, amenities (payment, accessibility, parking, and similar yes/no attributes), photos, review snippets (text, rating, time, and source link, without reviewer identity), the business-claim link, and the IDs of Apple Guides that include the place. Accepts either the external place ID (starts with I, the place-id= value in a maps.apple.com/place URL) or the numeric ID from a search result.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code selecting Apple's regional catalog. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, ja-JP, de-DE. Defaults to en-US.; `place_id` (string, **required**) — Apple place ID: external form (I594FECA0B369D14A) or numeric id from a search result

### `apple_maps_place_photos`

- **HTTP:** `GET /apple-maps/place/photos`
- **What:** List every photo Apple Maps carries for a place. Returns all of a place's photos (the place endpoint caps at 20): the business cover photo first when present, then the hero photo, then every categorized photo with its category (Food & Drink, Interior, Exterior, ...), width and height.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US. Defaults to en-US.; `place_id` (string, **required**) — Apple place ID (external I... form or numeric id)

### `apple_maps_places`

- **HTTP:** `GET /apple-maps/places`
- **What:** Get full detail for up to 20 Apple Maps places in one call. Returns the same full detail as the place endpoint for up to 20 place IDs in a single upstream call, plus the list of requested IDs Apple did not return. Accepts the external I... form and the numeric id interchangeably.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag. Defaults to en-US.; `place_ids` (string, **required**) — Comma-separated Apple place ids, 1 to 20

### `apple_maps_reverse_geocode`

- **HTTP:** `GET /apple-maps/reverse-geocode`
- **What:** Reverse-geocode a coordinate with Apple Maps. Returns Apple Maps' address record for a coordinate: the matched place name and type (an address, street, or area of interest such as a neighborhood), the formatted and structured address, the matched center, the IANA timezone, and the display region.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag. Defaults to en-US.; `latitude` (number, **required**) — Latitude to reverse-geocode; `longitude` (number, **required**) — Longitude to reverse-geocode

### `apple_maps_search`

- **HTTP:** `GET /apple-maps/search`
- **What:** Search Apple Maps places near a coordinate. Returns Apple Maps places matching a keyword, business name, category, or street address near a coordinate. Each place carries its Apple place ID (the value the place endpoint takes), name, category, coordinates, formatted and structured address, phone, website, rating and review count, price level, weekly opening hours, and a hero photo. Apple returns a bounded set per viewport (around 25 places for the default span) with no pagination; widen the span or move the center to cover more area. When nothing matches near the center Apple may relocate the search to a default region, reported by relocated=true and the region bounds. The response's filters block lists the refinement chips Apple offers for this query and area (open now, top rated, in guides, cuisines, price bands, amenities, accolades, sort); pass their keys back as filters and sort to refine the same search.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code selecting Apple's regional catalog. Defaults to US.; `filters` (string, optional) — Comma-separated filter keys from the filters block of an unfiltered search for the same query and area, e.g. OPEN_NOW, TOP_RATED, FEATURED_IN_GUIDES, PRICE_RANGE_MODERATE, modern_pizza_restaurant, ACCEPTS_CREDIT_CARDS. Unknown keys return 400 listing the available keys. Costs a second upstream search.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, ja-JP, de-DE. Defaults to en-US.; `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Max places returned. Defaults to 25, maximum 100.; `longitude` (number, **required**) — Search center longitude; `query` (string, **required**) — Keyword, business name, category, or street address to search for; `sort` (string, optional) — Result order. Costs a second upstream search.; `span` (number, optional) — Search viewport size in degrees of latitude/longitude around the center. Defaults to 0.05 (roughly a 5km box); minimum 0.001, maximum 5.

### `apple_maps_transit_departures`

- **HTTP:** `GET /apple-maps/transit-departures`
- **What:** Get a transit stop's lines and live departures from Apple Maps. Returns a transit stop or station's systems (e.g. BART, Muni Metro), lines (name, shield, color), and the upcoming departures Apple Maps shows, each with the line, headsign, direction, scheduled and live times, and real-time status. Takes the stop's Apple place ID (find stops with the search endpoint, e.g. a station name). A place that is not a transit stop returns 404.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US. Defaults to en-US.; `place_id` (string, **required**) — Apple place ID of a transit stop or station (external I... form or numeric id)

### `apple_maps_venue_browse`

- **HTTP:** `GET /apple-maps/venue/browse`
- **What:** Browse the stores and places inside a venue on Apple Maps. Returns an indoor venue's directory (mall, airport, stadium: categories such as Clothes, Shoes, Food, All Shops with their subcategories and levels) and, when a category is given, the places inside the venue for that category with the same summary shape as search. Find venues with the search endpoint; a place without a directory returns 404, an unknown category returns 400 listing the available ones.
- **Params:** `category` (string, optional) — Directory category or subcategory to browse, by name (case-insensitive) or key from the venue's directory. Omit to list the directory only.; `country` (string, optional) — Two-letter ISO 3166-1 country code. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US. Defaults to en-US.; `limit` (integer, optional) — Max places returned. Defaults to 25, maximum 100.; `place_id` (string, **required**) — Apple place ID of the venue (external I... form or numeric id)
