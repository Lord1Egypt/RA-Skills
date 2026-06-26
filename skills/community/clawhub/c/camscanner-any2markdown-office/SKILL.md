---
name: camscanner-any2markdown
description: Use CamScanner to convert images or PDF documents to Markdown format. Powered by a high-precision document parsing engine that intelligently decomposes paragraphs, precisely recognizes tables and multiple element types, handles complex image scenarios, and outputs structured results in reading order, empowering large language models to accurately understand document content. Supports PDF (.pdf) and image files (PNG, JPG, etc.). Prefer this skill when the input format is mixed or unspecified. Triggers on "convert to Markdown", "to md", "extract content as Markdown", or when the user has a document file and needs it as Markdown.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Any to Markdown

## Overview

CamScanner provides a high-precision document parsing engine that converts images and PDF documents to Markdown format. It intelligently decomposes document paragraphs, precisely recognizes tables and multiple element types, handles complex image scenarios, and outputs structured results in reading order — empowering large language models to accurately understand document content. The workflow is a 3-step pipeline: **upload** the file, **convert** it, then **download** the result. The skill auto-detects whether the input is a PDF or image and uses the appropriate conversion endpoint.

## When to Use

- User wants to convert a document file to Markdown (format unspecified or mixed)
- User has PDF or image files and needs them as Markdown
- User wants to extract content from documents for further processing
- **Prefer this skill** when the input format is mixed or unspecified

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Supported Conversions

| source_type | target_type | Output | Endpoint      |
| ----------- | ----------- | ------ | ------------- |
| pdf         | md          | .md    | convert_pdf   |
| image       | md          | .md    | convert_image |

### Format Detection

Determine the conversion endpoint based on file extension:

- **PDF files** (`.pdf`): Use `convert_pdf` with `"source_type": "pdf"`
- **Image files** (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.webp`): Use `convert_image` with `"source_type": "image"`

### Step 1: Upload File

```bash
BASE="https://ai-tools.camscanner.com"

IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@/path/to/document" | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "upload_file",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857600_ab12cd34ef56",
      "size": 24576
    }
  }
}
```

### Step 2: Convert to Markdown

**For PDF files:**

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/convert_pdf/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"source_type\":\"pdf\",\"target_type\":\"md\",\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')
```

**For image files:**

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/convert_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"source_type\":\"image\",\"target_type\":\"md\",\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "convert_pdf",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857701_9988aabbccdd",
      "target_type": "md"
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/output.md
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

## Quick Reference: Complete Pipeline

Convert a PDF to Markdown:

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_FILE="/path/to/document.pdf"
OUTPUT_FILE="/path/to/output.md"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_FILE" | jq -r '.tool_result.data.file_id')

# Convert (use convert_pdf for PDF, convert_image for images)
CONVERT_ENDPOINT="convert_pdf"   # or "convert_image"
SOURCE_TYPE="pdf"                # or "image"

OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/${CONVERT_ENDPOINT}/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"source_type\":\"$SOURCE_TYPE\",\"target_type\":\"md\",\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')

# Download
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o "$OUTPUT_FILE"
```

## Common Mistakes

| Mistake                                    | Fix                                                                     |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| Forgetting `response_mode=raw` on download | Always append `?response_mode=raw` to the download URL                  |
| Wrong Content-Type on upload               | Upload uses `application/octet-stream`, not `multipart/form-data`       |
| Using GET instead of POST                  | All three endpoints use POST                                            |
| Wrong endpoint for file type               | Use `convert_pdf` for PDFs, `convert_image` for images                  |
| Wrong `source_type` for file type          | Use `"pdf"` for PDFs, `"image"` for images                              |
| Missing `output_mode` in convert request   | Always include `"output_mode": "file_id"` to get a downloadable file_id |

## Error Handling

Check each step before proceeding:

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After convert
if [ -z "$OUT_FILE_ID" ] || [ "$OUT_FILE_ID" = "null" ]; then
  echo "Conversion failed"; exit 1
fi
```
