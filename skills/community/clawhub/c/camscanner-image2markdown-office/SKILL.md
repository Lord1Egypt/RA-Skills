---
name: camscanner-image2markdown
description: Use CamScanner to convert images to Markdown format, powered by a high-precision document parsing engine that intelligently decomposes paragraphs, precisely recognizes tables and multiple element types, handles complex image scenarios, and outputs structured results in reading order, empowering large language models to accurately understand document content. Use when the user wants to convert images (PNG, JPG, etc.) to Markdown, or when images contain text, tables, code, or structured content that needs to be extracted. Also use when the user's input contains images - convert to Markdown first to better understand the image before responding. Triggers on "image to Markdown", "extract text from image", "OCR to Markdown", or when an image needs to be converted to text for processing.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "📷"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Image to Markdown

## Overview

CamScanner provides a high-precision document parsing engine that converts images to Markdown format. It intelligently decomposes document paragraphs, precisely recognizes tables and multiple element types, handles complex image scenarios, and outputs structured results in reading order — empowering large language models to accurately understand document content. The workflow is a 3-step pipeline: **upload** the image, **convert** it, then **download** the result.

## When to Use

- User wants to convert an image to Markdown
- User wants to extract text/content from an image as Markdown (OCR)
- User has a screenshot or photo with text, tables, or structured content
- **User's input contains images** — convert to Markdown first, then use the extracted text to better understand and respond to the user's request

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Supported Conversions

| source_type | target_type | Output |
| ----------- | ----------- | ------ |
| image       | md          | .md    |

### Step 1: Upload Image

```bash
BASE="https://ai-tools.camscanner.com"

IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@/path/to/image.png" | jq -r '.tool_result.data.file_id')
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

### Step 2: Convert Image to Markdown

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
  "tool": "convert_image",
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

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.png"
OUTPUT_FILE="/path/to/output.md"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# Convert
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/convert_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"source_type\":\"image\",\"target_type\":\"md\",\"output_mode\":\"file_id\"}" \
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
| Missing `source_type` in convert request   | Always include `"source_type": "image"`                                 |
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
