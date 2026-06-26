---
name: camscanner-pdf2office
description: Use CamScanner to convert PDF documents to editable Word (.docx) or Excel (.xlsx) format, with intelligent content recognition and accurate format preservation. Triggers on "PDF to Word", "PDF to Excel", "convert PDF to docx", "convert PDF to xlsx", or when the user has a PDF and needs it as an editable Office document.
metadata:
  author: CamScanner
  version: "1.0"
  openclaw:
    emoji: "📄"
    requires:
      bins: ["curl", "jq"]
  homepage: "https://www.camscanner.com"
---

# CamScanner PDF to Office

## Overview

CamScanner provides document conversion capabilities that convert PDF documents to Word or Excel documents while preserving original formatting. The workflow is a 3-step pipeline: **upload** the PDF, **convert** it, then **download** the result.

## When to Use

- User wants to convert a PDF to Word (.docx) or Excel (.xlsx)
- User wants to make a PDF editable
- User has a PDF and needs it as an Office document

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
| pdf         | word        | .docx  |
| pdf         | excel       | .xlsx  |

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
      "file_id": "file_1741857600_ab12cd34ef56",
      "size": 24576
    }
  }
}
```

### Step 2: Convert PDF

```bash
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/convert_pdf/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"source_type\":\"pdf\",\"target_type\":\"TARGET\",\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')
```

Replace `TARGET` with one of: `word`, `excel`.

**Response:**

```json
{
  "code": 200,
  "tool": "convert_pdf",
  "tool_result": {
    "success": true,
    "data": {
      "file_id": "file_1741857722_ddeeff001122",
      "target_type": "word"
    }
  }
}
```

### Step 3: Download Result

```bash
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o /path/to/output.docx
```

**Critical:** The `response_mode=raw` query parameter is required to get the binary file. Without it, the response is JSON.

## Quick Reference: Complete Pipeline

```bash
BASE="https://ai-tools.camscanner.com"
INPUT_PDF="/path/to/document.pdf"
TARGET_TYPE="word"          # word | excel
OUTPUT_FILE="/path/to/output.docx"

# Upload
IN_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/upload_file/execute" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$INPUT_PDF" | jq -r '.tool_result.data.file_id')

# Convert
OUT_FILE_ID=$(curl -sS -X POST "$BASE/v1/tools/convert_pdf/execute" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$IN_FILE_ID\",\"source_type\":\"pdf\",\"target_type\":\"$TARGET_TYPE\",\"output_mode\":\"file_id\"}" \
  | jq -r '.tool_result.data.file_id')

# Download
curl -sS -X POST "$BASE/v1/tools/download_file/execute?response_mode=raw" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\":\"$OUT_FILE_ID\"}" \
  -o "$OUTPUT_FILE"
```

## File Extension Mapping

| target_type | Extension |
| ----------- | --------- |
| word        | .docx     |
| excel       | .xlsx     |

## Common Mistakes

| Mistake                                    | Fix                                                                     |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| Forgetting `response_mode=raw` on download | Always append `?response_mode=raw` to the download URL                  |
| Wrong Content-Type on upload               | Upload uses `application/octet-stream`, not `multipart/form-data`       |
| Using GET instead of POST                  | All three endpoints use POST                                            |
| Missing `source_type` in convert request   | Always include `"source_type": "pdf"`                                   |
| Missing `output_mode` in convert request   | Always include `"output_mode": "file_id"` to get a downloadable file_id |
| Wrong output extension                     | Match extension to target_type (see table above)                        |

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
