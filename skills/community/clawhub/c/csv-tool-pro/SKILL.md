---
name: csv-tool-pro
description: CSV Swiss army knife - view, filter, sort, merge, split, dedupe, convert (JSON/YAML/TSV/Markdown), stats, and pivot tables. Pure Python, zero external dependencies. GitHub: https://github.com/darbling/clawhub-skills 当用户需要处理CSV文件、数据清洗、格式转换、表格合并、去重、统计时触发。
---

# 📊 CSV Tool Pro

**Author: Lin Hui** | [GitHub](https://github.com/darbling/clawhub-skills) | MIT License | v1.0.0

One command to rule all your CSV files. View, filter, sort, merge, split, dedupe, convert, and analyze — all without leaving your terminal or opening Excel.

## ✨ Features

### Core Operations
- **View** — Pretty-print CSV with alignment and truncation
- **Filter** — Row filtering by column value, regex, or numeric range
- **Sort** — Single or multi-column sort (asc/desc)
- **Dedupe** — Remove duplicate rows by key columns

### Multi-File Operations
- **Merge** — Combine multiple CSVs (union by headers)
- **Join** — Inner/left/right/full join on key columns
- **Split** — Split large CSV into smaller files by row count or column value

### Format Conversion
- **to JSON** — Array of objects or nested format
- **to YAML** — Clean YAML output
- **to TSV** — Tab-separated output
- **to Markdown** — GitHub-flavored markdown table
- **to HTML** — Styled HTML table

### Analytics
- **Stats** — Count, mean, median, min, max, std for numeric columns
- **Frequency** — Value frequency distribution
- **Pivot** — Pivot table aggregation

## 🚀 Usage

### View a CSV file
```
Read the CSV file at /path/to/data.csv and show the first 20 rows in a nice table.
```

### Filter and sort
```
Read sales.csv, filter rows where amount > 1000, sort by date descending.
```

### Merge multiple CSVs
```
Merge january.csv and february.csv into a single file Q1.csv.
```

### Convert to JSON
```
Convert users.csv to JSON format and save as users.json.
```

### Stats
```
Show statistics for all numeric columns in metrics.csv.
```

### Dedupe
```
Remove duplicate rows from contacts.csv based on the email column.
```

### Pivot table
```
Create a pivot table from sales.csv with region as rows, product as columns, sum of amount as values.
```

## ⚙️ Technical Details

- **Runtime**: Python 3.6+
- **Dependencies**: Zero (stdlib only: csv, json, statistics, re, argparse, os)
- **Encoding**: Auto-detect UTF-8/GBK/UTF-8-BOM
- **Large files**: Streaming processing for files >100MB
- **Delimiters**: Auto-detect comma, tab, semicolon, pipe

## 📝 Notes

- Auto-detects delimiter (comma, tab, semicolon, pipe)
- Handles quoted fields with embedded delimiters and newlines
- Preserves original encoding on write
- Supports gzip-compressed CSV files
