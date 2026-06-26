---
name: generate-pdf
description: "Generate a PDF document from HTML content or a public URL. Supports custom page sizes, fonts, margins, viewport dimensions, dynamic parameter substitution, and multiple output formats."
---

# Generate PDF

## What It Does
Generates a PDF document from either raw HTML content or a public URL using a headless Chromium browser. The API renders the page and returns the result as a downloadable URL, base64 string, or raw PDF file.

## When to Use
- Convert an HTML template (invoice, report, certificate) into a PDF
- Take a PDF snapshot of a live webpage
- Generate PDFs with dynamic data via placeholder substitution
- Create PDFs with custom fonts, margins, and page sizes

## Required Inputs
You must provide **one** of:
- `html_content` — raw HTML string to render
- `url` — a public URL to convert

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Invoice Generation** — Generate branded PDF invoices from HTML templates with dynamic customer data
- **Report Export** — Convert dashboard or analytics HTML pages into downloadable PDF reports
- **Certificate Creation** — Produce personalized certificates or diplomas with dynamic name/date substitution
- **Contract Generation** — Create contracts from templates with client-specific details filled in
- **Resume/CV Export** — Convert styled HTML resumes to PDF for download
- **Receipt Generation** — Auto-generate PDF receipts for e-commerce transactions
- **Webpage Archival** — Save a snapshot of any public webpage as a PDF for records

## Key Options
| Parameter | Description |
|-----------|-------------|
| `output_format` | `url` (default), `base64`, `file`/`pdf`/`binary` |
| `paper_size` | A4, A3, A5, Letter, Legal, Tabloid |
| `landscape` | `true` for landscape orientation |
| `margin` | Object with `top`, `right`, `bottom`, `left` (e.g. `"10mm"`) |
| `font` | Google Font names, pipe-separated |
| `dynamic_params` | Key-value object for `{{placeholder}}` replacement |
| `wait_till` | Seconds to wait before rendering (for JS-heavy pages) |

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/generatePdf \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "html_content": "<html><body><h1>Invoice #{{invoice_id}}</h1><p>Total: {{total}}</p></body></html>",
    "css_content": "body { font-family: Arial; }",
    "dynamic_params": { "invoice_id": "INV-001", "total": "$1,249.00" },
    "paper_size": "A4",
    "output_format": "url"
  }'
```

## Notes
- Boolean fields accept string values: `"true"`, `"1"`, `"yes"`, `"on"`
- Files are automatically deleted after 30 days
- Page count limits are tier-dependent
