---
name: Endpoint Standard
description: API endpoint conventions for consistent request/response format, auth, status codes, and errors. Use when designing or implementing backend API routes.
---

# Endpoint Standard

All API endpoints must follow these conventions so clients get predictable, consistent behaviour.

---

## 1. Response Format

- **Always return JSON** unless the client explicitly requests another format (e.g. `Accept: text/csv`).
- Use a **strict response envelope**:

```json
{
  "success": true,
  "data": {
    "id": "...",
    "items": []
  }
}
```

- On **error**, use the same envelope with `success: false` and an `error` object (see Error format below).
- The **HTTP status code** must always reflect the outcome (2xx success, 4xx client error, 5xx server error).

---

## 2. Error Response Format

Errors must use the same envelope and a consistent `error` shape:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User-friendly message",
    "details": {}
  }
}
```

- `code`: Machine-readable string (e.g. `UNAUTHORIZED`, `NOT_FOUND`, `VALIDATION_ERROR`).
- `message`: Short, user-facing message.
- `details`: Optional; validation errors, field list, or extra context. Omit if empty.

---

## 3. Authentication

- **Always use tokens for authentication**, not credentials in the request body.
- Prefer **Bearer token** in the `Authorization` header: `Authorization: Bearer <token>`.
- Do **not** send passwords or long-lived secrets in query params or JSON body for auth; use them only for login/token-exchange endpoints, then rely on tokens for all other requests.
- Return `401 Unauthorized` when the token is missing or invalid; return `403 Forbidden` when the token is valid but the user lacks permission.

---

## 4. Request Format

- **Body**: Use JSON for request bodies with `Content-Type: application/json`.
- **Ids and filters**: Prefer path params for resource ids (`/items/:id`). Use query params for filtering, sorting, pagination.
- **Pagination**: Use a consistent pattern, e.g. `?page=1&limit=20` or `?offset=0&limit=20`. Include pagination metadata in `data` (e.g. `total`, `page`, `limit`).

---

## 5. HTTP Status Codes

Use standard semantics:

| Outcome              | Status code |
|----------------------|------------|
| Success (GET, PATCH, etc.) | 200 |
| Created              | 201 |
| No content (e.g. delete) | 204 |
| Bad request          | 400 |
| Unauthorized (no/invalid token) | 401 |
| Forbidden (no permission) | 403 |
| Not found            | 404 |
| Conflict             | 409 |
| Validation error     | 422 (or 400 with error details) |
| Server error         | 500 |

---

## 6. Optional but Recommended

- **API versioning**: Prefix routes (e.g. `/api/v1/...`) or use headers so clients can rely on stability.
- **CORS**: Set appropriate `Access-Control-Allow-*` headers for web clients.
- **Rate limiting**: Return `429 Too Many Requests` with a consistent error body when limits are exceeded.
- **Idempotency**: For create/update/delete, support idempotency keys (e.g. header) where duplicate requests must be safe.
- **Health/readiness**: Expose a non-authenticated endpoint (e.g. `GET /health`) that returns 200 and minimal JSON when the service is up.

---

## Quick Reference

| Area           | Rule |
|----------------|------|
| Response       | JSON envelope: `{ success, data }` or `{ success, error }` |
| Status code    | Always set correctly (2xx / 4xx / 5xx) |
| Auth           | Token in `Authorization` header only; no auth credentials in body |
| Errors         | `success: false`, `error: { code, message, details? }` |
| Request body   | JSON; path/query for ids and filters |
| Pagination     | Consistent params and metadata in `data` |

Use the **Endpoint Compliance Check** skill to verify that an endpoint implementation meets this standard.
