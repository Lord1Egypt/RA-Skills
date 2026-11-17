# dining-demand-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 2 platform group(s).**

## OpenTable (4)

### `opentable_restaurant`

- **HTTP:** `GET /opentable/restaurant`
- **What:** Get an OpenTable restaurant's profile and live availability. Returns a restaurant's profile (location, cuisines, hours, price band, review summary) plus real-time bookable timeslots for the given date/time and party size.
- **Params:** `date_time` (string, optional) — Reservation date/time, RFC3339-minute local format; defaults to now; `party_size` (integer, optional) — Party size, default 2; `restaurant_id` (string, **required**) — OpenTable restaurant id

### `opentable_restaurant_menus`

- **HTTP:** `GET /opentable/restaurant/menus`
- **What:** Get an OpenTable restaurant's menus. Returns the menus of one OpenTable restaurant, identified by the required `restaurant_id`. Each menu has a title, a currency and sections, and each section lists items with title, price and description. The price is returned as a string in the menu's currency, for example HK$.
- **Params:** `restaurant_id` (string, **required**) — OpenTable restaurant id

### `opentable_restaurant_reviews`

- **HTTP:** `GET /opentable/restaurant/reviews`
- **What:** Get a page of an OpenTable restaurant's diner reviews. Returns one page of diner reviews for an OpenTable restaurant, identified by the required `restaurant_id`. `page` defaults to 1 and `size` to 20. Each review has its id, author and author's metro area, reservation and posted dates, text, a recommended flag, and ratings for overall, food, service, ambience, value and noise.
- **Params:** `page` (integer, optional) — Page number, default 1; `restaurant_id` (string, **required**) — OpenTable restaurant id; `size` (integer, optional) — Reviews per page, default 20

### `opentable_search`

- **HTTP:** `GET /opentable/search`
- **What:** Search OpenTable restaurants near a location. Searches restaurants by free-text term (cuisine, name, neighborhood) near a latitude/longitude, for a given date/time and party size, including inline live availability per result.
- **Params:** `date_time` (string, optional) — Reservation date/time, RFC3339-minute local format; defaults to now; `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `party_size` (integer, optional) — Party size, default 2; `size` (integer, optional) — Max results, default 10; `term` (string, **required**) — Free-text search term

## Resy (7)

### `resy_availability`

- **HTTP:** `GET /resy/availability`
- **What:** Get a Resy restaurant's bookable reservation timeslots. Returns the bookable reservation timeslots Resy currently shows for a restaurant, date, and party size -- the same read-only availability an anonymous visitor sees before signing in. The date is optional and defaults to the current date in UTC; the response echoes the date used. This is discovery only; it does not create, hold, modify, or cancel a reservation.
- **Params:** `date` (string, optional) — Reservation date, YYYY-MM-DD. Defaults to the current date in UTC; `party_size` (integer, optional) — Party size, default 2; `restaurant_id` (string, **required**) — Resy restaurant id

### `resy_cuisines`

- **HTTP:** `GET /resy/cuisines`
- **What:** Get the cuisines present in a Resy location. Returns the cuisines present among restaurants in a Resy location. Location is a short city code or numeric location id -- both already returned inline as location_code on resy-search and resy-restaurant results; there is no separate closed list of every valid location on Resy's own API, so this value always comes from a prior search/restaurant response rather than a guessed input.
- **Params:** `location` (string, **required**) — Resy location code or numeric id (from a prior resy-search/resy-restaurant response's location_code field)

### `resy_event_detail`

- **HTTP:** `GET /resy/event`
- **What:** Get a Resy ticketed dining event's full description and ticket packages. Returns a ticketed dining event's full description, event-day instructions, and per-ticket-tier package breakdown (price, what's included, live ticket availability). All three identifiers come from a prior resy-events result: event_url_slug is that result's url_slug, restaurant_url_slug is its restaurant_url_slug, and location is the same city identifier resy-events was called with. Read-only discovery -- does not purchase a ticket.
- **Params:** `event_url_slug` (string, **required**) — Event url_slug, from a prior resy-events result; `location` (string, **required**) — Resy location code or numeric id, same value resy-events was called with; `party_size` (integer, optional) — Party size, default 2; `restaurant_url_slug` (string, **required**) — Restaurant url_slug, from that same resy-events result's restaurant_url_slug

### `resy_events`

- **HTTP:** `GET /resy/events`
- **What:** Get ticketed dining events in a Resy location. Returns ticketed dining events (fixed-price, fixed-capacity experiences a restaurant hosts and sells tickets for, distinct from a regular reservation) in a Resy location. Read-only discovery -- does not create, hold, or purchase a ticket.
- **Params:** `date` (string, optional) — Only return events starting on or after this date, YYYY-MM-DD; defaults to the next calendar day; `limit` (integer, optional) — Max events returned, default 10; `location` (string, **required**) — Resy location code or numeric id (from a prior resy-search/resy-restaurant response's location_code field); `offset` (integer, optional) — Page past the first `limit` events, default 0

### `resy_locations`

- **HTTP:** `GET /resy/locations`
- **What:** List Resy's operating locations (cities). Returns Resy's full list of operating locations (cities), optionally filtered by a free-text substring and/or country. This is the discovery source for the location value used throughout the rest of this family (resy-search's/resy-restaurant's location_code, resy-cuisines'/resy-events'/resy-event-detail's location).
- **Params:** `country` (string, optional) — Case-insensitive exact match against a location's country name; `q` (string, optional) — Case-insensitive substring match against a location's name, code, or url_slug

### `resy_restaurant`

- **HTTP:** `GET /resy/restaurant`
- **What:** Get a Resy restaurant's profile. Returns a Resy restaurant's profile by the required `restaurant_id`: name, cuisine, `price_range` (1 to 4), rating, review count, address, neighborhood, coordinates, phone, website, menu URL, party size limits, description, `why_we_like_it`, `need_to_know` and images. `location_code` is a short city identifier.
- **Params:** `restaurant_id` (string, **required**) — Resy restaurant id

### `resy_search`

- **HTTP:** `GET /resy/search`
- **What:** Search Resy restaurants near a location. Searches restaurants by free-text term (name, cuisine, or neighborhood) near a latitude/longitude, optionally including live bookable-timeslot availability for a given date and party size.
- **Params:** `date` (string, optional) — Reservation date, YYYY-MM-DD; when set, results include live timeslots; `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `party_size` (integer, optional) — Party size, default 2; `size` (integer, optional) — Max results, default 10; `term` (string, optional) — Free-text search term (name, cuisine, or neighborhood)
