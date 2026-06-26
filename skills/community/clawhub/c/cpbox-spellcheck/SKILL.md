---
name: spellcheck
description: USE FOR spell correction. Returns corrected query if misspelled. Most search endpoints have spellcheck built-in; use this only for pre-search query cleanup or "Did you mean?" UI.
version: 1.0.0
---

# Spellcheck

Paid Spellcheck proxy via **x402 pay-per-use** (HTTP 402).

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
GET /api/x402/spellcheck
```

## Payment Flow (x402 Protocol)

1. **First request** -> `402 Payment Required` with requirements JSON
2. **Sign & retry** with `PAYMENT-SIGNATURE` -> result JSON

With `@springmint/x402-payment` or `x402-sdk-go`, payment is **automatic**.

## Quick Start (cURL)

```bash
curl -s "https://www.cpbox.io/api/x402/spellcheck" \
  -H "Accept: application/json" \
  -G \
  --data-urlencode "q=artifical inteligence" \
  --data-urlencode "lang=en" \
  --data-urlencode "country=US"
```

## Using with x402-payment

```bash
npx @springmint/x402-payment \
  --url "https://www.cpbox.io/api/x402/spellcheck?q=artifical%20inteligence&lang=en&country=US" \
  --method GET
```

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `q` | string | **Yes** | — | Query to spell check (1-400 chars, max 50 words) |
| `lang` | string | No | `en` | Language preference (2+ char language code, e.g. `en`, `fr`, `de`, `pt-br`, `zh-hans`). 51 codes supported |
| `country` | string | No | `US` | Search country (2-letter country code or `ALL`) |

## Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"spellcheck"` |
| `query.original` | string | The input query as submitted |
| `results` | array | Spell-corrected suggestions. May be empty when no correction is found |
| `results[].query` | string | A corrected version of the query |

## Example Response

```json
{
  "type": "spellcheck",
  "query": {
    "original": "artifical inteligence"
  },
  "results": [
    {
      "query": "artificial intelligence"
    }
  ]
}
```

## Use Cases

- **Pre-search query cleanup**: Check spelling before deciding which search endpoint to call
- **"Did you mean?" UI**: Show users a corrected suggestion before running the search
- **Batch query normalization**: Clean up user inputs in bulk

## Notes

- **Built-in alternative**: Web Search and LLM Context have `spellcheck=true` by default — use this standalone endpoint only when you need the correction before searching
- **Context-aware**: Corrections consider the full query context, not just individual words
