# bee-visitor-recent

> Version: 2.0.3

## Overview

A latest visitor data retrieval skill based on the "Bee Website Builder" Open API. It is used to obtain the latest visitor list and generate structured analysis data.

Supports paginated queries.

## Features

- ✅ Retrieve the latest visitors to enterprise websites built with Bee
- ✅ Support paginated queries, with page turning decided by the user
- ✅ Return each visitor's latest visit behavior and source information

## Request Parameters

### Required

| Parameter    | Type   | Description                                      |
|--------------|--------|--------------------------------------------------|
| `api_key`    | string | API authentication key (obtain from https://open.tradew.com) |
| `pagination` | object | Pagination settings                              |

#### `pagination` Structure

| Field          | Type    | Default | Description             |
|----------------|---------|---------|-------------------------|
| `current_page` | integer | 1       | Current page number, >= 1 |
| `page_size`    | integer | 10      | Items per page, range 10-50 |

## Response

### Base Structure

| Field    | Type         | Description                      |
|----------|--------------|----------------------------------|
| status   | boolean      | `true` for success / `false` for failure |
| msg      | string       | Response message                 |
| data     | object\|null | Response data (`null` on failure) |

### `data` Structure

| Field        | Type   | Description      |
|--------------|--------|------------------|
| pagination   | object | Pagination info  |
| list         | array  | Visitor list     |

---

### `pagination` Object

| Field          | Type    | Description                       |
|----------------|---------|-----------------------------------|
| current_page   | integer | Current page number               |
| page_size      | integer | Items per page                    |
| total_page     | integer | Total number of pages             |
| total_count    | integer | Total number of records           |
| has_next_page  | boolean | Whether a next page exists        |
| next_page      | integer | Next page number, or `null` if none |

---

### `list` Field Description

| Field             | Type    | Description                    |
|-------------------|---------|--------------------------------|
| ip                | string  | Visitor IP (IPv4 / IPv6)       |
| country_code      | string  | Country code (ISO 3166-1)      |
| page_views        | integer | Page view count                |
| first_visit       | object  | First visit record             |
| recent_visits     | array   | Recent visit records (up to 50) |
| first_visit_time  | string  | First visit time (ISO 8601)    |
| last_visit_time   | string  | Last visit time (ISO 8601)     |

---

### `first_visit` Object

| Field         | Type   | Description                 |
|---------------|--------|-----------------------------|
| page          | object | Page information            |
| screen        | object | Screen resolution info      |
| visit_time    | string | Visit time (ISO 8601)       |
| referer       | string | Referrer page URL           |
| current_url   | string | Current visit URL           |
| user_agent    | string | Browser User-Agent          |

---

### `page` Object

| Field | Type    | Description     |
|-------|---------|-----------------|
| id    | integer | Page ID         |
| name  | string  | Page name       |
| code  | string  | Page identifier |

---

### `screen` Object

| Field  | Type    | Description   |
|--------|---------|---------------|
| width  | integer | Screen width  |
| height | integer | Screen height |

---

### `recent_visits` Object

| Field         | Type   | Description                 |
|---------------|--------|-----------------------------|
| page          | object | Page information            |
| screen        | object | Screen resolution info      |
| visit_time    | string | Visit time (ISO 8601)       |
| referer       | string | Referrer page URL           |
| current_url   | string | Current visit URL           |
| user_agent    | string | Browser User-Agent          |

---

## Pagination Rules

- `data.pagination.has_next_page` indicates whether a next page exists
- `data.pagination.next_page` indicates the next page number; it is `null` when no next page exists
- **Whether to continue reading the next page must be decided by the user.** The agent must not automatically loop through all pages and fetch all data.

---

## Example Uses

- Enterprise foreign trade visitor behavior analysis
- Customer source channel statistics
- Page visit path analysis
- Customer profiling and device analysis
- High-frequency product visit analysis
