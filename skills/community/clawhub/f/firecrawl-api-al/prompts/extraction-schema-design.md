# Prompt: Extraction Schema Design (scrape `json` format)

## Purpose
Design a tight JSON schema and extraction prompt for Firecrawl's `scrape` `json` format so structured extraction is accurate, typed, and stable across runs.

## Reusable prompt template
```
Design a JSON schema and extraction prompt for Firecrawl scrape (json format).

PAGE_TYPE: {{page_type}}
FIELDS_NEEDED: {{fields_list}}
LIST_OR_SINGLE: {{single_record | list_of_records}}

Rules:
- Include ONLY fields in FIELDS_NEEDED. No "nice to have" fields (they cost tokens/credits).
- Give every field an explicit JSON type (string, number, boolean, array, object).
- Use enums for closed sets; use format hints (e.g., ISO date) in descriptions.
- Mark truly-required fields in "required"; leave optional ones out of "required".
- For LIST pages, wrap items in an array property (e.g., "items": { type:array, items:{...} }).
- The extraction prompt must say: "If a field is not present on the page, omit it or set null. Never invent values."

Output:
1) extraction_prompt: <concise instruction string>
2) schema: <valid JSON Schema object>
3) validation_notes: <how to post-validate types and missing fields>
```

## Variables
| Variable | Meaning | Example |
|----------|---------|---------|
| `{{page_type}}` | Kind of page | "e-commerce product page" |
| `{{fields_list}}` | Exact fields to extract | "title, price (number), currency, inStock (boolean)" |
| `{{LIST_OR_SINGLE}}` | One record or many | "single_record" |

## Example use
Product page → fields title/price/currency/inStock → produce prompt + schema with `price` typed `number` and `inStock` typed `boolean`.

## Bad example
```json
{ "type": "object", "properties": { "info": { "type": "string" } } }
```
Prompt: "Extract everything useful."

Wrong: vague field, no types, no required, invites hallucination and unstable output.

## Good example
extraction_prompt: "Extract the product title, current price as a number, ISO currency code, and stock status. If a field is absent, set it to null; never guess."
```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "price": { "type": "number" },
    "currency": { "type": "string", "description": "ISO 4217 code, e.g. USD" },
    "inStock": { "type": "boolean" }
  },
  "required": ["title", "price"]
}
```
validation_notes: "Reject if price is a string; treat null required field as 'not found', not failure-to-extract."

> Verification needed: confirm exact json-format schema keys with https://docs.firecrawl.dev
