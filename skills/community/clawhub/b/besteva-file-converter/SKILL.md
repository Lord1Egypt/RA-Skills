---
name: file-converter
version: 1.0.0
description: >
  This skill provides comprehensive file format conversion capabilities. 
  It should be used when users need to convert files between different formats,
  including PDF to Word, Word to PDF, image format conversions (PNG/JPG/WebP/BMP/GIF/TIFF),
  and Excel/CSV bidirectional conversion. Supports both single file and batch processing.
  Trigger keywords: 转换, convert, 格式转换, PDF转Word, Word转PDF, 图片转换, Excel转CSV, CSV转Excel.
---

# File Converter Skill

A comprehensive file format conversion toolkit supporting documents, images, and spreadsheets.

## When to Use

Activate this skill when any of these scenarios occur:

- **Document conversion**: User wants to convert between PDF and Word formats
- **Image conversion**: User needs images in a different format (PNG→JPG, JPG→WebP, etc.)
- **Spreadsheet conversion**: User needs to exchange data between Excel and CSV
- **Batch operations**: User has multiple files that need converting at once
- **Format queries**: User asks about supported formats or how to convert specific file types

## Supported Conversions

| Source Format | Target Format | Script | Notes |
|--------------|---------------|--------|-------|
| `.pdf` | `.docx` | `scripts/pdf_to_word.py` | Extracts text, tables, layout |
| `.docx`, `.doc` | `.pdf` | `scripts/word_to_pdf.py` | Requires MS Word on Windows |
| PNG/JPEG/WebP/BMP/GIF/TIFF | Any other image format | `scripts/image_converter.py` | Quality control, resize support |
| `.csv` | `.xlsx` | `scripts/excel_csv_converter.py` | Custom delimiter/encoding |
| `.xlsx`, `.xls` | `.csv` | `scripts/excel_csv_converter.py` | Multi-sheet support |

## Prerequisites

### Python Dependencies

Install required packages before first use:

```bash
pip install Pillow pdf2docx docx2pdf openpyxl xlrd
```

**Quick install command:**
```bash
pip install Pillow pdf2docx docx2pdf openpyxl xlrd
```

### Platform-Specific Requirements

- **Word → PDF (Windows)**: Microsoft Word must be installed (`docx2pdf` uses COM automation)
- **PDF → Word**: No external software required; uses `pdf2docx`
- **Image conversion**: Uses `Pillow` only, works on all platforms

## Workflow Guidelines

### Step 1: Identify Conversion Type

Determine what the user wants to convert:

```
User says "convert this PDF"        → PDF to Word
User says "turn this into PDF"       → Word to PDF  
User says "change this PNG to JPG"   → Image conversion
User says "export this Excel as CSV" → Excel to CSV
```

### Step 2: Check Dependencies

Before running any script, verify required packages are installed:

```bash
python -c "import PIL; import pdf2docx; import docx2pdf; import openpyxl"
```

If imports fail, prompt user to run:
```bash
pip install Pillow pdf2docx docx2pdf openpyxl xlrd
```

### Step 3: Execute Appropriate Script

#### PDF → Word

**Single file:**
```bash
python scripts/pdf_to_word.py <input.pdf> [output.docx]
```

**Batch mode:**
```bash
python scripts/pdf_to_word.py --batch ./pdf_folder --output-dir ./output_folder
```

**Options:**
- `--start N`: Start from page N (default: 0)
- `--end N`: End at page N (default: all pages)

#### Word → PDF

**Single file:**
```bash
python scripts/word_to_pdf.py <input.docx> [output.pdf]
```

**Batch mode:**
```bash
python scripts/word_to_pdf.py --batch ./docs_folder --output-dir ./pdfs_folder
```

**Check requirements:**
```bash
python scripts/word_to_pdf.py --check
```

#### Image Format Conversion

**Single file:**
```bash
python scripts/image_converter.py <input_image> --format <target_format>
```

**Batch mode:**
```bash
python scripts/image_converter.py --batch ./images_dir --format webp --output-dir ./webp_dir
```

**Target formats:** `png`, `jpg`/`jpeg`, `webp`, `bmp`, `gif`, `tiff`/`tif`

**Options:**
- `-q/--quality N`: Quality for lossy formats (1-100, default: 95)
- `--resize WIDTH HEIGHT`: Resize dimensions
- `--no-optimize`: Disable optimization
- `--info`: Display image info without converting

**Examples:**
```bash
# High-quality JPEG compression
python scripts/image_converter.py photo.png --format jpg -q 90

# Convert to WebP with smaller size
python scripts/image_converter.py photo.png --format webp -q 80

# Resize while converting
python scripts/image_converter.py large.png --format jpg --resize 1920 1080

# View image info
python scripts/image_converter.py image.png --info
```

#### Excel ↔ CSV

**CSV → Excel:**
```bash
python scripts/excel_csv_converter.py data.csv --format xlsx [options]
```

**Excel → CSV:**
```bash
python scripts/excel_csv_converter.py data.xlsx --format csv [options]
```

**Batch mode:**
```bash
python scripts/excel_csv_converter.py --batch ./data_dir --format csv
```

**Options:**
- `-d/--delimiter CHAR`: Custom separator (default: comma)
- `-e/--encoding ENC`: File encoding (default: utf-8)
- `--sheet NAME`: Specific sheet name (Excel→CSV)
- `--sheet-name NAME`: Output sheet name (CSV→Excel)
- `--no-header`: Skip header row
- `--info`: Show Excel structure info

**Examples:**
```bash
# European-style CSV (semicolon delimited)  
python scripts/excel_csv_converter.py data.csv --format xlsx -d ";"

# Chinese encoding support
python scripts/excel_csv_converter.py data.xlsx --format csv -e gbk

# Export specific sheet
python scripts/excel_csv_converter.py workbook.xlsx --format csv -s "Sales Report"

# View Excel info
python scripts/excel_csv_converter.py data.xlsx --info
```

### Step 4: Verify Results

After each conversion:

1. Confirm output file(s) exist at expected location(s)
2. Report file sizes to user (original vs converted)
3. For batch operations, report success count vs total count
4. If errors occurred, summarize them clearly

## Error Handling

### Common Issues and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing package | Run `pip install <package>` |
| `COMError` (Word→PDF) | MS Word not installed | Install MS Office or use alternative |
| `UnicodeDecodeError` | Wrong encoding | Specify correct `--encoding` |
| `FileNotFoundError` | Wrong path | Verify input path is absolute or relative correctly |
| Permission denied | Read-only directory | Use writable output directory |

### Encoding Guide

When dealing with non-UTF-8 files, common encodings:
- Chinese Windows: `gbk` / `gb18030`
- Western Europe: `latin-1` / `cp1252`
- Japanese: `shift-jis` / `cp932`
- Auto-detect: Try `utf-8` first, then fallback

## Best Practices

1. **Always use absolute paths** when calling scripts to avoid path confusion
2. **Create output directories** before batch operations if they don't exist
3. **Check dependencies once** at start of session, not before every call
4. **Report results clearly** with file paths, sizes, and success/failure counts
5. **Handle transparency** appropriately — JPEG doesn't support alpha channels
6. **Preserve quality** defaults are high (95%) but adjust based on use case
