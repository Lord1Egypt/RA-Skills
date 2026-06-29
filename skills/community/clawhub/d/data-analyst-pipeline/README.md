# Data Analyst Skill

AI-powered data analysis workflow — from data ingestion to interactive HTML report generation.

## Features

- **Multi-format support**: CSV, Excel, JSON, SQLite
- **4-layer data quality audit**: Health check → Structure integrity → Business rules → Model readiness
- **Automated EDA**: Distribution analysis, correlation, outlier detection, statistical summaries
- **Rich visualizations**: Histograms, boxplots, heatmaps, pair plots, categorical breakdowns
- **Interactive HTML report**: Scorecards, charts, data tables, actionable insights
- **Business rules engine**: YAML-configurable domain validation

## Quick Start

```bash
pip install pandas numpy matplotlib seaborn scipy pyyaml

# Analyze a CSV file
python scripts/run_analysis.py data.csv

# With target column and named report
python scripts/run_analysis.py sales.csv --target revenue --name "Sales Analysis"

# With business rules validation
python scripts/run_analysis.py data.csv --rules config/business_rules.yaml

# Sample large datasets
python scripts/run_analysis.py big_data.csv --sample 50000
```

## Pipeline

```
Load → Audit (4-layer) → Clean → EDA → Visualize → Report
```

# Skill for WorkBuddy

This is a WorkBuddy skill. Used within WorkBuddy, trigger words include:
分析数据、数据分析、数据报告、EDA、analyze data

## License

MIT
