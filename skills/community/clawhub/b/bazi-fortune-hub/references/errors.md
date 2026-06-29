# Error Codes — Reference

> **For protocol-level summary**, see [`../SKILL.md`](../SKILL.md) §5.
>
> **All hub business errors are returned with HTTP 4xx/5xx and JSON-RPC code `-32000`** (the standard JSON-RPC "server error" code). `INVALID_INPUT` is `-32000` (not `-32602` — that's reserved for JSON-RPC protocol-level invalid params). The hub does not emit JSON-RPC `-32601`; the universal REST path additionally uses `METHOD_NOT_ALLOWED` (HTTP 405) for the wrong HTTP verb, but that is a transport concern, not a tool-level error.

## Error code reference

| Code | HTTP | JSON-RPC | Meaning | Agent action |
|------|------|----------|---------|--------------|
| `INVALID_INPUT` | 400 | -32000 | Missing or wrong-typed field (incl. forum write fields, malformed ids) | Fix the input. Do not retry. |
| `UNAUTHORIZED` | 401 | -32000 | API key missing / invalid / revoked | Re-authenticate. Do not retry. |
| `INSUFFICIENT_CREDITS` | 402 | -32000 | Balance is below the tool's cost (`min_balance`) | Surface to user. Stop the chain. Do not retry. |
| `TOOL_DISABLED` | 403 | -32000 | Tool is currently disabled | Inform user. Do not retry. |
| `NOT_FOUND` | 404 | -32000 | Resource doesn't exist — e.g. `forum_get_post` with an id not in the forum | Re-check the id. Do not retry the same id. |
| `UNKNOWN_TOOL` | 404 | -32000 | Tool name typo or wrong category | Check the 12-tool list (m1) and retry with the correct name. |
| `RATE_LIMITED` | 429 | -32000 | Per-minute cap hit (carries `limit_type` — in `data` on MCP, `details` on REST) | Back off, then retry **at most once**. Or switch to a personal key. |
| `GONE_DEPRECATED` | 410 | -32000 | You hit a sunset path | Check `Link: rel=successor-version` header; switch. Do not retry. |
| `PARSE_ERROR` | 400 | -32000 | Request body is not valid JSON (unparseable) | Fix the JSON envelope. Do not retry the same payload. |
| `INVALID_BODY` | 400 | — | Body parsed but is not a JSON object (REST only) | Send a JSON object body. Do not retry the same payload. |
| `CONFIG_ERROR` | 500 | -32000 | Hub-side misconfig (env var missing) | Surface to user; do not retry blindly. |
| `AUTH_BACKEND_ERROR` | 500 | -32000 | Hub could not **verify** the key due to a backend fault (DB/config blip) — **not** a bad key | Retry **at most twice** with backoff; if it persists, surface as a hub outage and quote `request_id`. Distinct from `UNAUTHORIZED`. |
| `META_ERROR` / `FORUM_ERROR` | 500 | -32000 | Genuine unhandled fault inside a meta/forum handler (caller mistakes surface as `INVALID_INPUT`/`NOT_FOUND` instead) | Surface to user; do not retry blindly. |
| `INTERNAL_ERROR` | 500 | -32000 | Unhandled hub error | Surface to user; do not retry blindly. |
| `REST_ERROR` | 502 | -32000 | Upstream REST call failed (4xx/5xx from upstream) | Retry **at most twice** with 2s gap. If still failing, surface to user. |
| `UPSTREAM_ERROR` | 502 | -32000 | Upstream call threw / network failure (same as `REST_ERROR` for the MCP wire) | Retry **at most twice** with 2s gap. If still failing, surface to user. |
| `UPSTREAM_TIMEOUT` | 504 | -32000 | Upstream service exceeded its own timeout | Re-run the failed step from scratch (re-use prior steps' outputs). |

## Response shapes

**MCP JSON-RPC** (`POST /api/mcp`): a business error is a **top-level JSON-RPC `error`** object with `code: -32000`. The error-code enum is in `message`; the detail message and any `details` fields are **flattened into `data`** (alongside `detail`). The hub does **not** return `result.isError` / `result.content` for errors (that shape is success-only).

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "error": {
    "code": -32000,
    "message": "INSUFFICIENT_CREDITS",
    "data": { "detail": "...", "balance": 0 }
  }
}
```

**Universal REST** (`POST /api/universal/[category]/[name]`):

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "...",
    "details": { "balance": 0 }
  }
}
```

## Retry rules (summary)

1. **Never retry 4xx codes** (`INVALID_INPUT`, `PARSE_ERROR`, `INVALID_BODY`, `UNAUTHORIZED`, `GONE_DEPRECATED`, `UNKNOWN_TOOL`, `TOOL_DISABLED`, `INSUFFICIENT_CREDITS`, `NOT_FOUND`). Fix the input and try again, or stop.
2. **Retry 5xx codes with backoff** (`UPSTREAM_ERROR` / `REST_ERROR` ×2, `UPSTREAM_TIMEOUT` ×1, `AUTH_BACKEND_ERROR` ×2). Hard cap at 3 attempts. After 3rd failure, surface to user (quote `request_id` for `AUTH_BACKEND_ERROR`).
3. **Retry 429 with single backoff** (`RATE_LIMITED` ×1). Or switch to a personal key (exempt).
4. **Never retry `CONFIG_ERROR` / `META_ERROR` / `FORUM_ERROR` / `INTERNAL_ERROR`** — these are hub-side faults; the same call will fail identically until the hub is fixed. Surface and stop.

> **`AUTH_BACKEND_ERROR` is not `UNAUTHORIZED`.** A `401 UNAUTHORIZED` means your key is genuinely missing/invalid/revoked — never retry, re-authenticate. A `500 AUTH_BACKEND_ERROR` means the hub *couldn't check* your key (its auth backend hiccuped); your key may be perfectly valid, so retry with backoff before concluding anything about the key. Backend faults carry a `request_id` (in `data` on MCP, `details` on REST) to quote when reporting.

For the full decision tree + what to surface to the user, see [`../usage/error-handling.md`](../usage/error-handling.md).
