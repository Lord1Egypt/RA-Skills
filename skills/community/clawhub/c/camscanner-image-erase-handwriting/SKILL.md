---
name: camscanner-image-erase-handwriting
description: Use CamScanner to erase handwriting from images while preserving the printed content and original layout. Powered by a high-precision image enhancement engine that intelligently detects and removes handwritten strokes, annotations, and signatures, leaving the underlying document clean and legible. Use when the user wants to remove handwriting from a photo or scan, clean up annotated documents, or restore a blank form filled by hand. Triggers on "erase handwriting", "remove handwriting from image", "clean handwritten notes", "remove annotations from scan", or when the user has an image with handwritten content that needs to be removed.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "✍️"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Image Erase Handwriting

## Overview

CamScanner provides a high-precision image enhancement engine that removes handwriting from images while preserving the printed content and original layout. It intelligently detects handwritten strokes, annotations, and signatures and erases them, leaving the underlying document clean and legible. The workflow is a 3-step pipeline: **upload** the image, **enhance** it with `enhance_mode: 9` (erase handwriting), then **download** the result. For convenience, the enhance step also supports a `raw` output mode that returns the processed image bytes directly, skipping the download step.

## When to Use

- User wants to remove handwriting, annotations, or signatures from an image
- User has a scan or photo of a document with handwritten notes that need to be cleaned
- User wants to restore a blank form after it was filled in by hand
- User has an annotated scan and needs a clean copy for OCR, printing, or sharing

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Supported Enhancements

| source_type | enhance_mode | Operation          | Output |
| ----------- | ------------ | ------------------ | ------ |
| image       | 9            | Erase handwriting  | .jpg   |

### Step 1: Upload Image

```bash
BASE="https://ai-tools.camscanner.com"

IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@/path/to/image.jpg" | jq -r '.tool_result.data.file_id')
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

### Step 2: Enhance Image (Erase Handwriting)

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/enhance_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"enhance_mode\":9,\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "enhance_image",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857701_9988aabbccdd",
      "enhance_mode": 9
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/output.jpg
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

### Alternative: One-Shot Raw Output

If you don't need a reusable `file_id` for the result, pass `"output_mode": "raw"` to `enhance_image` and save the response body directly — this combines steps 2 and 3:

```bash
curl -sS -X POST "$BASE/v1/tools/enhance_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"enhance_mode\":9,\"output_mode\":\"raw\"}" \
  -o /path/to/output.jpg
```

## Quick Reference: Complete Pipeline

Erase handwriting from an image (three-step, keeps an output `file_id`):

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.jpg"
OUTPUT_FILE="/path/to/output.jpg"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# Enhance (erase handwriting)
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/enhance_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"enhance_mode\":9,\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')

# Download
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o "$OUTPUT_FILE"
```

Or one-shot (two-step, raw image stream straight from `enhance_image`):

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.jpg"
OUTPUT_FILE="/path/to/output.jpg"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# Enhance + download in one call
curl -sS -X POST "$BASE/v1/tools/enhance_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"enhance_mode\":9,\"output_mode\":\"raw\"}" \
  -o "$OUTPUT_FILE"
```

## Common Mistakes

| Mistake                                             | Fix                                                                           |
| --------------------------------------------------- | ----------------------------------------------------------------------------- |
| Forgetting `response_mode=raw` on download          | Always append `?response_mode=raw` to the download URL                        |
| Wrong Content-Type on upload                        | Upload uses `application/octet-stream`, not `multipart/form-data`             |
| Using GET instead of POST                           | All endpoints use POST                                                        |
| Passing `enhance_mode` as a string                  | `enhance_mode` is an integer — use `9`, not `"9"`                             |
| Missing `output_mode` in enhance request            | Must be either `"file_id"` (then download separately) or `"raw"` (stream out) |
| Parsing JSON when `output_mode` is `"raw"`          | With `raw`, the response body IS the image — write it to a file with `-o`    |
| Trying to download a `file_id` after `raw` response | `raw` mode returns no `file_id`; re-run in `file_id` mode if you need one     |

## Error Handling

Check each step before proceeding:

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After enhance (file_id mode)
if [ -z "$OUT_FILE_ID" ] || [ "$OUT_FILE_ID" = "null" ]; then
  echo "Enhancement failed"; exit 1
fi
```
