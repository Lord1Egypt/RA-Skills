# Bangumi Tracker - API Compliance

This document details the API compliance with the official [Bangumi API v0](https://github.com/bangumi/api) specification.

## Authentication

### OAuth 2.0 Flow

The implementation uses the Authorization Code Grant Type:

1. **Authorize URL**: `GET https://bgm.tv/oauth/authorize`
   - Parameters: `client_id`, `response_type=code`, `redirect_uri`

2. **Token URL**: `POST https://bgm.tv/oauth/access_token`
   - Parameters (authorization_code): `grant_type`, `client_id`, `client_secret`, `code`, `redirect_uri`
   - Parameters (refresh_token): `grant_type=refresh_token`, `client_id`, `client_secret`, `refresh_token`

3. **Token Usage**: Bearer token in Authorization header
   ```
   Authorization: Bearer <access_token>
   ```

### Token Endpoints

| Operation | Method | URL |
|-----------|--------|-----|
| Get access token | POST | `https://bgm.tv/oauth/access_token` |
| Refresh token | POST | `https://bgm.tv/oauth/access_token` |
| Check token status | POST | `https://bgm.tv/oauth/token_status` |

## Collection API

All collection endpoints require authentication.

### Get Collections

```http
GET /v0/users/{username}/collections
```

Query parameters:
- `subject_type`: 1=book, 2=anime, 3=music, 4=game, 6=real
- `type`: 1=wish, 2=doing, 3=collect, 4=on_hold, 5=dropped
- `limit`: pagination
- `offset`: pagination

### Get Single Collection

```http
GET /v0/users/{username}/collections/{subject_id}
```

Response:
```json
{
  "subject": { ... },
  "type": 2,
  "ep_status": 12,
  "vol_status": 0
}
```

### Add/Update Collection

```http
POST /v0/users/-/collections/{subject_id}
```

Request body:
```json
{
  "type": 2  // 1=wish, 2=doing, 3=collect, 4=on_hold, 5=dropped
}
```

### Update Collection (Partial)

```http
PATCH /v0/users/-/collections/{subject_id}
```

Request body (all fields optional):
```json
{
  "type": 2,
  "ep_status": 12,
  "vol_status": 0,
  "rating": 9,
  "comment": "great anime!",
  "private": false
}
```

### Remove Collection

**Important**: The official API does NOT have a DELETE endpoint.

To remove a collection, use PATCH with `type=0`:

```http
PATCH /v0/users/-/collections/{subject_id}
```

Request body:
```json
{
  "type": 0  // 0 = no collection status
}
```

## Known Limitations

1. **No DELETE endpoint**: Collections cannot be deleted via DELETE method
2. **Code expiration**: Authorization code expires in 60 seconds
3. **Rate limiting**: Follow Bangumi's rate limit policies

## Test Compliance

Run the compliance test to verify API usage:

```bash
python test_api_compliance.py
```

This tests:
- Correct HTTP methods (POST/PATCH, not PUT/DELETE)
- Correct endpoint paths (username, not numeric ID)
- Correct OAuth URLs