---
name: excel-builder
description: Build .xlsx files with formulas, merged cells, data validation, conditional formatting, pivot tables, and charts. Use when creating Excel spreadsheets, financial tables, data entry forms, or any structured .xlsx deliverable requiring formulas or formatting.
license: MIT
metadata:
  version: "1.0.0"
  domain: document-generation
  triggers: Excel, xlsx, spreadsheet, formula, pivot table, chart, data validation, conditional formatting, openpyxl, xlsxwriter, merged cells, workbook
  role: builder
  scope: implementation
  output-format: xlsx
  related-skills: financial-model-builder, data-analysis-report, pdf-report-generator
---

# Excel Builder

Builds structured `.xlsx` files programmatically using Python libraries (openpyxl or xlsxwriter).

## When to Use This Skill

- Creating Excel spreadsheets with formulas and calculated fields
- Building financial tables, budgets, or invoices
- Generating data entry forms with validation and dropdowns
- Producing reports with charts (bar, line, pie, scatter)
- Exporting structured data with conditional formatting or color coding
- Building pivot-ready data tables

## Core Workflow

1. **Choose library** — Use `openpyxl` for reading/modifying existing files; use `xlsxwriter` for new write-only files with rich charts
2. **Design structure** — Define sheets, columns, headers, and data rows before writing
3. **Write data** — Populate cells row by row; apply number formats (`"#,##0.00"`, `"YYYY-MM-DD"`)
4. **Add formulas** — Use Excel formula strings: `=SUM(B2:B100)`, `=IF(A2>0, "Yes", "No")`
5. **Format** — Apply styles: bold headers, column widths, merged cells, fill colors, borders
6. **Validate** — Add data validation (dropdown lists, numeric ranges) where applicable
7. **Charts** — Add charts referencing data ranges; set titles and axis labels
8. **Save and verify** — Save to output path; confirm file exists and is non-zero bytes

## Key Patterns

### openpyxl (read/write existing)
```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.active
ws.title = "Report"
ws["A1"] = "Revenue"
ws["A1"].font = Font(bold=True, size=12)
ws.column_dimensions["A"].width = 20
wb.save("output.xlsx")
```

### xlsxwriter (new files with charts)
```python
import xlsxwriter
wb = xlsxwriter.Workbook("output.xlsx")
ws = wb.add_worksheet("Summary")
bold = wb.add_format({"bold": True, "bg_color": "#4472C4", "font_color": "white"})
ws.write("A1", "Month", bold)
chart = wb.add_chart({"type": "column"})
chart.add_series({"values": "=Summary!$B$2:$B$13", "name": "Revenue"})
ws.insert_chart("D2", chart)
wb.close()
```

## Error Handling

- If `openpyxl` not installed: `pip install openpyxl`
- If `xlsxwriter` not installed: `pip install xlsxwriter`
- Always wrap `wb.save()` in try/except; report path conflicts
- Verify output with `os.path.getsize(path) > 0` before returning

## Output

Return the absolute path to the saved `.xlsx` file. If generating multiple sheets, list each sheet name and row count in a brief summary.
