# AgentWeb API Reference

Base URL: `https://api.agentweb.live/v1`

## Authentication

All endpoints except `/v1/health` require an API key.

### Register
```
POST /v1/register
Body: {"email": "you@example.com", "name": "My Agent"}
Response: {"api_key": "aw_live_...", "message": "..."}
```

### Auth methods (use any one)
- Header: `X-API-Key: aw_live_...`
- Header: `Authorization: Bearer aw_live_...`
- Query param: `?api_key=aw_live_...`

## Endpoints

### GET /v1/health
Public. Returns directory stats.
```json
{"status": "ok", "total_businesses": 11700000, "countries": 195}
```

### GET /v1/search
Search businesses by text, category, and/or location.

| Param | Type | Description |
|-------|------|-------------|
| q | string | Text search (name, category) |
| category | string | Exact category filter |
| lat | float | Latitude for geo search |
| lng | float | Longitude for geo search |
| radius_km | float | Radius 0.1-500 (default 10) |
| country_code | string | ISO 2-letter filter |
| limit | int | 1-100 (default 20) |
| cursor | string | Pagination cursor from previous response |

Response:
```json
{
  "status": "ok",
  "meta": {"total_results": 42, "returned": 10, "next_cursor": "10"},
  "results": [
    {
      "id": "uuid",
      "name": "Business Name",
      "category": "restaurant",
      "address": {"street": "...", "city": "...", "country": "DK"},
      "coordinates": {"lat": 55.67, "lng": 12.56},
      "phone_numbers": [{"type": "main", "number": "+45 12345678"}],
      "email": "info@example.com",
      "website": "https://example.com",
      "opening_hours": {"monday": {"ranges": [{"open": "09:00", "close": "17:00"}]}},
      "trust": {"confidence_score": 0.85}
    }
  ]
}
```

### GET /v1/business/{id}
Get full details for a single business by UUID.

### POST /v1/contribute
Add or enrich a business.

Body:
```json
{
  "name": "Business Name",
  "phone": "+45 12345678",
  "email": "info@example.com",
  "website": "https://example.com",
  "category": "restaurant",
  "address": {"street": "Main St 1", "city": "Copenhagen", "postcode": "1000", "country": "DK"},
  "country_code": "DK",
  "hours": {"mon": "9AM-5PM", "tue": "9AM-5PM", "sun": "Closed"},
  "lat": 55.676,
  "lng": 12.568
}
```

Only `name` is required. Returns:
- `{"status": "created", "business_id": "uuid"}` — new business
- `{"status": "enriched", "business_id": "uuid"}` — existing updated

### POST /v1/report
Report incorrect data.

Body:
```json
{
  "business_id": "uuid",
  "report_type": "closed",
  "details": "Optional details"
}
```

Types: `closed`, `wrong_phone`, `wrong_address`, `wrong_hours`, `spam`, `duplicate`, `other`.

### GET /v1/business/{id}/freshness
Check data freshness and reliability score for a business.

## Rate Limits
- Free tier: 100 requests/minute per API key
- 429 response with `retry_after` header when exceeded
