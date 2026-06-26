# API Reference

Base URL: `http://127.0.0.1:9090` (configurable)

## POST /v1/chat/completions

Standard OpenAI Chat Completions endpoint.

### Request

```json
{
  "model": "gemini",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello"}
  ],
  "stream": false
}
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | No | Model ID (default: config `defaultModel`) |
| `messages` | array | Yes | Array of message objects |
| `stream` | boolean | No | Enable SSE streaming (default: false) |

**Message content** supports three formats:
- `string` — Plain text
- `array` — Content parts: `[{"type":"text","text":"..."}, {"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]`
- `null` — Empty content

**Silently ignored parameters:** `temperature`, `top_p`, `max_tokens`, `stop`, `n`, `presence_penalty`, `frequency_penalty`, `tools`, `functions`

### Response (non-streaming)

```json
{
  "id": "chatcmpl-<uuid>",
  "object": "chat.completion",
  "created": 1711500000,
  "model": "gemini-2.5-flash",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Hello!"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 5,
    "total_tokens": 15
  }
}
```

### Response (streaming)

With `stream: true`, returns Server-Sent Events:

```
data: {"id":"chatcmpl-1","object":"chat.completion.chunk","created":1711500000,"model":"gemini-2.5-flash","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-1","object":"chat.completion.chunk","created":1711500000,"model":"gemini-2.5-flash","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

### Session Resumption

Multi-turn conversations use CLI session resumption:

1. First request: response includes `X-Session-Id` header
2. Subsequent requests: send `X-Session-Id: <id>` header to continue the conversation
3. The proxy maps this to the CLI's `--resume` flag
4. Only the latest user message is sent (CLI retains prior context)

Sessions expire after TTL (default: 30 minutes).

### Error Responses

| HTTP Status | Error Code | Cause |
|-------------|-----------|-------|
| 400 | `model_not_found` | Unknown model ID |
| 400 | `invalid_request_error` | Malformed request |
| 429 | `rate_limit_exceeded` | Concurrency limit reached |
| 502 | `cli_error` | CLI process error (non-zero exit) |
| 503 | `cli_not_found` | CLI tool not installed |
| 504 | `timeout` | CLI process timed out |

Error body format:
```json
{
  "error": {
    "message": "Description of the error",
    "type": "server_error",
    "code": "cli_error",
    "param": null
  }
}
```

## GET /v1/models

List configured models.

```json
{
  "object": "list",
  "data": [
    {"id": "gemini", "object": "model", "created": 1711500000, "owned_by": "gemini"},
    {"id": "claude", "object": "model", "created": 1711500000, "owned_by": "claude"}
  ]
}
```

## GET /health

Health check with provider status.

```json
{
  "status": "ok",
  "activeProcesses": 0,
  "concurrency": {
    "active": 0,
    "pending": 0,
    "max": 5,
    "maxQueued": 50
  },
  "providers": {
    "gemini": {"available": true, "version": "0.35.1"},
    "claude": {"available": true, "version": "2.1.88 (Claude Code)"}
  }
}
```

Returns HTTP 503 with `"status": "degraded"` if no CLI providers are available.

## CORS

All endpoints include permissive CORS headers so that browser-based tools running on the same machine can call the proxy without preflight hassle:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Expose-Headers: X-Session-Id`

⚠️ This is only safe while the proxy is bound to `127.0.0.1` (the default). If you bind to `0.0.0.0`, the combination of a wildcard CORS origin and no authentication means any webpage visited in any browser on your LAN can drive your local CLIs. Keep `server.host` at `127.0.0.1` unless you are fronting the proxy with a reverse proxy that enforces auth and a narrow CORS origin.
