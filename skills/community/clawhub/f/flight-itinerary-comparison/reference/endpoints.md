# flight-itinerary-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**4 endpoints across 2 platform group(s).**

## Agoda (3)

### `agoda_flights_itinerary_amenities`

- **HTTP:** `POST /agoda/flights/itinerary-amenities`
- **What:** Get Agoda flight segment amenities. Returns real-content amenities (aircraft type, seat layout, meals, entertainment, wifi) for one or more flight segments. Copy the segments straight from a flight search response's own segment fields.
- **Params:** `body` (object, **required**) — One or more flight segments to fetch amenities for
- **REST body:** Send the value of the MCP argument `body` directly as the JSON body; do not wrap it in a `body` property.

### `agoda_flights_search`

- **HTTP:** `GET /agoda/flights/search`
- **What:** Search Agoda one-way flights. Returns bookable one-way flight itineraries between two IATA airport codes for a departure date, including per-segment flight number, airline, times, layovers, aircraft type, and price. Resolve free-text city/airport names to codes first via the flight destination search endpoint.
- **Params:** `adults` (integer, optional) — Adult passengers (age 12+), defaults to 1; `cabin_class` (string, optional) — Cabin class, defaults to Economy; `children` (integer, optional) — Child passengers (age 2-11), defaults to 0; `departure_date` (string, **required**) — Departure date, YYYY-MM-DD; `destination` (string, **required**) — Destination IATA airport code; `infants` (integer, optional) — Infant passengers (under age 2), defaults to 0; `origin` (string, **required**) — Origin IATA airport code; `page` (integer, optional) — 1-indexed result page, defaults to 1

### `agoda_flights_search_locations`

- **HTTP:** `GET /agoda/flights/search-locations`
- **What:** Search Agoda flight destinations/airports. Resolves a free-text city or airport name into IATA airport codes for flight search, with each city's direct and nearby airports.
- **Params:** `keyword` (string, **required**) — Free-text city or airport name

## Expedia (1)

### `expedia_flights_search`

- **HTTP:** `POST /expedia/flights/search`
- **What:** Search Expedia flights. Searches Expedia flights between two IATA airport codes, `origin` and `destination`, on `departure_date` (`YYYY-MM-DD`). `return_date` is required for the default `round_trip`; `one_way` is the alternative `trip_type`. Optional `adults` (1-9, default 1), `cabin_class` (default `COACH`), `currency` and `locale`. Returns departing-leg offers only, with airline, times, duration, stops, route and price.
- **Params:** `option` (object, **required**) — Flights search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.
