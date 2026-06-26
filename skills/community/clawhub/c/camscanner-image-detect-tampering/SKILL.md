---
name: camscanner-image-detect-tampering
description: Use CamScanner to detect whether an image has been PS-edited, manipulated, or tampered with. Powered by a manipulation-detection engine that identifies photo-editing traces, splicing, retouching, and other signs of tampering. Returns a JSON result with `is_tampered` (boolean) and `result_text` (human-readable). Use when the user asks whether a photo is genuine, wants to verify an image's authenticity, or asks "is this PS-ed / photoshopped / edited". Triggers on "检测图片是否PS", "是否被篡改", "图片验真", "PS检测", "detect image tampering", "is this photoshopped", "check if image was edited", or when the user shares an image and asks whether it has been modified.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Image Detect Tampering

## Overview

CamScanner provides a manipulation-detection engine that determines whether an image has been PS-edited, spliced, retouched, or otherwise tampered with. The workflow is a 2-step pipeline: **upload** the image, then **validate** it with `validate_mode: 1`. Unlike conversion skills, this skill does not produce a file — the validate step returns a JSON result whose key fields (`is_tampered`, `result_text`) should be reported back to the user directly.

## When to Use

- User asks whether an image has been photoshopped, retouched, or manipulated
- User wants to verify the authenticity of a photo or scanned document
- User asks "is this PS-ed / tampered / edited?" or similar authenticity questions
- User shares an image and explicitly asks whether it has been modified

## Presenting the Result

- Always read `is_tampered` and `result_text` from the response and report them in plain language.
- **Match the user's language.** `result_text` is returned in Chinese by the API. If the user asked in English (or any other language), translate/rephrase it into that language. If the user asked in Chinese, you can use `result_text` as-is.
- Do not claim tampering when `is_tampered` is `false`; do not claim an image is clean when `is_tampered` is `true`.

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Result**: Only a JSON detection result is returned — no file is downloaded.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Supported Validations

| source_type | validate_mode | Detection                  | Engine                  |
| ----------- | ------------- | -------------------------- | ----------------------- |
| image       | 1             | PS / tampering detection   | manipulationdetection   |

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
      "file_id": "file_1741857600_ab12cd34ef56.jpg",
      "size": 24576
    }
  }
}
```

### Step 2: Validate Image (Detect Tampering)

```bash
curl -sS -X POST "$BASE/v1/tools/validate_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"validate_mode\":1}"
```

**Response (tampered example):**

```json
{
  "code": 200,
  "tool": "validate_image",
  "tool_result": {
    "success": true,
    "data": {
      "engine": "manipulationdetection",
      "file_id": "file_xxx.jpg",
      "is_tampered": true,
      "result_text": "检测到图片存在 PS/篡改痕迹",
      "review_state": "auto_checked",
      "validate_mode": 1
    },
    "metadata": {
      "engine": "manipulationdetection",
      "is_tampered": true,
      "result_text": "检测到图片存在 PS/篡改痕迹",
      "review_state": "auto_checked",
      "validate_mode": 1
    }
  }
}
```

## Interpreting the Result

| Field          | Type    | Meaning                                                                       |
| -------------- | ------- | ----------------------------------------------------------------------------- |
| `is_tampered`  | boolean | `true` = tampering detected, `false` = no tampering detected                  |
| `result_text`  | string  | Human-readable conclusion (Chinese by default — translate for other languages) |
| `review_state` | string  | Review status (e.g. `auto_checked`) — informational, not user-facing          |
| `validate_mode`| integer | Echo of the requested mode (always `1` for PS/tampering detection)            |

## Quick Reference: Complete Pipeline

Detect whether an image has been PS-edited (two-step, reads JSON result):

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.jpg"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# Validate and extract key fields
RESULT=$(curl -sS -X POST "$BASE/v1/tools/validate_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"validate_mode\":1}")

IS_TAMPERED=$(echo "$RESULT" | jq -r '.tool_result.data.is_tampered')
RESULT_TEXT=$(echo "$RESULT" | jq -r '.tool_result.data.result_text')

echo "is_tampered: $IS_TAMPERED"
echo "result_text: $RESULT_TEXT"
```

## Common Mistakes

| Mistake                                  | Fix                                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------- |
| Wrong Content-Type on upload             | Upload uses `application/octet-stream`, not `multipart/form-data`             |
| Using GET instead of POST                | Both endpoints use POST                                                       |
| Passing `validate_mode` as a string      | `validate_mode` is an integer — use `1`, not `"1"`                            |
| Including `output_mode` in the request   | `validate_image` does not use `output_mode`; it always returns JSON           |
| Treating a missing `is_tampered` as safe | Always check `code == 200` and `tool_result.success == true` before reading   |
| Reporting `result_text` verbatim in EN   | `result_text` is Chinese; translate to match the user's language              |

## Error Handling

Check each step before proceeding:

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After validate
if [ "$IS_TAMPERED" = "null" ] || [ -z "$IS_TAMPERED" ]; then
  echo "Validation failed"; exit 1
fi
```
