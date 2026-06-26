---
name: ai-data-visualizer
description: Automatically analyze and recommend optimal chart combinations based on data characteristics, generate beautiful interactive HTML dashboards (including line charts, bar charts, scatter plots, pie charts, etc.), support dark/light theme switching, CSV and JSON input, and data statistical summaries.
---

# AI Data Visualizer

Generate interactive HTML dashboards from CSV/JSON data with one click.

## Applicable Scenarios

- User provides CSV/JSON files that need visualization
- User needs a data analysis dashboard
- User mentions "data visualization", "generate chart", "plot", "chart"
- User uploads tabular data wanting intuitive display

## Quick Start

```bash
python3 "{SKILL_DIR}/scripts/generate_dashboard.py" data.csv -o dashboard.html
python3 "{SKILL_DIR}/scripts/generate_dashboard.py" data.json --json -o dashboard.html --theme dark
```

## Features

- **Smart Chart Recommendation**: Automatically detects column types (numeric/time/categorical/text) and recommends optimal chart combinations
- **6 Chart Types**: Line charts (trends), bar charts (comparison), scatter plots (correlation), pie/donut charts (proportions)
- **Interactive HTML**: Chart.js rendering, hover tooltips, dark/light theme toggle, responsive layout
- **Statistical Summary**: Automatically calculates mean, median, min/max values
- **Data Table**: Embedded raw data preview (limit 500 rows)

## Supported Chart Selections

The script automatically selects chart strategies based on data column types. See `{SKILL_DIR}/references/chart-selection.md`.

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | CSV or JSON file path | (required) |
| `-o, --output` | Output HTML path | `dashboard.html` |
| `--json` | Input is JSON format | auto-detect |
| `--stdin` | Read CSV from stdin | - |
| `--theme` | `light` or `dark` | `light` |
| `--title` | Dashboard title | `数据可视化仪表板` |

## Workflow

1. **Receive user data** — File path (CSV/JSON) or direct data content
2. **Preprocess data** — Clean and transform if necessary
3. **Generate dashboard** — Run script, output HTML
4. **Inform user** — Describe generated file and chart summary

If the user provides data content directly (rather than a file), write it to a temporary CSV file first, then call the script.

## Dependencies

- Python 3.7+
- Chart.js 4.x (CDN loaded in HTML output)
- No pip dependencies (pure standard library)

## Example

Input `sales.csv`:
```
Month,Product,Revenue,Units
2024-01,A,15000,120
2024-02,A,18000,145
2024-01,B,12000,95
2024-02,B,14000,110
```

Output: Automatically generates a dashboard with trend line charts, category comparison bar charts, and revenue proportion pie charts.