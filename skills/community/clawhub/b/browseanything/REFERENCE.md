# Browse Anything API Reference

Authoritative reference for what the wrapper scripts call. All requests
go to `${BROWSEANYTHING_API_URL:-https://platform.browseanything.io}` and
authenticate with `Authorization: Bearer ba_live_...` or
`X-API-Key: ba_live_...`.

Full OpenAPI spec lives at `/api/v1/docs` on the server.

## Auth

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer ba_live_<rest>` |
| `X-API-Key` | `ba_live_<rest>` (alternative) |

Errors:
- `401` — missing or invalid key
- `403` — valid key, missing scope (`tasks:read`, `tasks:write`)
- `429` — rate limit (100 req/min/key); see `X-RateLimit-Remaining` and
  `X-RateLimit-Reset` headers and `retry_after` in body

## Tasks

### `POST /api/v1/tasks` — create

Body:

```json
{
  "prompt": "Find the cheapest flight CDG→NRT in May, return airline + price.",
  "model": "gpt-5.2",
  "max_steps": 80,
  "proxy_location": "us",
  "metadata": { "source": "claude-code", "user": "alice" }
}
```

- `prompt` (string, required, ≤10 000 chars)
- `model` (string, optional). Allowed (paid tiers): `gpt-5.2`, `gpt-5.4`,
  `gpt-4.1`, `llama-4`, `openai/gpt-oss-120b`, `kimi-k2.5`, `kimi-k2.6`,
  `gemini-3-flash-preview`, `qwen/qwen3.5-9b`, `openai/gpt-5.4-mini`,
  `anthropic/claude-haiku-4.5`. Free tier: `kimi-k2.5`, `kimi-k2.6`,
  `gpt-5.2`. Invalid values fall back to the tier default.
- `max_steps` (int, optional, default 80)
- `proxy_location` (string, optional) — e.g. `us`, `eu`
- `metadata` (object, optional) — opaque, returned later

Response (`202 Accepted`):

```json
{
  "success": true,
  "task": { "id": "uuid", "status": "queued", "created_at": "..." }
}
```

### `GET /api/v1/tasks/{id}` — read

Response:

```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "status": "queued | running | requires_input | completed | failed | cancelled",
    "prompt": "...",
    "result": { "description": "...", "url": "...", "title": "...", "memory": {...} },
    "error_message": null,
    "execution_time_ms": 12345,
    "step_count": 17,
    "human_input_request": "Please provide your 2FA code",
    "created_at": "...",
    "started_at": "...",
    "completed_at": "..."
  }
}
```

### `GET /api/v1/tasks/{id}/screenshot`

Returns `image/png` binary of the latest captured frame. `404` if no
screenshot is available yet (typical for very early steps).

### `POST /api/v1/tasks/{id}/input`

Body: `{ "input": "..." }`. Resumes a `requires_input` task. Returns
`{ "success": true, "message": "Input received, task execution resumed" }`.

### `DELETE /api/v1/tasks/{id}`

Cancels a queued or running task. Idempotent.

### `GET /api/v1/tasks?limit=20&offset=0`

Paginated list of tasks owned by the current key. `limit` capped at 100.

## Service

### `GET /api/v1/status`

```json
{
  "success": true,
  "status": "operational",
  "service": {
    "running_tasks": 4,
    "max_concurrency": 50,
    "available_slots": 46
  }
}
```

## Webhooks (optional)

Tasks created via API also fire webhooks if the user has any registered
in their dashboard:

- `task.completed` — payload includes `result`, `execution_time_ms`,
  `step_count`, screenshot URL
- `task.failed` — `error`, `step_count`
- `task.requires_input` — `question`, link to dashboard

Webhooks are HMAC-signed. See dashboard → Webhooks for the secret and
signature header (`X-BrowseAnything-Signature`).

## Concurrency

| Tier | Concurrent tasks per user |
|------|---------------------------|
| free | 1 |
| pro  | 2 |
| ultra | 3 |

Exceeding the limit returns `400` with a clear error message.

## Step / time caps

- Default per-task hard cap: 80 agent steps
- Hard server-side timeout: 20 minutes
- Free-tier model and step limits are stricter; see dashboard for live values
