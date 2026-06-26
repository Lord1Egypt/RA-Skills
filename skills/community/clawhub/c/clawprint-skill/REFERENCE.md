# API Reference

**Quick reference for all endpoints and operations**

---

## Business Operations

### Create Business

**Via CLI** (confirm `path` / `method` from `GET /api/products` — run `node scripts/clawprint` with no args for the products list):

```bash
node scripts/clawprint --method POST --path /api/businesses \
  --body '{"requested_business_name":"My Business LLC"}'
```

**Via API:**
```bash
curl -X POST https://clawprintai.com/api/businesses \
  -H "X-Public-Key: $CLAWPRINT_PUBLIC_KEY" \
  -H "X-Secret-Key: $CLAWPRINT_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{"requested_business_name": "My Business LLC"}'
```

### Get Business

```bash
node scripts/clawprint --method GET --path /api/businesses/biz_123
```

**Via API:**
```bash
curl https://clawprintai.com/api/businesses/biz_123 \
  -H "X-Public-Key: $CLAWPRINT_PUBLIC_KEY" \
  -H "X-Secret-Key: $CLAWPRINT_SECRET_KEY"
```

---

## Environment Variables

```bash
CLAWPRINT_API_URL=https://clawprintai.com/api
# From POST /api/users — both required on protected routes.
CLAWPRINT_PUBLIC_KEY=
CLAWPRINT_SECRET_KEY=
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET, PATCH) |
| 201 | Created (POST) |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (missing/invalid public + secret key pair) |
| 404 | Not found |
| 409 | Conflict (duplicate email, etc.) |
| 500 | Server error |

---

## Error Response Format

```json
{
  "error": "Descriptive error message"
}
```

---

## Data Types

### Business Status
`pending` | `forming` | `active` | `suspended` | `dissolved`

---

## Rate Limiting

Default: 100 requests/minute per credential pair

Response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1708114800
```

---

## Programmatic use (Node.js)

Use **`lib/clawprint-http.js`** from this repo (same URL rules and auth as the CLI):

```javascript
const { clawprintRequest, buildClawprintUrl } = require('./lib/clawprint-http');

// Example: products list (same as CLI default)
const { body } = await clawprintRequest({
  method: 'GET',
  path: '/api/products',
  auth: false,
});
console.log(body);

// Example: authenticated call (uses CLAWPRINT_PUBLIC_KEY + CLAWPRINT_SECRET_KEY from env)
const res = await clawprintRequest({
  method: 'POST',
  path: '/api/businesses',
  body: { requested_business_name: 'Example LLC' },
});
console.log(res.body);
```

`clawprintRequest` reads `CLAWPRINT_API_URL` / `CLAWPRINT_SITE_URL`, `CLAWPRINT_PUBLIC_KEY`, and `CLAWPRINT_SECRET_KEY` from the environment unless you pass `publicKey` / `secretKey` or `auth: false`.

---

## Tips

- The `clawprint` CLI uses `CLAWPRINT_PUBLIC_KEY` and `CLAWPRINT_SECRET_KEY` from `.env` when present
- Requests are logged for audit trail

---

## Full Documentation

- **SETUP.md** — Getting started
- **README.md** — Overview & features
- **SKILL.md** — Complete skill documentation

---

**API base:** `https://clawprintai.com/api` (override `CLAWPRINT_API_URL` for local or other hosts).

More endpoints and details in the backend API documentation.
