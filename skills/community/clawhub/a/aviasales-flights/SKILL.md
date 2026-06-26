---
name: flights
description: Search for cheap flights and airfare via Travelpayouts/Aviasales API. Supports date-specific search, price calendar, round-trip, cheapest-price monitoring, popular destinations, and IATA code lookup. Use when user asks to find flights, airfare, cheap tickets, plane tickets, or says phrases like "find flights", "fly to", "book a ticket", "авиабилеты", "перелёт", "найди билеты", "дешёвые билеты", "купить билет".
---

# Flights — Airfare Search via Travelpayouts/Aviasales

## Prerequisites

Environment variable `TRAVELPAYOUTS_TOKEN` must be set with a valid Travelpayouts API token.

## Quick Reference

| Task | Command |
|------|---------|
| Search flights on a date | `--from MOW --to LED --date 2026-04-15 [--return 2026-04-20] [--direct] [--limit 10]` |
| Price calendar for a month | `--from MOW --to LED --month 2026-04` |
| Lookup IATA code | `--lookup "Istanbul"` |
| Latest found prices | `--from MOW --to AER --latest [--one-way]` |
| Popular destinations | `--from MOW --directions` |

## Usage

### 1. Resolve IATA codes

If the user provides a city name instead of an IATA code, resolve it first:

```bash
python3 scripts/search_flights.py --lookup "Istanbul"
```

Pick the most relevant result's `code` field.

### 2. Search flights on a specific date

```bash
python3 scripts/search_flights.py --from MOW --to LED --date 2026-04-15 --return 2026-04-20
```

Add `--direct` for non-stop only. Add `--limit N` to cap results (default 10).

### 3. Price calendar (cheapest days in a month)

```bash
python3 scripts/search_flights.py --from MOW --to LED --month 2026-04
```

Returns results sorted by price. Use to recommend the cheapest travel dates.

### 4. Latest found prices (price monitoring)

```bash
python3 scripts/search_flights.py --from MOW --latest
```

Shows recently found prices from the origin to any destination. Add `--to AER` to filter. Add `--one-way` for one-way only.

### 5. Popular destinations from a city

```bash
python3 scripts/search_flights.py --from MOW --directions
```

Returns destinations sorted by price — useful for "where can I fly cheaply from X?" queries.

## Output Format

All commands output JSON to stdout:

```json
{
  "query": {"from": "MOW", "to": "LED", "date": "2026-04-15"},
  "results": [
    {
      "price": 2454,
      "airline": "Pobeda",
      "airline_code": "DP",
      "flight": "DP 209",
      "from_airport": "VKO",
      "to_airport": "LED",
      "departure": "2026-04-07T07:50:00+03:00",
      "duration_min": 90,
      "duration_str": "1h 30min",
      "transfers": 0,
      "transfers_str": "non-stop",
      "link": "https://aviasales.ru/search/..."
    }
  ],
  "cheapest": 2454,
  "count": 5
}
```

## Presenting Results to the User

1. Highlight the **cheapest option** first.
2. For each result show: price, airline, flight number, departure time, duration, stop type.
3. Format the `link` field as a clickable URL for booking.
4. For calendar queries, recommend the cheapest dates.

## API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| GET | `https://api.travelpayouts.com/aviasales/v3/prices_for_dates` | Prices for specific dates |
| GET | `https://api.travelpayouts.com/aviasales/v3/get_latest_prices` | Latest found prices |
| GET | `https://api.travelpayouts.com/aviasales/v3/grouped_prices` | Min prices by month/day |
| GET | `https://api.travelpayouts.com/v1/city-directions` | Popular destinations |
| GET | `https://autocomplete.travelpayouts.com/places2` | IATA code autocomplete |

## Common IATA Codes

| City | Code |
|------|------|
| Moscow (all airports) | MOW |
| Moscow Sheremetyevo | SVO |
| Moscow Domodedovo | DME |
| Moscow Vnukovo | VKO |
| Saint Petersburg | LED |
| Sochi | AER |
| Kazan | KZN |
| Minsk | MSQ |
| Istanbul | IST |
| Dubai | DXB |
| Yerevan | EVN |
| Tbilisi | TBS |
| Bishkek | FRU |
| Tashkent | TAS |

## References

- **Airline codes**: See `references/airlines.md` for a reference mapping of IATA airline codes to names. The script auto-fetches the latest mapping from the Travelpayouts API with a 24-hour cache; this file serves as a fallback.
