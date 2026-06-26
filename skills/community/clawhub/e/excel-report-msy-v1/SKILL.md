---
name: excel-report
description: Create formatted Excel report workbooks from CSV files using openpyxl. Use when the user provides or references a .csv file and asks to convert it to .xlsx, make an Excel report, add header styling, comma number formats, numeric total rows, or a simple chart.
---

# Excel Report

Convert CSV files into polished Excel `.xlsx` reports with the bundled `openpyxl` script.

## Workflow

1. Locate the input CSV file and decide an output `.xlsx` path. Default to the same basename beside the CSV unless the user specifies otherwise.
2. Use the bundled script:

```bash
python3 /home/ubuntu/.openclaw/workspace/skills/excel-report/scripts/csv_to_excel_report.py input.csv output.xlsx
```

3. Verify the workbook was created. For important outputs, inspect the workbook with `openpyxl` or run a quick file check.
4. Return the generated `.xlsx` file path, and attach it with `MEDIA:<path>` when replying in a channel that supports file delivery.

## What the script does

- Reads CSV with UTF-8 BOM support and delimiter sniffing.
- Creates an Excel workbook with a `Report` sheet.
- Styles the header row with a dark blue fill and white bold text.
- Converts numeric-looking cells to numbers and applies thousands separators.
- Adds a bold total row with `SUM` formulas for numeric columns.
- Adds a simple bar chart for the first numeric column using the first column as categories, limited to the first 10 data rows.
- Adds an Excel table, filters, frozen header row, and autosized columns.

## Options

- Omit the output path to create `input.xlsx` beside the CSV.
- Use `--sheet-name "Name"` to set the worksheet title.

## Dependency

The script requires `openpyxl`. If it is missing, install it in the active Python environment before running:

```bash
python3 -m pip install openpyxl
```

Do not use pandas for the core conversion unless the user explicitly asks; this skill is designed around `openpyxl`.
