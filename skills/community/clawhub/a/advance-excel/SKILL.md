---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files into proper spreadsheets."
---

# XLSX Creation, Editing, and Analysis

## Step 0: Always Inspect First

Before reading or writing any unknown Excel file, run:

```bash
python skills/xlsx/scripts/inspect.py file.xlsx
```

This returns sheet names, merged cell ranges, the detected header row, formula count, and named ranges — essential for picking the right strategy. Check the `recommendations` field for immediate guidance.

## Library Selection

| Task | Library |
|---|---|
| Read + analyse data (clean file) | `pandas` |
| Inspect structure before deciding | `inspect.py` → then below |
| Read calculated values only | `openpyxl(data_only=True)` — **never save after** |
| Edit existing file | `openpyxl` → `recalc.py` |
| Create new complex file from scratch | `xlsxwriter` |
| Large files (100k+ rows) | `openpyxl(read_only=True)` or pandas chunking |

## Reading and Analysing Data

### Standard read
```python
import pandas as pd

df = pd.read_excel('file.xlsx')                          # first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None) # all sheets as dict
```

### Header not at row 0 (metadata/logos above data)

`inspect.py` reports `detected_header_row`. Use it:

```python
# inspect.py said detected_header_row: 3
df = pd.read_excel('file.xlsx', header=3)
```

Manual detection when uncertain:
```python
df_peek = pd.read_excel('file.xlsx', header=None, nrows=15)
header_row = int(df_peek.notna().sum(axis=1).idxmax())
df = pd.read_excel('file.xlsx', header=header_row)
```

### Merged cells

`inspect.py` flags merged ranges. Unmerge-and-fill before reading with pandas, otherwise merged cells produce `NaN`:

```python
from openpyxl import load_workbook

def unmerge_and_fill(ws):
    for merge in list(ws.merged_cells.ranges):
        top_left = ws.cell(merge.min_row, merge.min_col).value
        ws.unmerge_cells(str(merge))
        for row in ws.iter_rows(merge.min_row, merge.max_row,
                                merge.min_col, merge.max_col):
            for cell in row:
                cell.value = top_left

wb = load_workbook('file.xlsx')
for ws in wb.worksheets:
    unmerge_and_fill(ws)
wb.save('file_unmerged.xlsx')

import pandas as pd
df = pd.read_excel('file_unmerged.xlsx')
```

### Multi-level headers
```python
df = pd.read_excel('file.xlsx', header=[0, 1])  # two header rows
```

### Named ranges
```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx', data_only=True)
dn = wb.defined_names['TotalRevenue']
for sheet_title, coord in dn.destinations:
    ws = wb[sheet_title]
    print(ws[coord].value)
```

### Large files (read_only mode)
```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx', read_only=True)
ws = wb.active
for row in ws.iter_rows(values_only=True):
    process(row)
wb.close()  # always close read_only workbooks explicitly
```

### Two-pass pattern for calculated values + editing

**Never open with `data_only=True` and then save — formulas are permanently destroyed.**

```python
from openpyxl import load_workbook

# Pass 1: snapshot calculated values (read-only, never saved)
wb_vals = load_workbook('file.xlsx', data_only=True)
ws_vals = wb_vals.active
values = {cell.coordinate: cell.value
          for row in ws_vals.iter_rows() for cell in row}
wb_vals.close()

# Pass 2: edit the formula workbook (formulas intact)
wb = load_workbook('file.xlsx')
ws = wb.active
# reference `values['B5']` etc. for current calc results
ws['A1'] = 'Updated'
wb.save('output.xlsx')
```

## Writing Excel Files

### Editing existing files (openpyxl)
```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
ws = wb.active  # or wb['SheetName']

ws['A1'] = 'New Value'
ws.insert_rows(2)
ws.delete_cols(3)

new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
# Always recalculate after editing if formulas are present:
# python skills/xlsx/scripts/recalc.py modified.xlsx
```

### Creating new files from scratch (xlsxwriter — preferred for new files)

Use `xlsxwriter` when building a new file. It is faster, has richer chart/format APIs, and produces cleaner output than openpyxl for new workbooks.

```python
import xlsxwriter

wb = xlsxwriter.Workbook('output.xlsx')
ws = wb.add_worksheet('Summary')

# Formats
header_fmt = wb.add_format({'bold': True, 'bg_color': '#505050', 'font_color': 'white'})
yellow_fmt = wb.add_format({'bg_color': '#f2e358'})
currency_fmt = wb.add_format({'num_format': '$#,##0'})

# Write headers
for col, name in enumerate(['SKU', 'Description', 'Revenue']):
    ws.write(0, col, name, header_fmt)

# Write data
data = [['SKU-001', 'Widget A', 12500], ['SKU-002', 'Widget B', 8300]]
for row_idx, row in enumerate(data, start=1):
    ws.write(row_idx, 0, row[0])
    ws.write(row_idx, 1, row[1])
    ws.write(row_idx, 2, row[2], currency_fmt)

# Formula
ws.write_formula(len(data) + 1, 2, f'=SUM(C2:C{len(data) + 1})', currency_fmt)

# Column widths
ws.set_column('A:A', 12)
ws.set_column('B:B', 30)
ws.set_column('C:C', 14)

wb.close()
```

### Conditional formatting (xlsxwriter)
```python
# Highlight cells above threshold
ws.conditional_format('C2:C100', {
    'type': 'cell',
    'criteria': '>',
    'value': 10000,
    'format': wb.add_format({'bg_color': '#f2e358'}),
})

# Color scale
ws.conditional_format('C2:C100', {
    'type': '3_color_scale',
    'min_color': '#ffffff',
    'mid_color': '#f6ea86',
    'max_color': '#f2e358',
})
```

### Data validation / dropdown lists (xlsxwriter)
```python
ws.data_validation('D2:D100', {
    'validate': 'list',
    'source': ['Active', 'Inactive', 'Pending'],
})
```

### Freeze panes and auto-filter
```python
ws.freeze_panes(1, 0)       # freeze row 1
ws.autofilter('A1:Z1')      # filter on header row
```

### Conditional formatting (openpyxl — when editing existing file)
```python
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.styles import PatternFill

rule = CellIsRule(
    operator='greaterThan', formula=['10000'],
    fill=PatternFill(start_color='f2e358', end_color='f2e358', fill_type='solid')
)
ws.conditional_formatting.add('C2:C100', rule)
```

### Data validation (openpyxl — when editing existing file)
```python
from openpyxl.worksheet.datavalidation import DataValidation

dv = DataValidation(type='list', formula1='"Active,Inactive,Pending"', showDropDown=False)
ws.add_data_validation(dv)
dv.add('D2:D100')
```

## Recalculating Formulas

**Mandatory after any openpyxl edit that involves formulas:**

```bash
python skills/xlsx/scripts/recalc.py output.xlsx
```

The script:
- Runs LibreOffice headless to recalculate all formulas
- Scans every cell for `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`, `#NUM!`, `#NULL!`
- Returns JSON — if `status` is `errors_found`, fix the listed cells and recalc again

`xlsxwriter` files do **not** need recalc — they never contain unresolved formula strings.

## CRITICAL: Use Formulas, Not Hardcoded Values

```python
# WRONG
sheet['B10'] = df['Sales'].sum()

# CORRECT
sheet['B10'] = '=SUM(B2:B9)'
```

## Corvera Branding

When creating spreadsheets for reports or deliverables, apply Corvera brand styling. Reference `skills/corvera-brand/` for the full brand kit. Quick summary:

- **Header rows:** Charcoal (#505050) background, white text, Poppins font (Bold)
- **Accent rows/highlights:** Yellow (#f2e358) or Pale Yellow (#f6ea86) background
- **Body text:** Charcoal (#505050) colour, Poppins font (Regular)
- **Background:** White (#ffffff) or Oatmeal (#f7f0e6) for alternating rows

## Charts with Spreadsheets

For visual data summaries alongside spreadsheets, reference `skills/data-visualization/` for chart type selection and brand styling.

**Embedded Excel charts (xlsxwriter — preferred):**
```python
chart = wb.add_chart({'type': 'column'})
chart.add_series({
    'name': 'Revenue',
    'categories': '=Summary!$A$2:$A$13',
    'values': '=Summary!$C$2:$C$13',
    'fill': {'color': '#f2e358'},
})
chart.set_title({'name': 'Monthly Revenue'})
ws.insert_chart('E2', chart)
```

**Embedded Excel charts (openpyxl — when editing existing):**
```python
from openpyxl.chart import BarChart, Reference
chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_row=13)
chart.add_data(data, titles_from_data=True)
chart.series[0].graphicalProperties.solidFill = 'f2e358'
ws.add_chart(chart, 'E2')
```

## Requirements for Outputs

### All Excel files

- Use Poppins if available, otherwise Arial for all deliverables
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Study and EXACTLY match existing format, style, and conventions when modifying files

### Financial Models

**Color coding:**
- **Blue (0,0,255):** Hardcoded inputs
- **Black (0,0,0):** Formulas and calculations
- **Green (0,128,0):** Links from other worksheets
- **Red (255,0,0):** External links to other files
- **Yellow background (255,255,0):** Key assumptions

**Number formatting:**
- Years: text strings ("2024" not "2,024")
- Currency: `$#,##0` — always include units in headers ("Revenue ($mm)")
- Zeros: use `$#,##0;($#,##0);-` to display as `-`
- Percentages: `0.0%`
- Multiples: `0.0x`
- Negative numbers: parentheses (123) not minus -123

**Formula rules:**
- Place ALL assumptions in separate cells; use cell references not hardcoded values
- Comment beside hardcoded values: "Source: [System], [Date], [Reference]"

## Formula Verification Checklist

- [ ] Run `inspect.py` before editing an unfamiliar file
- [ ] Test 2-3 sample references before building full model
- [ ] Confirm Excel columns match expected (column 64 = BL, not BK)
- [ ] Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)
- [ ] Check for NaN before division (`pd.notna()`)
- [ ] Verify cross-sheet references use correct format (`Sheet1!A1`)
- [ ] Run `recalc.py` after every openpyxl edit with formulas

## Code Style

- Write minimal, concise Python without unnecessary comments
- Avoid verbose variable names and redundant operations
- Add comments to cells with complex formulas or important assumptions
