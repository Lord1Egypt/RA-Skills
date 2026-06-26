---
name: docs-pdf
description: >
  Use this skill whenever the user wants to do anything with PDF files.
  Triggers include: reading or extracting text/tables from PDFs, combining or
  merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding
  watermarks, creating new PDFs from scratch, filling PDF forms, encrypting or
  password-protecting PDFs, extracting images from PDFs, OCR on scanned PDFs,
  compressing/optimizing PDFs, viewing PDF info/metadata, converting images
  to PDF, converting PDF to images, comparing two PDFs, reordering pages,
  repairing corrupted PDFs, and listing fonts. Also trigger when the user
  uploads a .pdf file and asks you to do something with it, or when they
  mention "PDF" in any context involving file creation, editing, or data
  extraction — even if they don't say "PDF skill" explicitly.
---

# PDF Skill

Complete guide for PDF operations using Python libraries and CLI tools.

## ⚡ Feature Cheat Sheet

> One-line lookup for every supported operation — find the right tool instantly.

| What you want to do | Command / Script | One-liner example |
|---|---|---|
| 📖 Extract text | `scripts/extract_text.py` | `python scripts/extract_text.py doc.pdf` |
| 📊 Extract tables → Excel | `scripts/extract_tables.py` | `python scripts/extract_tables.py report.pdf -o tables.xlsx` |
| 🔗 Merge PDFs | `scripts/merge_pdfs.py` | `python scripts/merge_pdfs.py "*.pdf" -o merged.pdf` |
| ✂️ Split PDF | `scripts/split_pdf.py` | `python scripts/split_pdf.py big.pdf --each` |
| 🔄 Rotate pages | `scripts/batch_convert.py rotate` | `python scripts/batch_convert.py rotate input.pdf -d 90` |
| 🔀 Reorder pages | `scripts/reorder_pdf.py` | `python scripts/reorder_pdf.py input.pdf --order "3,1,2,4-" -o reordered.pdf` |
| 💧 Add text watermark | `scripts/watermark.py` | `python scripts/watermark.py doc.pdf -t "CONFIDENTIAL"` |
| 🖼️ Add image watermark | `scripts/watermark.py` | `python scripts/watermark.py doc.pdf --image logo.png --alpha 0.3` |
| 🔒 Encrypt PDF | pypdf (inline) | see [Password Protect](#password-protect) below |
| 📝 Fill PDF form | `scripts/fill_pdf_form.py` | `python scripts/fill_pdf_form.py form.pdf -o filled.pdf --set name="Alice"` |
| 🔍 Check form fields | `scripts/check_fillable_fields.py` | `python scripts/check_fillable_fields.py form.pdf` |
| 🖼️ OCR scanned PDF | `scripts/ocr_pdf.py` | `python scripts/ocr_pdf.py scan.pdf --lang eng` |
| 📄 Create PDF from scratch | reportlab (inline) | see [references/create.md](references/create.md) |
| 📦 Batch operations | `scripts/batch_convert.py` | `python scripts/batch_convert.py merge --help` |
| 📏 Compress / optimize | `scripts/compress_pdf.py` | `python scripts/compress_pdf.py input.pdf -o output.pdf --quality medium` |
| ℹ️ View PDF info | `scripts/pdf_info.py` | `python scripts/pdf_info.py input.pdf` |
| 🖼️→📄 Images to PDF | `scripts/images_to_pdf.py` | `python scripts/images_to_pdf.py "photos/*.jpg" -o album.pdf --page-size A4` |
| 📄→🖼️ PDF to images | `scripts/pdf_to_images.py` | `python scripts/pdf_to_images.py input.pdf -o pages/ --format png --dpi 200` |
| 🔎 Compare two PDFs | `scripts/compare_pdf.py` | `python scripts/compare_pdf.py old.pdf new.pdf -o diff_report.html` |
| 🔧 Repair corrupted PDF | `scripts/repair_pdf.py` | `python scripts/repair_pdf.py broken.pdf -o fixed.pdf` |
| 🔤 List fonts | `scripts/list_fonts.py` | `python scripts/list_fonts.py input.pdf` |

> 💡 Run any script with `--help` to see all available options.

---

## Quick Decision Guide

```
What do you need?
├── Create a new PDF from scratch     → reportlab  (see references/create.md)
├── Extract text / tables             → pdfplumber  (see references/extract.md)
├── Merge / split / rotate pages      → pypdf or qpdf CLI
├── Reorder pages                     → scripts/reorder_pdf.py
├── Add watermark / encrypt / protect → pypdf
├── Fill out a PDF form               → pdf-lib (JS) or pypdf  (see FORMS.md)
├── Extract images from PDF           → pdfimages CLI or pypdf
├── OCR a scanned PDF                 → pdf2image + pytesseract
├── Compress / reduce file size       → scripts/compress_pdf.py (qpdf + pypdf)
├── View PDF info / metadata          → scripts/pdf_info.py
├── Convert images → PDF              → scripts/images_to_pdf.py (reportlab)
├── Convert PDF → images              → scripts/pdf_to_images.py (pdf2image)
├── Compare / diff two PDFs           → scripts/compare_pdf.py
├── Repair a corrupted PDF            → scripts/repair_pdf.py (qpdf + pypdf)
└── List fonts in a PDF               → scripts/list_fonts.py
```

## Installation

### Linux (Ubuntu/Debian)

```bash
# Python libraries
pip install pypdf pdfplumber reportlab pdf2image pytesseract Pillow --break-system-packages

# System tools
sudo apt-get install -y poppler-utils tesseract-ocr qpdf

# For Chinese OCR
sudo apt-get install -y tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# Node.js (form filling)
npm install pdf-lib
```

### macOS (Homebrew)

```bash
# System tools (required for OCR and CLI operations)
brew install qpdf poppler tesseract

# IMPORTANT: Language packs must be installed separately for non-English OCR
brew install tesseract-lang

# Python libraries
pip install pypdf pdfplumber reportlab pdf2image pytesseract Pillow --break-system-packages

# Node.js (form filling)
npm install pdf-lib
```

> ⚠️ **macOS 注意:** `tesseract-lang` 必须单独安装，否则中文/日文等非英文 OCR 会失败。安装后运行 `tesseract --list-langs` 确认可用语言。

### Verify Installation

```bash
# Check Python libraries
python3 -c "import pypdf, pdfplumber, reportlab, PIL; print('✓ Python libs OK')"

# Check system tools
which qpdf       && echo "✓ qpdf OK"       || echo "✗ qpdf not installed"
which tesseract   && echo "✓ tesseract OK"  || echo "✗ tesseract not installed"
which pdftotext   && echo "✓ poppler OK"    || echo "✗ poppler not installed"

# Check OCR languages
tesseract --list-langs 2>/dev/null | head -5
```

---

## Core Operations

### Read & Extract Text

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

→ For advanced extraction options, see **references/extract.md**

### Extract Tables → DataFrame

```python
import pdfplumber, pandas as pd

with pdfplumber.open("report.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            df = pd.DataFrame(table[1:], columns=table[0])
            print(df)
```

### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    writer.append(PdfReader(path))
with open("merged.pdf", "wb") as f:
    writer.write(f)
```

### Split PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    w = PdfWriter()
    w.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        w.write(f)
```

### Rotate Pages

```python
reader = PdfReader("scan.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.rotate(90)   # 90 / 180 / 270
    writer.add_page(page)
with open("rotated.pdf", "wb") as f:
    writer.write(f)
```

### Password Protect

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("doc.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.encrypt("user_pass", "owner_pass", use_128bit=False)  # AES-256
with open("encrypted.pdf", "wb") as f:
    writer.write(f)
```

---

## CLI Quick Reference (qpdf)

```bash
# Merge
qpdf --empty --pages a.pdf b.pdf -- merged.pdf

# Extract pages 1-5
qpdf input.pdf --pages . 1-5 -- out.pdf

# Rotate all pages 90°
qpdf input.pdf output.pdf --rotate=+90

# Remove password
qpdf --password=secret --decrypt locked.pdf unlocked.pdf

# Linearize (web-optimized)
qpdf --linearize input.pdf output.pdf
```

---

## Available Scripts

Use these scripts directly — no need to rewrite from scratch:

| Script | Purpose |
|---|---|
| `scripts/extract_text.py` | Extract all text, page by page, to .txt |
| `scripts/extract_tables.py` | Extract all tables to .xlsx |
| `scripts/merge_pdfs.py` | Merge multiple PDFs from a glob pattern |
| `scripts/split_pdf.py` | Split by page ranges |
| `scripts/reorder_pdf.py` | Reorder pages (flexible syntax: "3,1,2,4-") |
| `scripts/watermark.py` | Add text or image watermark |
| `scripts/ocr_pdf.py` | Full OCR pipeline for scanned PDFs |
| `scripts/batch_convert.py` | Batch operations (merge/split/rotate) CLI |
| `scripts/check_fillable_fields.py` | List all form fields in a PDF |
| `scripts/fill_pdf_form.py` | Fill AcroForm fields programmatically |
| `scripts/create_test_form.py` | Generate a sample fillable PDF form for testing |
| `scripts/compress_pdf.py` | Compress / optimize PDF to reduce file size |
| `scripts/pdf_info.py` | View PDF metadata, page count, encryption, fonts |
| `scripts/images_to_pdf.py` | Convert images (JPG/PNG/etc.) to PDF |
| `scripts/pdf_to_images.py` | Convert PDF pages to PNG/JPEG images |
| `scripts/compare_pdf.py` | Compare two PDFs and generate diff report |
| `scripts/repair_pdf.py` | Attempt to repair corrupted PDF files |
| `scripts/list_fonts.py` | List all fonts used in a PDF |

Run any script with `--help` to see its options.

---

## Reference Files

Load these when you need deeper guidance:

- **references/create.md** — Building PDFs from scratch with reportlab (Platypus, Canvas, styles, tables, headers/footers)
- **references/extract.md** — Advanced text/table/image extraction, coordinate-based cropping, word-level data
- **references/security.md** — Watermarks, encryption, permissions, digital signatures
- **references/ocr.md** — OCR pipeline, language packs, image preprocessing, quality tuning
- **FORMS.md** — Complete guide to PDF form filling (AcroForm + XFA, pdf-lib JS)

---

## Quick Reference Table

| Task | Best Tool | Key Method |
|---|---|---|
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Merge PDFs | pypdf | `writer.append()` |
| Split PDFs | pypdf | one page per writer |
| Rotate pages | pypdf | `page.rotate(90)` |
| Reorder pages | pypdf | `writer.add_page(reader.pages[i])` |
| Create PDF | reportlab | Platypus or Canvas |
| Watermark | pypdf + reportlab | `page.merge_page()` |
| Encrypt | pypdf | `writer.encrypt()` |
| Fill form | pypdf / pdf-lib | see FORMS.md |
| OCR scanned | pytesseract | see references/ocr.md |
| Compress PDF | qpdf + pypdf | `compress_identical_objects()` |
| View PDF info | pypdf | `PdfReader` metadata + fields |
| Images → PDF | reportlab | `canvas.drawImage()` |
| PDF → images | pdf2image | `convert_from_path()` |
| Compare PDFs | pdfplumber + difflib | text diff per page |
| Repair PDF | qpdf / pypdf | `qpdf --linearize` or re-write |
| List fonts | pypdf | page `/Resources` → `/Font` |
| CLI merge | qpdf | `--empty --pages` |
| Extract images | pypdf / pdfimages | `page.images` |

---

## Common Pitfalls

- **Never use Unicode subscripts/superscripts** (₂, ⁰) in reportlab — use `<sub>` / `<super>` XML tags instead, or they render as black boxes
- **pdfplumber, not pypdf, for text extraction** — pypdf's `extract_text()` loses layout; pdfplumber is layout-aware
- **Encrypted PDFs**: pass `password=` to `PdfReader()` and `pdfplumber.open()`
- **pip in sandbox**: always add `--break-system-packages` flag
- **qpdf for speed**: for large batch jobs, prefer qpdf CLI over Python loops
- **macOS OCR 语言包**: `brew install tesseract` 仅含英文；非英文 OCR 需额外执行 `brew install tesseract-lang`
- **macOS 系统依赖**: OCR 和 CLI 操作需先安装 `brew install qpdf poppler tesseract`
- **测试表单填充**: 没有可填写 PDF 时，先运行 `python scripts/create_test_form.py` 生成测试表单
- **OCR vs pdfplumber**: OCR 只适用于**扫描件**（图片型 PDF）。对原生文本 PDF 提取内容，应使用 `pdfplumber`（更快更准）
- **中文表单填充**: pypdf 内置字体不支持 CJK 字符，中文值可能显示为方块。需要中文表单填充时，使用 pdf-lib (JS) 方案（见 FORMS.md）
- **旋转页面**: 没有独立 rotate 脚本，使用 `python scripts/batch_convert.py rotate input.pdf -d 90`

---

## ⛔ Limitations (Not Suitable For)

| 场景 | 原因 | 替代方案 |
|------|------|----------|
| 复杂排版 PDF（杂志、海报） | 提取会丢失格式布局 | 使用专业排版工具 |
| 扫描件中的表格提取 | OCR 表格精度有限 | 使用专业表格识别工具如 Camelot |
| CJK 字符的表单填充 | pypdf 内置字体不含 CJK | 使用 pdf-lib (JS)，见 FORMS.md |
| 超大 PDF (>500MB) | 内存可能不足 | 用 qpdf CLI 或分批处理 |
