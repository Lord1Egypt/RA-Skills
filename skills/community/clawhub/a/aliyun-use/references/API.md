# AliYun Bailian API Reference

## Base URL

Default: `https://coding.dashscope.aliyuncs.com/v1`

Configure via environment variable `ALIYUN_BAILIAN_API_HOST`.

Other available endpoints:
| Region | Base URL |
|--------|----------|
| China (Beijing) | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| US (Virginia) | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| Singapore | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |

## Authentication

API key passed as Bearer token:
```
Authorization: Bearer $ALIYUN_BAILIAN_API_KEY
```

## Chat Completion

**Endpoint:** `POST /chat/completions`

**Request:**
```json
{
  "model": "qwen-plus",
  "messages": [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello"}
  ],
  "temperature": 0.7,
  "max_tokens": 2048
}
```

**Response:**
```json
{
  "id": "chatcmpl-xxx",
  "model": "qwen-plus",
  "choices": [
    {
      "message": {"role": "assistant", "content": "Hello! How can I help you?"},
      "finish_reason": "stop",
      "index": 0
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 15,
    "total_tokens": 35
  }
}
```

## Key Differences from OpenAI

1. **API Key:** Set `ALIYUN_BAILIAN_API_KEY` env var, not `OPENAI_API_KEY`
2. **Base URL:** Set via `ALIYUN_BAILIAN_API_HOST` env var (default: `https://coding.dashscope.aliyuncs.com/v1`)
3. **Region-specific:** API keys are region-bound — use matching base URL

## Streaming

Set `"stream": true` in request. Response uses Server-Sent Events (SSE).

## Error Handling

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "invalid_request_error",
    "code": 401
  }
}
```
