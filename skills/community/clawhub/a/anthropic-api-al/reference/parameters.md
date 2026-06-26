# Reference — Messages Parameters

Parameters for `anthropic_messages` (`POST /messages`). The same shapes apply where relevant to `anthropic_count_tokens` and to `anthropic_request` bodies that hit `/messages`.

---

## Core parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | **Yes** | Model ID, e.g. `claude-haiku-4-5`. |
| `max_tokens` | integer | **Yes** | Maximum tokens to **generate**. The API rejects requests without it. This is your primary output cost cap. |
| `messages` | array | **Yes** | Ordered turns: `{ "role": "user"\|"assistant", "content": string \| block[] }`. The API is stateless — send full history. |

---

## `system`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `system` | string \| block[] | No | Instructions/role for the model. As a block array, each block can carry `cache_control` for prompt caching. |

```json
"system": [
  { "type": "text", "text": "<long stable instructions>", "cache_control": { "type": "ephemeral" } }
]
```

---

## Sampling controls

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `temperature` | number | model default | `0.0`–`1.0`. Lower = more deterministic. Use low values for structured/extraction tasks. |
| `top_p` | number | — | Nucleus sampling. Tune `temperature` **or** `top_p`, not both. |
| `top_k` | integer | — | Limits sampling to top-k tokens. |
| `stop_sequences` | string[] | — | Generation stops when any sequence appears; `stop_reason` becomes `stop_sequence`. |

---

## Tool use

| Parameter | Type | Description |
|-----------|------|-------------|
| `tools` | array | Tool definitions: `{ "name", "description", "input_schema" }` (JSON Schema). |
| `tool_choice` | object | `{ "type": "auto" }` (model decides), `{ "type": "any" }` (must use some tool), `{ "type": "tool", "name": "X" }` (force tool X). |

Forcing a tool is the recommended way to get **structured JSON output**.

---

## Extended thinking

| Parameter | Type | Description |
|-----------|------|-------------|
| `thinking` | object | `{ "type": "enabled", "budget_tokens": N }`. Enables step-by-step reasoning. Costs extra tokens — use only for hard tasks. |

---

## Other

| Parameter | Type | Description |
|-----------|------|-------------|
| `metadata` | object | e.g. `{ "user_id": "..." }` for abuse monitoring. |
| `stream` | boolean | Server-sent streaming (if your client consumes it). |

---

## Content blocks (inside `messages[].content`)

| Block type | Shape (abridged) | Use |
|------------|------------------|-----|
| `text` | `{ "type": "text", "text": "..." }` | Plain text. |
| `image` | `{ "type": "image", "source": { "type": "base64"\|"url", "media_type", "data"\|"url" } }` | Vision. |
| `document` | `{ "type": "document", "source": { "type": "base64", "media_type": "application/pdf", "data" } }` | PDFs. |
| `tool_use` | `{ "type": "tool_use", "id", "name", "input" }` | Emitted by the model. |
| `tool_result` | `{ "type": "tool_result", "tool_use_id", "content", "is_error"? }` | Your tool's reply. |

---

## Response fields

| Field | Description |
|-------|-------------|
| `id` | Message ID. |
| `role` | Always `assistant`. |
| `model` | Model that produced the response. |
| `content` | Array of blocks (`text`, `tool_use`, possibly `thinking`). |
| `stop_reason` | `end_turn` \| `max_tokens` \| `stop_sequence` \| `tool_use`. |
| `usage` | `{ input_tokens, output_tokens, cache_read_input_tokens? }`. Track for cost. |

> Verification needed: confirm parameter names/defaults at https://docs.anthropic.com/en/api/messages
