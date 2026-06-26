---
name: camscanner-translate-image
description: Use CamScanner to translate text in images to another language while preserving the original layout. Detects text in the image, translates it to the target language, and renders the translated text back onto the image. Use when the user wants to translate text in an image, photo, screenshot, or scanned document to another language. Triggers on "translate image", "translate text in image", "image translation", "translate this to English/Japanese/Korean/etc.", or when the user has an image with foreign text and wants it translated.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner Translate Image

## Overview

CamScanner provides image translation: detect text in images, translate to the target language, and render translated text preserving the original layout. The workflow is a 3-step pipeline: **upload** the image, **translate** it, then **download** the result.

## When to Use

- User wants to translate text in an image to another language
- User has a photo, screenshot, or scanned document with foreign text
- User wants to understand text in an image that is in a different language

## Privacy & Data

> **Important: Privacy & Data Flow Notice**
>
> - **Third-party service**: This skill sends your files to CamScanner's official servers (`ai-tools.camscanner.com`) for processing.
> - **Data retention**: CamScanner servers process your files in real-time. Files are not permanently stored on the server.
> - **Local files**: Output files are saved to your local filesystem at the path you specify.

## API Reference

**Base URL:** `https://ai-tools.camscanner.com`

### Target Language (`to` parameter)

The `to` parameter specifies the target language code. Determine it from the user's intent.

**Common language mapping (use this first):**

| User says (English) | User says (Chinese) | `to` code |
| ------------------- | ------------------- | --------- |
| English | 英语/英文 | `en` |
| Chinese Simplified | 简体中文/中文 | `zh-Hans` |
| Chinese Traditional | 繁体中文 | `zh-Hant` |
| Cantonese | 粤语 | `yue` |
| Japanese | 日语/日文 | `ja` |
| Korean | 韩语/韩文 | `ko` |
| French | 法语/法文 | `fr` |
| German | 德语/德文 | `de` |
| Spanish | 西班牙语 | `es` |
| Portuguese | 葡萄牙语 | `pt` |
| Russian | 俄语/俄文 | `ru` |
| Arabic | 阿拉伯语 | `ar` |
| Italian | 意大利语 | `it` |
| Dutch | 荷兰语 | `nl` |
| Thai | 泰语/泰文 | `th` |
| Vietnamese | 越南语 | `vi` |
| Indonesian | 印尼语 | `id` |
| Malay | 马来语 | `ms` |
| Turkish | 土耳其语 | `tr` |
| Polish | 波兰语 | `pl` |
| Swedish | 瑞典语 | `sv` |
| Danish | 丹麦语 | `da` |
| Hindi | 印地语 | `hi` |
| Bengali/Bangla | 孟加拉语 | `bn` |
| Ukrainian | 乌克兰语 | `uk` |
| Czech | 捷克语 | `cs` |
| Greek | 希腊语 | `el` |
| Hebrew | 希伯来语 | `he` |
| Finnish | 芬兰语 | `fi` |
| Hungarian | 匈牙利语 | `hu` |

**If the target language is NOT in the table above**, look up the language code dynamically:

```bash
LANG_DATA=$(curl -sS "https://open.camscanner.com/sync/get_languages")
# Parse LANG_DATA to find the matching language code by name or chineseName
# Example: find code for "Romanian"
TO=$(echo "$LANG_DATA" | jq -r '.data | to_entries[] | select(.value.name == "Romanian" or .value.chineseName == "罗马尼亚语") | .key')
```

The API returns all supported languages with `name` (English), `nativeName`, and `chineseName` (Chinese) fields.

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

### Step 2: Translate Image

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/translate_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"to\":\"$TO\"}" \
  | jq -r '.tool_result.data.file_id')
```

Replace `$TO` with the target language code (e.g., `en`, `ja`, `zh-Hans`).

**Response:**

```json
{
  "code": 200,
  "tool": "translate_image",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857701_9988aabbccdd",
      "target_type": ""
    },
    "metadata": {
      "engine": "imagetranslate"
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/translated.png
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

## Quick Reference: Complete Pipeline

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_IMAGE="/path/to/image.png"
OUTPUT_FILE="/path/to/translated.png"
TO="en"   # target language code — see mapping table above

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_IMAGE" | jq -r '.tool_result.data.file_id')

# Translate
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/translate_image/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"to\":\"$TO\"}" \
  | jq -r '.tool_result.data.file_id')

# Download
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o "$OUTPUT_FILE"
```

## Language Code Lookup (for uncommon languages)

If the user requests a language not in the common mapping table, look it up dynamically:

```bash
TARGET_LANG="Romanian"   # or Chinese name like "罗马尼亚语"

LANG_DATA=$(curl -sS "https://open.camscanner.com/sync/get_languages")
TO=$(echo "$LANG_DATA" | jq -r --arg lang "$TARGET_LANG" \
  '.data | to_entries[] | select(.value.name == $lang or .value.chineseName == $lang or .value.nativeName == $lang) | .key')

if [ -z "$TO" ] || [ "$TO" = "null" ]; then
  echo "Unsupported language: $TARGET_LANG"; exit 1
fi
```

## Common Mistakes

| Mistake                                    | Fix                                                                     |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| Forgetting `response_mode=raw` on download | Always append `?response_mode=raw` to the download URL                  |
| Wrong Content-Type on upload               | Upload uses `application/octet-stream`, not `multipart/form-data`       |
| Using GET instead of POST                  | All three endpoints use POST                                            |
| Missing `to` parameter                     | Always include target language code in the translate request             |
| Wrong language code                        | Use codes from the mapping table; for uncommon languages, use the lookup API |
| Using "zh" instead of "zh-Hans"            | Chinese Simplified is `zh-Hans`, not `zh`; Traditional is `zh-Hant`     |

## Error Handling

Check each step before proceeding:

```bash
# After upload
if [ -z "$IN_FILE_ID" ] || [ "$IN_FILE_ID" = "null" ]; then
  echo "Upload failed"; exit 1
fi

# After translate
if [ -z "$OUT_FILE_ID" ] || [ "$OUT_FILE_ID" = "null" ]; then
  echo "Translation failed"; exit 1
fi
```
