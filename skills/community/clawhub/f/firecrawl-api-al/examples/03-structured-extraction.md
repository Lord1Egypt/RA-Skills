# Example 03 — Structured Field Extraction with a JSON Schema

## User request

> "From this product page, give me the product name, current price, currency, whether it's in stock, and the average star rating as clean JSON: https://shop.example/products/widget-pro"

## Agent reasoning summary

- User wants specific typed fields, not prose → use scrape's `json` format with an explicit schema so the model fills known keys.
- A schema constrains types and prevents extra/hallucinated fields; pair it with a short prompt for disambiguation.
- After extraction I validate the returned object against the schema before trusting it.

## Firecrawl operation to use

`scrape` (synchronous) with the `json` format object: `{ "type": "json", "prompt": "...", "schema": {...} }`. This runs LLM extraction over the scraped page and returns `data.json` conforming to the schema. Cost: JSON extraction costs more credits than a plain markdown scrape (LLM work); the exact amount is reported in `metadata.creditsUsed`. Synchronous — no polling.

## Request shape

```json
POST https://api.firecrawl.dev/v2/scrape
Authorization: Bearer $FIRECRAWL_API_KEY

{
  "url": "https://shop.example/products/widget-pro",
  "formats": [
    {
      "type": "json",
      "prompt": "Extract the product's commercial details. Use the displayed selling price (not the crossed-out list price). If a field is absent, return null.",
      "schema": {
        "type": "object",
        "properties": {
          "name":        { "type": "string" },
          "price":       { "type": "number" },
          "currency":    { "type": "string", "description": "ISO 4217 code, e.g. USD" },
          "inStock":     { "type": "boolean" },
          "avgRating":   { "type": ["number", "null"], "minimum": 0, "maximum": 5 }
        },
        "required": ["name", "price", "currency", "inStock"]
      }
    }
  ],
  "onlyMainContent": true
}
```

Including `markdown` alongside the `json` format is optional but useful for spot-checking the extraction against source text.

## Response handling

```json
{
  "success": true,
  "data": {
    "json": {
      "name": "Widget Pro",
      "price": 49.99,
      "currency": "USD",
      "inStock": true,
      "avgRating": 4.6
    },
    "metadata": {
      "sourceURL": "https://shop.example/products/widget-pro",
      "statusCode": 200,
      "creditsUsed": 5
    }
  }
}
```

Validation steps (do not skip):
1. `success === true` and `statusCode` 2xx, else error-handle.
2. `data.json` exists and is an object.
3. All `required` keys present and correctly typed (`price` is a `number`, not `"49.99"`; `inStock` is a real boolean).
4. Range checks: `avgRating` within 0–5; `currency` looks like a 3-letter code.
5. If validation fails, retry once with a sharper `prompt` (e.g. clarify which price element to read); if it fails again, return the partial object and flag the bad field rather than inventing a value.

## Citation behavior

Cite `data.metadata.sourceURL` as the provenance of the extracted record. Structured output still needs a source — the JSON is a claim about that page.

## Final answer pattern

```json
{
  "name": "Widget Pro",
  "price": 49.99,
  "currency": "USD",
  "inStock": true,
  "avgRating": 4.6,
  "_source": "https://shop.example/products/widget-pro"
}
```

> Extracted via Firecrawl scrape (json schema), 5 credits. Source: https://shop.example/products/widget-pro

## Common failure mode

Trusting `data.json` as-is. Common defects: `price` returned as a string `"49.99"`, the crossed-out list price captured instead of the sale price, `avgRating` hallucinated as `5` when the page shows no reviews (should be `null`), or extra keys the schema didn't ask for.

## Improved version

- Make the schema strict: declare `required`, use precise types (allow `null` only where it's legitimate), and add `minimum`/`maximum`/`description` hints.
- Validate the response object against the schema in code before returning it.
- Use the `prompt` to resolve ambiguity ("displayed selling price, not list price").
- On validation failure, retry once with a refined prompt, then degrade gracefully:

```json
{ "name": "Widget Pro", "price": 49.99, "currency": "USD", "inStock": true,
  "avgRating": null, "_warning": "No rating found on page; avgRating set to null." }
```

This guarantees typed, schema-conformant output and never fabricates a missing field.
