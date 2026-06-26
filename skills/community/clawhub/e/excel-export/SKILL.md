---
name: excel-export
version: 1.1.0
description: Generate polished .xlsx workbooks from structured JSON — multiple sheets, frozen headers, filters, typed columns, formulas, totals, and French/Morocco formatting defaults. Use when the user needs database results or context-derived data exported as an Excel file.
metadata: { "openclaw": { "emoji": "XL", "requires": { "bins": ["python3"] } } }
---

## When to Use

Use when the agent must deliver a `.xlsx` Excel file — sales reports, query results, multi-sheet data exports, financial summaries, or any structured data that needs polished spreadsheet formatting.  This skill handles workbook **creation only**.  Do not use it to read, edit, or preserve existing Excel files.

## Setup

```bash
python3 -m venv ~/.openclaw/workspace/.venv_excel
~/.openclaw/workspace/.venv_excel/bin/pip install xlsxwriter
```

No credentials required.

## How to Run

```bash
~/.openclaw/workspace/.venv_excel/bin/python skills/excel-export/scripts/build_xlsx.py \
  --input  <path/to/workbook.json> \
  --output <path/to/report.xlsx>
```

Default export directory: `~/.openclaw/workspace/exports/excel/`.

The script prints a JSON summary to stdout on success:

```json
{
  "success": true,
  "output": "/absolute/path/to/report.xlsx",
  "sheets": [
    { "sheet": "Ventes", "rows": 42 },
    { "sheet": "Charges", "rows": 18 }
  ]
}
```

## Input Format

The input is a single JSON file.  Top-level shape:

```json
{
  "sheets": [ ... ]
}
```

Each sheet object:

| Field      | Required | Description                              |
|------------|----------|------------------------------------------|
| `name`     | yes      | Sheet tab name (max 31 chars)            |
| `title`    | no       | Bold title row above the table           |
| `subtitle` | no       | Muted subtitle row below the title       |
| `columns`  | yes      | Array of column definitions              |
| `rows`     | no       | Array of data objects (keyed by `key`)   |

Each column object:

| Field     | Required | Description                                         |
|-----------|----------|-----------------------------------------------------|
| `key`     | yes      | Row-object key for this column's values              |
| `header`  | yes      | Display header in the table                          |
| `type`    | no       | Data type (default `text`) — see table below         |
| `width`   | no       | Explicit column width (overrides auto-estimate)      |
| `numfmt`  | no       | Custom Excel number format (overrides type default)  |
| `formula` | no       | Excel table structured-reference formula             |
| `total`   | no       | Totals-row function: `sum`, `average`, or `count`    |

Rows are **objects keyed by column `key`**, not positional arrays.  Missing keys produce blank cells.  Unknown keys cause a validation error.

## Column Types

| Type       | Default format          | Notes                                |
|------------|-------------------------|--------------------------------------|
| `text`     | —                       | Always stored as text                |
| `integer`  | `#,##0`                 | Rounded to whole number              |
| `number`   | `#,##0.00`              | Two decimal places                   |
| `percent`  | `0.0%`                  | Pass 0.15 for 15 %                   |
| `currency` | `#,##0.00 "MAD"`        | Moroccan dirham by default           |
| `date`     | `dd/mm/yyyy`            | Accepts `YYYY-MM-DD` strings         |
| `datetime` | `dd/mm/yyyy hh:mm`      | Accepts ISO 8601 strings             |
| `boolean`  | —                       | Rendered as `Oui` / `Non`            |

Use `numfmt` on any column to override its type's default format.

## Rendering Rules

**Layout** — fixed, deterministic, never configured per-sheet:
- No title/subtitle → table header on row 1.
- Title only → title row 1, blank row 2, table header row 3.
- Title + subtitle → title row 1, subtitle row 2, blank row 3, table header row 4.

**Freeze pane** — always at the first data row (`A2`, `A4`, or `A5` depending on title presence).

**Table style** — each sheet is one rectangular Excel table with filters, banded rows, and `Table Style Medium 9`.

**Column widths** — auto-estimated from headers and sampled values, capped at 50 characters.  Explicit `width` in the column definition overrides the estimate.

**Formulas** — use Excel structured references (e.g. `=[@Revenue]/SUM([Revenue])`).  Formula columns are injected through the table definition, not written cell-by-cell, so they apply to every data row automatically.

**Totals row** — if any column has `total`, the table includes a totals row.  The first column displays "Total" as a label unless it has its own total function.

**Empty datasets** — produce a valid workbook with headers, filters, styling, and zero data rows.

## Data-Integrity Doctrine

These rules are always enforced — they are not optional:

1. **Preserve data types.**  Leading-zero strings, phone numbers (`+212…`), and numeric strings longer than 15 digits are always stored as text.  Excel silently corrupts these if written as numbers.

2. **Keep calculations in Excel.**  When the workbook should stay live, write formulas — not hardcoded derived values from Python.  Use structured references so formulas survive row insertions and deletions.

3. **Treat dates explicitly.**  Dates are serial numbers with legacy quirks.  The script writes real date objects with explicit `dd/mm/yyyy` formatting — never raw serial numbers or ambiguous strings.

4. **Validate before delivery.**  The script validates every input field, rejects unknown keys, and fails fast with clear error messages.  A workbook should never ship with silent data loss.

5. **Regional defaults are French / Morocco.**  Date format `dd/mm/yyyy`, currency `MAD`, booleans `Oui / Non`.  Note: final display still depends partly on the viewer's local Excel regional settings.

## Full Example

```json
{
  "sheets": [
    {
      "name": "Ventes Q1",
      "title": "Rapport des Ventes — Q1 2026",
      "subtitle": "Direction Commerciale",
      "columns": [
        { "key": "region",  "header": "Région",     "type": "text" },
        { "key": "ca",      "header": "CA (MAD)",   "type": "currency", "total": "sum" },
        { "key": "volume",  "header": "Volume",     "type": "integer",  "total": "sum" },
        { "key": "growth",  "header": "Croissance", "type": "percent" },
        { "key": "date",    "header": "Date",       "type": "date" },
        { "key": "active",  "header": "Actif",      "type": "boolean" }
      ],
      "rows": [
        { "region": "Casablanca", "ca": 1250000, "volume": 340, "growth": 0.15, "date": "2026-03-31", "active": true },
        { "region": "Rabat",      "ca": 980000,  "volume": 210, "growth": -0.03, "date": "2026-03-31", "active": true },
        { "region": "Tanger",     "ca": 670000,  "volume": 155, "growth": 0.08,  "date": "2026-03-31", "active": false }
      ]
    }
  ]
}
```

```bash
~/.openclaw/workspace/.venv_excel/bin/python skills/excel-export/scripts/build_xlsx.py \
  --input  ~/.openclaw/workspace/exports/ventes_q1.json \
  --output ~/.openclaw/workspace/exports/excel/ventes_q1.xlsx
```

## Validation Rules

The script fails fast with a clear error on:
- Invalid or missing JSON
- Duplicate sheet names
- Sheet names exceeding 31 characters, containing `[ ] : * ? / \`, or starting/ending with apostrophes
- `subtitle` without `title`
- Row count above 1,048,576 or column count above 16,384
- Unknown keys in row objects
- Invalid `type` or `total` values
- Non-string `formula` definitions
- Unrecognized boolean values (only `true/false`, `1/0`, `yes/no`, `oui/non` accepted)
- Non-integer values in `integer` columns (e.g. `12.9` is rejected, not truncated)
- Unparseable dates, datetimes, or numeric strings in typed columns

## SQL-Driven Exports

When generating Excel files from SQL query results, read `references/SQL_TO_EXCEL_RECIPE.md` for the standard pipeline: query with `mssql`, normalize values, build the JSON spec, then render.  The recipe includes SQL-to-JSON type mappings, normalization rules, ready-made templates, and common mistakes.

## Limitations (v1)

- Creation only — does not read or edit existing workbooks.
- No template preservation, merged cells, or conditional formatting.
- One fixed visual theme — no configurable colour system.
- No CSV input — upstream steps must produce JSON.
- `xlsxwriter` does not calculate formulas; the recipient's Excel client recalculates on open.
