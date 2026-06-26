---
name: fred-data-viz
description: "Create publication-ready economic comparison charts from Federal Reserve Economic Data (FRED). Use when the user needs to visualize, compare, or analyze economic time series data such as GDP, wages, inflation, employment, corporate profits, or any FRED-series data. Triggers on requests for economic charts, FRED data visualization, productivity-pay gap graphs, wage growth comparisons, GDP vs compensation charts, indexed economic data plots, or annotated timeline visualizations of macroeconomic indicators."
---

# FRED Data Visualization

Create indexed comparison charts from Federal Reserve Economic Data (FRED) series.

## Quick Start

For a simple two-series comparison:

```bash
python3 scripts/fred_chart.py --config chart_config.json --output chart.png
```

## Workflow

### 1. Identify the FRED series

Find series IDs at [fred.stlouisfed.org](https://fred.stlouisfed.org):

| Indicator | Common Series |
|---|---|
| Real GDP | `GDPC1` |
| GDP Per Capita | `A939RX0Q048SBEA` (or compute from GDPC1 + POPTHM) |
| Compensation Per Hour | `COMPRNFB` |
| Median Weekly Earnings | `LES1252881600Q` |
| Corporate Profits | `CP` |
| CPI | `CPIAUCSL` |
| Unemployment | `UNRATE` |

### 2. Create config JSON

```json
{
  "title": "USA: GDP vs Wages (1959 = 100)",
  "series": [
    {
      "id": "A939RX0Q048SBEA",
      "label": "Real GDP Per Capita",
      "color": "#2E86AB"
    },
    {
      "id": "COMPRNFB",
      "label": "Real Compensation Per Hour",
      "color": "#F18F01"
    }
  ],
  "start_date": "1959-01-01",
  "end_date": "2026-12-31",
  "fill_gap": true,
  "annotations": [
    {
      "date": "1971-08-15",
      "label": "Nixon Shock",
      "position": "top",
      "y": 140
    }
  ]
}
```

**Config fields:**
- `title`: Chart title
- `series[].id`: FRED series ID
- `series[].label`: Legend label
- `series[].color`: Optional hex color
- `start_date`/`end_date`: Date range filter
- `fill_gap`: Shade area between first two series (default: true)
- `annotations[].date`: Event date (YYYY-MM-DD)
- `annotations[].label`: Event text (supports newlines with `\n`)
- `annotations[].position`: `"top"` or `"bottom"`
- `annotations[].y`: Vertical position for label placement

### 3. Generate chart

```bash
python3 scripts/fred_chart.py --config my_chart.json --output my_chart.png
```

## Advanced: GDP Per Capita Calculation

When FRED lacks a direct GDP per capita series, compute it from GDP (`GDPC1`) and population (`POPTHM`):

```python
# gdp_pc = (GDP in billions * 1e9) / (Population in thousands * 1e3)
# Or use the pre-computed series: A939RX0Q048SBEA (available from 1979)
# For earlier dates, manual calculation required
```

## Tips

- **Indexing**: All series are automatically indexed to their first observation (set to 100) for fair comparison
- **Annotations**: Use `\n` for multi-line labels. Position alternates top/bottom to avoid overlap
- **Zooming**: Use `start_date`/`end_date` to focus on specific eras (e.g., 1959-1985)
- **Colors**: Choose contrasting colors. Blue (#2E86AB) and orange (#F18F01) work well
- **Multiple series**: Up to 5 series supported. Gap fill only applies to first two

## Common Chart Patterns

| Pattern | Series | Use Case |
|---|---|---|
| Productivity-Pay Gap | `A939RX0Q048SBEA`, `COMPRNFB` | Show worker compensation vs economic output |
| Wage-Inflation Comparison | `CES0500000003`, `CPIAUCSL` | Real vs nominal wage growth |
| Profit-Wage Divergence | `CP`, `COMPRNFB` | Where surplus goes |
| Historical Events | Any + annotations | Annotated economic timeline |
