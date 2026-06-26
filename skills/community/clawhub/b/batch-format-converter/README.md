# Batch Format Converter · 格式批量互转

A powerful batch file format conversion tool that supports converting between CSV, Excel, JSON, PDF, and Markdown formats with one click.

一款强大的批量文件格式转换工具，支持 CSV、Excel、JSON、PDF、Markdown 之间的互相转换，一键批量处理。

---

## Features · 功能特点

- **Multi-format Support** — Convert between CSV, Excel (xlsx/xls), JSON, PDF, and Markdown
- **Batch Processing** — Convert multiple files at once with parallel processing
- **Smart Parsing** — Auto-detect file encoding and table structures
- **PDF OCR** — Extract text from scanned PDFs using OCR
- **Feishu Integration** — Push conversion results to Feishu channels
- **Configurable** — YAML-based configuration for all conversion settings

---

## Installation · 安装步骤

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and edit configuration
cp config.yaml.example config.yaml
# Then edit config.yaml with your settings
```

---

## Configuration · 配置说明

Edit `config.yaml` to configure:

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

---

## Quick Start · 快速开始

```python
from converter import BatchConverter

# Initialize converter
converter = BatchConverter()

# Convert single file
converter.convert("data.csv", "output.xlsx")

# Batch convert
converter.batch_convert(
    input_files=["file1.csv", "file2.json"],
    target_format="xlsx",
    output_dir="./results"
)
```

**CLI Usage:**
```bash
python main.py convert input.csv --output output.xlsx
python main.py batch --input ./files --format pdf
```

---

## Supported Formats · 支持格式

| Input \\ Output | CSV | Excel | JSON | PDF | Markdown |
|-----------------|-----|-------|------|-----|----------|
| CSV             | —   | ✓     | ✓    | ✓   | ✓        |
| Excel           | ✓   | —     | ✓    | ✓   | ✓        |
| JSON            | ✓   | ✓     | —    | ✓   | ✓        |
| PDF             | ✓   | ✓     | ✓    | —   | ✓        |
| Markdown        | ✓   | ✓     | ✓    | ✓   | —        |

---

## Notes · 注意事项

1. **PDF OCR** requires Tesseract OCR to be installed on the system
2. Large file conversion may take longer; batch processing has a progress bar
3. Excel files with multiple sheets: convert the active sheet by default
4. Configure Feishu webhook before enabling Feishu push
5. Use `preserve_structure: true` to maintain nested JSON structure during conversion
-e 
> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
