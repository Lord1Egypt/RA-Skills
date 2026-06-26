---
name: camscanner-extract-formula
description: Use CamScanner to extract formulas from images. Powered by OCR recognition engine that detects formula regions in images, crops them, and stitches into a single clean PNG image. Use when the user wants to extract mathematical formulas, equations, or expressions from images (photos, screenshots, scanned documents). Triggers on "extract formula", "get formulas from image", "crop formulas", "formula extraction", or when the user has an image containing math formulas and needs them extracted as a clean image.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "🔢"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Extract Formula

## Overview

CamScanner provides formula extraction from images: OCR recognition detects formula regions, crops them, and vertically stitches all formulas into a single clean PNG image. The workflow is a 3-step pipeline: **upload** the image, **extract** formulas, then **download** the result.

## When to Use

- User wants to extract mathematical formulas or equations from an image
- User has a photo, screenshot, or scanned document containing formulas
- User needs formulas cropped out as a clean image for further use
- User wants to isolate math content from surrounding text in an image

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Supported Modes

| extract_mode | Description                                          | Output |
| ------------ | ---------------------------------------------------- | ------ |
| formula      | Extract math formulas, crop and stitch into one image | .png   |

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

### Step 2: Extract Formulas

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/extract_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"extract_mode\":\"formula\"}" \
  | jq -r '.tool_result.data.file_id')
```

**Response:**

```json
{
  "code": 200,
  "tool": "extract_image",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857701_9988aabbccdd",
      "target_type": ""
    },
    "metadata": {
      "engine": "extractformula",
      "formula_count": 6
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/formulas.png
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

## Quick Reference: Complete Pipeline

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.png"
OUTPUT_FILE="/path/to/formulas.png"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# Extract
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/extract_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"extract_mode\":\"formula\"}" \
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
| Missing `extract_mode` in extract request  | Always include `"extract_mode": "formula"`                              |
| Saving output with wrong extension         | Output is always PNG format — use `.png` extension                      |

## Error Handling

Check each step before proceeding:

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After extract
if [ -z "$OUT_FILE_ID" ] || [ "$OUT_FILE_ID" = "null" ]; then
  echo "Extraction failed"; exit 1
fi
```
