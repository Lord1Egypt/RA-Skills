---
name: data-analyst
description: 数据分析师自动化工作流。从数据加载、质量审计、数据清洗、探索性分析(EDA)、统计建模到可视化HTML报告生成，覆盖完整数据分析管线。支持CSV/Excel/JSON/SQLite多格式输入，内置4层数据防御体系。触发词：分析数据、数据分析、帮我分析数据、数据报告、EDA、data analysis、analyze data、生成数据报告、数据可视化、探索性分析。
agent_created: true
---

# 数据分析师 (Data Analyst)

AI-powered data analysis workflow. Cover the full pipeline from data ingestion to interactive HTML report generation.

## When to Use

Trigger when the user asks to:
- Analyze a dataset (CSV / Excel / JSON / SQLite)
- Generate a data analysis report
- Do exploratory data analysis (EDA)
- Clean or preprocess data
- Create data visualizations
- Understand data distributions and relationships

## Workflow Overview

The skill follows a 7-phase CRISP-DM pipeline, executed automatically:

1. **Data Loading** — Auto-detect format, load into DataFrame
2. **Data Audit** — 4-layer defense: health check, structure, business rules, model readiness
3. **Data Cleaning** — Missing values, outliers, type conversion, dedup
4. **EDA** — Distribution analysis, correlation, group aggregation
5. **Statistical Analysis** — Descriptive stats, hypothesis tests, trend detection
6. **Visualization** — Charts for distributions, correlations, category breakdowns
7. **Report Generation** — Interactive HTML report with scorecards, charts, and insights

## Usage

### Quick Start

To analyze a data file:

```bash
python {baseDir}/scripts/run_analysis.py <data_file> [--output report.html]
```

The script auto-detects the file format and runs the full pipeline.

### Module-Level Usage

Each module can be used independently:

```python
# Load data
from data_loader import load_data
df = load_data("sales.csv")

# Audit data quality
from data_auditor import audit_data
report = audit_data(df)

# Clean data
from data_cleaner import clean_data
df_clean = clean_data(df)

# Run EDA
from eda_runner import run_eda
eda_results = run_eda(df_clean)

# Generate report
from report_builder import build_report
build_report(df_clean, eda_results, "report.html")
```

## Scripts Reference

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `scripts/run_analysis.py` | Main entry — orchestrates full pipeline | data file path | HTML report |
| `scripts/data_loader.py` | Multi-format data loading | file path | pandas DataFrame |
| `scripts/data_auditor.py` | 4-layer quality defense | DataFrame | audit dict |
| `scripts/data_cleaner.py` | Data cleaning & preprocessing | DataFrame | cleaned DataFrame |
| `scripts/eda_runner.py` | Exploratory data analysis | DataFrame | EDA results dict |
| `scripts/visualizer.py` | Chart generation | DataFrame + config | saved .png charts |
| `scripts/report_builder.py` | HTML report generation | Data + results | HTML report |

## Templates

- `templates/report.html` — Jinja2 template for the final HTML report

## Config

- `config/business_rules.yaml` — Optional business validation rules

## Dependencies

Install before first use:

```bash
pip install pandas numpy matplotlib seaborn scipy jinja2 pyyaml missingno
```

## Notes

- For files > 100MB, the audit module uses sampling (n=50000) to stay performant
- Business rules in `config/business_rules.yaml` are optional; skip if no domain-specific rules exist
- All charts are saved to a `charts/` subdirectory in the output folder before embedding in HTML
