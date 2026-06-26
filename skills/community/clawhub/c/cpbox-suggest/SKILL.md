---
name: suggest
description: USE FOR query autocomplete/suggestions. Fast (<100ms). Returns suggested queries as user types. Supports rich suggestions with entity info. Typo-resilient.
version: 1.0.0
---

# Suggest / Autocomplete

Paid Suggest proxy via **x402 pay-per-use** (HTTP 402).

> **Prerequisites**: This skill requires x402-payment. Complete the [setup steps](https://github.com/springmint/cpbox-skills#prerequisites) before first use.
>
> **Security**: Documentation only — no executable code or credentials. Wallet/keys stay on your machine; never stored here.

## Service URLs

| Role | Domain |
|------|--------|
| **API Provider** | https://www.cpbox.io |
| **Facilitator** | https://www.cppay.finance |

## Endpoint (Agent Interface)

```http
GET /api/x402/suggest
```

## Payment Flow (x402 Protocol)

1. **First request** -> `402 Payment Required` with requirements JSON
2. **Sign & retry** with `PAYMENT-SIGNATURE` -> result JSON

With `@springmint/x402-payment` or `x402-sdk-go`, payment is **automatic**.

## Quick Start (cURL)

### Basic Suggestions
```bash
curl -s "https://www.cpbox.io/api/x402/suggest?q=how+to+" \
  -H "Accept: application/json"
```

### With All Parameters
```bash
curl -s "https://www.cpbox.io/api/x402/suggest" \
  -H "Accept: application/json" \
  -G \
  --data-urlencode "q=albert" \
  --data-urlencode "country=US" \
  --data-urlencode "lang=en" \
  --data-urlencode "count=10" \
  --data-urlencode "rich=true"
```

## Using with x402-payment

```bash
npx @springmint/x402-payment \
  --url "https://www.cpbox.io/api/x402/suggest?q=albert&rich=true&count=10" \
  --method GET
```

**Optional Headers**:
- `Accept-Encoding: gzip` — Enable response compression

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `q` | string | **Yes** | — | Suggest search query (1-400 chars, max 50 words) |
| `lang` | string | No | `en` | Language preference (2+ char language code, e.g. `fr`, `de`, `zh-hans`) |
| `country` | string | No | `US` | Search country (2-letter country code or `ALL`) |
| `count` | int | No | `5` | Number of suggestions (1-20). Actual results may be fewer |
| `rich` | bool | No | `false` | Enhance with entity info (title, description, image). Paid Search plan required |

## Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"suggest"` |
| `query.original` | string | The original suggest search query |
| `results` | array | List of suggestions (may be empty) |
| `results[].query` | string | Suggested query completion |
| `results[].is_entity` | bool? | Whether the suggested enriched query is an entity (rich only) |
| `results[].title` | string? | The suggested query enriched title (rich only) |
| `results[].description` | string? | The suggested query enriched description (rich only) |
| `results[].img` | string? | The suggested query enriched image URL (rich only) |

Fields with `null` values are excluded from the response. Non-rich results contain only the `query` field.

### Rich Response Example (`rich=true`)
```json
{
  "type": "suggest",
  "query": { "original": "albert" },
  "results": [
    {
      "query": "albert einstein",
      "is_entity": true,
      "title": "Albert Einstein",
      "description": "German-born theoretical physicist",
      "img": "https://imgs.search.provider/..."
    },
    { "query": "albert einstein quotes", "is_entity": false }
  ]
}
```

## Use Cases

- **Search-as-you-type UI**: Real-time autocomplete dropdown. Debounce 150-300ms.
- **Query refinement for RAG**: Expand partial/ambiguous queries before calling `web-search` or `llm-context`.
- **Entity detection**: Use `rich=true` to detect entities with title, description, and image for preview cards.
- **Typo-tolerant input**: Get clean suggestions from misspelled input without separate spellcheck.

## Notes

- **Latency**: Designed for <100ms response times
- **Country/lang**: Hints for suggestion relevance, not strict filters
- **Typo handling**: Suggestions handle common typos without separate spellcheck
