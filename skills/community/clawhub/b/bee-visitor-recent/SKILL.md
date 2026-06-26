---
name: bee-visitor-recent
description: A latest visitor data retrieval skill based on the "Bee Website Builder" Open API. It is used to obtain the latest visitor list and generate structured analysis data.
homepage: https://open.tradew.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🐝",
        "requires": { "env": ["BEE_API_KEY"] },
        "primaryEnv": "BEE_API_KEY"
      }
  }
---

# bee-visitor-recent

> Version: 2.0.3

## Overview

Use the Bee Website Builder Open API to retrieve the latest visitor data and generate a structured analysis report.

Supports paginated queries.

---

## Input Parameters

### `api_key` (string, **Required**)

API authentication key used for caller identity verification and interface access control.

- **Get it from:** https://open.tradew.com
- **Recommended configuration:** Inject it via `skills.entries.env.BEE_API_KEY` to avoid passing it in plaintext on every call.

---

### `pagination` (object, **Required**)

Pagination configuration parameters.

#### `current_page` (integer)

- Default: 1
- Minimum: 1
- Pagination rules:
  - Must rely on `data.pagination.has_next_page`
  - Use `data.pagination.next_page` as the next page number
  - Do not infer pages based on `total_page` or manual increments
  - Requests must stop when `has_next_page=false`

#### `page_size` (integer)

- **Default:** 10
- **Range:** 10 ~ 50

---

## Output Structure

### Top-Level Fields

| Field  | Type           | Description                            |
|--------|----------------|----------------------------------------|
| status | boolean        | Request status, `true` for success / `false` for failure |
| msg    | string         | Response message                       |
| data   | object \| null | Response data, `null` on failure       |

---

### `data.pagination`

| Field          | Type         | Description            |
|----------------|--------------|------------------------|
| current_page   | integer      | Current page number    |
| page_size      | integer      | Items per page         |
| total_page     | integer      | Total pages            |
| total_count    | integer      | Total records          |
| has_next_page  | boolean      | Whether a next page exists |
| next_page      | integer/null | Next page number       |

---

### `data.list[]` (visitor data list)

| Field            | Type    | Description                   |
|------------------|---------|-------------------------------|
| ip               | string  | Visitor IP (IPv4 / IPv6)      |
| country_code     | string  | Country code (ISO 3166-1)     |
| page_views       | integer | Page view count               |
| first_visit      | object  | First visit record            |
| recent_visits    | array   | Recent visit records (up to 50) |
| first_visit_time | string  | First visit time (ISO 8601)   |
| last_visit_time  | string  | Last visit time (ISO 8601)    |

---

### `first_visit` Object

| Field        | Type   | Description              |
|--------------|--------|--------------------------|
| page         | object | First visited page info  |
| screen       | object | Screen resolution        |
| visit_time   | string | First visit time         |
| referer      | string | Referrer URL             |
| current_url  | string | Current visit URL        |
| user_agent   | string | Browser User-Agent       |

#### `first_visit.page`

| Field | Type    | Description     |
|-------|---------|-----------------|
| id    | integer | Page ID         |
| name  | string  | Page name       |
| code  | string  | Page identifier |

#### `first_visit.screen`

| Field  | Type    | Description   |
|--------|---------|---------------|
| width  | integer | Screen width  |
| height | integer | Screen height |

---

### `recent_visits[]` Object

| Field        | Type   | Description         |
|--------------|--------|---------------------|
| page         | object | Page information    |
| screen       | object | Screen resolution   |
| visit_time   | string | Visit time          |
| referer      | string | Referrer URL        |
| current_url  | string | Current URL         |
| user_agent   | string | Browser User-Agent  |

#### `recent_visits.page`

| Field | Type    | Description     |
|-------|---------|-----------------|
| id    | integer | Page ID         |
| name  | string  | Page name       |
| code  | string  | Page identifier |

#### `recent_visits.screen`

| Field  | Type    | Description |
|--------|---------|-------------|
| width  | integer | Width       |
| height | integer | Height      |

---

### Notes

1. `data` may be `null` on failure
2. `recent_visits` contains at most 50 entries
3. All time fields use ISO 8601
4. `next_page` is valid only when `has_next_page=true`
5. Whether to continue pagination is decided by the caller
