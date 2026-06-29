# Document OCR Agent Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `google-document-ai-ocr`

x402 availability: not enabled for this product.

## `process_document`

Action slug: `process-document`

Price: `20` credits

Extract text, entities, and structured data from a document using Google Document AI. Provide exactly one input source: file_urls, file_ids, or content_base64.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_base64` | `string` | no | Base64-encoded file content to process. |
| `document_type` | `string` | no | Document type. Use 'general' for plain OCR, or a specialized type to extract structured fields (dates, amounts, line items, etc). |
| `file_ids` | `array` | no | Cloud file ID(s) to process. One ID for a single file, or up to 10 image IDs to batch into a multi-page document. |
| `file_urls` | `array` | no | URL(s) to process. One URL for a single file, or up to 10 image URLs to batch into a multi-page document. |
| `include_entities` | `boolean` | no | Include extracted entities. |
| `include_pages` | `boolean` | no | Include per-page summary data. |
| `include_raw_document` | `boolean` | no | Include full raw Document AI response object. |
| `max_entities` | `integer` | no | Max extracted entities to return. |
| `max_text_chars` | `integer` | no | Max characters of extracted text to return. |
| `mime_type` | `string` | no | MIME type of the input (e.g. application/pdf, image/png). Auto-detected if omitted. |

Sample parameters:

```json
{
  "content_base64": "Draft marketing copy to check for banned phrases.",
  "document_type": "general",
  "file_ids": [
    "example file id"
  ],
  "file_urls": [
    "https://example.com"
  ],
  "include_entities": true,
  "include_pages": true,
  "include_raw_document": true,
  "max_entities": 200
}
```

Generated JSON parameter schema:

```json
{
  "content_base64": {
    "description": "Base64-encoded file content to process.",
    "required": false,
    "type": "string"
  },
  "document_type": {
    "default": "general",
    "description": "Document type. Use 'general' for plain OCR, or a specialized type to extract structured fields (dates, amounts, line items, etc).",
    "enum": [
      "general",
      "bank_statement",
      "expense",
      "invoice",
      "drivers_license",
      "passport",
      "utility",
      "w2",
      "w9"
    ],
    "required": false,
    "type": "string"
  },
  "file_ids": {
    "description": "Cloud file ID(s) to process. One ID for a single file, or up to 10 image IDs to batch into a multi-page document.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "file_urls": {
    "description": "URL(s) to process. One URL for a single file, or up to 10 image URLs to batch into a multi-page document.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "include_entities": {
    "default": true,
    "description": "Include extracted entities.",
    "required": false,
    "type": "boolean"
  },
  "include_pages": {
    "default": true,
    "description": "Include per-page summary data.",
    "required": false,
    "type": "boolean"
  },
  "include_raw_document": {
    "description": "Include full raw Document AI response object.",
    "required": false,
    "type": "boolean"
  },
  "max_entities": {
    "default": 200,
    "description": "Max extracted entities to return.",
    "maximum": 2000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "max_text_chars": {
    "default": 12000,
    "description": "Max characters of extracted text to return.",
    "maximum": 250000,
    "minimum": 200,
    "required": false,
    "type": "integer"
  },
  "mime_type": {
    "description": "MIME type of the input (e.g. application/pdf, image/png). Auto-detected if omitted.",
    "required": false,
    "type": "string"
  }
}
```
