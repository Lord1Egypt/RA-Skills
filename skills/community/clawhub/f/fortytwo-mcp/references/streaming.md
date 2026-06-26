# MCP Streaming via progressToken

## When streaming is used

Streaming activates when `tools/call` includes `_meta.progressToken`.
The server returns `text/event-stream` (SSE) instead of a single JSON response.

## Request

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "ask_fortytwo_prime",
    "arguments": {"query": "{user_question}"},
    "_meta": {"progressToken": "tok-1"}
  }
}
```

Same payment headers apply (`payment-signature` or `x-session-id`).

When using curl, add `-N` (no-buffer) to receive SSE chunks in real time:
```bash
curl -s -N --max-time 600 \
  -H "Content-Type: application/json" \
  -H "x-session-id: {uuid}" \
  -H "x-idempotency-key: $(uuidgen)" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"ask_fortytwo_prime","arguments":{"query":"..."},"_meta":{"progressToken":"tok-1"}}}' \
  https://mcp.fortytwo.network/mcp
```

## SSE event format

Each chunk contains an **incremental text delta** (not accumulated text):
```
event: message
data: {"jsonrpc":"2.0","method":"notifications/progress","params":{"progressToken":"tok-1","progress":1.0,"total":0.0,"message":"partial text delta"}}
```

Note: `progress` and `total` are floats (e.g. `1.0`, `0.0`), not integers.

Final result event (after all progress chunks) contains the **full accumulated answer**:
```
event: message
data: {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"full accumulated answer"}],"_meta":{"usage":{"tokens_in":50,"tokens_out":20}}}}
```

## Parsing algorithm

1. Read SSE events until a frame contains `"result"` (not `"method"`)
2. Each `notifications/progress` event's `params.message` is an **incremental delta** — concatenate them for live display
3. Final answer: `result.content[0].text` from the last event (this is the complete text, not a delta)
4. Usage (for billing): `result._meta.usage.tokens_in` / `tokens_out`

## Error during stream

```
event: message
data: {"jsonrpc":"2.0","id":3,"error":{"code":-32099,"message":"Swarm stream error","data":{"reason":"..."}}}
```

On stream error:
- retry once with the same `x-session-id` and a new `x-idempotency-key`
- if repeated `409`/`410`/`402`, restart payment flow from challenge step
- if gateway returns the same stream error repeatedly, surface the failure to user

## Notes

- Without `_meta.progressToken`: server returns plain JSON (non-streaming)
- `total: 0` in progress notifications is expected — swarm length is unknown upfront
- The same payment/session rules apply; streaming does not bypass x402
