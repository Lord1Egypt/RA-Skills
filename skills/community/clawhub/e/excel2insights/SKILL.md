# Excel2Insights

## Overview

Excel2Insights is a data analysis and visualization tool designed for structured data (CSV, XLSX, XLS, TSV). It helps you quickly understand the contents of any tabular dataset through automated statistical analysis, data quality checks, visualization generation, and structured reporting.

The skill works in two modes:
- **Quick Scan** — Load a file, preview shape/dtypes, descriptive stats, and missing values
- **Deep Analysis** — Full pipeline: profile + clean + analyze + visualize + report

---

## When to Use

- You receive a CSV/XLSX and need to understand what's in it fast
- You need a structured data quality report before further processing
- You want to generate charts and summaries from tabular data
- You need to compare two datasets or check for anomalies
- You want to transform raw data into a readable insight report

---

## Workflow

### Step 1: Load & Inspect

Use `excel-reader.py` to load the file. The script returns:
- File metadata (rows, columns, size)
- Column names and dtypes
- First/last 5 rows preview
- Missing value count per column
- Basic data quality flags

```python
# Agent internally calls:
python3 scripts/excel-reader.py --file path/to/data.csv
# Output: structured JSON with metadata + preview
```

### Step 2: Statistical Analysis

Use `data-analyzer.py` to compute:
- Numeric columns: mean, median, std, min, max, quartiles, skewness
- Categorical columns: value counts, unique count, mode, frequency distribution
- Date columns: date range, gaps, frequency
- Cross-column: correlation matrix (numeric), cross-tabulation (categorical)

Output is structured JSON grouped by column type.

### Step 3: Data Quality Check

Built into the analysis phase:
- Missing value ratio per column
- Duplicate rows
- Outlier detection (IQR method)
- Data type inconsistencies
- Value range violations

Flagged issues are included in the final report.

### Step 4: Generate Visualizations

Use `chart-generator.py` to create charts:
- **histogram** — distribution of numeric columns
- **boxplot** — outliers and spread for numeric columns
- **bar** — frequency counts for categorical columns
- **line** — trends for date-indexed data
- **pie** — proportion breakdown for categorical data
- **correlation heatmap** — pairwise numeric correlation
- **scatter** — relationship between two numeric columns
- **pairplot** — pairwise scatter matrix (small datasets)

All charts are saved as PNG files and embedded into the final report.

### Step 5: Generate Report

Use `report-generator.py` to produce a comprehensive Markdown report containing:
- Executive summary
- File overview (metadata + quality)
- Column-by-column analysis
- Charts gallery
- Key insights and anomalies
- Recommendations

The report is written to `output/` directory.

---

## Available Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `scripts/excel-reader.py` | Load file, display metadata and preview | `python3 scripts/excel-reader.py --file DATA` |
| `scripts/data-analyzer.py` | Full statistical analysis | `python3 scripts/data-analyzer.py --file DATA [--output JSON_OUTPUT]` |
| `scripts/chart-generator.py` | Generate visualization charts | `python3 scripts/chart-generator.py --file DATA [--charts CHART_TYPES] [--output DIR]` |
| `scripts/report-generator.py` | Generate markdown insight report | `python3 scripts/report-generator.py --file DATA [--charts DIR] [--output REPORT_PATH]` |
| `scripts/auto-pipeline.py` | Run full pipeline (analyze + chart + report) | `python3 scripts/auto-pipeline.py --file DATA [--charts CHART_TYPES] [--output DIR]` |

### Script Options

**excel-reader.py**
- `--file PATH` — Path to Excel/CSV/TSV file
- `--sheet NAME` — Sheet name (XLSX only, default: first sheet)
- `--encoding ENC` — File encoding (default: utf-8)
- `--preview N` — Preview rows count (default: 5)

**data-analyzer.py**
- `--file PATH` — Path to data file
- `--output PATH` — Output JSON path (optional)
- `--correlation` — Include correlation matrix
- `--outliers` — Enable outlier detection
- `--categorical-top N` — Top N value counts (default: 20)

**chart-generator.py**
- `--file PATH` — Path to data file
- `--charts CHART_TYPES` — Comma-separated: histogram,boxplot,bar,line,pie,heatmap,scatter,pairplot
- `--columns COLS` — Specific columns to visualize
- `--output DIR` — Output directory (default: output/charts)
- `--theme THEME` — Chart theme (default: clean)

**report-generator.py**
- `--file PATH` — Path to data file
- `--analysis PATH` — Pre-computed analysis JSON (optional)
- `--charts DIR` — Charts directory (optional)
- `--output PATH` — Output report path (default: output/report.md)
- `--format FORMAT` — Output format: markdown, html, pdf

**auto-pipeline.py**
- `--file PATH` — Path to data file (required)
- `--charts CHART_TYPES` — Chart types (default: histogram,boxplot,bar,correlation)
- `--output DIR` — Output directory (default: output/)
- `--format FORMAT` — Report format (default: markdown)

---

## Examples

### Example 1: Quick scan a CSV file

Agent reads a CSV and runs the reader:

```
📄 File: sales_data.csv
   Rows: 10,000 | Columns: 15 | Size: 1.2 MB

📊 Column Overview:
   date        datetime64  non-null  10000
   product     object      non-null  10000
   category    object      non-null  9985    (0.15% missing)
   revenue     float64     non-null  10000
   quantity    int64       non-null  9990    (0.10% missing)

⚠  Data Quality Flags:
   - 2 columns with missing values (<1%) — acceptable
   - 12 duplicate rows detected (0.12%)
```

### Example 2: Full deep analysis pipeline

Agent runs the auto-pipeline on a sales dataset:

```bash
python3 scripts/auto-pipeline.py --file data/sales_2024.csv --charts histogram,bar,line,heatmap
```

Output:

```
📈 Charts generated (4):
   output/charts/revenue_histogram.png
   output/charts/top_products_bar.png
   output/charts/monthly_trend_line.png
   output/charts/correlation_heatmap.png

📝 Report generated:
   output/report.md

🏆 Key Insights:
   - Top 3 products account for 62% of total revenue
   - July-September shows 28% seasonal dip
   - Region A has highest average order value ($245)
   - Customer repeat rate: 34% (improvement opportunity)
```

### Example 3: Custom chart selection

```bash
python3 scripts/chart-generator.py --file data.csv --charts histogram,scatter --columns revenue,quantity,price
```

---

## Output Format

Reports are structured Markdown with the following sections:

```markdown
# Data Insight Report

## Executive Summary
...

## Dataset Overview
- Rows / Columns / File size
- Column types summary

## Data Quality
- Missing values table
- Duplicates
- Outliers

## Column Analysis (per column)
- Type-specific stats (numeric/categorical/date)
- Distribution summary
- Notable patterns

## Visualizations
- Embedded chart images
- Chart descriptions

## Key Insights
- Top findings ranked by importance
- Anomalies detected
- Recommendations

## Appendix
- Methodology notes
- Configuration used
```

---

## Dependencies

- Python 3.9+
- pandas
- numpy
- openpyxl (for XLSX support)
- matplotlib
- seaborn (for advanced charts)
- tabulate (for formatted tables)

See `requirements.txt` for exact versions.

---

## License

MIT-0 (No Attribution Required)
