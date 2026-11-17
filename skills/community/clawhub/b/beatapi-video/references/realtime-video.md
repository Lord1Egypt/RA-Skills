# Realtime Video sessions

Use the canonical guide at <https://docs.beatapi.io/realtime-video> together
with the bundled OpenAPI contract.

## Trust boundary

- Create sessions only from trusted server-side application code. Agent, MCP,
  and Skills-only CLI flows may inspect or close existing sessions, but must not
  create one because the response contains a one-time browser secret. Never put
  a long-lived `sk_` API key in browser JavaScript.
- `POST /v1/realtime/sessions` may return a one-time, short-lived
  `client_secret`. Pass it to the supported browser SDK through the
  application's authenticated backend; do not repeat it in chat, logs,
  analytics, or issue reports.
- The browser SDK owns camera permission, WebRTC negotiation, connection state,
  and remote media rendering. Server-side tools cannot prove those browser
  steps succeeded.

## Create

Creation requires:

- `max_duration_seconds`: exactly 15, 60, or 300;
- `allowed_origins`: 1-10 exact HTTPS origins, with no path;
- `Idempotency-Key`: a stable unique value reused only for retrying the same
  logical request;
- optional string-to-string `metadata`.

Do not run session creation through the agent. Implement the documented
`POST /v1/realtime/sessions` call in the application's authenticated backend so
neither the returned `client_secret` nor a retrieval path enters model-visible
output.

Treat session creation as paid and credit-reserving. A `ready` response means
the allocation exists; it does not mean the browser connected or received a
remote frame.

## Inspect and close

```bash
beatapi realtime sessions get SESSION_ID
beatapi realtime sessions close SESSION_ID
```

Close abandoned sessions promptly. Inspect `status`, `connected_at`,
`closed_at`, and the reserved/settled/refunded credit fields. Billing becomes
active only after BeatAPI accepts the first heartbeat following remote output.

Do not blindly retry `realtime_disabled`, `realtime_capacity_unavailable`,
`user_concurrency_exceeded`, `origin_not_allowed`, or
`invalid_client_secret`. Correct configuration or wait/close capacity first.
