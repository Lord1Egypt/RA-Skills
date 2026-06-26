---
name: azure-content-layout
description: Extract document structure, text, tables, and figures from documents using Azure Content Understanding prebuilt-layout analyzer. Converts PDF, images, Office docs into Markdown and structured JSON. Use when asked to extract text from documents, convert PDF/images to markdown, perform OCR, analyze document layout, or extract tables from files. Requires AZURE_CU_ENDPOINT and AZURE_CU_API_KEY environment variables.
metadata:
  openclaw:
    requires:
      env:
        - AZURE_CU_ENDPOINT
        - AZURE_CU_API_KEY
        - AZURE_CU_API_VERSION
    primaryEnv: AZURE_CU_API_KEY
---

# Azure Content Understanding — Layout Analyzer

Extract structured content from documents using Azure's prebuilt-layout analyzer. Outputs Markdown and structured JSON with text, tables, figures, and document hierarchy.

## Setup

Set environment variables:

```bash
export AZURE_CU_ENDPOINT="https://YOUR_RESOURCE.services.ai.azure.com/"
export AZURE_CU_API_KEY="YOUR_KEY_HERE"
```

Optional: set API version (defaults to `2025-05-01-preview`):
```bash
export AZURE_CU_API_VERSION="2025-11-01"
```

## Quick Usage

### Analyze a URL and print Markdown

```bash
node scripts/analyze.mjs --url "https://example.com/document.pdf"
```

### Analyze a local file (pipe via stdin)

```bash
cat invoice.pdf | node scripts/analyze.mjs --stdin --markdown output.md --output result.json
```

### Save both Markdown and full JSON

```bash
node scripts/analyze.mjs --url "https://example.com/report.pdf" \
  --markdown report.md \
  --output report.json
```

## Direct API Call

When the script isn't available, use curl:

```bash
# Submit analysis (preview API)
curl -s -X POST "$AZURE_CU_ENDPOINT/contentunderstanding/analyzers/prebuilt-layout:analyze?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: $AZURE_CU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/doc.pdf"}'

# Response includes Operation-Location header — poll that URL for results
```

For GA API (2025-11-01), the body format changes:
```json
{"inputs": [{"url": "https://example.com/doc.pdf"}]}
```

## Output

### Markdown
The analyzer produces GitHub Flavored Markdown preserving:
- **Headings** (h1–h6)
- **Tables** (as HTML `<table>` blocks)
- **Selection marks** (☒ checked, ☐ unchecked)
- **Figures** (with references)
- **Paragraphs** with reading order

### Structured JSON
The full result includes detailed per-element data:
- `pages` — dimensions, word/line counts per page
- `paragraphs` — text blocks with bounding regions and semantic roles
- `tables` — cells with row/column spans
- `figures` — detected images/charts with bounding regions
- `sections` — hierarchical document structure

## Supported Formats

PDF, JPEG, PNG, BMP, TIFF, HEIF, DOCX, XLSX, PPTX, HTML

## Best Practices

- **Async operation** — the API returns 202; poll `Operation-Location` for results
- **Poll interval** — 3 seconds is reasonable; results typically arrive in 5–60 seconds
- **Large documents** — up to 2,000 pages supported; processing time scales linearly
- **File upload** — use `Content-Type: application/octet-stream` with binary body
- **Tables** — rendered as HTML in markdown for complex layouts (merged cells, etc.)

## API Reference

See [references/api.md](references/api.md) for full request/response details.
