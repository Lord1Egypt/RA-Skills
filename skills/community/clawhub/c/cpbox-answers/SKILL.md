---
name: answers
description: "USE FOR AI-grounded answers via OpenAI-compatible /chat/completions. Two modes: single-search (fast) or deep research (enable_research=true, thorough multi-search). Streaming/blocking. Citations."
---

# Answers — AI Grounding

Paid Answers proxy via **x402 pay-per-use** (HTTP 402).

> **Prerequisites**: This skill requires x402-payment. Complete the [setup steps](../../README.md#prerequisites) before first use.

## Service URLs

| Role | Domain |
|------|--------|
| **API Provider** | https://www.cpbox.io |
| **Facilitator** | https://www.cppay.finance |

## Endpoint (Agent Interface)

```http
POST /api/x402/answers
```

## Payment Flow (x402 Protocol)

1. **First request** (no `PAYMENT-SIGNATURE`) -> `402 Payment Required` with requirements JSON
2. **Client signs** (EIP-712) -> `PAYMENT-SIGNATURE`
3. **Retry** with `PAYMENT-SIGNATURE` -> Server settles and returns response

With `@springmint/x402-payment` or `x402-sdk-go`, payment is **automatic**.

## When to Use

| Use Case | Skill | Why |
|--|--|--|
| Quick factual answer (raw context) | `llm-context` | Single search, returns raw context for YOUR LLM |
| Fast AI answer with citations | **`answers`** (single-search) | streaming, citations |
| Thorough multi-search deep research | **`answers`** (research mode) | Iterative deep research, synthesized cited answer |

**This endpoint** (`/res/v1/chat/completions`) supports two modes:
- **Single-search** (default): Fast AI-grounded answer from a single search. Supports `enable_citations`.
- **Research** (`enable_research=true`): Multi-iteration deep research with progress events and synthesized cited answer.

## Quick Start (cURL)

### Blocking (Single-Search)
```bash
curl -X POST "https://www.cpbox.io/api/x402/answers" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "How does the James Webb Space Telescope work?"}],
    "model": "default",
    "stream": false
  }'
```

### Streaming with Citations (Single-Search)
```bash
curl -X POST "https://www.cpbox.io/api/x402/answers" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What are recent breakthroughs in fusion energy?"}],
    "model": "default",
    "stream": true,
    "enable_citations": true
  }'
```

### Research Mode
```bash
curl -X POST "https://www.cpbox.io/api/x402/answers" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Compare quantum computing approaches"}],
    "model": "default",
    "stream": true,
    "enable_research": true,
    "research_maximum_number_of_iterations": 3,
    "research_maximum_number_of_seconds": 120
  }'
```

## Using with x402-payment

### CLI (AI Agent)

```bash
npx @springmint/x402-payment \
  --url https://www.cpbox.io/api/x402/answers \
  --method POST \
  --input '{"messages":[{"role":"user","content":"How does the James Webb Space Telescope work?"}],"model":"default","stream":false}'
```

## Payload/Response

OpenAI-compatible `chat.completions` JSON + SSE streaming (pass-through).

## Two Modes

| Feature | Single-Search (default) | Research (`enable_research=true`) |
|--|--|--|
| Speed | Fast | Slow |
| Searches | 1 | Multiple (iterative) |
| Streaming | Optional (`stream=true/false`) | **Required** (`stream=true`) |
| Citations | `enable_citations=true` (streaming only) | Built-in (in `<answer>` tag) |
| Progress events | No | Yes (`<progress>` tags) |
| Blocking response | Yes (`stream=false`) | No |

## Parameters

### Standard Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `messages` | array | **Yes** | - | Single user message (exactly 1 message) |
| `model` | string | **Yes** | - | Use `"default"` |
| `stream` | bool | No | true | Enable SSE streaming |
| `country` | string | No | "US" | Search country (2-letter country code or `ALL`) |
| `language` | string | No | "en" | Response language |
| `safesearch` | string | No | "moderate" | Search safety level (`off`, `moderate`, `strict`) |
| `max_completion_tokens` | int | No | null | Upper bound on completion tokens |
| `enable_citations` | bool | No | false | Include inline citation tags (single-search streaming only) |
| `web_search_options` | object | No | null | OpenAI-compatible; `search_context_size`: `low`, `medium`, `high` |

### Research Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `enable_research` | bool | No | `false` | **Enable research mode** |
| `research_allow_thinking` | bool | No | `true` | Enable extended thinking |
| `research_maximum_number_of_tokens_per_query` | int | No | `8192` | Max tokens per query (1024-16384) |
| `research_maximum_number_of_queries` | int | No | `20` | Max total search queries (1-50) |
| `research_maximum_number_of_iterations` | int | No | `4` | Max research iterations (1-5) |
| `research_maximum_number_of_seconds` | int | No | `180` | Time budget in seconds (1-300) |
| `research_maximum_number_of_results_per_query` | int | No | `60` | Results per search query (1-60) |

### Constraints (IMPORTANT)

| Constraint | Error |
|--|--|
| `enable_research=true` requires `stream=true` | "Blocking response doesn't support 'enable_research' option" |
| `enable_research=true` incompatible with `enable_citations=true` | "Research mode doesn't support 'enable_citations' option" |
| `enable_citations=true` requires `stream=true` | "Blocking response doesn't support 'enable_citations' option" |

## Notes for Agent Usage

- Use `x402-payment` to handle the payment handshake automatically, especially for streaming (`stream=true`).

## Response Format

### Blocking Response (`stream=false`, single-search only)

Standard OpenAI-compatible JSON:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "choices": [{"message": {"role": "assistant", "content": "The James Webb Space Telescope works by..."}, "index": 0, "finish_reason": "stop"}],
  "usage": {"prompt_tokens": 10, "completion_tokens": 50, "total_tokens": 60}
}
```

### Streaming Response

SSE response with OpenAI-compatible chunks:

```text
data: {"id":"chatcmpl-...","object":"chat.completion.chunk","choices":[{"delta":{"content":"Based on"},"index":0}]}

data: {"id":"chatcmpl-...","object":"chat.completion.chunk","choices":[{"delta":{"content":" recent research"},"index":0}]}

data: [DONE]
```

### Streaming Tags by Mode

#### Single-Search (with `enable_citations=true`)

| Tag | Purpose |
|--|--|
| `<citation>` | Inline citation references |
| `<usage>` | JSON cost/billing data |

#### Research Mode

| Tag | Purpose | Keep? |
|--|--|--|
| `<queries>` | Generated search queries | Debug |
| `<analyzing>` | URL counts (verbose) | Debug |
| `<thinking>` | URL selection reasoning | Debug |
| `<progress>` | Stats: time, iterations, queries, URLs analyzed, tokens | Monitor |
| `<blindspots>` | Knowledge gaps identified | **Yes** |
| `<answer>` | Final synthesized answer (only the final answer is emitted; intermediate drafts are dropped) | **Yes** |
| `<usage>` | JSON cost/billing data (included at end of streaming response) | **Yes** |

### Usage Tag Format

The `<usage>` tag contains JSON-stringified cost and token data:

```text
<usage>{"X-Request-Requests":1,"X-Request-Queries":8,"X-Request-Tokens-In":15000,"X-Request-Tokens-Out":2000,"X-Request-Requests-Cost":0.005,"X-Request-Queries-Cost":0.032,"X-Request-Tokens-In-Cost":0.075,"X-Request-Tokens-Out-Cost":0.01,"X-Request-Total-Cost":0.122}</usage>
```

## Use Cases

- **Chat interface integration**: Use this endpoint to get a web-grounded answer payload in OpenAI-compatible format.
- **Deep research / comprehensive topic research**: Use research mode (`enable_research=true`) for complex questions needing multi-source synthesis (e.g., "Compare approaches to nuclear fusion").
- **OpenAI SDK drop-in**: Same SDK, same streaming format — just change `base_url` and `api_key`. Works with both sync and async clients.
- **Cited answers**: Enable `enable_citations=true` in single-search mode for inline citation tags, or use research mode which automatically includes citations in its answer.

## Notes

- **Timeout**: Set client timeout to at least 30s for single-search, 300s (5 min) for research
- **Single message**: The `messages` array must contain exactly 1 user message
- **Cost monitoring**: Parse the `<usage>` tag from streaming responses to track costs
