---
name: delete-file
description: "Delete a file from cloud storage by URL. Only the API key that uploaded the file can delete it."
---

# Delete File

## What It Does
Deletes a file from cloud storage by its URL. Verifies ownership — only the API key that uploaded the file can delete it.

## When to Use
- Remove files you no longer need
- Clean up storage before the 30-day auto-deletion

## Required Inputs
- `url` — the file URL returned by the upload endpoint

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Privacy Compliance** — Delete files immediately after processing to meet GDPR/privacy requirements
- **Storage Cleanup** — Remove files you no longer need before the 30-day auto-deletion
- **Workflow Cleanup** — Delete intermediate files after a multi-step pipeline completes
- **Sensitive Document Handling** — Immediately remove confidential documents after processing

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/file/delete \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://bucket.s3.amazonaws.com/pdf/abc123_my_report.pdf" }'
```

## Notes
- Returns 403 if the file doesn't belong to the requesting API key
