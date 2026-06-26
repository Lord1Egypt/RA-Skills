---
name: camscanner-watermark-image
description: Use CamScanner to add a tiled text watermark across an entire image. Triggers on "add watermark to image", "watermark image", "add copyright text to image", "stamp image with text", or when the user wants to overlay repeating text (e.g. "Confidential", "Draft", copyright notices) on an image. Supports custom color, opacity, and font size.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "💧"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Watermark Image

## Overview

CamScanner applies a full-page tiled text watermark to an image. The watermark text is repeated in a diagonal grid pattern across the entire image. The workflow is a 3-step pipeline: **upload** the image, **apply watermark**, then **download** the result.

## When to Use

- User wants to add a text watermark to an image
- User needs to stamp "Confidential", "Draft", "Copyright", etc. on an image
- User wants repeating diagonal text overlay on a photo

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Parameters

| Parameter | Required | Type | Default | Description |
| --------- | -------- | ---- | ------- | ----------- |
| `file_id` | Yes | string | — | Uploaded image file_id |
| `text` | Yes | string | — | Watermark text (max 200 chars) |
| `color` | No | string | `#000000` | Hex color, e.g. `#FF0000` for red |
| `opacity` | No | number | `0.4` | Transparency 0-1 (0=invisible, 1=opaque) |
| `size` | No | integer | `36` | Font size 1-200 |

**Do NOT pass** `mode`, `x`, `y`, `width`, `height`, or `rotation` — these are fixed internally for tiled watermark layout.

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

### Step 2: Apply Watermark

**Minimal call** (recommended — uses sensible defaults):

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/watermark_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"text\":\"Copyright 2026\",\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')
```

**With custom styling** (only add fields the user explicitly requests):

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/watermark_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"text\":\"Confidential\",\"color\":\"#FF0000\",\"opacity\":0.5,\"size\":60,\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "watermark_image",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857701_9988aabbccdd.jpg",
      "target_type": ""
    },
    "metadata": {
      "engine": "imageprocess"
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/watermarked.jpg
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

## Quick Reference: Complete Pipeline

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.jpg"
TEXT="Copyright 2026"
OUTPUT_FILE="/path/to/watermarked.jpg"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# Watermark
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/watermark_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"text\":\"$TEXT\",\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')

# Download
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o "$OUTPUT_FILE"
```

## Common Mistakes

| Mistake | Fix |
| ------- | --- |
| Forgetting `response_mode=raw` on download | Always append `?response_mode=raw` to the download URL |
| Missing `text` parameter | `text` is required — ask the user what text to use |
| Passing internal params like `mode`, `x`, `y` | Never pass these — they are fixed for tiled layout |
| Color without `#` prefix | Both `FF0000` and `#FF0000` work, but always use 6 hex digits |
| RGBA PNG input (4-channel with alpha) | May cause 500 error from upstream — convert to JPEG first if this happens |
| Wrong Content-Type on upload | Upload uses `application/octet-stream`, not `multipart/form-data` |

## Error Handling

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After watermark
if [ -z "$OUT_FILE_ID" ] || [ "$OUT_FILE_ID" = "null" ]; then
  echo "Watermark failed"; exit 1
fi
```

### Known Limitations

- **RGBA PNG (4-channel)**: The upstream image processing service may return a 500 error for images with alpha channel. Workaround: convert to JPEG before uploading (`sips -s format jpeg input.png --out input.jpg` on macOS).
