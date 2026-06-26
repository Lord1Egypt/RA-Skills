---
name: api-bridge
description: Curated free public APIs for AI agents — geocoding, weather, forex, validation, facts, finance, and test data. Use when an agent needs real-world data without paid API keys.
version: 1.0.0
metadata:
  category: data
  tags: [api, http, weather, forex, geocoding, validation, facts, finance]
  credits: 1
---

# API Bridge — Curated Public API Toolkit for AI Agents

AI agents constantly need real-world data. This skill provides a curated, tested collection of the highest-value free public APIs organized by use case. Each entry includes the endpoint pattern, output shape, and curl example.

**Philosophy:** Curation + examples = the product. These are stable, mostly key-free APIs with good uptime.

## Quick Reference

| Category | API | No Key | CORS |
|----------|-----|--------|------|
| Weather | wttr.in | ✅ | ✅ |
| Weather | Open-Meteo | ✅ | ✅ |
| Geocoding | ipapi (IP→location) | ✅ | ❌ |
| Geocoding | Nominatim (geocode) | ✅ | ✅ |
| Forex | open.er-api.org | ✅ | ❌ |
| Crypto | CoinGecko | ✅ | ✅ |
| Validation | urlmeta, icon.horse | ✅ | ✅ |
| Facts | catfact.ninja | ✅ | ✅ |
| Images | dog.ceo, thecatapi | ✅ | ✅ |
| Finance | Polygon.io | ✅ | ✅ |
| Reference | Wikipedia REST | ✅ | ✅ |
| Test data | jsonplaceholder, randomuser | ✅ | ✅ |

---

## Weather

### wttr.in — Minimal Weather (CORS: ✅, No Key)

```bash
curl -s "wttr.in/San+Jose,CA?format=j1"
```

**Use:** Current conditions, 3-day forecast, moon phase, airport weather.

**Output:** JSON with `current_condition`, `weather[]` (daily), `nearest_area`.

```bash
# Specific location
curl -s "wttr.in/San+Jose,CA?format=3"
# Named locations work well; coordinates less so
```

---

### Open-Meteo — Open Source Weather API (CORS: ✅, No Key)

**Base:** `https://api.open-meteo.com/v1/forecast`

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=37.34&longitude=-121.89&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FLos_Angeles"
```

**Use:** Current conditions + hourly forecast, no key needed, global coverage.

**Parameters:**
- `latitude`, `longitude` — required
- `current=` — comma-separated variables: `temperature_2m`, `relative_humidity_2m`, `weather_code`, `wind_speed_10m`, `precipitation`, `cloud_cover`
- `hourly=` — same variables for 48h forecast
- `daily=` — daily forecast: `temperature_2m_max`, `temperature_2m_min`, `precipitation_sum`, `weather_code`
- `temperature_unit=fahrenheit|celsius`
- `timezone=America%2FLos_Angeles` (or auto)

**Weather codes:** 0=clear, 1-3=partly cloudy, 45-48=fog, 51-67=rain/drizzle, 71-77=snow, 80-82=rain showers, 95-99=thunderstorm.

---

## Geocoding

### ipapi.co — IP Geolocation (CORS: ❌, No Key)

**Base:** `https://ipapi.co/json/` or `https://ipapi.co/{IP}/json/`

```bash
# Your sandbox出口IP
curl -s "https://ipapi.co/json/" | jq '.location, .city, .region, .country_name, .latitude, .longitude'
# Specific IP
curl -s "https://ipapi.co/8.8.8.8/json/" | jq '{city, region, country_name}'
```

**Use:** IP → city/region/country/lat-lon. Not CORS-friendly for browser use. Good for server/CLI agents.

**Fields:** `ip`, `city`, `region`, `region_code`, `country_name`, `country_code`, `latitude`, `longitude`, `timezone`, `utc_offset`, `asn`, `org`.

---

### Nominatim — OpenStreetMap Geocoder (CORS: ✅, No Key, Rate Limited)

**Base:** `https://nominatim.openstreetmap.org/search`

```bash
curl -s "https://nominatim.openstreetmap.org/search?q=1600+Amphitheatre+Parkway,+Mountain+View,+CA&format=json&limit=1&addressdetails=1" \
  -H "User-Agent: api-bridge/1.0"
```

**Use:** Address → lat/lon (forward) or lat/lon → address (reverse).

**Reverse:**
```bash
curl -s "https://nominatim.openstreetmap.org/reverse?lat=37.4223&lon=-122.0848&format=json" \
  -H "User-Agent: api-bridge/1.0"
```

**Parameters:**
- `q=` — search query
- `format=json` — always use this
- `limit=1` — first result
- `addressdetails=1` — include parsed address components
- `accept-language=en` — language preference

**Rate limits:** 1 req/sec. Always set `User-Agent`. Free for non-commercial use.

---

## Forex

### open.er-api.org — Free Forex (CORS: ❌, No Key)

**Base:** `https://open.er-api.com/v6/latest/{CURRENCY}`

```bash
curl -s "https://open.er-api.com/v6/latest/USD" | jq '.rates | {JPY, EUR, GBP, CNY, CAD}'
```

**Use:** Current exchange rates. USD as base, all currencies relative to it.

**Output:** `{ "rates": { "JPY": 149.5, "EUR": 0.92, ... }, "time_last_update_utc": "..." }`

---

## Crypto

### CoinGecko — Crypto Prices (CORS: ✅, No Key, Rate Limited)

**Base:** `https://api.coingecko.com/api/v3`

```bash
# Simple price
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"

# Market data
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum&order=market_cap_desc&per_page=5&sparkline=false&price_change_percentage=24h"
```

**Rate limit:** 10-30 calls/min on free tier. Cache responses when possible.

---

## Validation

### icon.horse — Favicon Checker (CORS: ✅, No Key)

**Base:** `https://icon.horse/`

```bash
# Favicon URL for any domain
curl -s "https://icon.horse/feedburner.com"
# Returns: { "url": "https://feedburner.com/favicon.ico", "found": true }
```

**Use:** Find favicon for any domain — useful for link previews and metadata enrichment.

---

### urlmeta — URL Metadata (CORS: ❌, No Key)

**Base:** `https://urlmeta.org/?`

```bash
curl -s "https://urlmeta.org/?url=https://example.com"
```

**Use:** Get Open Graph / Twitter card metadata for any URL without scraping.

---

## Facts

### catfact.ninja — Cat Facts (CORS: ✅, No Key)

```bash
curl -s "https://catfact.ninja/fact"
# {"fact":"Cats have over 20 vocalizations...","length":42}
```

**Use:** Random fact generation for demos, tests, social content. Also: `/breeds`, `/fact` endpoints.

---

### dog.ceo — Random Dog Images (CORS: ✅, No Key)

```bash
curl -s "https://dog.ceo/api/breeds/image/random"
# {"message":"https://.../images/n02102040_1005.jpg","status":"success"}

curl -s "https://dog.ceo/api/breeds/list/all" | jq '.message | keys'
```

**Use:** Random images for demos, placeholders, UI testing.

---

### thecatapi — Random Cat Images (CORS: ✅, No Key)

```bash
curl -s "https://api.thecatapi.com/v1/images/search"
# [{"id":"d5D", "url":"https://...","width":1600,"height":1200}]
```

---

## Finance

### Polygon.io — Market Status & Stock Quotes (CORS: ❌, No Key)

**Base:** `https://api.polygon.io/v1`

```bash
# Market status
curl -s "https://api.polygon.io/v1/marketstatus?apiKey=DEMO_KEY"

# Last trade for a stock  
curl -s "https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey=DEMO_KEY"
```

**Note:** `DEMO_KEY` works for some endpoints. Real keys are free at polygon.io.

**Also useful:**
- `https://api.polygon.io/v2/aggs/ticker/{TICKER}/prev` — previous day close
- `https://api.polygon.io/v2/aggs/ticker/{TICKER}/range?from={DATE}&to={DATE}` — historical range

---

## Reference

### Wikipedia REST API — Article Summaries (CORS: ✅, No Key)

**Base:** `https://en.wikipedia.org/api/rest_v1`

```bash
# Article summary
curl -s "https://en.wikipedia.org/api/rest_v1/page/summary/OpenAI" | jq '{title, extract, thumbnail}'

# Related pages
curl -s "https://en.wikipedia.org/api/rest_v1/page/related/OpenAI" | jq '.pages[:3] | .[].title'
```

**Use:** Factual summaries, links, thumbnails for topics. Good for enriching agent responses with context.

---

## Test Data

### jsonplaceholder — Fake JSON API (CORS: ✅, No Key)

**Base:** `https://jsonplaceholder.typicode.com`

```bash
# Posts
curl -s "https://jsonplaceholder.typicode.com/posts?userId=1" | jq '.[0]'
# Comments
curl -s "https://jsonplaceholder.typicode.com/comments?postId=1" | jq '.[0]'
# Users
curl -s "https://jsonplaceholder.typicode.com/users/1" | jq '{name, email, phone}'
# Todos
curl -s "https://jsonplaceholder.typicode.com/todos?completed=false" | jq '.[0]'
```

**Use:** API prototyping, testing HTTP clients, mock backend during development.

---

### randomuser.me — Fake User Profiles (CORS: ✅, No Key)

```bash
curl -s "https://randomuser.me/api/?results=3" | jq '.results[] | {name: .name, email, phone, location}'
```

**Use:** Generate realistic fake users with names, emails, photos, addresses for demos and tests.

---

## Reliability Notes

### ✅ Reliable (tested, stable)
- `wttr.in` — always up, lightweight
- `api.open-meteo.com` — professional open source project, excellent uptime
- `api.coingecko.com` — large project, stable
- `catfact.ninja` — simple, reliable
- `dog.ceo` / `thecatapi.com` — pet image APIs, very stable
- `jsonplaceholder.typicode.com` — standard test API
- `randomuser.me` — standard test API
- `en.wikipedia.org/api/rest_v1` — Wikipedia infrastructure, very stable

### ⚠️ Use with caution
- `nominatim.openstreetmap.org` — rate limited to 1 req/sec, requires User-Agent
- `open.er-api.org` — simple project, less redundancy
- `icon.horse` — small project, less redundancy
- `polygon.io` — free tier sufficient for light use

### ❌ Avoid / Unreliable
- `worldtimeapi.org` — frequently down (2026-03 check failed)
- `dog-api.kinduff.com` — certificate expired, broken (2026-03 check failed)

---

## Adding to an OpenClaw Skill

Install as a skill in your workspace skills directory:

```bash
# In your OpenClaw workspace:
ls skills/
# Add api-bridge/ subdirectory with this SKILL.md
```

The skill is documentation-first — no code to install. Agents read the SKILL.md and invoke the APIs directly.
