---
name: geocode
description: Reverse geocode latitude/longitude to a human-readable region using geocode.com.cn. Triggers on reverse geocode, lat/lng, latitude/longitude, coordinates to address, 经纬度转地址, 坐标查地点.
metadata: { "openclaw": { "emoji": "🧭", "requires": { "bins": ["curl"] } } }
---

# geocode

Resolve coordinates back to a place name.

Provider: `https://geocode.com.cn` via `curl`.

Current root response behavior:

- `GET https://geocode.com.cn/` without params returns `400 Bad Request`
- returns field labels for Chinese and English display
- demo: `https://geocode.com.cn/?lat=39.9042&lon=116.4074`

## Quick Start

```bash
{baseDir}/scripts/geocode.sh hint
{baseDir}/scripts/geocode.sh reverse 32.9042 110.805 --lang zh-CN
{baseDir}/scripts/geocode.sh reverse 37.819929 -122.478255 --lang en
```

## When to Use

- "Reverse geocode 32.9042, 110.805"
- "Coordinates to address"
- "根据经纬度查地点"
- "把经纬度转成地址"

## When NOT to Use

- Address/place name to coordinates (forward geocoding): use another provider
- Rich place details, reviews, opening hours, or POI metadata: use `goplaces`
- Routing, distance matrices, or navigation
- High-volume batch geocoding

## Query Rules

- Pass decimal latitude and longitude.
- The endpoint supports reverse geocoding only via `GET /?lat=<latitude>&lon=<longitude>`.
- A bare root request returns a field-label hint payload describing the reverse-geocode result columns.
- `accept-language` may still be passed, but the documented contract on the site only guarantees `lat` and `lon`.

## Config

- `GEOCODE_BASE_URL` optionally points at another endpoint for testing or self-hosting.
- `GEOCODE_USER_AGENT` overrides the default identifying `User-Agent`.

## Public API Limits

- Use public endpoints only for low-frequency, interactive lookups.
- Send an identifying `User-Agent`; do not use default curl UA for repeated calls.
- Do not loop, bulk geocode, or aggressively retry against the public endpoint.

## Commands

### Scripted Reverse Geocode

```bash
{baseDir}/scripts/geocode.sh reverse 32.9042 110.805 --lang zh-CN
```

```bash
{baseDir}/scripts/geocode.sh reverse 37.819929 -122.478255 --lang en
```

### Raw Reverse Geocode

```bash
curl --get 'https://geocode.com.cn/' \
  -A 'openclaw-geocode-skill/1.0 (interactive use)' \
  --data 'lat=32.9042' \
  --data 'lon=110.805'
```

### Scripted Root Hint

```bash
{baseDir}/scripts/geocode.sh hint
```

### Raw Root Hint Response

```bash
curl -iL 'https://geocode.com.cn/'
```

Current response body:

```json
{
  "demo": "https://geocode.com.cn/?lat=25.7433&lon=123.4733",
  "zh": ["国家/地区", "省", "市", "县", "乡镇/街道"],
  "en": ["Country", "admin1", "admin2", "", "name"]
}
```

## Response Shape

Successful responses return a compact JSON array, not an object. The root hint now documents five display fields instead of the old six-field output description.

Fixed order mapping:

- index `0`: `Country` / `国家/地区`
- index `1`: `admin1` / `省`
- index `2`: `admin2` / `市`
- index `3`: county-level field when present / `县`
- index `4`: `name` / `乡镇/街道`

Example:

```json
["CN", "Taiwan Province", "Yilan County", "Toucheng Township", ""]
```

## What to Return

- The original coordinates
- Best available locality/region text assembled from `name`, county, `admin2`, and `admin1`
- Country or region value when present
- A note that some positions may be empty, especially the county or `name` slot over water or remote areas
- A short note if any fields are empty

## Notes

- The bundled script prints raw JSON to stdout and keeps dependencies to `curl` only.
- `search` is intentionally unsupported because geocode.com.cn explicitly says it only supports `GET /?lat=<latitude>&lon=<longitude>`.
- If the user needs address-to-coordinate lookup, switch to a forward-geocoding provider instead of this endpoint.
