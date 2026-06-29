---
name: excel-to-pdf
description: Convert Excel (.xlsx) sign-in sheets and rosters to print-ready A4 PDFs with Chinese font support. Use when the user needs to (1) convert an Excel table/roster/sign-in sheet to PDF for printing, (2) generate A4 PDF from .xlsx with table formatting, (3) batch export Excel sheets to PDF with Chinese text. Triggers on requests like "turn this Excel into PDF", "print this table as PDF", "convert xlsx to pdf for printing", "generate a printable PDF from this spreadsheet".
---

# Excel → A4 PDF Converter

Convert Excel spreadsheets to print-ready A4 PDF tables with proper Chinese rendering. Column headers keep their original text (no English translation).

## Quick start

Run the bundled script directly on the Excel file:

```powershell
python scripts/excel_to_pdf_signin.py "C:\path\to\file.xlsx"
```

The script auto-detects:
- Column layout (drops empty/merged placeholder columns)
- Page orientation (landscape for ≥7 columns or >35 rows)
- Chinese system font (Windows: Microsoft YaHei; macOS: PingFang; Linux: Noto CJK)
- Output path (same directory, same name, `.pdf` extension)

## Common options

```powershell
# Set custom title and wider margins
python scripts/excel_to_pdf_signin.py roster.xlsx --title "签到表" --margin 12

# Force landscape, higher rows for manual sign-in
python scripts/excel_to_pdf_signin.py signin.xlsx --orientation LANDSCAPE --row-height 8

# Pick specific columns (0-based indices), custom widths
python scripts/excel_to_pdf_signin.py sheet.xlsx --columns 0,1,2,3,7,8 --col-widths 0.1,0.2,0.15,0.2,0.2,0.15

# Larger font for sparse data (e.g. room lists)
python scripts/excel_to_pdf_signin.py rooms.xlsx --font-size 12 --margin 12 --row-height 8

# Explicit output path
python scripts/excel_to_pdf_signin.py data.xlsx --out "D:\output\result.pdf"

# Specific sheet (for multi-sheet workbooks)
python scripts/excel_to_pdf_signin.py multi.xlsx --sheet "1号台"

# Custom column widths (13 columns, give more space to 学号/电话 to avoid wrapping)
python scripts/excel_to_pdf_signin.py roster.xlsx --col-widths 0.07,0.13,0.10,0.10,0.04,0.05,0.10,0.07,0.08,0.04,0.05,0.09,0.08
```

## Decision guide

### Orientation
- **Portrait (default)**: ≤6 columns and ≤35 rows — typical for sign-in sheets
- **Landscape**: ≥7 columns or >35 rows

### Margins
- Crowded tables: `--margin 5`
- Normal: `--margin 8` (default)
- Sparse data (room lists, etc.): `--margin 12`

### Row height
- Dense sign-in sheets: `--row-height 6` (default)
- Hand-writing sign-in sheets (needs space): `--row-height 8`
- Room/roster lists (fewer rows): `--row-height 10`

### Column selection
- The `--columns` flag takes 0-based indices (A=0, B=1, ...).
- If omitted, the script auto-drops columns where both header AND all data rows are empty.
- Typical sign-in sheet (skip sign-number placeholder columns): `--columns 0,1,2,3,7,8`

### Column widths
- Equal width by default: `usable_width / ncols`
- Use `--col-widths` with ratios summing to ~1.0 to allocate more space to wide columns (学号, 电话, 导师, 院系) and less to narrow ones (性别, 年度).

## Full reference

```
usage: excel_to_pdf_signin.py EXCEL [options]

Options:
  --title TEXT         PDF title (default: derived from filename)
  --orientation PORTRAIT|LANDSCAPE  (default: auto-detect)
  --margin N           Page margin in mm (default: 8)
  --row-height N       Row top/bottom padding in pt (default: 6)
  --columns LIST       Column indices (0-based), comma-separated
  --col-widths LIST    Column width ratios, comma-separated
  --font PATH          Chinese .ttf/.ttc file path
  --font-size N        Cell font size in pt (default: 10)
  --sheet TEXT         Sheet name to process (default: active sheet)
  --out PATH           Output PDF path
```

## Output style

All generated PDFs share:
- Blue header row (`#4472C4`) with white text
- White body background with black grid borders
- Center-aligned text throughout
- Bold bottom border on header row
- Original Chinese column headers preserved (no translation)

## Dependencies

Install once per environment:

```bash
pip install openpyxl reportlab
```

Requires a Chinese-capable font on the system (auto-detected).
