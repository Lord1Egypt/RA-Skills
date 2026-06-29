---
name: document-ocr-agent
description: "Document OCR Agent: OCR and document intelligence tool. Send any PDF, image, or scanned document and receive extracted text, structured entities (dates, amounts, names, addresses, line items), and per-page metadata. Use when an agent needs document ocr agent, google document ai ocr, receipt ocr and text extraction, invoice parsing and field extraction, pdf document text extraction, scanned image ocr, process document, document type through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/google-document-ai-ocr
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/google-document-ai-ocr"}}
---
# Document OCR Agent

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Hire the OCR AI model to extract text, structured entities, and page-level data from scanned documents, receipts, invoices, PDFs, and image. Supports OCR text extraction from photos of receipts, handwritten notes, printed forms, business cards, shipping labels, contracts, and any document type. Identifies structured fields like dates, amounts, addresses, line items, tax totals, vendor names, and more. Accepts input via base64 content, public URL, or AgentPMT file storage ID. Ideal for expense tracking, invoice processing, receipt scanning, document digitization, data entry automation, bookkeeping ingestion, form parsing, and archival workflows.

## Product Instructions
### Google Document AI OCR

Extract text, entities, and structured data from PDFs, receipts, invoices, and images using Google Document AI. No credentials or project IDs needed -- the tool uses a backend service account automatically.

#### Overview

This tool processes documents through Google Document AI with specialized processors for different document types. Provide a file via URL, cloud file ID, or base64-encoded content, and receive extracted text, structured entities (dates, amounts, names, line items), and per-page statistics. Multiple images can be batched into a single multi-page document for processing.

#### Actions

##### process_document

Extract text and structured data from a document.

**Required parameters (exactly one of):**
- `file_urls` (array of strings) -- URL(s) to process. One URL for a single file, or up to 10 image URLs to batch into a multi-page document.
- `file_ids` (array of strings) -- Cloud file ID(s) to process. One ID for a single file, or up to 10 image IDs to batch into a multi-page document.
- `content_base64` (string) -- Base64-encoded file content to process (single file only).

**Optional parameters:**
- `document_type` (string, default: `"general"`) -- Selects the specialized processor. Options: `general`, `bank_statement`, `expense`, `invoice`, `drivers_license`, `passport`, `utility`, `w2`, `w9`.
- `mime_type` (string) -- MIME type of the input (e.g., `application/pdf`, `image/png`). Auto-detected from URL headers if omitted; defaults to `application/pdf` when unresolvable.
- `max_text_chars` (integer, default: 12000, min: 200, max: 250000) -- Max characters of extracted text to return.
- `max_entities` (integer, default: 200, min: 1, max: 2000) -- Max extracted entities to return.
- `include_pages` (boolean, default: true) -- Include per-page summary data (page dimensions, token/line/paragraph/block/table/form field counts).
- `include_entities` (boolean, default: true) -- Include extracted entities (type, mention text, confidence, normalized value).
- `include_raw_document` (boolean, default: false) -- Include the full raw Document AI response object.

###### Document Types

| `document_type` | Best for | Extracts |
|---|---|---|
| `general` (default) | Any document or image | Raw OCR text only |
| `bank_statement` | Bank statements | Transactions, balances, dates, account info |
| `expense` | Receipts, expense reports | Line items, totals, tax, vendor, date |
| `invoice` | Invoices | Line items, amounts, due dates, vendor, PO numbers |
| `drivers_license` | US driver's licenses | Name, DOB, address, license number, expiry |
| `passport` | US passports | Name, DOB, nationality, passport number, expiry |
| `utility` | Utility bills | Account number, billing period, charges, usage |
| `w2` | W-2 tax forms | Employer info, wages, tax withheld, SSN |
| `w9` | W-9 tax forms | Name, business name, TIN, address, tax classification |

###### Example: Basic OCR from URL

```json
{
  "action": "process_document",
  "file_urls": ["https://example.com/document.pdf"]
}
```

###### Example: Receipt with structured extraction

```json
{
  "action": "process_document",
  "document_type": "expense",
  "file_urls": ["https://example.com/receipt.jpg"]
}
```

###### Example: Invoice from base64

```json
{
  "action": "process_document",
  "document_type": "invoice",
  "content_base64": "JVBERi0xLjQK...",
  "mime_type": "application/pdf"
}
```

###### Example: Batch multiple images into one document

```json
{
  "action": "process_document",
  "file_urls": [
    "https://example.com/page1.jpg",
    "https://example.com/page2.jpg",
    "https://example.com/page3.jpg"
  ]
}
```

###### Example: Process from cloud file ID with limited output

```json
{
  "action": "process_document",
  "document_type": "w2",
  "file_ids": ["abc123"],
  "max_text_chars": 50000,
  "include_pages": false
}
```

###### Example: Get full raw response

```json
{
  "action": "process_document",
  "file_ids": ["abc123"],
  "include_raw_document": true
}
```

#### Workflows

##### Extract text from a scanned document
1. Call `process_document` with `file_urls` pointing to the scanned PDF or image.
2. Read `result.text_excerpt` for the extracted text content.

##### Parse a receipt for expense reporting
1. Call `process_document` with `document_type: "expense"` and the receipt file.
2. Read `result.entities` for structured line items, totals, tax, vendor, and date.

##### Process a multi-page document from images
1. Provide up to 10 image URLs in `file_urls`.
2. The images are fetched in parallel, combined into a single multi-page PDF, and processed as one document.
3. Use `include_pages: true` to get per-page statistics.

##### Extract data from tax forms
1. Use `document_type: "w2"` or `"w9"` with the tax form file.
2. Entities will include employer info, wages, tax withheld, TIN, etc.

#### Notes

- **Supported file types:** PDF, PNG, JPEG, TIFF, GIF, BMP, WebP.
- **Maximum input file size:** 20 MB (including combined PDF in batch mode).
- **Maximum pages:** 10 pages per PDF, or 10 images in batch mode.
- **Input source:** Exactly one of `file_urls`, `file_ids`, or `content_base64` must be provided. Providing multiple sources returns an error.
- **Batch mode:** When 2+ URLs or file IDs are provided, all images are downloaded in parallel, combined into a single multi-page PDF (one image per page), and sent to Document AI as one request.
- **MIME type auto-detection:** When `mime_type` is omitted, it is inferred from URL response headers or file metadata. Falls back to `application/pdf` if unresolvable.
- **Text truncation:** Extracted text is truncated to `max_text_chars` characters. Increase this value for long documents.
- **Entity truncation:** Entities are truncated to `max_entities`. Increase for documents with many structured fields.

## When To Use
- Use this skill for `Document OCR Agent` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: document ocr agent, google document ai ocr, receipt ocr and text extraction, invoice parsing and field extraction, pdf document text extraction, scanned image ocr, process document, document type.
- Supported action names: `process_document`.

## Use Cases
- Receipt OCR and text extraction
- Invoice parsing and field extraction
- PDF document text extraction
- Scanned image OCR
- Handwritten note digitization
- Business card scanning
- Expense report data capture
- Automated bookkeeping ingestion
- Contract and legal document text extraction
- Shipping label and barcode text reading
- Tax form field extraction
- Medical record digitization
- Insurance claim document processing
- Bank statement parsing
- Purchase order data extraction
- Form field recognition

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)
- File Storage - Over 10MB: ../file-storage-over-10mb (ClawHub: `file-storage-over-10mb`, page: https://clawhub.ai/agentpmt/file-storage-over-10mb; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-over-10mb`)
- File Storage - 10MB or less: ../file-storage-10mb-or-less (ClawHub: `file-storage-10mb-or-less`, page: https://clawhub.ai/agentpmt/file-storage-10mb-or-less; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-10mb-or-less`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `process_document` (action slug: `process-document`): Extract text, entities, and structured data from a document using Google Document AI. Provide exactly one input source: file_urls, file_ids, or content_base64. Price: `20` credits. Parameters: `content_base64`, `document_type`, `file_ids`, `file_urls`, `include_entities`, `include_pages`, `include_raw_document`, `max_entities`, plus 2 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "google-document-ai-ocr"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "google-document-ai-ocr"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "google-document-ai-ocr"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "google-document-ai-ocr"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "google-document-ai-ocr"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "google-document-ai-ocr"
  }
}
```

## Call This Tool
Product slug: `google-document-ai-ocr`

Marketplace page: https://www.agentpmt.com/marketplace/google-document-ai-ocr

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Document-OCR-Agent",
    "arguments": {
      "action": "process_document",
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
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "google-document-ai-ocr",
  "parameters": {
    "action": "process_document",
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
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `process_document` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/google-document-ai-ocr
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
