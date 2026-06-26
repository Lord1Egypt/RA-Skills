# SQL → Excel Export Recipe

Standard pattern for turning `mssql` query results into `excel-export` workbooks.
Copy the relevant sections into your agent's `AGENTS.md` under the excel-export skill entry.

---

## Pipeline

```
mssql (query) → normalize → build JSON spec → excel-export (render)
```

Never skip the normalize step.  Raw SQL output is not ready for the Excel renderer.

---

## Step 1 — Query with mssql

Run the query and capture delimiter-separated output:

```bash
bash skills/mssql/scripts/mssql_query.sh \
  --query "SELECT Region, Revenue, Volume, Growth, ReportDate, IsActive FROM sales.vw_Q1" \
  --out exports/raw_q1.dsv
```

The result is a semicolon-delimited text file with a header row.

---

## Step 2 — Normalize values

Apply these rules when converting each SQL row into a JSON row object:

| SQL value | JSON value | Why |
|---|---|---|
| `NULL` | `null` | Renders as blank cell |
| Date `2026-03-31` | `"2026-03-31"` | Script parses `YYYY-MM-DD` into typed Excel date |
| Datetime `2026-03-31 14:30:00` | `"2026-03-31 14:30:00"` | Script parses ISO-like string into typed Excel datetime |
| Bit `1` / `0` | `true` / `false` | Script renders as `Oui` / `Non` |
| Decimal `1250000.00` | `1250000.00` | Keep as JSON number — script handles formatting |
| Integer `340` | `340` | Keep as JSON number |
| Percentage `0.15` | `0.15` | Pass the decimal, not `15` — the `percent` type formats it |
| ID with leading zeros `"007842"` | `"007842"` | **Must be a string** — script forces text storage |
| Long numeric ID `9876543210123456` | `"9876543210123456"` | **Must be a string** if > 15 digits — Excel truncates otherwise |
| Phone `+212661000000` | `"+212661000000"` | **Must be a string** — script detects `+` prefix |
| Code/reference `"ABC-2026-001"` | `"ABC-2026-001"` | Already a string, safe as-is |
| Empty string `""` | `null` | Treat blanks as null for clean rendering |

**Rule of thumb:** if it's an identifier, code, or phone number — always pass it as a JSON string, even if it looks numeric.

---

## Step 3 — Build the JSON spec

### Choosing column types

Map SQL types to excel-export column types:

| SQL type | excel-export type | Default format |
|---|---|---|
| `varchar`, `nvarchar`, `char` | `text` | — |
| `int`, `bigint`, `smallint` | `integer` | `#,##0` (but use `text` if the column is an ID/code that can exceed 15 digits) |
| `decimal`, `float`, `real`, `money` | `number` | `#,##0.00` |
| `decimal` used as percentage | `percent` | `0.0%` |
| `money` / `decimal` as currency | `currency` | `#,##0.00 "MAD"` |
| `date` | `date` | `dd/mm/yyyy` |
| `datetime`, `datetime2` | `datetime` | `dd/mm/yyyy hh:mm` |
| `bit` | `boolean` | `Oui` / `Non` |

### One sheet vs multiple sheets

| Scenario | Approach |
|---|---|
| Single query result | One sheet |
| Same data grouped by a dimension (region, month, department) | One sheet per group |
| Unrelated datasets in one report (sales + charges + inventory) | One sheet per dataset |
| Summary + detail | Two sheets: summary first, detail second |

### Minimal flat-table spec (80% of cases)

```json
{
  "sheets": [
    {
      "name": "Ventes Q1",
      "title": "Ventes — Premier Trimestre 2026",
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
        { "region": "Rabat",      "ca": 980000,  "volume": 210, "growth": -0.03, "date": "2026-03-31", "active": true }
      ]
    }
  ]
}
```

### Advanced spec (formulas + totals + multi-sheet)

```json
{
  "sheets": [
    {
      "name": "Résumé",
      "title": "Rapport Consolidé — Q1 2026",
      "subtitle": "Direction Financière",
      "columns": [
        { "key": "region",  "header": "Région",     "type": "text" },
        { "key": "ca",      "header": "CA (MAD)",   "type": "currency", "total": "sum" },
        { "key": "charges", "header": "Charges",     "type": "currency", "total": "sum" },
        { "key": "marge",   "header": "Marge",       "type": "currency", "total": "sum", "formula": "=[@[CA (MAD)]]-[@Charges]" },
        { "key": "pct",     "header": "% du Total",  "type": "percent",  "formula": "=[@[CA (MAD)]]/SUBTOTAL(109,[CA (MAD)])" }
      ],
      "rows": [
        { "region": "Casablanca", "ca": 1250000, "charges": 875000 },
        { "region": "Rabat",      "ca": 980000,  "charges": 715000 },
        { "region": "Tanger",     "ca": 670000,  "charges": 510000 }
      ]
    },
    {
      "name": "Détail Casablanca",
      "title": "Détail — Casablanca",
      "columns": [
        { "key": "product", "header": "Produit",   "type": "text" },
        { "key": "qty",     "header": "Quantité",  "type": "integer", "total": "sum" },
        { "key": "unit",    "header": "Prix Unit.", "type": "currency" },
        { "key": "total",   "header": "Total",     "type": "currency", "total": "sum", "formula": "=[@Quantité]*[@[Prix Unit.]]" }
      ],
      "rows": [
        { "product": "Produit A", "qty": 120, "unit": 3500 },
        { "product": "Produit B", "qty": 85,  "unit": 5200 },
        { "product": "Produit C", "qty": 135, "unit": 2800 }
      ]
    }
  ]
}
```

---

## Step 4 — Render

```bash
~/.openclaw/workspace/.venv_excel/bin/python skills/excel-export/scripts/build_xlsx.py \
  --input  exports/ventes_q1.json \
  --output exports/excel/ventes_q1.xlsx
```

The script prints a JSON summary to stdout:

```json
{
  "success": true,
  "output": "/home/agent/.openclaw/workspace/exports/excel/ventes_q1.xlsx",
  "sheets": [
    { "sheet": "Résumé", "rows": 3 },
    { "sheet": "Détail Casablanca", "rows": 3 }
  ]
}
```

---

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Pass `15` instead of `0.15` for percent | Excel shows `1500%` | Always pass the decimal fraction |
| Pass `NULL` as the string `"NULL"` | Cell shows the text "NULL" | Use JSON `null` |
| Pass a 16-digit ID as a number | Excel rounds it | Pass as a string `"9876543210123456"` |
| Forget `type` on a date column | Dates render as raw text | Always set `"type": "date"` or `"type": "datetime"` |
| Use positional arrays for rows | Validation error | Rows must be objects keyed by column `key` |
| Put `subtitle` without `title` | Validation error | `subtitle` requires `title` |
| Pass boolean to a numeric column | Validation error | Use `boolean` type, or convert to 0/1 integer upstream |
