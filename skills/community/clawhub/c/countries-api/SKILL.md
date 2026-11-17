---
name: countries-api
description: >
  Query the free countries.dev REST API (no API key needed) for country data
  (names, capitals, populations, currencies, languages, flags, borders,
  timezones), city/place search and reverse geocoding, postal/ZIP code lookup,
  IP geolocation, and distance between locations. Use this skill whenever the
  user asks about countries, capitals, country codes (ISO alpha-2/alpha-3),
  currencies by country, national flags, neighbouring countries, city
  coordinates, "which country is this IP in", ZIP/postal code lookups, or
  distances between cities — even if they don't mention countries.dev or an
  API by name.
---

# countries.dev API

A free, no-auth REST API for country, city, postal-code, and IP-geolocation
data. Base URL: `https://countries.dev`

- **No API key, no signup, no documented rate limits.** Just send GET requests.
- All responses are JSON (errors like "Country not found" come back as plain
  text with a 404 status — always check the HTTP status code).
- CORS is enabled, so it works from browsers as well as `curl`/server code.
- Data sources: country data plus GeoNames (~34k cities, ~12M places, ~1.8M
  postal codes across ~121 countries).

## Quick start

```bash
# One country by ISO code (alpha-2 or alpha-3, case-insensitive)
curl https://countries.dev/alpha/JP

# Search by name (substring match, returns an array)
curl "https://countries.dev/name/japan?fields=name,capital,population"

# All countries, top 10 by population
curl "https://countries.dev/countries?fields=name,population&sort=population&order=desc&limit=10"

# Find a city and its coordinates
curl "https://countries.dev/cities?q=taipei&limit=5"

# Geolocate an IP
curl https://countries.dev/ip/8.8.8.8
```

## Choosing the right endpoint

| You need... | Use |
|---|---|
| One country, and you have its ISO code | `/alpha/{code}` (most reliable — prefer this) |
| One country by name | `/name/{name}` (substring match — may return several; pick the best match) |
| Lists filtered by region/currency/language/etc. | `/region/…`, `/currency/…`, `/lang/…`, etc. |
| Countries in a population or area range | `/population?min=&max=`, `/area?min=&max=` |
| A country's neighbours (full records) | `/borders/{country name}` — **takes a name like `germany`, NOT an ISO code** |
| City search / coordinates | `/cities?q=…` (ranked by population) |
| Any geographic feature (mountains, rivers…) | `/places?q=…&class=…` |
| Nearest city/place to coordinates | `/cities/near?lat=&lng=`, `/places/near?lat=&lng=` |
| ZIP/postal code → place + coordinates | `/postal/{alpha2}/{code}` |
| IP → country | `/ip` (caller), `/ip/{ip}`, or `POST /ip` for batches |
| Distance between two points | `/distance?lat1=&lng1=&lat2=&lng2=` or `?from=&to=` (GeoNames IDs, not names) |

For the complete endpoint list, every query parameter, response schemas, and
verified examples, read [references/endpoints.md](references/endpoints.md).

## Key conventions (learned from live testing — trust these)

1. **Single-lookup endpoints return an object; search/filter endpoints return
   an array** — even when only one item matches. `/alpha/JP` → object;
   `/name/japan` → `[ {...} ]`.
2. **Use `fields=` aggressively.** Full country records are large. Request
   only what you need: `?fields=name,capital,population`. Use `?fields=full`
   to get everything including `altSpellings`, `maps`, `translations`, and
   `regionalBlocs` (these four are omitted by default).
3. **List endpoints support** `sort`, `order` (`asc`/`desc`), `limit`,
   `offset` for sorting and pagination.
4. **Name search is substring-based**: `/name/united` returns every country
   containing "united". Don't assume the first result is the intended one —
   match on the `name` field or fall back to `/alpha/{code}` when you know
   the code.
5. **`/borders` takes a country *name*** (`/borders/germany` works;
   `/borders/DE` and `/borders/DEU` return 404 "Country not found"). To get
   just neighbour codes, read the `borders` array (alpha-3 codes) from the
   country record instead.
6. **`/distance` does not accept city names or country codes** — only
   `lat1/lng1/lat2/lng2` coordinates or GeoNames IDs via `from`/`to`. To get
   the distance between two named cities, first resolve each via
   `/cities?q=name` to get its `geonameId`, then call `/distance?from=ID&to=ID`.
7. **URL-encode special characters**: timezone lookups need the `+` encoded,
   e.g. `/timezone/UTC%2B08:00`.
8. **Flags**: the `flag` field is an emoji (🇹🇼); image URLs live in
   `flags.png` / `flags.svg` (hosted on flagcdn.com).
