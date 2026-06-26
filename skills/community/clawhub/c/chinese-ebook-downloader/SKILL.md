---
name: chinese-ebook-downloader
description: >
  Download Chinese-language ebooks from multiple sources with automatic A→B→C fallback.
  Primary source: online book library with ~100% coverage, no daily limit.
  Fallback sources: secondary library, Anna's Archive.
  Supports EPUB→PDF auto-conversion via weasyprint. Handles file host decryption,
  countdown wait, JS API extraction, GBK-encoded ZIP. Formats: PDF, EPUB, MOBI, AZW3.
  Use when: "下载电子书", "下载这本书", "找一下某本书的电子版", "帮我下个epub/mobi/azw3/pdf".
---

# Chinese Ebook Downloader

Download Chinese ebooks from multiple sources with automatic fallback and format conversion.

## Quick Start

```bash
# Single book download (multi-source fallback)
python scripts/download_book.py --title "超越百岁" --author "彼得·阿提亚"

# Multi-source batch download (A→B→C fallback + EPUB→PDF conversion)
python scripts/multi_source_download.py ~/Books/

# Search Anna's Archive directly
python scripts/search_source_c.py "书名" "作者"

# Convert EPUB to PDF
python scripts/epub_to_pdf.py book.epub book.pdf
```

## Download Sources (Priority Order)

| Source | Coverage | Limit | Notes |
|--------|----------|-------|-------|
| **Source A** (online book library) | ~100% | None | Primary — high coverage for popular Chinese books |
| **Source B** (secondary library) | ~8% | None | Fallback for missing titles |
| **Source C** (Anna's Archive) | Wide | Rate-limited | Last resort — uses libgen.li mirrors |

> **Note:** Z-Library has been deprecated due to 10/day download limit.

## Multi-Source Fallback

The `multi_source_download.py` script automatically tries sources in order:

```
Source A → Source B → Source C → EPUB→PDF Conversion
```

**Workflow per book:**
1. Try Source A (ZIP → extract PDF/EPUB)
2. If failed, try Source B (file host download)
3. If failed, try Source C (Anna's Archive via libgen.li)
4. If only EPUB found, auto-convert to PDF using weasyprint

**Usage:**
```bash
# Edit BOOKS list in script, then run:
python scripts/multi_source_download.py ~/Books/
```

## EPUB → PDF Conversion

When only EPUB format is available, auto-convert using weasyprint:

```bash
# Single file
python scripts/epub_to_pdf.py input.epub output.pdf

# Batch convert directory
python scripts/epub_to_pdf.py --batch ~/Books/
```

**Requirements:** `ebooklib`, `weasyprint`, CJK fonts installed.

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `download_book.py` | Primary download from Source A |
| `search_secondary_source.py` | Source B search & download |
| `search_source_c.py` | Anna's Archive search & download |
| `batch_download.py` | Batch download from JSON list |
| `multi_source_download.py` | Multi-source A→B→C fallback |
| `epub_to_pdf.py` | EPUB/MOBI to PDF conversion |
| `anna_iso_batch.sh` | Anna's Archive isolated batch (one process per book) |

## Source A Workflow (Primary)

```
Search → Get file host link → Decrypt → Wait countdown → API fetch → curl download → Extract ZIP
```

### Step 1: Search
Search the primary library for the book title. Navigate to download page, extract file host URL and password.

### Step 2: Decrypt
Navigate to file host URL, enter password, click decrypt.

### Step 3: Wait for countdown
File hosting service requires countdown before download. **Do not skip.**

### Step 4: Fetch real download URL

**Get page variables:**
```javascript
JSON.stringify({api_server, userid, file_id, share_id, file_chk, start_time, wait_seconds, verifycode})
```

**Call API:**
```javascript
(async () => {
  var url = api_server + '/get_file_url.php?uid=' + userid
    + '&fid=' + file_id + '&folder_id=0&share_id=' + share_id
    + '&file_chk=' + file_chk + '&start_time=' + start_time
    + '&wait_seconds=' + wait_seconds + '&mb=0&app=0&acheck=0'
    + '&verifycode=' + verifycode + '&rd=' + Math.random();
  var headers = typeof getAjaxHeaders === 'function' ? getAjaxHeaders() : {};
  var resp = await fetch(url, {headers: headers});
  return JSON.stringify(await resp.json());
})()
```

Response `code: 200` → `downurl` is real URL.

### Step 5: Download
```bash
curl -L -o "book.zip" "DOWNURL" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  --max-time 1200
```

### Step 6: Extract ZIP (GBK encoding)
```python
import zipfile
with zipfile.ZipFile('book.zip', 'r') as z:
    for info in z.infolist():
        try:
            name = info.filename.encode('cp437').decode('gbk')
        except:
            name = info.filename
        ext = os.path.splitext(name)[1].lower()
        if ext in ('.epub', '.azw3', '.mobi', '.pdf', '.txt'):
            data = z.read(info.filename)
            with open(os.path.basename(name), 'wb') as f:
                f.write(data)
```

## Book Name Matching Strategy

When a book title is long or contains multiple names (e.g. box sets):

- Removes subtitles (after "：" or ":")
- Removes parenthetical content ("（...）", "(...)")
- Removes "套装共X册" bundle descriptions
- Splits "+"-connected titles into individual books
- Tries each keyword until match found
- Falls back to full title + author

**Examples:**
- "杨定一全部生命系列：真原医+静坐+好睡（套装3册）" → tries "真原医", "静坐", "好睡"
- "超越百岁：长寿的科学与艺术" → tries "超越百岁", then "超越百岁 彼得·阿提亚"

## Format Selection

| Flag | Description |
|------|-------------|
| `--format pdf` | PDF only (default, preferred for NotebookLM) |
| `--format epub` | EPUB only |
| `--format mobi` | MOBI only |
| `--format azw3` | AZW3 only |
| `--format any` | Accept any available format |

## Batch Download

```bash
python scripts/batch_download.py --book-list books.json --output-dir ~/Books/
```

JSON format:
```json
[
  {"title": "超越百岁", "file_url": "<file_host_url>", "password": "<password>"}
]
```

Features: resume via `_progress.json`, skip existing, rate limiting.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| IP blocking | Use browser tool, not web_fetch |
| Link 404 | Link expired, re-search |
| API non-200 | Re-navigate and re-decrypt |
| Download is HTML | URL expired, fresh API call needed |
| ZIP filenames garbled | Use Python cp437→gbk, not unzip |
| Timeout on large files | Increase `--max-time` to 1200 |
| Anna's Archive blocked | Try different mirror, use `anna_iso_batch.sh` |
