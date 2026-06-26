---
name: chart-mpl
version: 1.1.0
description: Generate PNG/SVG charts (line, bar, hbar, pie, stacked, scatter, area) from CSV data using matplotlib. Use when the user asks to visualize tabular data, produce BI-ready chart images, or compare multiple series.
metadata: { "openclaw": { "emoji": "CH", "requires": { "bins": ["python3"] } } }
---

# Chart MPL

Generate chart images from CSV files with `scripts/chart_mpl.py`.

## Setup

Create a virtual environment and install matplotlib (one-time):

```bash
python3 -m venv ~/.openclaw/workspace/.venv_chart
~/.openclaw/workspace/.venv_chart/bin/pip install matplotlib
```

## Quick start

Run from workspace root:

```bash
~/.openclaw/workspace/.venv_chart/bin/python skills/chart-mpl/scripts/chart_mpl.py \
  --csv /path/to/data.csv \
  --xcol Mois \
  --ycol Valeur \
  --kind line \
  --title "Monthly trend" \
  --xlabel "Month" \
  --ylabel "Value"
```

Output defaults to:
`~/.openclaw/workspace/exports/images`

## Inputs

- `--csv` path to CSV file
- `--xcol` column for X axis
- `--ycol` numeric column(s) for Y axis — comma-separated for multi-series (e.g. `Sales,Costs`)
- `--kind` chart type: `line`, `bar`, `hbar`, `pie`, `stacked`, `scatter`, `area`
- Optional: `--delim` if auto-detection fails (`;`, `,`, `\t`, `|`)
- Optional: `--out` custom output path (PNG or SVG — format detected from extension)
- Optional: `--title`, `--xlabel`, `--ylabel`
- Optional: `--top N` show only top N categories by value (bar, hbar, pie, stacked). Multi-series ranks by row total.
- Optional: `--sort` sort data before plotting: `x-asc`, `x-desc`, `y-desc`, `none` (default: `none`)
- Optional: `--numfmt` number format on Y axis: `fr` (1,5M) or `en` (1.5M) — default: `fr`

## Chart types

| Kind      | Description                          | Multi-series |
|-----------|--------------------------------------|:------------:|
| `line`    | Line chart with markers              | yes          |
| `bar`     | Vertical bar chart (grouped when multi-series) | yes          |
| `hbar`    | Horizontal bar chart (grouped when multi-series) | yes          |
| `pie`     | Pie chart (first Y column only)      | no           |
| `stacked` | Stacked vertical bar (requires 2+ Y) | yes          |
| `scatter` | Scatter plot                         | yes          |
| `area`    | Filled area chart                    | yes          |

## Notes

- Script auto-detects delimiters when possible.
- Script tolerates European and US numeric formats (`1 234,56`, `1,234.56`).
- Non-numeric values in `ycol` are converted to `NaN` with a warning.
- Handles BOM-encoded CSV files (`utf-8-sig`).
- Multi-series charts automatically show a legend and cycle through an 8-color palette.
- Y-axis ticks use human-readable formatting (K, M, G suffixes) with French or English decimals.
- `--top N` keeps the N highest categories. For pie charts, the remainder is aggregated into an "Other" slice. For bar/hbar/stacked, the rest are excluded.
- Output format (PNG or SVG) is detected from the `--out` file extension. Default is PNG.

## End-to-end flow with SQL skill

1. Export query result to CSV using the `mssql` skill.
2. Run this script on that CSV.
3. Share the generated PNG path.
