# Cogmate API Details

## Full Endpoint Reference

### Public Endpoints (No Token Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/hub/profile` | GET | Get Cogmate profile info |
| `/api/public/info` | GET | Basic instance info |
| `/health` | GET | Health check |

### Protected Endpoints (Token Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ask` | POST | Ask questions |
| `/api/visual/facts` | GET | List/search facts |
| `/api/visual/stats` | GET | Knowledge statistics |
| `/api/visual/graph` | GET | Graph visualization data |
| `/api/visual/health` | GET | Detailed health metrics |
| `/api/auth/check` | GET | Verify token validity |

## Request/Response Examples

### /api/hub/profile

**Response:**
```json
{
  "name": "Agent Name",
  "title": "Knowledge Explorer",
  "bio": "A personal knowledge management system...",
  "avatar": "",
  "stats": {"facts": 87},
  "api_version": "1.0"
}
```

### /api/ask?token=YOUR_TOKEN

**Request:**
```json
{
  "question": "What are the key concepts?"
}
```

> **Note:** Token must be passed as query parameter, not in JSON body.

**Response:**
```json
{
  "answer": "Based on the knowledge base, the key concepts are...",
  "sources": [
    {"id": "fact_001", "summary": "Source fact 1"},
    {"id": "fact_002", "summary": "Source fact 2"}
  ],
  "confidence": 0.85
}
```

### /api/visual/facts

**Query Parameters:**
- `token`: Access token (required)
- `search`: Search query (optional)
- `layer`: Filter by layer - fact/connection/abstract (optional)
- `limit`: Max results (optional, default 50)
- `offset`: Pagination offset (optional)

**Response:**
```json
{
  "facts": [
    {
      "id": "fact_001",
      "summary": "Key insight about topic X",
      "layer": "fact",
      "created_at": "2026-03-10T12:00:00Z",
      "tags": ["topic", "insight"]
    }
  ],
  "total": 87,
  "has_more": true
}
```

### /api/visual/stats

**Response:**
```json
{
  "facts": 87,
  "connections": 45,
  "abstracts": 12,
  "total_nodes": 144,
  "total_edges": 89
}
```

### /api/auth/check

**Query:** `?token=YOUR_TOKEN`

**Response:**
```json
{
  "valid": true,
  "scope": "qa_public",
  "permissions": {
    "chat": true,
    "browse": false,
    "full_access": false
  },
  "usage": {
    "qa_limit": 10,
    "qa_used": 3,
    "qa_remaining": 7
  },
  "expires_at": "2026-03-28T00:00:00Z"
}
```

## Error Responses

All errors return JSON:

```json
{
  "detail": "Error message",
  "error_code": "INVALID_TOKEN"
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| INVALID_TOKEN | 401 | Token not found or expired |
| INSUFFICIENT_SCOPE | 403 | Token lacks required permission |
| QUOTA_EXCEEDED | 429 | Usage limit reached |
| NOT_FOUND | 404 | Resource not found |
| INTERNAL_ERROR | 500 | Server error |

## Rate Limits

- `qa_public` tokens: Limited by `qa_limit` in token metadata
- `full` tokens: No hard limit, but reasonable use expected
- All tokens: 60 requests/minute per token
