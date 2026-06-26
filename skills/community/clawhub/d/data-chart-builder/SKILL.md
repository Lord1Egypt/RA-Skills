---
name: data-chart-builder
description: "Create publication-ready charts from any data source (CSV, JSON, FRED API, or inline data). Supports line, bar, scatter, area-fill, indexed series, annotations, and multi-series overlays. Use for economic data visualization, time series comparison, trend analysis, gap/shaded region charts, annotated timelines, or any custom plotting task. Triggers on requests for charts, graphs, plots, data visualization, time series comparison, indexed data plots, or annotated economic/social/technical charts."
---

# Data Chart Builder

Build publication-ready charts from CSV, JSON, FRED, or inline data.

## Quick Start

```bash
python3 scripts/chart_builder.py --config chart.json
```

## Workflow

### 1. Prepare data or identify source

**Options:**
- **CSV file**: Local or URL
- **JSON**: Inline in config or external file
- **FRED**: Federal Reserve series ID
- **Inline**: Direct data array in config

### 2. Write config JSON

```json
{
  "title": "My Chart Title",
  "series": [
    {
      "csv": "/path/to/data.csv",
      "date_col": "date",
      "value_col": "price",
      "label": "Stock Price",
      "color": "#2E86AB",
      "index": true
    }
  ],
  "output": "/tmp/my_chart.png"
}
```

### 3. Generate

```bash
python3 scripts/chart_builder.py --config my_chart.json
```

## Config Reference

### Top-level fields

| Field | Type | Description |
|---|---|---|
| `title` | string | Chart title |
| `series` | array | Data series to plot (required) |
| `output` | string | Output path (default: `/tmp/chart.png`) |
| `figsize` | [w, h] | Figure size in inches (default: `[12, 7]`) |
| `start_date` / `end_date` | string | Filter range (YYYY-MM-DD) |
| `index_all` | bool | Index all series to 100 |
| `fill` | bool | Shade between first two series |
| `fill_color` | string | Fill color (default: `red`) |
| `fill_alpha` | float | Fill opacity (default: `0.15`) |
| `hline` | number | Draw horizontal reference line |
| `grid` | bool | Show grid (default: `true`) |
| `ylim` | [min, max] | Y-axis limits |
| `annotations` | array | Vertical event markers |

### Series fields

| Field | Type | Description |
|---|---|---|
| `label` | string | Legend label (required) |
| `csv` | string | Path or URL to CSV |
| `json` | string | Path to JSON file |
| `fred` | string | FRED series ID |
| `data` | array | Inline data: `[{"date": "...", "value": 100}, ...]` |
| `date_col` | string | Date column name (default: `date`) |
| `value_col` | string | Value column name (default: `value`) |
| `type` | string | `line`, `bar`, `scatter` |
| `color` | string | Hex color |
| `width` | number | Line width |
| `style` | string | Line style: `-`, `--`, `-.`, `:` |
| `index` | bool | Index this series to 100 |
| `base_date` | string | Index base date (default: first observation) |

### Annotations

```json
{
  "date": "2008-09-15",
  "label": "Lehman Bankruptcy",
  "position": "top",
  "y": 120,
  "fontsize": 9
}
```

## Examples

### Economic comparison (FRED)

```json
{
  "title": "USA: GDP vs Wages (1959 = 100)",
  "series": [
    {"fred": "A939RX0Q048SBEA", "label": "GDP Per Capita", "color": "#2E86AB", "index": true},
    {"fred": "COMPRNFB", "label": "Compensation Per Hour", "color": "#F18F01", "index": true}
  ],
  "start_date": "1959-01-01",
  "end_date": "1985-12-31",
  "fill": true,
  "annotations": [
    {"date": "1971-08-15", "label": "Nixon Shock", "position": "top", "y": 140},
    {"date": "1973-10-01", "label": "Oil Crisis", "position": "bottom", "y": 90}
  ],
  "output": "gdp_wages.png"
}
```

### Stock price vs volume

```json
{
  "title": "AAPL Price vs Volume",
  "series": [
    {"csv": "aapl.csv", "label": "Price", "color": "#2E86AB", "type": "line"},
    {"csv": "aapl.csv", "label": "Volume", "color": "#F18F01", "type": "bar", "value_col": "volume"}
  ],
  "output": "aapl_chart.png"
}
```

### Inline data

```json
{
  "title": "Sales Q1-Q4",
  "series": [
    {
      "label": "Revenue",
      "data": [
        {"date": "2024-01-01", "value": 100},
        {"date": "2024-04-01", "value": 120},
        {"date": "2024-07-01", "value": 140},
        {"date": "2024-10-01", "value": 180}
      ],
      "color": "#2E86AB",
      "type": "bar"
    }
  ],
  "output": "sales.png"
}
```

### Scatter plot

```json
{
  "title": "Height vs Weight",
  "series": [
    {"csv": "patients.csv", "label": "Male", "color": "blue", "type": "scatter", "date_col": "height", "value_col": "weight"},
    {"csv": "patients.csv", "label": "Female", "color": "red", "type": "scatter", "date_col": "height", "value_col": "weight"}
  ]
}
```

## Tips

- **Indexing**: Use `"index": true` on each series or `"index_all": true` globally to compare growth rates on equal footing
- **Colors**: Use contrasting hex codes. Good pairs: `#2E86AB` (blue) + `#F18F01` (orange), or `#C73E1D` (red) + `#3B1F2B` (dark)
- **Annotations**: Alternate `position: "top"` and `"bottom"` to avoid overlap
- **Date parsing**: Ensure dates are ISO format (YYYY-MM-DD) for reliable parsing
- **FRED**: Find series IDs at [fred.stlouisfed.org](https://fred.stlouisfed.org)

## Data Source Flexibility

| Source | How to specify | Best for |
|---|---|---|
| Local CSV | `"csv": "/path/to/file.csv"` | Custom datasets |
| URL CSV | `"csv": "https://example.com/data.csv"` | API endpoints |
| FRED | `"fred": "GDPC1"` | Economic time series |
| Inline | `"data": [...]` | Small static datasets |
