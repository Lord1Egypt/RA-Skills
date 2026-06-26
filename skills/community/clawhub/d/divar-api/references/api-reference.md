# Divar.ir API Skills

> Extracted via browser developer tools on **divar.ir** (Tehran real-estate section).  
> Base URL: `https://api.divar.ir`  
> All endpoints use **JSON** bodies and return **JSON** responses.  
> Authentication is handled via **cookies** (session-based); unauthenticated calls return `RBAC: access denied`.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Endpoint Reference](#endpoint-reference)
   - [Search & Listings](#search--listings)
   - [Post Detail](#post-detail)
   - [Contact Info](#contact-info)
   - [Map / Geo-clustering](#map--geo-clustering)
   - [Autocomplete / Prediction](#autocomplete--prediction)
   - [Filters](#filters)
   - [User & Notifications](#user--notifications)
   - [Analytics & Telemetry](#analytics--telemetry)
3. [Widget System](#widget-system)
4. [Pagination Pattern](#pagination-pattern)
5. [Category Slugs](#category-slugs)
6. [Infrastructure Notes](#infrastructure-notes)

---

## Architecture Overview

Divar uses a **widget-based API** (similar to server-driven UI). Nearly every response is a list of typed `widget_type` objects that the client renders. Field values use [Protocol Buffers](https://protobuf.dev/) type annotations via the `@type` field.

| Concern | Domain |
|---------|--------|
| Core API | `api.divar.ir` |
| Chat API | `api.divar.ir/chat/...` |
| Map tiles | `map.divarcdn.com`, `tiles.raah.ir` |
| Map style | `map.divar.ir` |
| CDN / Assets | `s100.divarcdn.com`, `postimage01.divarcdn.com` |
| Error tracking | `sentry.divar.cloud` |
| Action logging | `actionlog.divar.ir` |

---

## Endpoint Reference

### Search & Listings

#### `POST /v8/postlist/w/search`
Returns a paginated list of post widgets matching the given search criteria.

**Initial request body** (no pagination token):
```json
{
  "city_ids": ["1"],
  "source_view": "SEARCH",
  "disable_recommendation": false,
  "map_state": {
    "camera_info": {
      "bbox": {},
      "zoom": 9.04
    },
    "page_state": "HALF_STATE"
  },
  "search_data": {
    "form_data": {
      "data": {
        "category": { "str": { "value": "residential-rent" } }
      }
    },
    "server_payload": {
      "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
      "additional_form_data": {
        "data": {
          "sort": { "str": { "value": "sort_date" } }
        }
      }
    },
    "query": "آپارتمان"
  }
}
```

**Paginated request body** (page 2+):
```json
{
  "city_ids": ["1"],
  "pagination_data": {
    "@type": "type.googleapis.com/post_list.PaginationData",
    "last_post_date": "2026-04-01T09:33:50.416192Z",
    "page": 2,
    "layer_page": 2,
    "search_uid": "<uuid>",
    "cumulative_widgets_count": 50,
    "viewed_tokens": "<gzip+base64 encoded token list>"
  },
  "search_data": {
    "form_data": {
      "data": {
        "category": { "str": { "value": "residential-rent" } }
      }
    }
  }
}
```

**Response** (initial):
```json
{
  "list_top_widgets": [ ... ],
  "list_widgets": [ ... ]
}
```
- `list_top_widgets`: headline, search-alert toggle, category suggestion rows
- `list_widgets`: `POST_ROW` widgets (one per listing)

**Response** (paginated):
```json
{
  "list_widgets": [ ... ]
}
```

**POST_ROW widget structure**:
```json
{
  "widget_type": "POST_ROW",
  "data": {
    "@type": "type.googleapis.com/widgets.PostRowData",
    "title": "70 متر / 2 خواب / آسانسور",
    "action": {
      "type": "VIEW_POST",
      "payload": {
        "@type": "type.googleapis.com/widgets.ViewPostPayload",
        "token": "QaJr0xgc",
        "web_info": {
          "title": "...",
          "district_persian": "شمس‌آباد",
          "city_persian": "تهران"
        }
      }
    },
    "image_url": "https://s100.divarcdn.com/...",
    "bottom_description_text": "دقایقی پیش",
    "middle_description_text": "۸,۵۰۰,۰۰۰,۰۰۰ تومان",
    "has_divider": true,
    "image_count": 4
  }
}
```

---

### Post Detail

#### `GET /v8/posts-v2/web/{token}`
Returns the full detail page for a single post, as a list of sections containing widget arrays.

**URL parameters**:
- `token` — unique post identifier (e.g. `QaJr0xgc`)

**Response**:
```json
{
  "sections": [
    {
      "section_name": "BREADCRUMB",
      "widgets": [ ... ]
    },
    {
      "section_name": "HEADER",
      "widgets": [ ... ]
    },
    {
      "section_name": "IMAGES",
      "widgets": [ ... ]
    },
    {
      "section_name": "DETAILS",
      "widgets": [ ... ]
    }
  ]
}
```

Each widget in a section follows the same `{ widget_type, data }` pattern. Common `widget_type` values on the detail page include `BREADCRUMB`, `TITLE`, `KEY_VALUE`, `DESCRIPTION`, `IMAGE_GALLERY`, `MAP`, `SHARE_BUTTON`, `BOOKMARK`.

---

### Contact Info

#### `POST /v8/postcontact/web/contact_info_v2/{token}`
Returns the seller's contact details for a specific listing. Requires user authentication.

**URL parameters**:
- `token` — post token (e.g. `QaJr0xgc`)

**Request body**: empty `{}` or omitted.

**Response**:
```json
{
  "widget_list": [
    {
      "widget_type": "UNEXPANDABLE_ROW",
      "data": {
        "@type": "type.googleapis.com/widgets.UnexpandableRowData",
        "title": "شمارهٔ موبایل",
        "value": "۰۹۱۲XXXXXXX",
        "action": {
          "type": "CALL_PHONE",
          "payload": {
            "@type": "type.googleapis.com/widgets.CallPhonePayload",
            "phone_number": "0912XXXXXXX"
          }
        },
        "compact": true,
        "has_copy_to_clipboard": true,
        "send_action_log_on_copy": true
      }
    },
    {
      "widget_type": "STATEMENT",
      "data": {
        "@type": "type.googleapis.com/widgets.StatementData",
        "title": "درخواست بیعانه، از نشانه‌های کلاهبرداری",
        "description": "..."
      }
    }
  ]
}
```

---

### Map / Geo-clustering

#### `POST /v8/mapview/viewport`
Returns geo-clustered listing counts for the current map bounding box. Used to render cluster markers on the map.

**Request body**:
```json
{
  "city_ids": ["1"],
  "search_data": {
    "form_data": {
      "data": {
        "category": { "str": { "value": "residential-rent" } }
      }
    },
    "query": "آپارتمان"
  },
  "camera_info": {
    "bbox": {
      "min_latitude": 35.449596,
      "min_longitude": 51.107464,
      "max_latitude": 35.982539,
      "max_longitude": 51.636307
    },
    "place_hash": "1||real-estate",
    "zoom": 9.047565829378147
  }
}
```

**Response**:
```json
{
  "clusters": [
    {
      "lon": 51.1083984375,
      "lat": 35.7522137,
      "long_preview_title": "۳۹۳",
      "properties": {
        "geometry": {
          "type": "Point",
          "coordinates": [51.1083984375, 35.7522137]
        },
        "properties": {
          "count": 393,
          "text": "۳۹۳",
          "lat": 35.7522137,
          "lon": 51.1083984375,
          "destination_zoom": 11
        },
        "type": "Feature"
      }
    }
  ]
}
```

Each cluster object is a GeoJSON `Feature` with a `count` property and a `destination_zoom` suggesting what zoom level to use when the user taps the cluster.

---

### Autocomplete / Prediction

#### `POST /v8/prediction/w/query`
Returns autocomplete suggestions as the user types in the search bar.

**Request body**:
```json
{
  "query": "آپارتمان",
  "cities": ["1"]
}
```

**Response**:
```json
{
  "suggestions": [
    {
      "title": "آپارتمان",
      "subtitle": "در فروش آپارتمان",
      "display_text": "۱۰ هزار آگهی",
      "search_data": {
        "form_data": {
          "data": {
            "category": { "str": { "value": "apartment-sell" } },
            "districts": { "repeated_string": {} }
          }
        },
        "query": "اپارتمان"
      },
      "change_city": {},
      "probability": 0.5905,
      "ad_count": "10148"
    }
  ]
}
```

---

### Filters

#### `POST /v8/postlist/w/filters`
Returns the dynamic filter panel for the current search context (districts, price range, size, etc.).

**Request body**:
```json
{
  "city_ids": ["1"],
  "data": {
    "form_data": {
      "data": {
        "category": { "str": { "value": "residential-rent" } }
      }
    },
    "server_payload": {
      "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
      "additional_form_data": {
        "data": {
          "sort": { "str": { "value": "sort_date" } }
        }
      }
    },
    "query": "آپارتمان"
  },
  "source_view": "SEARCH"
}
```

**Response**:
```json
{
  "page": {
    "widget_list": [
      {
        "widget_type": "I_LAZY_MULTI_SELECT_DISTRICT_ROW",
        "data": {
          "@type": "type.googleapis.com/widgets.ILazyMultiSelectHierarchyRowData",
          "has_divider": true,
          "field": {
            "key": "districts",
            "validators": {},
            "type": "repeated_string"
          },
          "online_search": {
            "min_query_length": 2,
            "placeholder": "جستجو",
            "delay_ms": 300,
            "field_key": "districts",
            "source": "filter"
          },
          "lazy_payload": {
            "@type": "type.googleapis.com/post_list.LazyFilterPayload",
            "filter_name": "districts",
            "version": "68",
            "place_ids": ["1"],
            "category_slug": "..."
          }
        }
      }
    ]
  }
}
```

---

### User & Notifications

#### `GET /v8/search-bookmark/web/get-search-bar-empty-state`
Returns saved searches and the empty-state content for the search bar. Requires authentication (returns `RBAC: access denied` for unauthenticated users).

#### `GET /v8/call/call-history/unacted-bundle-count`
Returns the count of unread/unacted call history bundles for the logged-in user. Used to render notification badges.

#### `GET /chat/api/unread`
Returns the count of unread chat messages. Used for the chat notification badge in the navbar.

#### `GET /v8/premium-user/post-page/business-data/{token}/lazy`
Lazy-loads premium/business seller data for a post detail page. Returns promoted listings, agency info, etc.

---

### Analytics & Telemetry

#### `POST /v1/client-exporter/send-report` (beacon)
General client-side analytics and error reporting. Sent as a [Navigator.sendBeacon](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon) call (non-blocking).

#### `POST /v8/actionlog/send` (beacon)
Sends user interaction action logs (views, clicks, engagement events). Non-blocking beacon.

#### `POST https://actionlog.divar.ir/log` (beacon)
Secondary action-logging endpoint (separate subdomain). Non-blocking beacon.

#### `POST https://sentry.divar.cloud/api/5/envelope/`
[Sentry](https://sentry.io/) error and performance monitoring. Uses Sentry JS SDK v8.13.0 with React integration.

---

## Widget System

All API responses use a **server-driven widget architecture**. Each widget follows:

```json
{
  "widget_type": "<TYPE_STRING>",
  "data": {
    "@type": "type.googleapis.com/widgets.<WidgetDataType>",
    // ...fields
  }
}
```

### Common widget types observed

| widget_type | Description |
|-------------|-------------|
| `POST_ROW` | A single listing card in the list view |
| `POST_LIST_HEADLINE` | Page heading text |
| `SEARCH_ALERT_TOGGLE_ROW` | "Notify me on new listings" toggle |
| `BREADCRUMB` | Navigation breadcrumb |
| `KEY_VALUE` | Property detail row (e.g. size, floor) |
| `DESCRIPTION` | Freeform listing description |
| `IMAGE_GALLERY` | Scrollable image gallery |
| `MAP` | Embedded map widget |
| `UNEXPANDABLE_ROW` | Contact detail row (phone number) |
| `STATEMENT` | Warning / informational text block |
| `I_LAZY_MULTI_SELECT_DISTRICT_ROW` | District multi-select filter |

### Action types

Actions inside widgets trigger navigation/behavior:

| action.type | Behavior |
|-------------|----------|
| `VIEW_POST` | Open post detail page |
| `CALL_PHONE` | Dial phone number |
| `OPEN_POSTLIST_PAGE_GRPC` | Navigate to a search result page |

---

## form_data Field Types

Each filter field in `form_data.data` uses a typed wrapper. The wrapper type depends on the field — using the wrong type returns HTTP 400.

| Field | Wrapper type | Value format | Example |
|-------|-------------|--------------|---------|
| `category` | `str` | category slug string | `{ "str": { "value": "residential-rent" } }` |
| `sort` | `str` | sort slug string | `{ "str": { "value": "sort_date" } }` |
| `districts` | `repeated_string` | array of district ID strings | `{ "repeated_string": { "value": ["920", "82"] } }` |
| `rooms` | `repeated_string` | array of Persian room strings | `{ "repeated_string": { "value": ["یک", "دو"] } }` |
| `rent` | `number_range` | min/max as strings | `{ "number_range": { "minimum": "20000000", "maximum": "60000000" } }` |
| `credit` | `number_range` | min/max as strings | `{ "number_range": { "minimum": "300000000", "maximum": "600000000" } }` |
| `size` | `number_range` | min/max as strings (m²) | `{ "number_range": { "minimum": "80", "maximum": "120" } }` |
| `balcony` | `boolean` | JS boolean | `{ "boolean": { "value": true } }` |
| `parking` | `boolean` | JS boolean | `{ "boolean": { "value": true } }` |

**Verified working example** (residential rental, Tehran, districts from URL `almahdi` search):
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
        "rent":      { "number_range":    { "minimum": "20000000",  "maximum": "60000000"  } },
        "credit":    { "number_range":    { "minimum": "300000000", "maximum": "600000000" } },
        "size":      { "number_range":    { "minimum": "80",        "maximum": "120"       } },
        "balcony":   { "boolean":         { "value": true } },
        "parking":   { "boolean":         { "value": true } }
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

---

## Pagination Pattern

Divar uses **cursor-based pagination** for the search feed:

1. **First page**: send `source_view` + `search_data`, no `pagination_data`
2. **Subsequent pages**: include `pagination_data` with:
   - `last_post_date` — ISO8601 timestamp of last seen post
   - `page` / `layer_page` — incrementing page counters
   - `search_uid` — UUID that stays constant for the whole session
   - `cumulative_widgets_count` — total widgets loaded so far
   - `viewed_tokens` — gzip+base64-encoded bloom filter of seen post tokens (used server-side for deduplication)

---

## Category Slugs

Categories are passed as `category.str.value` in `form_data`. **These are API slugs and differ from the URL path segments on divar.ir.**

| API Slug | URL path segment | Description (Persian) |
|----------|-----------------|----------------------|
| `residential-rent` | `rent-residential` | اجاره مسکونی (residential rental) |
| `apartment-sell` | `apartment-sell` | فروش آپارتمان (apartment sale) |
| `apartment-rent` | `rent-apartment` | اجاره آپارتمان (apartment rental) |
| `buy-residential` | `buy-residential` | فروش مسکونی (residential sale) |
| `real-estate` | `real-estate` | همه انواع ملک (all real estate) |
| `buy-commercial-property` | `buy-commercial-property` | فروش اداری و تجاری (commercial sale) |
| `rent-commercial-property` | `rent-commercial-property` | اجاره اداری و تجاری (commercial rental) |
| `rent-temporary` | `rent-temporary` | اجاره کوتاه‌مدت (short-term rental) |
| `real-estate-services` | `real-estate-services` | پروژه‌های ساخت‌وساز (construction) |

> ⚠️ The URL path segment (`/s/tehran/rent-residential/...`) is **not** the same as the API slug. Always use the API slug column above. When in doubt, intercept a real search via browser DevTools to read the actual `category.str.value` being sent.

---

## Infrastructure Notes

- **API version**: v8 is the current stable API version; v1 is used only for legacy analytics (`client-exporter`)
- **Protocol**: All core API calls are JSON over HTTPS; no gRPC detected at the network level (protobuf type annotations are embedded in JSON values via `@type`)
- **Auth**: Cookie-based session authentication (`token` cookie) plus `Authorization: Basic <jwt>` header — both are the same JWT value. The search endpoint works with browser session cookies alone when called from `divar.ir` (same-site). Cross-origin calls require the explicit `Authorization` header.
- **CORS**: API endpoints are same-origin from `divar.ir`; cross-origin XHR is blocked
- **Map tiles**: Served from `tiles.raah.ir` and `map.divarcdn.com` (custom Mapbox-compatible tile server)
- **Images**: Hosted on `postimage01.divarcdn.com` and `s100.divarcdn.com` in WebP format with thumbnails at path pattern `/static/photo/neda/webp_thumbnail/{hash}/{uuid}.webp`
- **Error monitoring**: Sentry SDK `sentry.javascript.react@8.13.0` sending to `sentry.divar.cloud`
- **JS bundle**: Built with Webpack, hosted on `s100.divarcdn.com/web-assets/2026/03/`, React-based SPA
