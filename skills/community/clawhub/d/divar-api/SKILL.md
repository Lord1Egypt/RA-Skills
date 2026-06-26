---
name: divar-api
description: >
  Use this skill whenever the user wants to search, query, or extract data from Divar (divar.ir) —
  Iran's largest classifieds platform. Triggers include: searching rental or sale listings, filtering
  by district/price/size/rooms/amenities, paginating through results, fetching post details, getting
  contact info, building any kind of Divar search tool or scraper, or any question about the Divar API
  structure. Also use when the user pastes a divar.ir URL and wants to replicate or automate that search.
  Always use this skill when Divar, divar.ir, or Iranian real-estate search is mentioned.
---

# Divar API Skill

Divar uses a **server-driven widget API** (JSON over HTTPS, protobuf type annotations embedded via `@type`).
All responses are lists of typed `widget_type` objects. Base URL: `https://api.divar.ir`.

## Critical: form_data field types

Every filter field uses a typed wrapper. **Wrong type = HTTP 400.** Use this table exactly:

| Field | Wrapper | Example |
|-------|---------|---------|
| `category` | `str` | `{ "str": { "value": "residential-rent" } }` |
| `sort` | `str` | `{ "str": { "value": "sort_date" } }` |
| `districts` | `repeated_string` | `{ "repeated_string": { "value": ["920", "82"] } }` |
| `rooms` | `repeated_string` | `{ "repeated_string": { "value": ["یک", "دو"] } }` |
| `rent` | `number_range` | `{ "number_range": { "minimum": "20000000", "maximum": "60000000" } }` |
| `credit` | `number_range` | `{ "number_range": { "minimum": "300000000", "maximum": "600000000" } }` |
| `size` | `number_range` | `{ "number_range": { "minimum": "80", "maximum": "120" } }` |
| `balcony` | `boolean` | `{ "boolean": { "value": true } }` |
| `parking` | `boolean` | `{ "boolean": { "value": true } }` |

> `number_range` min/max values are **strings**, not numbers.
> `boolean` value is a **JS boolean** (`true`/`false`), not a string.

## Critical: category slugs

The API slug differs from the divar.ir URL path segment. Never use the URL segment as the slug.

| API slug (`category.str.value`) | URL path | Persian |
|---------------------------------|----------|---------|
| `residential-rent` | `rent-residential` | اجاره مسکونی |
| `apartment-sell` | `apartment-sell` | فروش آپارتمان |
| `apartment-rent` | `rent-apartment` | اجاره آپارتمان |
| `buy-residential` | `buy-residential` | فروش مسکونی |
| `real-estate` | `real-estate` | همه ملک |
| `buy-commercial-property` | `buy-commercial-property` | فروش اداری/تجاری |
| `rent-commercial-property` | `rent-commercial-property` | اجاره اداری/تجاری |
| `rent-temporary` | `rent-temporary` | اجاره کوتاه‌مدت |

When in doubt, intercept a real browser request via DevTools to read the actual `category.str.value`.

## Search endpoint

`POST /v8/postlist/w/search`

**Verified working payload** (residential rental, Tehran, tested 2026-04-01 → returned 24 listings):

```json
{
  "city_ids": ["1"],
  "source_view": "SEARCH",
  "disable_recommendation": false,
  "search_data": {
    "form_data": {
      "data": {
        "category":  { "str":            { "value": "residential-rent" } },
        "districts": { "repeated_string": { "value": ["139","143","145","4162","75","78","82","920","921"] } },
        "rooms":     { "repeated_string": { "value": ["دو","یک"] } },
        "rent":      { "number_range":   { "minimum": "20000000",  "maximum": "60000000"  } },
        "credit":    { "number_range":   { "minimum": "300000000", "maximum": "600000000" } },
        "size":      { "number_range":   { "minimum": "80",        "maximum": "120"       } },
        "balcony":   { "boolean":        { "value": true } },
        "parking":   { "boolean":        { "value": true } }
      }
    },
    "server_payload": {
      "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
      "additional_form_data": {
        "data": { "sort": { "str": { "value": "sort_date" } } }
      }
    }
  }
}
```

**Response:** `{ "list_top_widgets": [...], "list_widgets": [...] }`

Filter to `widget_type === "POST_ROW"` to get listings. Each POST_ROW has:
- `data.title` — listing title (Persian)
- `data.middle_description_text` — price string
- `data.bottom_description_text` — relative time ("دقایقی پیش")
- `data.action.payload.token` — unique post ID (use for detail/contact endpoints)
- `data.action.payload.web_info.district_persian` — district name
- `data.image_count` — number of photos

## Pagination

Cursor-based. On page 1, no `pagination_data`. On page 2+, add:

```json
{
  "pagination_data": {
    "@type": "type.googleapis.com/post_list.PaginationData",
    "last_post_date": "<ISO8601 from previous last post>",
    "page": 2,
    "layer_page": 2,
    "search_uid": "<uuid — keep constant for the session>",
    "cumulative_widgets_count": 24
  }
}
```

`viewed_tokens` is an optional gzip+base64 bloom filter for server-side deduplication — safe to omit.

## Post detail

`GET /v8/posts-v2/web/{token}`

Returns sections (`BREADCRUMB`, `HEADER`, `IMAGES`, `DETAILS`) each containing widget arrays.
Common detail widget types: `KEY_VALUE` (room count, floor, etc.), `DESCRIPTION`, `IMAGE_GALLERY`, `MAP`.

## Contact info (requires auth)

`POST /v8/postcontact/web/contact_info_v2/{token}`

Body: `{}`. Returns `widget_list` with `UNEXPANDABLE_ROW` containing phone number.
Returns `RBAC: access denied` without authentication.

## Authentication

- **Cookie-based**: `token` cookie + `did` (device ID) cookie, set by divar.ir on login.
- **Header**: `Authorization: Basic <jwt>` — same JWT value as the `token` cookie.
- The search endpoint works with session cookies alone when called same-origin from `divar.ir`.
- Cross-origin calls (e.g. from a script) need the `Authorization` header explicitly.

## Parsing a divar.ir search URL → API payload

When a user pastes a URL like:
`https://divar.ir/s/tehran/rent-residential/almahdi?balcony=true&credit=300000000-600000000&districts=920%2C82&rent=20000000-60000000&rooms=%D8%AF%D9%88%2C%DB%8C%DA%A9&size=80-120`

Map query params to `form_data` fields:

| URL param | form_data field | Wrapper |
|-----------|----------------|---------|
| URL path segment (e.g. `rent-residential`) | `category` → look up API slug | `str` |
| `districts=920,82,...` | `districts` | `repeated_string` (split on `,`) |
| `rooms=دو,یک` | `rooms` | `repeated_string` (split on `,`) |
| `rent=min-max` | `rent` | `number_range` (split on `-`) |
| `credit=min-max` | `credit` | `number_range` (split on `-`) |
| `size=min-max` | `size` | `number_range` (split on `-`) |
| `balcony=true` | `balcony` | `boolean` |
| `parking=true` | `parking` | `boolean` |
| `map_bbox=...` | not in form_data — belongs in `/v8/mapview/viewport` `camera_info.bbox` | — |
| `map_place_hash=...` | not in form_data | — |

For full API reference (all endpoints, widget system, map/geo, autocomplete, filters):
→ read `references/api-reference.md`
