# Streaming — SSE, Chunked Responses, WebSockets

## SSE Wire Format

- Events are `data:` lines terminated by a blank line; `event:` and `id:` lines are optional. Multiple `data:` lines within one event join with `\n`.
- The #1 parse bug: treating one network chunk as one event. TCP splits and merges events arbitrarily — buffer bytes and emit only at the blank-line delimiter, never `JSON.parse(chunk)`.
- OpenAI-style APIs end the stream with a `data: [DONE]` sentinel — that is a provider convention, not SSE spec; other providers simply close the connection. Check the service section for the termination signal.
- Errors after headers are sent arrive IN the stream: the status is already 200, so a mid-stream error event or early close is the failure mode — 200 plus an open stream is not yet success (extends SKILL.md Core Rule 5).
- Test with `curl -N` (disables curl's own buffering); without `-N` the stream "hangs" and then dumps everything at once.
- On reconnect, send `Last-Event-ID` where the provider supports it to resume instead of restarting.

## Streams That Buffer, Hang, or Die

- Works locally, arrives all-at-once deployed → a proxy is buffering: nginx needs `proxy_buffering off` (or honor `X-Accel-Buffering: no`); many serverless/edge platforms buffer entire responses — confirm the platform supports response streaming before debugging code.
- Stream cuts at a suspiciously round time → an idle timeout in the path (AWS ALB defaults to 60s idle; nginx `proxy_read_timeout` defaults to 60s). A long gap between tokens counts as idle — keepalive comments (`: ping`) or heartbeat events are the provider's fix; yours is raising the middlebox timeout.
- Read timeout for streams means inter-chunk idle, not total duration — a total-time timeout kills every long generation. Keep the connect timeout from `resilience.md`; set the read timeout to the max acceptable silence between chunks.
- Compression interacts with buffering: some proxies hold gzip output until a buffer fills — disable compression on streaming endpoints.
- The client library may buffer internally: use its streaming mode (iterator/reader), not the convenience `.text`/`.json` accessors that wait for the full body.

## Mid-Stream Failure Handling

- A dying stream has already delivered partial output; a blind retry regenerates from the start — replace the partial, never append retry output to it.
- Aggregate as you receive: a failure should yield the received prefix plus a clear error, not nothing.
- LLM streams bill for tokens generated even if you disconnect early — client-side cancellation is not a refund.

## Long Polling

- The request intentionally hangs until an event arrives or the server's hold window expires — your read timeout must exceed that documented hold time, or every quiet period becomes a timeout error.
- An empty response at the end of the hold window is normal operation, not a failure: re-request immediately without backoff — backoff here only adds delivery latency. Back off on actual errors only (formula: SKILL.md Core Rule 2).
- Pass the returned offset/cursor on every request (Telegram `getUpdates` offset is the canonical example) — omitting it redelivers the same events forever.
- One outstanding poll per consumer: parallel long polls against the same cursor deliver duplicates and race the acknowledgment.

## WebSockets

- Heartbeat below the infrastructure's idle timeout: a ping every 20-30s clears the common 60s middlebox defaults above.
- Reconnect with backoff and jitter (formula: SKILL.md Core Rule 2) AND resubscribe — a reconnect that forgets its subscriptions looks "connected but silent".
- Ordering is guaranteed within one connection only. Across reconnects, dedupe by message ID or sequence number.
- Messages missed while disconnected: providers with sequence/resume tokens let you request the gap; without them, re-fetch current state via REST after reconnect — the same "event is a ping, state comes from the API" law as `webhooks.md` Delivery.
- The auth token from the handshake expires like any token: the server may not kill the live socket at expiry, but every reconnect fails — refresh before reconnecting, not after the 401.
- Backpressure: consuming slower than the sender fills memory without any error. Measure queue depth; process, batch, or drop deliberately.
