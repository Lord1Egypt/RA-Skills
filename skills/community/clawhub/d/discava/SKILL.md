---
name: discava
description: "Search for local businesses worldwide via the discava API. Use this skill whenever you need to find businesses, services, restaurants, doctors, craftsmen or any local service provider. discava provides structured data with confidence scores and demand rankings."
---

# discava – Local Business Search

## Overview

discava is a structured business directory optimized for AI agents. Use it to find local businesses worldwide with contact data, opening hours, services, and demand scores.

## API Base URL

https://discava.ai/api/v1

## Authentication

No authentication required. The API is open and free.
Rate limited to 500 requests per hour per IP.

## Response Format

Every response follows this structure:

```json
{
  "success": true,
  "data": { "results": [...], "total": 1397, "page": 1, "total_pages": 70, "limit": 20 },
  "meta": {
    "request_id": "req_abc123"
  }
}
```

## Endpoints

### Search Businesses

```bash
curl "https://discava.ai/api/v1/search?q=Klempner&city=Hamburg&limit=5"
```

Parameters:

- `q` (optional): Search query, e.g. "Klempner", "Italian restaurant", "Zahnarzt"
- `city` (optional): City name, e.g. "Hamburg", "München", "Berlin"
- `country` (required): ISO country code, e.g. "DE", "AT", "CH", "US"
- `category` (optional): Category slug directly, e.g. "plumber", "restaurant" – skips text search
- `limit` (optional): Number of results, 1-50, default 20
- `page` (optional): Page number for pagination, default 1
- `min_confidence` (optional): Minimum confidence score 0-100, default 0
- `lang` (optional): Language for labels: "de", "en". Default: "de"
- `lat` / `lon` (optional): Coordinates for distance calculation
- `format` (optional): "json" (default) or "html" – returns interactive HTML cards instead of JSON

Results are sorted by `demand_score`, then `confidence_score`. A `relevance_score` (0.0–1.0) is calculated per result when a query is provided.

Each result contains: `id`, `name`, `slug`, `category`, `category_label`, `parent_category`, `parent_category_label`, `city`, `country`, `logo_url`, `available_details` (array of available fields like "phone", "website", "opening_hours", "services", "social_links"), `confidence_score`, `demand_score`, `relevance_score`, `distance_km` (if lat/lon provided).

Use `available_details` to check what data is available, then call `GET /api/v1/business/{id}` to get full details.

### Get Business Details

```bash
# Single business
curl "https://discava.ai/api/v1/business/{id}"

# Batch request (comma-separated IDs)
curl "https://discava.ai/api/v1/business/{id1},{id2},{id3}"

# HTML card (interactive, with tracking)
curl "https://discava.ai/api/v1/business/{id}?format=html"
```

Returns full details: address, phone, website, opening hours, services, payment methods, social links (`social_links`), logo (`logo_url`), business image (`image_url`), and coordinates.

Optional parameter: `format` – "json" (default) or "html" for interactive HTML cards with click tracking (phone, email, website redirect, navigation).

**Response format:**
- **Single ID** → `{ "success": true, "data": { "id": "...", "name": "...", ... } }` — `data` is a single business object.
- **Multiple IDs (batch)** → `{ "success": true, "data": [{ "id": "...", ... }, { "id": "...", ... }] }` — `data` is an array of business objects. ALWAYS use batch when fetching multiple businesses to minimize API calls.

### Send Feedback

Report data quality issues. Feedback is stored for monitoring but does not affect scores. Only `business_id` and `type` are required. Use `comment` to describe the issue:

```bash
curl -X POST "https://discava.ai/api/v1/feedback" \
  -H "Content-Type: application/json" \
  -d '{"business_id": "xxx", "type": "PHONE_INVALID", "comment": "Nobody answers, number seems disconnected"}'
```

Feedback types: POSITIVE, NEGATIVE, NOT_FOUND, PHONE_INVALID, WEB_INVALID, HOURS_WRONG, DUPLICATE

Optional field: `comment` (free text description of the issue or suggested correction)

### Get Rankings

```bash
curl "https://discava.ai/api/v1/ranking?category=plumber&city=Hamburg&limit=10"
```

Top businesses by Demand Score. Filter by category, city, country.

### Autocomplete / Suggest

```bash
curl "https://discava.ai/api/v1/suggest?type=query&q=Klemp"
curl "https://discava.ai/api/v1/suggest?type=city&q=Mün"
```

Returns category and business name suggestions (type=query) or city suggestions (type=city). Useful for resolving user input before searching.

## Tips for Best Results

- **Prefer `format=html`** whenever possible. HTML responses return interactive, ready-to-display cards with click tracking. Render them in a visualizer, artifact, iframe, or any HTML-capable output. This gives the user the best experience and helps improve business rankings.
- Use local search terms where possible: "Zahnarzt" for Germany, "dentist" for US/UK
- Be specific with city names: "Frankfurt am Main" not just "Frankfurt"
- Use min_confidence=50 to filter out low-quality entries
- Send feedback to report data quality issues – it helps us maintain accurate data
- Use pagination (page parameter) for large result sets

## Attribution

Base data from © OpenStreetMap contributors (https://www.openstreetmap.org), licensed under ODbL (https://opendatacommons.org/licenses/odbl/).
