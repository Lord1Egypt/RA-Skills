---
name: csv-data-processor
description: CSV and delimited data processing toolkit for transforming, filtering, merging, validating, and converting data files. Use when the user wants to: (1) View, filter, or sort CSV files, (2) Merge or join multiple CSV files, (3) Convert between CSV, JSON, and SQL, (4) Clean and validate CSV data (remove duplicates, fix encoding), (5) Extract columns or apply transformations, (6) Generate statistics and summaries, (7) Handle TSV, pipe-delimited, or custom delimiter files.
---

# CSV Data Processor

Transform, filter, clean, and convert delimited data files. No external dependencies — uses Python csv/JSON stdlib only.

## Quick Start

```bash
# View first 10 rows
python3 skills/csv-data-processor/scripts/csv_view.py data.csv

# Filter rows
python3 skills/csv-data-processor/scripts/csv_filter.py data.csv --where "age > 25"

# Convert to JSON
python3 skills/csv-data-processor/scripts/csv_convert.py data.csv --to json
```

## Common Commands

### Preview Data
```bash
python3 skills/csv-data-processor/scripts/csv_view.py data.csv --head 10 --stats
```

### Filter Rows
```bash
python3 skills/csv-data-processor/scripts/csv_filter.py data.csv --where "price > 100" --sort price --limit 20
```

### Merge Files
```bash
python3 skills/csv-data-processor/scripts/csv_merge.py sales_2024.csv sales_2025.csv --output combined.csv
```

### Join on Column
```bash
python3 skills/csv-data-processor/scripts/csv_join.py left.csv right.csv --on user_id --output joined.csv
```

### Clean Data
```bash
python3 skills/csv-data-processor/scripts/csv_clean.py dirty.csv --dedupe --fill-missing N/A --output clean.csv
```

### Statistics
```bash
python3 skills/csv-data-processor/scripts/csv_stats.py data.csv --numeric age,revenue
```

## Scripts

| Script | Purpose |
|--------|---------|
| `csv_view.py` | Preview, head/tail, summary stats |
| `csv_filter.py` | Filter rows, sort, select columns |
| `csv_merge.py` | Concatenate multiple CSV files |
| `csv_join.py` | Join/merge on shared columns |
| `csv_convert.py` | Convert CSV ↔ JSON ↔ SQL |
| `csv_clean.py` | Dedupe, fill missing, fix encoding |
| `csv_stats.py` | Numeric stats, value counts, histograms |

## Key Options

All scripts accept:
- `--delimiter` — Field delimiter (default: `,` for CSV, `\t` for TSV)
- `--encoding` — File encoding (default: utf-8)
- `--has-header` / `--no-header` — Column header handling
- `--output` / `-o` — Output file path
