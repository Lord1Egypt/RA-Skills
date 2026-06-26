# DeepEvidence API Reference

Complete API specification for the DeepEvidence OpenAI-compatible interface.

**Base URL**: `https://deepevid.medsci.cn/`

---

## Table of Contents

- [Authentication](#authentication)
- [Chat Completions](#chat-completions)
- [Conversations (Extension)](#conversations-extension)
- [Error Handling](#error-handling)
- [Rate Limits & Quotas](#rate-limits--quotas)

---

## Authentication

All requests require Bearer Token authentication:

```
Authorization: Bearer sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

Contact your administrator to obtain an API key.

### User Mapping

Two methods for identifying end users (for multi-tenant scenarios):

**Method 1 — Request body `user` parameter (recommended)**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | string | External user ID (from third-party system) |
| `metadata.user_name` | string | Display name (optional) |
| `metadata.user_email` | string | Email (optional) |
| `metadata.user_metadata` | object | Additional user metadata (optional) |

**Method 2 — HTTP Headers**:

| Header | Description |
|--------|-------------|
| `X-User-ID` | External user ID (required for mapping) |
| `X-User-Name` | Username (optional) |
| `X-User-Email` | Email (optional) |
| `X-User-Avatar` | Avatar URL (optional) |

> If both `user` param and `X-User-ID` header are provided, `user` param takes precedence.

---

## Chat Completions

### POST /v1/chat/completions

Create a chat completion with the medical AI assistant.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | No | Model ID, default `deepevidence-agent-v1` (fixed value) |
| `messages` | array | Yes | Array of message objects |
| `stream` | boolean | No | Stream response, default `false` |
| `user` | string | No | External user ID |
| `metadata` | object | No | Extension metadata |
| `metadata.conversation_id` | string | No | Continue existing conversation |
| `metadata.project_id` | string | No | Associate with a project |
| `metadata.locale` | string | No | Language preference (`en`, `zh-CN`) |
| `metadata.user_name` | string | No | Username (with `user`) |
| `metadata.user_email` | string | No | Email (with `user`) |
| `metadata.user_metadata` | object | No | Additional user metadata |

**Message format**:

```json
{
  "role": "user" | "assistant" | "system",
  "content": "message content"
}
```

### Non-Streaming Response

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1705123456,
  "model": "deepevidence-agent-v1",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Diabetes symptoms include..."},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 120,
    "total_tokens": 135
  },
  "metadata": {
    "conversation_id": "abc123def"
  }
}
```

---

## Conversations (Extension)

> These are DeepEvidence extension APIs, NOT part of the OpenAI standard.

### GET /v1/conversations

List conversations.

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | number | Max results, default 20, max 100 |
| `offset` | number | Pagination offset, default 0 |
| `q` | string | Search keyword |

**Response**:

```json
{
  "object": "list",
  "data": [
    {
      "id": "abc123",
      "object": "conversation",
      "title": "Diabetes symptoms",
      "created_at": 1705123456,
      "is_favorited": false,
      "project_id": null
    }
  ],
  "has_more": false,
  "offset": 0,
  "limit": 10
}
```

### GET /v1/conversations/:id

Get conversation detail including messages.

**Response** includes a `messages` array with all conversation messages.

### DELETE /v1/conversations/:id

Delete a conversation.

**Response**:

```json
{
  "id": "abc123",
  "object": "conversation.deleted",
  "deleted": true
}
```

---

## Error Handling

All errors follow OpenAI standard format:

```json
{
  "error": {
    "message": "Error description",
    "type": "error_type",
    "param": null,
    "code": "error_code"
  }
}
```

### Error Types

| Type | HTTP Status | Description | Suggested Action |
|------|-------------|-------------|-----------------|
| `authentication_error` | 401 | Invalid or missing API key | Check `DEEPEVIDENCE_API_KEY` |
| `permission_error` | 403 | Insufficient permissions | Contact admin for access |
| `invalid_request_error` | 400 | Invalid request parameters | Check request body format |
| `not_found_error` | 404 | Resource not found | Verify conversation/model ID |
| `rate_limit_error` | 429 | Too many requests or quota exhausted | Reduce request frequency or contact admin |
| `server_error` | 500 | Internal server error | Retry after a moment |

---

## Rate Limits & Quotas

Quotas are dynamically configured per API key by administrators:

- **Daily quota**: Maximum requests per day
- **Rate limit**: Maximum requests per minute/second
- **Token limit**: Maximum tokens per single request

Contact your administrator for specific quota details.
