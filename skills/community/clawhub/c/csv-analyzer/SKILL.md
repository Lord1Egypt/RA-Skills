---
name: csv-analyzer
description: Analyze CSV/Excel files with natural language. Get statistics, filter rows, find anomalies, generate summaries, and export results. No pandas needed — uses Python stdlib for lightweight operation.
author: zacjiang
version: 1.0.0
tags: csv, excel, data, analysis, statistics, filter, report, lightweight
---

# CSV Analyzer

Analyze CSV files with simple commands. Get instant statistics, filter data, detect anomalies, and export results — all without pandas or heavy dependencies.

## Usage

### Quick stats
```bash
python3 {baseDir}/scripts/csv_analyze.py stats data.csv
```
Shows row count, column types, min/max/mean for numeric columns, unique counts for text columns.

### Filter rows
```bash
python3 {baseDir}/scripts/csv_analyze.py filter data.csv --where "amount>1000" --output big_orders.csv
```

### Top/Bottom N
```bash
python3 {baseDir}/scripts/csv_analyze.py top data.csv --column revenue --n 10
python3 {baseDir}/scripts/csv_analyze.py bottom data.csv --column revenue --n 5
```

### Detect anomalies (values outside 2σ)
```bash
python3 {baseDir}/scripts/csv_analyze.py anomalies data.csv --column price
```

### Group and aggregate
```bash
python3 {baseDir}/scripts/csv_analyze.py group data.csv --by category --agg "sum:amount" "count:id"
```

## Features

- 📊 Automatic column type detection (numeric, date, text)
- 🔍 Flexible filtering with comparison operators
- 📈 Statistical summary (mean, median, std, min, max, percentiles)
- 🚨 Anomaly detection (z-score based)
- 📋 Grouping and aggregation
- 💾 Export filtered/processed results
- 🪶 **Zero external dependencies** — Python stdlib only (csv module)

## Dependencies

None! Uses only Python standard library.

## Why Not Pandas?

Pandas is great but:
- Takes 100MB+ RAM just to import
- Overkill for quick analysis tasks
- This skill runs on 2GB RAM servers without issues
- For truly large datasets, the agent can recommend installing pandas

## Limitations

- Designed for files up to ~100MB (loads into memory)
- For larger files, use streaming mode or install pandas
- Date parsing is basic (ISO format preferred)
