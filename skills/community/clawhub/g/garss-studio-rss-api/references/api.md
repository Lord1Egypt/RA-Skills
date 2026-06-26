# GARSS Studio Backend API Reference

Project repository: `https://github.com/zhaoolee/garss`.

All paths are relative to the single public base URL, usually `http://127.0.0.1:25173`.

## Public Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/docs` | Swagger UI for interactive API docs. |
| `GET` | `/api/openapi.json` | Machine-readable OpenAPI JSON. |
| `GET` | `/api/health` | Backend health, RSSHub base URL, subscription count, server time. |
| `GET` | `/api/image-proxy?url={imageUrl}` | Proxy remote images for reader previews. |
| `POST` | `/api/auth/login` | Login with JSON `{ "accessCode": "banana" }`; returns Bearer token. |

## Protected Endpoints

Use `Authorization: Bearer <token>`.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/auth/session` | Validate current token/session. |
| `GET` | `/api/subscriptions` | List subscriptions and categories. |
| `POST` | `/api/subscriptions` | Create a subscription. `routePath` can be RSSHub path or full RSS URL. |
| `POST` | `/api/subscriptions/test` | Test a subscription route before saving. |
| `PUT` | `/api/subscriptions/{id}` | Update subscription metadata, route, categories, enabled state. |
| `DELETE` | `/api/subscriptions/{id}` | Delete subscription and cached reader data. |
| `GET` | `/api/settings` | Read fetch scheduler settings for the authenticated user bucket. |
| `PUT` | `/api/settings` | Update auto refresh interval and parallel fetch count. |
| `POST` | `/api/categories` | Create explicit category. |
| `PUT` | `/api/categories/{name}` | Rename category and update related subscriptions. |
| `DELETE` | `/api/categories/{name}` | Delete category; affected subscriptions move to fallback category. |
| `GET` | `/api/rsshub/fetch?routePath={path}` | Fetch raw RSS XML for an RSSHub path. |
| `GET` | `/api/reader/items?refresh={boolean}` | Read aggregated items across enabled subscriptions. `refresh=true` forces upstream fetch. |
| `GET` | `/api/reader/subscriptions/{id}?refresh={boolean}` | Read one enabled subscription. `refresh=true` refreshes that source. |

## Socket.IO

Connect to `/socket.io` on the same base URL and pass the token in `auth.token`.

The server emits backend status and reader task progress events used by the UI. Prefer REST endpoints for one-shot AI news reading.

## Useful Request Examples

Login:

```bash
BASE_URL='http://127.0.0.1:25173'
TOKEN="$(curl -sS -X POST "$BASE_URL/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"accessCode":"banana"}' \
  | node -pe 'JSON.parse(fs.readFileSync(0, "utf8")).token')"
```

Read cached aggregated news:

```bash
curl -sS "$BASE_URL/api/reader/items" \
  -H "Authorization: Bearer $TOKEN"
```

Force refresh all enabled sources:

```bash
curl -sS "$BASE_URL/api/reader/items?refresh=true" \
  -H "Authorization: Bearer $TOKEN"
```

List subscriptions:

```bash
curl -sS "$BASE_URL/api/subscriptions" \
  -H "Authorization: Bearer $TOKEN"
```
