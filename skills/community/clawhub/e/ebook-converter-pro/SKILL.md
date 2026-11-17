---
name: ebook-converter-pro
description: 電子書轉換工具箱：支援 EPUB / PDF / MOBI / AZW3 / FB2 → TXT / Markdown / HTML / JSON；批量轉換、封面萃取、元資料讀寫、圖書館自動分類。
---

# 📖 電子書轉換工具箱（Ebook Converter Pro）

## 概述

全功能電子書轉換系統，支援主流格式的讀取、轉換、組織、元資料管理。

**觸發關鍵字：** 轉換電子書、EPUB 轉 TXT、PDF 轉 Markdown、批量轉檔、圖書整理、元資料、萃取封面、電子書管理、格式轉換、epub、pdf 轉檔

---

## 支援格式

| 輸入格式 | 輸出格式 |
|---------|---------|
| EPUB | TXT、Markdown、HTML、JSON |
| PDF | TXT、Markdown、圖片（PNG/JPG）|
| MOBI / AZW3 | TXT |
| FB2 | TXT、Markdown |
| TXT（純文字）| 任意文字格式 |

---

## 腳本清單

| 腳本 | 用途 |
|------|------|
| `scripts/epub_converter.py` | EPUB 萬用轉換（→ TXT / MD / HTML / JSON，支援封面萃取）|
| `scripts/pdf_converter.py` | PDF 轉換（→ TXT / Markdown / 圖片 / OCR，支援分割/合併）|
| `scripts/batch_converter.py` | 批量轉換引擎（多目錄、並行處理、進度條、轉換報告）|
| `scripts/ebook_metadata.py` | 元資料讀寫（讀取/編輯/匯出 BibTeX / JSON，批量書目）|
| `scripts/ebook_organizer.py` | 圖書館管理器（依作者/格式自動分類，支援軟連結）|

---

## 環境依賴

```bash
# 核心依賴（Python 標準庫，無需額外安裝）
# 以下為進階功能可選依賴：
brew install poppler tesseract    # macOS: PDF OCR 和 pdftotext
# 或
sudo apt install poppler-utils tesseract-ocr  # Ubuntu/Debian

# Windows: 建議使用 WSL 或安裝 poppler-windows
```

---

## 快速使用

```bash
# EPUB → TXT（單檔）
python3 scripts/epub_converter.py book.epub

# EPUB → Markdown
python3 scripts/epub_converter.py book.epub -f md

# 萃取封面圖
python3 scripts/epub_converter.py book.epub --cover

# 批量 EPUB → TXT
python3 scripts/epub_converter.py ./ebooks/ -f txt --batch

# PDF → TXT（含 OCR）
python3 scripts/pdf_converter.py txt input.pdf --ocr

# PDF → Markdown
python3 scripts/pdf_converter.py md input.pdf -p 1-10

# 批量轉換（多格式自動偵測）
python3 scripts/batch_converter.py ./ebooks/ -f txt -r --report

# 讀取元資料
python3 scripts/ebook_metadata.py read book.epub

# 批量書目匯出
python3 scripts/ebook_metadata.py export *.epub -f bibtex -o bibliography.bib

# 依作者自動分類書庫（軟連結，不移動原檔）
python3 scripts/ebook_organizer.py organize ./ebooks/ -o ./library/ -m author --link

# 依格式自動分類
python3 scripts/ebook_organizer.py organize ./ebooks/ -o ./library/ -m format

# 生成書庫報告
python3 scripts/ebook_organizer.py report ./ebooks/ -r -o library_report.md
```

---

## 功能差異對照

| 功能 | 其他轉換工具 | 本工具 |
|------|------------|--------|
| EPUB → MD/HTML/JSON | 需 Calibre | ✅ 純 Python |
| PDF OCR | 需付費軟體 | ✅ Tesseract 免費 |
| 批量並行 | 單執行緒 | ✅ 多執行緒 + 進度條 |
| 元資料編輯 | 需 Calibre | ✅ 命令列直改 EPUB |
| 軟連結組織 | ❌ 無 | ✅ 不移動原檔 |
| 轉換報告 | ❌ 無 | ✅ Markdown 報告 |
| 作者自動分類 | ❌ 無 | ✅ 從 EPUB 讀取 |
