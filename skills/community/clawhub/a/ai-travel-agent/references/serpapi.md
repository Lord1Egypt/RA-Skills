# SerpAPI Reference

## Auth
API key stored in user's credentials file (see SKILL.md for location convention).
All requests: `GET https://serpapi.com/search` with `api_key` param.

## Flights — `engine=google_flights`

### Key Parameters
| Param | Description |
|---|---|
| `departure_id` | Airport IATA code (e.g. `LGW`, `LHR`) |
| `arrival_id` | Airport IATA code (e.g. `BCN`, `JFK`) |
| `outbound_date` | `YYYY-MM-DD` |
| `return_date` | `YYYY-MM-DD` (omit for one-way) |
| `type` | `1`=round-trip (default), `2`=one-way, `3`=multi-city |
| `travel_class` | `1`=Economy, `2`=Premium Economy, `3`=Business, `4`=First |
| `adults` | Number of adult passengers |
| `children` | Number of children |
| `currency` | ISO currency code (e.g. `GBP`) |
| `hl` | Language (`en`) |
| `deep_search` | `true` for exact Google Flights parity (slower) |

### Response Fields (per flight)
- `price` — total price (all passengers)
- `stops` — number of stops (0 = direct)
- `total_duration` — total journey time in minutes
- `flights[]` — array of legs:
  - `airline`, `flight_number`
  - `departure_airport.id/name/time`
  - `arrival_airport.id/name/time`
  - `duration` — leg duration in minutes
  - `travel_class` — e.g. "Economy"
  - `airplane` — aircraft type
  - `legroom` — e.g. "29 in"
  - `overnight` — bool
  - `often_delayed_by_over_30_min` — bool
- `booking_token` — use with `google_flights_booking` engine for booking link

### Getting a Booking Link
```
GET https://serpapi.com/search?engine=google_flights_booking&booking_token=TOKEN&api_key=KEY
```
Returns `booking_options[]` with direct airline/OTA URLs.

---

## Hotels — `engine=google_hotels`

### Key Parameters
| Param | Description |
|---|---|
| `q` | Location query (e.g. `"Barcelona beachfront hotels"`) |
| `check_in_date` | `YYYY-MM-DD` |
| `check_out_date` | `YYYY-MM-DD` |
| `adults` | Number of adults |
| `children` | Number of children |
| `min_star_rating` | `1`–`5` |
| `sort_by` | `3`=Lowest price, `8`=Highest rating, `13`=Most reviewed |
| `currency` | ISO currency code |
| `gl` | Country for results (e.g. `uk`) |
| `amenities` | Comma-separated filter (see below) |

### Amenity Filter Values
Common values: `pool`, `free_breakfast`, `beach_access`, `free_parking`, `pet_friendly`, `spa`, `restaurant`, `gym`, `air_conditioning`, `wifi`

### Response Fields (per property)
- `name`, `type` (e.g. "Hotel", "Vacation rental")
- `hotel_class` — star rating (1–5)
- `overall_rating` — guest score (e.g. 4.6)
- `reviews` — review count
- `rate_per_night.lowest` — price string (e.g. "£275")
- `rate_per_night.before_taxes_fees` — pre-tax price
- `amenities[]` — list of amenity strings
- `nearby_places[]` — nearby landmarks with transport times
- `description` — short description
- `link` — direct Google Hotels booking link
- `images[]` — thumbnail URLs

---

## Destination Inspiration — `engine=google_travel_explore`
Use when user doesn't know where to go. Returns destinations with price estimates.

### Key Parameters
| Param | Description |
|---|---|
| `departure_id` | Departure airport IATA code |
| `currency` | ISO currency code |
| `hl` | Language (`en`) |

### Response
Returns `destinations[]` with `name`, `image`, `flight_price`, `date_range` suggestions.

---

---

## Transport / Directions — `engine=google_maps_directions`
Use via `scripts/search_transport.py`. Returns trains, buses, ferries between two cities with operator names, durations, prices, and **direct booking links**.

### Key Parameters
| Param | Description |
|---|---|
| `start_addr` | Origin city/place (e.g. `"Rome, Italy"`) |
| `end_addr` | Destination city/place (e.g. `"Florence, Italy"`) |
| `travel_mode` | `3` = Transit (always use this for public transport) |
| `hl` | Language (`en`) |

### Response Fields (per route)
- `formatted_duration` — e.g. "1 hr 26 min"
- `formatted_distance` — e.g. "275 km"
- `cost` + `currency` — price estimate when available
- `trips[0].service_run_by.name` — operator (e.g. "Trenitalia", "FlixBus")
- `trips[0].service_run_by.link` — **direct booking URL**
- `trips[0].start_stop.name` / `.time` — departure stop + time
- `trips[0].end_stop.name` / `.time` — arrival stop + time
- `trips[0].icon` — use to infer transport type (bus/train/ferry)

### Notes
- Results include trains, buses, and sometimes ferries depending on the route
- Booking links go directly to the operator (Trenitalia, FlixBus, Italo, etc.)
- Prices are estimates — final price on operator site may vary
- Times shown are for a specific departure — actual timetable varies by date
- Each call = 1 SerpAPI search

---

## Usage Limits (Free Tier)
- 100 searches/month across all engines
- Each `search_flights.py` call = 1 search
- Each `search_hotels.py` call = 1 search
- Booking token lookup = 1 search
- Monitor usage at: https://serpapi.com/manage-api-key
