# Batch Format Converter

**Slug:** batch-format-converter
**Name:** Batch Format Converter
**Category:** Productivity / Data Tools
**Tags:** format, conversion, batch, CSV, Excel, JSON, PDF, converter

---

## Description

A powerful batch file format conversion tool that supports converting between CSV, Excel, JSON, PDF, and Markdown formats with one click. Designed for data professionals, analysts, and anyone who frequently works with multiple file formats.

---

## Features

- **Multi-format Support** — Seamless conversion between CSV, Excel (xlsx/xls), JSON, PDF, and Markdown
- **Batch Processing** — Convert multiple files simultaneously with parallel processing
- **Smart Parsing** — Automatic file encoding detection and intelligent table structure recognition
- **PDF OCR** — Extract text from scanned PDFs using Tesseract OCR
- **Feishu Integration** — Push conversion results and notifications to Feishu channels via webhook
- **YAML Configuration** — Easy-to-use configuration file for all conversion settings
- **CLI Interface** — Full command-line interface for automation and scripting
- **Progress Tracking** — Real-time progress bar for batch operations

---

## Pricing

| Plan   | Price     | Features                                          |
|--------|-----------|---------------------------------------------------|
| FREE   | ¥0        | Up to 10 files per batch, single format pair      |
| STD    | ¥9.9/mo   | Up to 100 files per batch, all format pairs       |
| PRO    | ¥29/mo    | Unlimited files, OCR enabled, Feishu push         |
| MAX    | ¥69/mo    | Everything in PRO + API access + priority support |

---

## Requirements

```
pandas>=2.0.0
openpyxl>=3.0.0
python-docx>=1.0.0
pytesseract>=0.3.10
pdf2image>=1.16.0
Pillow>=10.0.0
requests>=2.28.0
```

**System-level dependencies:**
- Tesseract OCR (for PDF text extraction)
  - Ubuntu/Debian: `sudo apt install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

---

## Quick Start

**1. Install**
```bash
pip install -r requirements.txt
```

**2. Configure**
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your settings
```

**3. Use as Python Library**
```python
from converter import BatchConverter

converter = BatchConverter()

# Single file conversion
converter.convert("data.csv", "output.xlsx")

# Batch conversion
converter.batch_convert(
    input_files=["file1.csv", "file2.json", "file3.xlsx"],
    target_format="pdf",
    output_dir="./results"
)
```

**4. Use as CLI**
```bash
# Single file
python main.py convert input.csv --output output.xlsx

# Batch mode
python main.py batch --input ./folder --format pdf --output ./results

# With Feishu push
python main.py batch --input ./data --format xlsx --feishu
```

---

## Supported Formats

| Input \\ Output | CSV | Excel | JSON | PDF | Markdown |
|-----------------|-----|-------|------|-----|----------|
| CSV             | —   | ✓     | ✓    | ✓   | ✓        |
| Excel           | ✓   | —     | ✓    | ✓   | ✓        |
| JSON            | ✓   | ✓     | —    | ✓   | ✓        |
| PDF             | ✓   | ✓     | ✓    | —   | ✓        |
| Markdown        | ✓   | ✓     | ✓    | ✓   | —        |

---

## Configuration Options

```yaml
conversion:
  default_encoding: utf-8
  excel_engine: openpyxl
  pdf_dpi: 300
  ocr_enabled: true
  ocr_lang: chi_sim+eng

feishu:
  enabled: false
  webhook_url: ""
  push_results: true

output:
  overwrite: false
  output_dir: ./output
  preserve_structure: true
```
