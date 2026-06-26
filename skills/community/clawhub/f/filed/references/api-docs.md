# Filed API Reference

Base URL: `https://filed.dev/api/v1`

## Authentication

All requests require an API key in the Authorization header:
```
Authorization: Bearer fd_live_your_api_key
```

## Endpoints

### GET /search

Search business entities by name, registered agent, officer, or filing number.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | * | Business name (* = required if agent/filing_number not set) |
| state | string | Yes | Two-letter state code (FL, NY, PA, CT, CO, OR, IA, AK) |
| agent | string | * | Registered agent name |
| officer | string | No | Officer/director/manager name |
| filing_number | string | No | State-assigned filing number |
| status | string | No | active, inactive, or all (default: all) |
| type | string | No | llc, corporation, lp |
| formed_after | date | No | YYYY-MM-DD — entities formed after this date |
| formed_before | date | No | YYYY-MM-DD — entities formed before this date |
| exact | boolean | No | Exact name match (default: false) |
| limit | integer | No | Results per page, max 50 (default: 10) |
| offset | integer | No | Pagination offset (default: 0) |

Response:
```json
{
  "data": [
    {
      "id": "ent_mNqR7xKp",
      "name": "ACME HOLDINGS LLC",
      "state": "FL",
      "type": "LLC",
      "status": "Active",
      "formedDate": "2019-03-14",
      "registeredAgent": { "name": "CSC Global", "address": "1234 Main St, Tallahassee, FL 32301" },
      "principalAddress": "123 Main St, Miami, FL 33101",
      "officerCount": 3,
      "lastUpdated": "2026-02-27T12:00:00Z"
    }
  ],
  "meta": { "total": 1, "limit": 10, "offset": 0, "state": "FL", "source": "Florida Division of Corporations" }
}
```

### GET /entity/{id}

Get full entity details including officers and filing history.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Entity ID from search results |

Response:
```json
{
  "data": {
    "id": "ent_mNqR7xKp",
    "name": "ACME HOLDINGS LLC",
    "state": "FL",
    "stateEntityId": "L19000123456",
    "type": "LLC",
    "status": "Active",
    "formedDate": "2019-03-14",
    "registeredAgent": { "name": "CSC Global", "address": "1234 Main St, Tallahassee, FL 32301" },
    "principalAddress": "123 Main St, Miami, FL 33101",
    "officers": [{ "name": "John Smith", "title": "Member/Manager" }],
    "filings": [{ "type": "Annual Report", "date": "2025-11-01" }]
  },
  "meta": { "source": "Florida Division of Corporations", "lastUpdated": "2026-02-27T12:00:00Z" }
}
```

### POST /batch

Run multiple searches in one request (Pro plan and above). Max 25 queries.

Request body:
```json
{
  "queries": [
    { "name": "Acme", "state": "FL" },
    { "name": "Widget", "state": "NY", "limit": 5 }
  ]
}
```

## Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | invalid_params | Missing or invalid query parameters |
| 401 | unauthorized | Missing or invalid API key |
| 403 | tier_insufficient | Endpoint requires a higher plan |
| 404 | not_found | Entity not found |
| 429 | rate_limit_exceeded | Monthly or per-minute limit hit |
| 500 | internal_error | Server error |
| 502 | upstream_error | State data source temporarily unavailable |
