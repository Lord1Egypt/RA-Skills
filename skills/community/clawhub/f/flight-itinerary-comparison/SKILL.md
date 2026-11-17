---
name: flight-itinerary-comparison
description: Compare public Agoda and Expedia flight offers through Crawlora with matched airports, dates, passengers, cabin, price basis, segment timing, and connection evidence. Use for a flight shortlist or itinerary tradeoff brief while preserving one-way and departing-leg coverage limits.
---

# Flight itinerary comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound requests by the requested scope and credit budget. Preserve
source IDs, URLs, source dates, and retrieval/crawl times separately.

Build a comparable shortlist of observed flight offers. Establish airport versus
city scope, travel dates, passenger ages/counts, cabin, currency, timing needs,
connection preferences, and baggage requirements before querying providers.

## Resolve routes and equivalent search criteria

- Resolve free-text airports/cities with Agoda flight location search. Use
  `airports[].code`; a `city_code` can be blank, and nearby airports are alternate
  routes rather than exact replacements. Do not infer airport codes from names.
- Agoda supports one-way search only, with adult/child/infant counts and its own
  cabin names (`Economy`, `PremiumEconomy`, `Business`, `First`). Expedia's body
  supports adult count and cabin names (`COACH`, `PREMIUM_ECONOMY`, `BUSINESS`,
  `FIRST`); it exposes no equivalent child/infant fields. State an unsupported
  passenger mix rather than quietly comparing it with an adult-only query.
- Expedia defaults to `round_trip`, which requires a return date after departure.
  Set `trip_type=one_way` for an equivalent Agoda comparison. Send the MCP
  `option` value as the flat REST body, not an `option` wrapper.
- Expedia returns departing-leg offers even for a round-trip request; return-leg
  selection is unimplemented. Preserve displayed `price_note` and request basis.
  Do not call a departing offer a completed round-trip itinerary or compare a
  roundtrip-per-traveler price with a one-way price as if they buy the same trip.

```sh
scripts/crawlora.sh /agoda/flights/search-locations keyword="Bangkok"
scripts/crawlora.sh /agoda/flights/search origin=BKK destination=HKT departure_date=2026-10-20 adults=1 cabin_class=Economy page=1
scripts/crawlora.sh -X POST /expedia/flights/search '{"origin":"BKK","destination":"HKT","departure_date":"2026-10-20","trip_type":"one_way","adults":1,"cabin_class":"COACH","currency":"USD","locale":"en_US"}'
```

## Match itineraries and compare conditions

Use returned airports, local dates/times, carrier/flight numbers, segment order,
stop count, and whole-journey duration to match offers. Keep marketing/operating
carrier and nonstop/direct/connecting distinctions explicit where supplied.
For codeshares, verify segment identity rather than double-counting flight numbers.
Overnight/date-line trips cannot be compared by subtracting local clock times
without timezone evidence; use supplied durations and mark missing offsets.

Follow Agoda page/`last_page` bounds rather than assuming the first page is every
flight. Selected amenity calls use each returned segment's airport codes, local
`departure_date_time`, `flight_number`, airline `carrier_code`, and `cabin_code`
(as the body's `cabin_class`), plus fare basis when available. Send that flat
`segments` object; missing amenities are unavailable content, not proof a service
is absent. Amenities are source reports, not guarantees for the aircraft operated.

Preserve currency, per-passenger versus group basis, cabin/fare basis, source URL,
observation time, taxes/fees, baggage, refund/change conditions, and unknowns.
Do not infer included baggage or flexibility from cabin or an opaque fare code,
compute a final checkout total from incomplete prices, or invent a conversion
rate. A search snapshot does not guarantee seats, price, connection feasibility,
transfer/visa eligibility, or a protected through-ticket. Return an itinerary
comparison with price-basis and missing-condition columns and tradeoffs under
the user's criteria. Do not book, pay, sign in, or contact an airline unless requested.
