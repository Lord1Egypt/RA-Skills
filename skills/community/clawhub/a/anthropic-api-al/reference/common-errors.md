# Reference — Common Errors

The Anthropic API returns a consistent error envelope. React appropriately — and **never retry errors that won't fix themselves**.

---

## Error envelope

```json
{
  "type": "error",
  "error": { "type": "rate_limit_error", "message": "..." },
  "request_id": "req_01..."
}
```

Log `request_id` for support.

---

## Status codes, types, reactions

| HTTP | `error.type` | Retry? | Reaction |
|------|--------------|--------|----------|
| 400 | `invalid_request_error` | **No** | Fix the request: add **`max_tokens`**, fix `messages`, ensure version/beta headers. |
| 401 | `authentication_error` | **No** | Fix `ANTHROPIC_API_KEY`. **Do not retry** — it will keep failing. |
| 403 | `permission_error` | No | Key lacks access; check permissions/plan. |
| 404 | `not_found_error` | No | Fix path or model ID. |
| 413 | `request_too_large` | No | Shrink input; use files/batches. |
| 429 | `rate_limit_error` | **Yes** | Backoff/retry; reduce rate or use batches. |
| 500 | `api_error` | **Yes** | Backoff/retry. |
| 529 | `overloaded_error` | **Yes** | Transient overload; backoff/retry. |

---

## The three most common mistakes

1. **Missing `max_tokens`** → `400 invalid_request_error`. It is mandatory on every `anthropic_messages` call.
2. **Missing `anthropic-version` header** → `400`. Keep `ANTHROPIC_VERSION` set (default `2023-06-01`).
3. **Beta endpoint without `ANTHROPIC_BETA`** → `400`. Set the beta flag for features like `/files`.

---

## Retry policy

- Retry **only** 429 / 5xx / 529, with exponential backoff (the MCP server does this up to `ANTHROPIC_MAX_RETRIES`).
- Honor `Retry-After` when present.
- **Never** retry 400/401/403/404 unchanged — fix the cause first. Retrying a 401 wastes calls and can look like abuse.

---

## Cost-aware handling

- Validate inputs and (for big jobs) run `anthropic_count_tokens` **before** generation so a 400 doesn't waste a billed round trip.
- Don't loop-retry failures; a runaway retry loop on a billed endpoint burns money.

See the MCP error guide for examples: [../../mcp/docs/05-error-handling.md](../../mcp/docs/05-error-handling.md).

> Verification needed: confirm the full status/type list at https://docs.anthropic.com/en/api/errors
