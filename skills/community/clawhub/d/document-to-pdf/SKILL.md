---
name: document-to-pdf
description: "Convert office documents (DOCX, DOC, PPT, PPTX, XLS, XLSX, CSV, TXT, ODT, RTF) to PDF via the PDFAPIHub cloud API. Documents are uploaded to pdfapihub.com for conversion. Requires a CLIENT-API-KEY."
---

# Document to PDF

## What It Does
Converts office documents to PDF via the PDFAPIHub hosted API. Your document is uploaded to PDFAPIHub servers for processing and the converted PDF is returned. Supports a wide range of input formats including Word, PowerPoint, Excel, and text files.

## When to Use
- Convert DOCX/DOC files to PDF
- Convert spreadsheets (XLS/XLSX/CSV) to PDF
- Convert presentations (PPT/PPTX) to PDF
- Convert plain text or RTF to PDF

## Supported Input Formats
`doc`, `docx`, `odt`, `rtf`, `txt`, `ppt`, `pptx`, `odp`, `xls`, `xlsx`, `ods`, `csv`

## Required Inputs
Provide one of:
- `url` — public URL to the document
- `file` — base64-encoded document (set `input_format` too)
- Multipart upload with `file` field

## Authentication
This skill calls the PDFAPIHub hosted API at `https://pdfapihub.com/api`. Your document is sent to PDFAPIHub servers for conversion.

Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

**Privacy note:** Documents you convert are uploaded to PDFAPIHub's cloud service. Do not send confidential documents unless you trust the service. Files are auto-deleted after 30 days.

## Use Cases
- **Document Standardization** — Convert uploaded DOCX/PPTX/XLSX files to PDF for consistent viewing
- **E-Signature Workflows** — Convert Word contracts to PDF before sending for signature
- **Archival** — Convert office documents to PDF/A for long-term storage
- **Email Attachments** — Convert spreadsheets or presentations to PDF before emailing
- **Publishing Pipelines** — Convert authored DOCX content to PDF for distribution
- **LMS Content** — Convert course materials (PPTX, DOCX) to PDF for student downloads

## Aliases
- `/v1/convert/document/pdf` is an alias for this endpoint

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/convert/docx/pdf \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://pdfapihub.com/sample.docx",
    "output": "url"
  }'
```
