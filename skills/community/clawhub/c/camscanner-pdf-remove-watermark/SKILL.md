---
name: camscanner-pdf-remove-watermark
description: Use CamScanner to remove watermarks from PDF documents while preserving the underlying text, images, and original layout. Powered by a high-precision document enhancement engine that intelligently detects and erases overlaid watermarks, stamps, and translucent logos across every page, leaving the document clean and legible. Use when the user wants to remove watermarks from a PDF, clean up stamped PDFs, or recover a clean copy of a watermarked PDF. Triggers on "remove watermark from PDF", "erase PDF watermark", "delete watermark from pdf", "unwatermark pdf", "clean watermarked PDF", or when the user has a PDF with a watermark that needs to be removed.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "💧"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner PDF Remove Watermark

## Overview

CamScanner provides a high-precision document enhancement engine that removes watermarks from PDF documents while preserving the underlying text, images, and original layout. It intelligently detects overlaid watermarks, stamps, and translucent logos across every page and erases them, leaving the document clean and legible. The workflow is a 3-step pipeline: **upload** the PDF, **remove watermark** via `remove_watermark_pdf`, then **download** the result. For convenience, the remove-watermark step also supports a `raw` output mode that returns the processed PDF bytes directly, skipping the download step.

## When to Use

- User wants to remove watermarks, stamps, or translucent logos from a PDF
- User has a watermarked PDF that needs to be cleaned before sharing or printing
- User wants to recover a clean copy of a watermarked PDF
- User has a watermarked PDF and needs a clean copy for OCR or further processing

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Supported Operation

| source_type | Operation              | Endpoint               | Output |
| ----------- | ---------------------- | ---------------------- | ------ |
| pdf         | Remove watermark (PDF) | remove_watermark_pdf   | .pdf   |

### Parameters

| Field         | Required | Default | Notes                                                                  |
| ------------- | -------- | ------- | ---------------------------------------------------------------------- |
| `file_id`     | yes      | —       | The `file_id` returned by `upload_file` for the source PDF             |
| `dpi`         | no       | 144     | Rendering DPI; 144 is the recommended default                          |
| `timeout_sec` | no       | —       | Processing timeout in seconds; use 180 for long PDFs                   |
| `output_mode` | yes      | —       | `"file_id"` (then download separately) or `"raw"` (stream PDF bytes)   |

### Step 1: Upload PDF

```bash
BASE="https://ai-tools.camscanner.com"

IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@/path/to/document.pdf" | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "upload_file",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857600_ab12cd34ef56.pdf",
      "size": 524288
    }
  }
}
```

### Step 2: Remove Watermark

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/remove_watermark_pdf/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"dpi\":144,\"timeout_sec\":180,\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "remove_watermark_pdf",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857701_9988aabbccdd.pdf"
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/output.pdf
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

### Alternative: One-Shot Raw Output

If you don't need a reusable `file_id` for the result, pass `"output_mode": "raw"` to `remove_watermark_pdf` and save the response body directly — this combines steps 2 and 3:

```bash
curl -sS -X POST "$BASE/v1/tools/remove_watermark_pdf/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"dpi\":144,\"timeout_sec\":180,\"output_mode\":\"raw\"}" \
  -o /path/to/output.pdf
```

## Quick Reference: Complete Pipeline

Remove watermark from a PDF (three-step, keeps an output `file_id`):

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_PDF="/path/to/document.pdf"
OUTPUT_FILE="/path/to/output.pdf"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_PDF" | jq -r '.tool_result.data.file_id')

# Remove watermark
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/remove_watermark_pdf/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"dpi\":144,\"timeout_sec\":180,\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')

# Download
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o "$OUTPUT_FILE"
```

Or one-shot (two-step, raw PDF stream straight from `remove_watermark_pdf`):

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_PDF="/path/to/document.pdf"
OUTPUT_FILE="/path/to/output.pdf"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_PDF" | jq -r '.tool_result.data.file_id')

# Remove watermark + download in one call
curl -sS -X POST "$BASE/v1/tools/remove_watermark_pdf/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"dpi\":144,\"timeout_sec\":180,\"output_mode\":\"raw\"}" \
  -o "$OUTPUT_FILE"
```

## Common Mistakes

| Mistake                                             | Fix                                                                           |
| --------------------------------------------------- | ----------------------------------------------------------------------------- |
| Forgetting `response_mode=raw` on download          | Always append `?response_mode=raw` to the download URL                        |
| Wrong Content-Type on upload                        | Upload uses `application/octet-stream`, not `multipart/form-data`             |
| Using GET instead of POST                           | All endpoints use POST                                                        |
| Using `enhance_image` for a PDF                     | PDFs use the dedicated `remove_watermark_pdf` endpoint, not `enhance_image`   |
| Passing `dpi` or `timeout_sec` as strings           | Both are integers — use `144` and `180`, not `"144"` / `"180"`                |
| Missing `output_mode` in request                    | Must be either `"file_id"` (then download separately) or `"raw"` (stream out) |
| Timeout on long PDFs                                | Increase `timeout_sec` (e.g. `180` or more) for documents with many pages     |
| Parsing JSON when `output_mode` is `"raw"`          | With `raw`, the response body IS the PDF — write it to a file with `-o`      |
| Trying to download a `file_id` after `raw` response | `raw` mode returns no `file_id`; re-run in `file_id` mode if you need one     |

## Error Handling

Check each step before proceeding:

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After remove watermark (file_id mode)
if [ -z "$OUT_FILE_ID" ] || [ "$OUT_FILE_ID" = "null" ]; then
  echo "Watermark removal failed"; exit 1
fi
```
