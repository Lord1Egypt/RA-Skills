---
name: camscanner-image-hd
description: Use CamScanner to enhance image clarity and quality. Applies auto-crop then HD super filter to produce a cleaner, sharper image. Optionally removes moire patterns when explicitly requested. Use when the user wants to make an image clearer, sharper, higher quality, or HD. Triggers on "HD image", "enhance image clarity", "make image clearer", "sharpen image", "high definition", "improve image quality", "super filter", or when the user wants to improve the visual quality of a photo or scanned document. Only use demoire mode when the user explicitly mentions removing moire patterns.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Image HD

## Overview

CamScanner provides HD image enhancement: auto-crop followed by super filter processing to produce cleaner, sharper images. Optionally supports demoire mode to remove moire patterns when explicitly requested. The workflow is a 3-step pipeline: **upload** the image, **enhance** it, then **download** the result.

## When to Use

- User wants to make an image clearer or sharper
- User wants HD or high-definition image processing
- User wants to enhance image quality of a photo or scanned document
- User wants to apply a super filter to an image
- User explicitly asks to remove moire patterns (use `hd_mode=demoire`)

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Supported Modes

| hd_mode   | Description                                      | When to Use                          |
| --------- | ------------------------------------------------ | ------------------------------------ |
| *(empty)* | Auto-crop + super filter (default)               | General HD enhancement               |
| demoire   | Auto-crop + demoire deblur                       | Only when user explicitly asks for moire removal |

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

### Step 2: HD Enhancement

**Default mode (super filter):**

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/image_hd/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\"}" \
  | jq -r '.tool_result.data.file_id')
```

**Demoire mode (only when user explicitly requests moire removal):**

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/image_hd/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"hd_mode\":\"demoire\"}" \
  | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "image_hd",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857701_9988aabbccdd",
      "target_type": ""
    },
    "metadata": {
      "crop_engine": "cropenhance",
      "hd_engine": "imagefilter"
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/image_hd.jpg
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

## Quick Reference: Complete Pipeline

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.png"
OUTPUT_FILE="/path/to/image_hd.jpg"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# HD enhance (default: super filter; add "hd_mode":"demoire" only for explicit moire removal)
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/image_hd/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\"}" \
  | jq -r '.tool_result.data.file_id')

# Download
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o "$OUTPUT_FILE"
```

## Mode Selection Guide

| User says                                           | hd_mode parameter          |
| --------------------------------------------------- | -------------------------- |
| "make it clearer", "HD", "enhance quality"          | *(omit — default filter)*  |
| "sharpen", "super filter", "improve clarity"        | *(omit — default filter)*  |
| "remove moire", "fix moire pattern", "demoire"      | `"hd_mode": "demoire"`    |

**Default to no hd_mode parameter** unless the user explicitly mentions moire patterns.

## Common Mistakes

| Mistake                                    | Fix                                                                     |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| Forgetting `response_mode=raw` on download | Always append `?response_mode=raw` to the download URL                  |
| Wrong Content-Type on upload               | Upload uses `application/octet-stream`, not `multipart/form-data`       |
| Using GET instead of POST                  | All three endpoints use POST                                            |
| Setting hd_mode when not requested         | Only use `"hd_mode": "demoire"` when user explicitly asks for moire removal |
| Wrong output extension                     | Output is typically JPEG — use `.jpg` extension                         |

## Error Handling

Check each step before proceeding:

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After enhance
if [ -z "$OUT_FILE_ID" ] || [ "$OUT_FILE_ID" = "null" ]; then
  echo "Enhancement failed"; exit 1
fi
```
