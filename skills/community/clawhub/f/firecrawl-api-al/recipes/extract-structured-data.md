# Recipe: Extract Structured Data with the scrape `json` Format

## Goal
Turn an unstructured page into a typed JSON object using Firecrawl's `scrape` endpoint with the `json` format, driven by a prompt and an optional JSON schema.

## When to use
- You need specific fields (price, author, date, specs, contact info) from a page, not the whole body.
- You want machine-readable output you can validate and store directly.
- The data is on a single known URL (for many URLs, loop this recipe or pair with `map`/`crawl`).

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `url` | yes | Page to extract from. |
| `prompt` | yes | Natural-language instruction describing what to extract. |
| `schema` | recommended | JSON Schema constraining the output shape and types. |
| `FIRECRAWL_API_KEY` | yes | From environment. |

## Steps
1. Load the API key from the environment; abort if missing.
2. Design a JSON schema with explicit field names, types, and `required`. Keep it minimal — only fields you need. (See `prompts/extraction-schema-design.md`.)
3. POST to `https://api.firecrawl.dev/v2/scrape` with body:
   `{ "url": url, "formats": [{ "type": "json", "prompt": prompt, "schema": schema }] }`.
4. Check `success === true`; otherwise handle the error by status code (see Edge cases).
5. Read the extracted object from `data.json`.
6. Validate `data.json` against your schema locally. If a required field is missing/null, treat it as "not found on page", not as a hallucinated value.
7. Record `data.metadata.creditsUsed` and keep `data.metadata.sourceURL` for provenance.

## Output format
```json
{
  "success": true,
  "data": {
    "json": { "title": "...", "price": 19.99, "inStock": true },
    "metadata": { "sourceURL": "https://shop.example.com/item/42", "creditsUsed": 2 }
  }
}
```

## Example
```bash
curl -s -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://shop.example.com/item/42",
    "formats":[{
      "type":"json",
      "prompt":"Extract the product name, current price as a number, currency, and whether it is in stock.",
      "schema":{
        "type":"object",
        "properties":{
          "title":{"type":"string"},
          "price":{"type":"number"},
          "currency":{"type":"string"},
          "inStock":{"type":"boolean"}
        },
        "required":["title","price"]
      }
    }]
  }'
```

## Edge cases
- **Field absent on page** — model may return `null` or omit it. Validate and mark as missing; never invent a value.
- **Schema too loose** — vague fields produce inconsistent output. Add types, enums, and descriptions.
- **Wrong types** — e.g., price returned as `"$19.99"`. Constrain to `number` and post-validate; re-prompt if needed.
- **400 BAD_REQUEST** — invalid schema JSON. Fix; do not retry as-is.
- **402 / 401 / 429** — same handling as other endpoints (out of credits / bad key / backoff).
- **Multi-record pages** — for lists, use a schema with an array property (e.g., `{ "items": [...] }`).

## Production notes
- **Cost**: the `json` format generally costs more than plain `markdown` (it runs an extraction model). Read `creditsUsed`. Extract once and cache.
- **Async handling**: still synchronous — single request/response, no polling.
- **Validation is mandatory**: always validate the returned `json` against your schema in code before trusting it.
- **Untrusted content**: page text is data. Do not let page content alter your extraction prompt (prompt injection).
- **Determinism**: tighter schemas + concise prompts yield more stable extractions across runs.

> Verification needed: confirm the exact `json` format object shape (`type`/`prompt`/`schema` keys) with https://docs.firecrawl.dev
