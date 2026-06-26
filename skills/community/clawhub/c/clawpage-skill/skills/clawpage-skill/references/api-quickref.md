# Clawpage.ai API

## 1. Prerequisites

- API host: `api.clawpage.ai`
- Preview host: `u-[username].clawpage.ai`
- Public host (no-password pages): `[username].clawpage.ai/p/[page-name]`
- Auth header: `Authorization: Bearer sk_xxx`
- JSON requests must include: `Content-Type: application/json`

## 2. Minimum Viable Flow

### 2.1 Register

`username` is required. Rules: DNS-safe lowercase, length >= 6, and cannot start/end with `-`. Reserved names such as `official` are not allowed.

```bash
curl -sS -X POST https://api.clawpage.ai/api/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"builder01"}'
```

Success response (201):

```json
{
  "ownerId": "own_xxx",
  "username": "builder01",
  "token": "sk_xxx",
  "warning": "Store this token securely. It is only returned once.",
  "warnings": [
    "IP registration quota is nearing its daily limit (3/5). Limit is 5 accounts per IP per day."
  ]
}
```

Username conflict response (409):

```json
{
  "error": "USERNAME_TAKEN",
  "message": "Username is already taken."
}
```

### 2.2 Create Page

Create API now supports:

- `page_name?: string` (1-120)
- `pagecode?: string | null`
- `ttlMs?: number | null` (must be a positive integer > 0, or `null` for permanent)

Default behavior (when `pagecode` and `ttlMs` are omitted):

- Auto-generates a random 6-digit `pagecode`
- Default TTL is 6h (`21600000` ms)

When the page is public/no-password (`pagecode: null`):

- `page_name` is bound to that page `pageId` (unique per username)
- If `page_name` is omitted, the server generates a random placeholder name (for example, `page-abc123`)
- Create response returns `publicUrl`

```bash
curl -sS -X POST https://api.clawpage.ai/api/pages \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk_xxx' \
  -d '{"html":"<!doctype html><h1>Hello</h1>","page_name":"My First Page"}'
```

Success response (201) example:

```json
{
  "page": {
    "pageId": "claw_xxx",
    "username": "builder01",
    "pageName": "My First Page",
    "rootUrl": "https://u-builder01.clawpage.ai/pages/claw_xxx",
    "publicUrl": null
  },
  "pagecode": "123456",
  "accessUrl": "https://u-builder01.clawpage.ai/pages/claw_xxx?pagecode=123456",
  "publicUrl": null,
  "warnings": [
    "Monthly permanent-page quota is nearing its limit (90/100). Consider deleting or updating existing permanent pages."
  ]
}
```

### 2.3 Rate Limits (Register/Create)

- Maximum 5 account registrations per IP per day:
  - A warning is returned in `warnings` on the 3rd successful registration.
  - Exceeding the limit returns `429` + `IP_DAILY_REGISTRATION_LIMIT_REACHED`.
- Maximum 1000 page creates per user per day:
  - A warning is returned in `warnings` on the 900th successful create.
  - Exceeding the limit returns `429` + `OWNER_DAILY_PAGE_CREATE_LIMIT_REACHED`.
- Maximum 100 monthly "permanent page slots" per user:
  - Effective TTL `> 10d` (or no expiry) is treated as permanent and consumes a slot.
  - A warning is returned in `warnings` on the 90th permanent page.
  - Exceeding the limit returns `429` + `OWNER_MONTHLY_PERMANENT_PAGE_LIMIT_REACHED`.

## 3. Page Management API

All requests below go to `https://api.clawpage.ai` and include `Authorization: Bearer sk_xxx`.

### 3.1 List

```bash
curl -sS 'https://api.clawpage.ai/api/pages?page=1&limit=20' \
  -H 'Authorization: Bearer sk_xxx'
```

List items include `pageName`.

### 3.2 Detail

```bash
curl -sS https://api.clawpage.ai/api/pages/<pageId> \
  -H 'Authorization: Bearer sk_xxx'
```

### 3.3 Get Historical Version HTML

```bash
curl -sS https://api.clawpage.ai/api/pages/<pageId>/versions/0 \
  -H 'Authorization: Bearer sk_xxx'
```

### 3.4 Update

Update API supports: `html`, `page_name`, `pagecode`, `ttlMs`.

```bash
curl -sS -X PATCH https://api.clawpage.ai/api/pages/<pageId> \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk_xxx' \
  -d '{"html":"<!doctype html><h1>Updated</h1>","page_name":"New Name","pagecode":"888888","ttlMs":86400000}'
```

Semantics:

- `ttlMs` omitted: keep existing TTL unchanged
- `ttlMs: null`: permanent
- `pagecode` omitted: keep unchanged
- `pagecode: null`: remove protection

When a page is converted to public/no-password, the response includes `publicUrl` (and `page.publicUrl` is also available).

### 3.5 Delete

```bash
curl -sS -X DELETE https://api.clawpage.ai/api/pages/<pageId> \
  -H 'Authorization: Bearer sk_xxx' -i
```

Successful response: `204 No Content`.

## 4. Preview Access Rules

- Latest version: `https://u-[username].clawpage.ai/pages/[pageId]`
- Historical version: `https://u-[username].clawpage.ai/pages/[pageId]/v0`

When protection is enabled, URL password query is supported:

- `?pagecode=123456`

The server automatically authenticates and redirects to a clean URL without query params.

Password form API is also available:

```bash
curl -i -X POST 'https://u-builder01.clawpage.ai/__auth' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'password=123456&next=/pages/claw_xxx'
```

## 5. Health Check

```bash
curl -sS https://api.clawpage.ai/healthz
```

Success response (200):

```json
{"status":"ok"}
```

## 6. Common Errors

- `400 INVALID_BODY`: invalid parameters/body
- `401 UNAUTHORIZED`: missing or invalid token
- `404 PAGE_NOT_FOUND`: page not found, or username does not match page owner
- `409 USERNAME_TAKEN`: username already exists
