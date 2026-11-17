# countries.dev — Complete Endpoint Reference

Base URL: `https://countries.dev` — all endpoints are `GET` unless noted.
No authentication. All examples below were verified live against the API.

## Table of contents

1. [Common query parameters](#common-query-parameters)
2. [Country object schema](#country-object-schema)
3. [Country lookup](#country-lookup)
4. [Country filters](#country-filters)
5. [Reference data](#reference-data)
6. [Cities](#cities)
7. [Places (full GeoNames gazetteer)](#places)
8. [Distance](#distance)
9. [Postal codes](#postal-codes)
10. [IP geolocation](#ip-geolocation)
11. [Error handling](#error-handling)

---

## Common query parameters

These work on every country-returning endpoint (lookup, filter, and list):

| Param | Type | Notes |
|---|---|---|
| `fields` | string | Comma-separated field names, e.g. `fields=name,capital,flag`. Special value `fields=full` returns every field including the four normally omitted (`altSpellings`, `maps`, `translations`, `regionalBlocs`). |
| `full` | boolean | `full=true` — same effect as `fields=full`. |
| `sort` | string | Field to sort by, e.g. `sort=population`. List endpoints only. |
| `order` | string | `asc` (default) or `desc`. |
| `limit` | integer | Max results per page. |
| `offset` | integer | Pagination offset. |

## Country object schema

Default fields (verified via `/alpha/US`):

```
name, alpha2Code, alpha3Code, numericCode, cioc,
capital, region, subregion, latlng,
population, populationDensity, area, gini,
demonym, nativeName, independent,
borders            — array of alpha-3 codes, e.g. ["CAN","MEX"]
callingCodes       — array of strings, e.g. ["1"]
topLevelDomain     — array, e.g. [".us"]
timezones          — array, e.g. ["UTC-05:00", ...]
currencies         — [{code, name, symbol}]
languages          — [{name, iso639_1, iso639_2, nativeName}]
flag               — emoji string, e.g. "🇺🇸"
flags              — {png: "https://flagcdn.com/w320/us.png", svg: "https://flagcdn.com/us.svg"}
```

Extra fields only with `fields=full` / `full=true`:

```
altSpellings, maps, translations, regionalBlocs
```

Example record (trimmed):

```json
{
  "name": "Taiwan", "alpha2Code": "TW", "alpha3Code": "TWN",
  "numericCode": "158", "cioc": "TPE",
  "capital": "Taipei", "region": "Asia", "subregion": "Eastern Asia",
  "latlng": [23.5, 121], "population": 23503349, "area": 36193,
  "populationDensity": 649.39, "demonym": "Taiwanese",
  "nativeName": "臺灣", "independent": true,
  "timezones": ["UTC+08:00"], "callingCodes": ["886"],
  "topLevelDomain": [".tw"],
  "currencies": [{"code": "TWD", "name": "New Taiwan dollar", "symbol": "$"}],
  "languages": [{"name": "Chinese", "iso639_1": "zh", "iso639_2": "zho", "nativeName": "中文 (Zhōngwén)"}],
  "flag": "🇹🇼",
  "flags": {"png": "https://flagcdn.com/w320/tw.png", "svg": "https://flagcdn.com/tw.svg"}
}
```

## Country lookup

| Endpoint | Returns | Notes |
|---|---|---|
| `/countries` | array | Every country. Combine with `fields`, `sort`, `limit`, `offset`. |
| `/alpha/{code}` | **object** | ISO alpha-2 or alpha-3, case-insensitive. `/alpha/tw`, `/alpha/TWN` both work. |
| `/name/{name}` | array | **Substring match**, case-insensitive. `/name/united` → 5 countries. Always inspect results; don't assume one match. |
| `/numericcode/{code}` | object | ISO numeric, e.g. `/numericcode/158`. |
| `/cioc/{code}` | object | IOC/Olympic code, e.g. `/cioc/TPE`. |
| `/random` | object | One random country. Supports `fields`. |

Examples:

```bash
curl "https://countries.dev/alpha/JP?fields=name,capital,currencies"
curl "https://countries.dev/name/korea?fields=name,alpha2Code"     # both Koreas
curl "https://countries.dev/countries?fields=name,area&sort=area&order=desc&limit=5"
```

## Country filters

All return an **array** of country objects and accept the common params.

| Endpoint | Argument | Example |
|---|---|---|
| `/region/{region}` | One of `/regions` values | `/region/asia` |
| `/subregion/{subregion}` | One of `/subregions` values | `/subregion/eastern%20asia` |
| `/capital/{capital}` | Capital name (substring) | `/capital/tokyo` |
| `/currency/{code}` | ISO 4217 code | `/currency/twd` |
| `/lang/{code}` | ISO 639-1 or 639-2 | `/lang/zh` |
| `/callingcode/{code}` | Calling code, no `+` | `/callingcode/886` |
| `/timezone/{zone}` | `UTC±HH:MM`, **URL-encode the `+`** | `/timezone/UTC%2B08:00` |
| `/tld/{domain}` | Top-level domain | `/tld/.tw` |
| `/demonym/{demonym}` | Demonym | `/demonym/taiwanese` |
| `/population` | `?min=&max=` (either optional) | `/population?min=50000000&max=70000000` |
| `/area` | `?min=&max=` (km²) | `/area?min=9000000` |
| `/independent/{bool}` | `true` or `false` **in the path** | `/independent/false` (dependent territories) |
| `/borders/{name}` | **Country NAME, not code** | `/borders/germany` → full records of all 9 neighbours |

Gotchas verified by testing:

- `/borders/DE` and `/borders/DEU` → 404 `Country not found`. Only names work
  (`/borders/germany`). For just the codes, read the `borders` field from
  `/alpha/DE` instead.
- `/independent?status=true` (query form) does **not** work — the boolean goes
  in the path: `/independent/true`.
- `/population?gte=...` does **not** filter; the parameters are `min` / `max`.

## Reference data

| Endpoint | Returns |
|---|---|
| `/regions` | `["Africa","Americas","Antarctic","Antarctic Ocean","Asia","Europe","Oceania","Polar"]` |
| `/subregions` | Array of subregion name strings |
| `/currencies` | `[{code, name, symbol}]` for all currencies |
| `/languages` | `[{name, iso639_1, iso639_2, nativeName}]` |
| `/timezones` | `[{timezone: "UTC+08:00", countries: <count>}]` |

## Cities

~34k populated places (population > 15k, plus all capitals), from GeoNames,
**ranked by population descending**. Accent-insensitive matching.

### `GET /cities`

| Param | Type | Notes |
|---|---|---|
| `q` | string | Substring name match. **The param is `q`, not `name` or `search`** — wrong param names are silently ignored and you get the global most-populous cities. |
| `country` | string | ISO alpha-2 filter, e.g. `country=TW`. |
| `limit` | integer | Default 20, max 100. |

```bash
curl "https://countries.dev/cities?q=paris&country=FR&limit=5"
```

City object:

```json
{
  "geonameId": 1668341, "name": "Taipei", "asciiName": "Taipei",
  "countryCode": "TW", "admin1Code": "04",
  "latitude": 25.05306, "longitude": 121.52639,
  "population": 7871900, "timezone": "Asia/Taipei", "featureCode": "PPLC"
}
```

`featureCode` values: `PPLC` = capital, `PPLA` = admin-1 seat, `PPL` = populated place, etc.

### `GET /cities/{geonameId}`

Single city by GeoNames ID → object. `/cities/1668341` → Taipei.

### `GET /cities/near?lat=&lng=`

Reverse geocoding: nearest cities to coordinates, each with an added
`distanceKm` field. Supports `limit`.

```bash
curl "https://countries.dev/cities/near?lat=48.85&lng=2.35&limit=3"
```

## Places

Full GeoNames gazetteer — ~12M features (cities, towns, mountains, rivers,
lakes, regions...), ranked by population.

### `GET /places`

| Param | Type | Notes |
|---|---|---|
| `q` | string | Substring name match. |
| `country` | string | ISO alpha-2. |
| `class` | string | GeoNames feature class: `A`=admin region, `P`=populated place, `H`=water, `T`=terrain/mountain, `L`=area, `S`=spot/building, `R`=road, `V`=vegetation, `U`=undersea. |
| `limit` | integer | Default 20, max 100. |

```bash
curl "https://countries.dev/places?q=kilimanjaro&country=TZ&class=T"
```

Place object = city object plus `featureClass`:

```json
{
  "geonameId": 149232, "name": "Kilimanjaro", "asciiName": "Kilimanjaro",
  "featureClass": "T", "featureCode": "MT", "countryCode": "TZ",
  "admin1Code": "06", "latitude": -3.07583, "longitude": 37.35333,
  "population": 0, "timezone": "Africa/Dar_es_Salaam"
}
```

### `GET /places/{geonameId}` and `GET /places/near?lat=&lng=`

Same behavior as the `/cities` equivalents (`/places/near` adds `distanceKm`).

## Distance

### `GET /distance`

Great-circle (haversine) distance. Two mutually exclusive input forms:

1. Coordinates: `?lat1=&lng1=&lat2=&lng2=`
2. GeoNames IDs: `?from={geonameId}&to={geonameId}` — **numeric IDs only;
   city names and country codes are NOT accepted** (they return an empty
   response). Resolve names via `/cities?q=` first.

```bash
curl "https://countries.dev/distance?lat1=25.03&lng1=121.56&lat2=35.68&lng2=139.69"
# → {"from":{"latitude":25.03,"longitude":121.56},
#    "to":{"latitude":35.68,"longitude":139.69},
#    "distanceKm":2098.7,"distanceMiles":1304}

curl "https://countries.dev/distance?from=2988507&to=2643743"   # Paris → London
# with IDs, "from"/"to" contain the full city objects
```

Recipe — distance between two named cities:

```bash
FROM=$(curl -s "https://countries.dev/cities?q=taipei&limit=1" | jq '.[0].geonameId')
TO=$(curl -s "https://countries.dev/cities?q=tokyo&limit=1" | jq '.[0].geonameId')
curl -s "https://countries.dev/distance?from=$FROM&to=$TO"
```

## Postal codes

~1.8M postal/ZIP codes across ~121 countries (GeoNames). Coordinates are
approximate; some countries have reduced precision.

### `GET /postal/{country}/{code}`

Path params: `country` = ISO alpha-2, `code` = postal/ZIP code.
Returns an **array** (a code can map to several places).

```bash
curl "https://countries.dev/postal/US/90210"
```

```json
[{
  "countryCode": "US", "postalCode": "90210", "placeName": "Beverly Hills",
  "admin1": {"name": "California", "code": "CA"},
  "admin2": {"name": "Los Angeles", "code": "037"},
  "latitude": 34.0901, "longitude": -118.4065, "accuracy": 4
}]
```

### `GET /postal/countries`

Lists supported countries and their coverage.

## IP geolocation

Three forms:

| Form | Use |
|---|---|
| `GET /ip` | Geolocate the **caller's own** IP. |
| `GET /ip/{ip}` | Specific IPv4 or IPv6 address, e.g. `/ip/8.8.8.8`. |
| `POST /ip` | Batch: JSON array body of up to 100 IPs, e.g. `["8.8.8.8","1.1.1.1"]`. |

Supports `?fields=` to trim the embedded country record
(`/ip/8.8.8.8?fields=name,capital`).

```bash
curl "https://countries.dev/ip/8.8.8.8?fields=name,alpha2Code"
curl -X POST https://countries.dev/ip \
  -H "Content-Type: application/json" -d '["8.8.8.8","1.1.1.1"]'
```

Response shape (single): `{"ip": "...", "countryCode": "US", "country": {<country object>}}`.
Batch returns an array of the same shape.

## Error handling

| Status | Meaning | Body |
|---|---|---|
| 200 | OK | JSON |
| 400 | Malformed request | text |
| 404 | Not found | Plain text, e.g. `Country not found` — **not JSON**, so check status before parsing |
| 429 | Too many requests | back off and retry |

Two silent-failure modes to watch for:

- **Unknown query params are ignored, not rejected.** A typo like
  `?name=paris` on `/cities` returns 200 with the default (unfiltered)
  result set. If results look unrelated to your query, re-check param names.
- **Hitting a non-API path returns the website's HTML** (200 with
  `<!DOCTYPE html>...`). If you receive HTML instead of JSON, the path or
  its shape is wrong (e.g. `/borders?country=DE` instead of `/borders/germany`).
