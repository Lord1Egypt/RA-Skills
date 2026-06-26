# Table & Data Extractor — Reference Guide

## Purpose
Detect, extract, clean, and output structured tabular data from PDFs, images, HTML, and text documents as CSV, JSON, or Markdown. Handle merged cells, multi-level headers, footnotes, and multi-table documents.

---

## Step 1 — Source Type Detection

| Source Type | Detection Method | Extraction Approach |
|---|---|---|
| Native PDF (text layer) | Run table_extractor.py — pdfplumber detects table borders and text positioning | Script → CSV/JSON |
| Scanned PDF / image PDF | pdfplumber may return empty or garbled — fallback to visual read | Visual extraction |
| Image (screenshot, photo) | Read visually | Visual extraction |
| HTML with `<table>` tags | Read HTML structure | Parse `<td>`, `<th>`, `<tr>` tags |
| Markdown tables | `|` pipe character rows | Parse pipe-delimited rows |
| Plain text with alignment | Column alignment by whitespace | Parse fixed-width columns |
| CSV / TSV uploaded | Already structured | Validate, clean, and summarize |
| Excel screenshot | Visible grid with cell borders | Visual extraction |

---

## Step 2 — Run Extraction Script (PDF)

```bash
# Basic extraction — auto-detect all tables, output as CSV
python skills/doc-process/scripts/table_extractor.py --file document.pdf --output data.csv

# JSON output
python skills/doc-process/scripts/table_extractor.py --file document.pdf --output data.json --format json

# Specific page range
python skills/doc-process/scripts/table_extractor.py --file document.pdf --output data.csv --pages 3-8

# List all tables without extracting
python skills/doc-process/scripts/table_extractor.py --file document.pdf --list

# Extract only the second table
python skills/doc-process/scripts/table_extractor.py --file document.pdf --output data.csv --table 2
```

---

## Step 3 — Visual / Manual Extraction

For images and scanned PDFs, extract each table visually:

### Table Inventory
First, list all tables found in the document:
| Table # | Page / Location | Title / Caption | Approx. Rows | Approx. Cols | Table Type |
|---|---|---|---|---|---|

**Table type classification:**
- **Data table**: rows = records, columns = attributes (most common)
- **Cross-tab / pivot**: row and column headers both meaningful (e.g., sales by region × quarter)
- **Summary / totals table**: contains subtotals and grand totals
- **Schedule / calendar table**: time-based rows or columns
- **Comparison table**: yes/no or metric comparisons across options
- **Financial statement**: income statement, balance sheet, cash flow

### Column Header Handling

**Simple headers (1 row):**
Extract verbatim. Clean trailing whitespace and newlines within cells.

**Multi-level / merged headers:**
Flatten by concatenating parent + child header:
```
Revenue          → Q1 Revenue, Q2 Revenue, Q3 Revenue, Q4 Revenue
  Q1  Q2  Q3  Q4
```

**Rotated headers:**
Some tables have column headers rotated 90°. Read each header individually and note rotation.

**No header row:**
Generate generic names: `Column1, Column2, …, ColumnN`. Note in output:
"No header row detected — generic column names used. Please rename as needed."

---

## Step 4 — Data Cleaning Rules

Apply these cleaning rules to every extracted cell:

| Issue | Rule |
|---|---|
| Leading/trailing whitespace | Strip |
| Internal line breaks within a cell | Join with space (or `\n` if content is list-like) |
| Multiple spaces | Normalize to single space |
| Empty cell | Output as empty string `""` (not "N/A", "null", "—" unless that was the original value) |
| Dash-only cell `—` or `-` | Preserve as-is — may represent zero or absence |
| Numbers with thousands separators | Preserve as-is in CSV (e.g., `1,234.56`); optionally parse to float in JSON |
| Numbers with currency symbols | Preserve (e.g., `$1,234.56`); optionally parse in JSON |
| Percentage values | Preserve as-is (e.g., `12.5%`); optionally parse as 0.125 in JSON |
| Date values | Preserve original format; note detected format |
| Footnote markers (*, †, ‡, 1, a) | Keep in cell; list footnote text after the table |
| Merged cell spanning N rows | Repeat the value in each spanned row |
| Merged cell spanning N columns | Distribute the value to the first column; leave others empty |
| HTML entities | Decode (`&amp;` → `&`, `&lt;` → `<`) |

---

## Step 5 — Data Type Inference

For each column, infer the data type:
| Column | Detected Type | Sample Values | Notes |
|---|---|---|---|
| Date | Date (YYYY-MM-DD) | 2024-01-15, 2024-02-01 | |
| Revenue | Numeric (currency) | $1,234.56, $2,100.00 | USD |
| Growth | Numeric (percent) | 12.5%, -3.2% | |
| Category | Categorical (text) | Q1, Q2, Q3, Q4 | 4 distinct values |
| Notes | Free text | Varies | |

---

## Step 6 — Statistical Summary (on request or if applicable)

For numeric columns, provide:
| Column | Min | Max | Mean | Median | Sum | Non-null Count |
|---|---|---|---|---|---|---|

For categorical columns:
| Column | Unique Values | Top Value | Frequency |
|---|---|---|---|

---

## Step 7 — Multiple Table Handling

If more than one table is found:

**Separate output strategy:**
- Present each table individually with its title
- Ask if user wants all tables in one file or separate files
- For CSV: use comment headers `# Table 1: [title]` between tables
- For JSON: array of table objects

**Related tables:**
If tables share a key column, note: "Table 1 and Table 3 share the 'Product ID' column — they can be joined."

**Summary tables:**
If a table is clearly a summary of another (same columns, fewer rows with totals), flag this relationship.

---

## Step 8 — Output Formats

### CSV
```
# Table 1: Quarterly Revenue by Region
Region,Q1 Revenue,Q2 Revenue,Q3 Revenue,Q4 Revenue,Total
North America,"$1,234,567","$1,456,789","$1,567,890","$1,890,123","$6,149,369"
Europe,"$876,543","$923,456","$998,765","$1,123,456","$3,922,220"
```

**CSV spec compliance:**
- Fields with commas, quotes, or newlines enclosed in double quotes
- Internal double quotes escaped by doubling: `"He said ""hello"""`
- UTF-8 encoding
- LF line endings

### JSON
```json
{
  "table_title": "Quarterly Revenue by Region",
  "source": "annual_report.pdf",
  "page": 4,
  "headers": ["Region", "Q1 Revenue", "Q2 Revenue", "Q3 Revenue", "Q4 Revenue", "Total"],
  "column_types": {
    "Region": "categorical",
    "Q1 Revenue": "currency_USD",
    "Total": "currency_USD"
  },
  "rows": [
    {"Region": "North America", "Q1 Revenue": 1234567, "Q2 Revenue": 1456789, "Q3 Revenue": 1567890, "Q4 Revenue": 1890123, "Total": 6149369}
  ],
  "row_count": 2,
  "footnotes": ["* Excludes intercompany transactions"],
  "extraction_notes": []
}
```

### Markdown (for inline display)
```markdown
| Region | Q1 Revenue | Q2 Revenue | Q3 Revenue | Q4 Revenue | Total |
|---|---|---|---|---|---|
| North America | $1,234,567 | $1,456,789 | $1,567,890 | $1,890,123 | $6,149,369 |
```

---

## Step 9 — Preview Before Saving

Always show the first 5 rows in a Markdown table before confirming save:

"Found **[N] table(s)** with **[total rows]** total rows across **[N] pages**. Here's a preview of Table 1:

| Col1 | Col2 | … |
|---|---|---|
| … | … | … |

Showing rows 1–5 of [total]. Full extraction ready."

---

## Step 10 — Post-Extraction Operations (on request)

| Operation | How |
|---|---|
| Filter rows | "Show only rows where [Column] = [value]" |
| Sort | "Sort by [Column] descending" |
| Column totals | Sum/average/min/max for numeric columns |
| Pivot | Group by one column, aggregate another |
| Merge tables | Join two tables on a shared key column |
| Remove duplicates | Flag and optionally remove identical rows |
| Export as chart description | Describe what a bar/line chart of this data would show |
| Data validation | Check for expected value ranges, required fields |

---

## Limitations & Edge Cases
- Handwritten tables: extract best-effort; flag uncertain cells with `[?]`
- Very large tables (>10,000 rows): warn user; offer to extract in chunks or provide statistics only
- Nested tables (table within a table cell): extract outer table first; note inner table separately
- Tables spanning multiple pages: stitch together by matching column headers
- Color-coded cells: note the color coding pattern (cannot replicate in CSV/JSON); describe it in notes

## Action Prompt
End with: "Would you like me to:
- Filter or sort the extracted data?
- Calculate column statistics?
- Export as CSV, JSON, or Markdown?
- Join multiple tables on a shared key column?
- Describe what a visualization of this data would look like?"
