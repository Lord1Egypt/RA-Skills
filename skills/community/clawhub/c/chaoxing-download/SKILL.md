---
name: chaoxing-download
description: Download PDF documents from Chaoxing (超星) contest/platform viewer URLs and convert to TXT. Use when user wants to download files from contestyd.chaoxing.com, 超星, or provides Chaoxing WPS viewer URLs with objectid parameters. Supports single or batch downloads with page count validation and automatic PDF-to-TXT conversion.
argument-hint: "[viewer URL(s) and names, one per line: 页数 名称 URL]"
---

# Chaoxing Document Downloader (超星文档下载)

Download PDFs from Chaoxing WPS viewer URLs using the `getYunFiles` API.

## Core Principle

Every Chaoxing viewer URL contains an `objectid` (32-char hex). Call the `getYunFiles` API to get the direct PDF link — no cookies or auth tokens needed.

## Arguments

`$ARGUMENTS` contains the user's download request — typically one or more entries with page count, name, and viewer URL. Parse them to extract the data.

## Download Method

### Step 1: Extract objectid from each URL

Find the `objectid=([a-f0-9]{32})` parameter in each viewer URL.

### Step 2: Call getYunFiles API

For each objectid, call:
```
https://contestyd.chaoxing.com/app/files/{objectid}/getYunFiles?key=allData
```

Response JSON contains:
- `data.pdf` — direct PDF URL on `s3.cldisk.com` or `s3.ananas.chaoxing.com` (preferred)
- `data.download` — alternative download URL with auth tokens (fallback)
- `data.filename` — original filename
- `data.pagenum` — page count

### Step 3: Download the PDF

Use the `data.pdf` URL to download directly. No authentication headers needed.

Save to: `~/Downloads/chaoxing_pdfs/{用户给的名称}.pdf`

### Step 4: Validate page count

Compare `data.pagenum` with the user's expected page count. Report any mismatch.

### Step 5: Convert PDF to TXT (with OCR fallback)

After downloading each PDF, automatically extract text to a plain text file. Use a two-stage approach: native text extraction first, then OCR fallback for image-based pages.

**Prerequisites:**

```bash
pip install pymupdf rapidocr-onnxruntime
```

**Conversion method (Python):**

```python
import sys, os, fitz
from rapidocr_onnxruntime import RapidOCR

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ocr = RapidOCR()
pdf_path = "~/Downloads/chaoxing_pdfs/{name}.pdf"
doc = fitz.open(pdf_path)
all_text = []

for i, page in enumerate(doc):
    # Stage 1: Try native text extraction
    native = page.get_text().strip()
    if len(native) > 50:
        all_text.append(f"--- 第{i+1}页 ---\n{native}")
        continue
    # Stage 2: OCR fallback for image-based pages
    pix = page.get_pixmap(dpi=200)
    img_bytes = pix.tobytes("png")
    result, _ = ocr(img_bytes)
    ocr_text = "\n".join([item[1] for item in result]) if result else ""
    label = "OCR" if len(ocr_text) > 0 else "(empty)"
    all_text.append(f"--- 第{i+1}页 [{label}] ---\n{ocr_text}")

doc.close()
full_text = "\n".join(all_text)

with open(pdf_path.replace(".pdf", ".txt"), "w", encoding="utf-8") as f:
    f.write(full_text)

# Summary
native_pages = sum(1 for p in all_text if "[OCR]" not in p and "[empty]" not in p)
ocr_pages = sum(1 for p in all_text if "[OCR]" in p)
print(f"Native: {native_pages}p, OCR: {ocr_pages}p, Total: {len(full_text)} chars")
```

**Output files per download:**
- `{name}.pdf` — original PDF
- `{name}.txt` — plain text extraction (native + OCR pages marked with `[OCR]`)

**How it works:**
1. Each page is first checked for native text (text layer PDF)
2. If native text < 50 chars, the page is rendered to image at 200 DPI and processed by RapidOCR
3. OCR pages are labeled `[OCR]` in the output for easy identification
4. Empty pages (no text and OCR fails) are labeled `[empty]`

## CLI Tool (Alternative)

A CLI tool is available at `C:/Users/Cameron/Downloads/chaoxing_dl.py`:

```bash
# Single download
python ~/Downloads/chaoxing_dl.py "VIEWER_URL" -n "文件名"

# Batch from JSON file
python ~/Downloads/chaoxing_dl.py --batch tasks.json

# With page validation
python ~/Downloads/chaoxing_dl.py "URL" -n "name" --json

# Force overwrite
python ~/Downloads/chaoxing_dl.py "URL" -n "name" -f
```

Batch JSON format:
```json
[
  {"name": "文件名", "url": "viewer_url_or_objectid", "pages": 22},
  ...
]
```

## Batch Processing (Without CLI Tool)

For multiple downloads without the CLI, use bash loop:

```bash
for oid_name in "OBJECTID1:名称1" "OBJECTID2:名称2"; do
  oid="${oid_name%%:*}"; name="${oid_name##*:}"
  info=$(curl -s -L "https://contestyd.chaoxing.com/app/files/$oid/getYunFiles?key=allData")
  pagenum=$(echo "$info" | grep -o '"pagenum":[0-9]*' | cut -d: -f2)
  pdf_url=$(echo "$info" | grep -o '"pdf":"[^"]*"' | head -1 | tr -d '"' | sed 's/^pdf://')
  echo "$name: ${pagenum}p"
  curl -s -L -o ~/Downloads/chaoxing_pdfs/${name}.pdf "$pdf_url"
done
```

## Key Notes

- Only `objectid` is needed — no `resid`, `tk`, `addPointInfo`, or cookies
- Always validate page count against user expectation
- The PDF URLs on `s3.cldisk.com` are direct links, publicly accessible
- If `data.pdf` is empty, fall back to `data.download`
- Skip files that already exist unless user specifies overwrite
