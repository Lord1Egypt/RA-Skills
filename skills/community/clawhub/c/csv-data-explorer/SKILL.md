---
name: csv-data-explorer
description: Explore, filter, summarize, and visualize CSV data directly in terminal with interactive queries.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - pandas
        - matplotlib
---

# CSV Data Explorer

## What This Does

A CLI tool to explore, analyze, and visualize CSV data directly from the terminal. Load CSV files, filter rows, calculate statistics, generate summaries, and create basic visualizations without leaving your terminal.

Key features:
- **Load and preview CSV files** with automatic delimiter detection
- **Explore data structure** - view columns, data types, missing values
- **Filter rows** based on conditions (equality, inequality, contains, regex)
- **Select columns** - include/exclude specific columns
- **Calculate statistics** - mean, median, min, max, standard deviation, percentiles
- **Generate summaries** - count, unique values, frequency distributions
- **Basic visualizations** - histograms, bar charts, scatter plots (ASCII or simple terminal output)
- **Export results** - filtered data, statistics, summaries to new CSV/JSON files
- **Interactive mode** - step-by-step exploration with prompts
- **Command-line mode** - scriptable operations for automation

## When To Use

- You need to quickly explore CSV data without opening spreadsheets
- You want to filter and analyze data for reporting or debugging
- You need to calculate basic statistics on datasets
- You're working on servers/remote machines without GUI tools
- You want to automate CSV data processing in scripts
- You need to share analysis results with team members
- You're teaching data analysis concepts in terminal environment

## Usage

Basic commands:

```bash
# Load and preview a CSV file
python3 scripts/main.py preview data.csv

# Show basic statistics
python3 scripts/main.py stats data.csv

# Filter rows where column 'age' > 30
python3 scripts/main.py filter data.csv --where "age > 30"

# Select specific columns
python3 scripts/main.py select data.csv --columns name,age,salary

# Generate histogram for a column
python3 scripts/main.py histogram data.csv --column age --bins 10

# Count unique values in a column
python3 scripts/main.py unique data.csv --column category

# Export filtered data
python3 scripts/main.py filter data.csv --where "salary > 50000" --output filtered.csv

# Interactive exploration mode
python3 scripts/main.py interactive data.csv
```

## Examples

### Example 1: Preview and basic statistics

```bash
python3 scripts/main.py preview sales.csv --limit 10
```

Output:
```
CSV File: sales.csv (1000 rows × 5 columns)

First 10 rows:
┌─────┬────────────┬───────────┬────────┬───────────┐
│ Row │ Date       │ Product   │ Amount │ Region    │
├─────┼────────────┼───────────┼────────┼───────────┤
│ 1   │ 2024-01-01 │ Widget A  │ 150.50 │ North     │
│ 2   │ 2024-01-01 │ Widget B  │ 89.99  │ South     │
│ ... │ ...        │ ...       │ ...    │ ...       │
└─────┴────────────┴───────────┴────────┴───────────┘

Column summary:
- Date: 1000 non-null, type: datetime
- Product: 1000 non-null, type: string (5 unique values)
- Amount: 1000 non-null, type: float (min: 10.00, max: 999.99)
- Region: 1000 non-null, type: string (4 unique values)
```

### Example 2: Filter and calculate statistics

```bash
python3 scripts/main.py filter sales.csv --where "Region == 'North' and Amount > 100" --stats
```

Output:
```
Filtered data: 237 rows (from 1000 total)

Statistics for filtered data:
- Count: 237
- Mean Amount: 245.67
- Median Amount: 210.50
- Min Amount: 101.00
- Max Amount: 999.99
- Standard Deviation: 145.23
```

### Example 3: Generate histogram

```bash
python3 scripts/main.py histogram sales.csv --column Amount --bins 5
```

Output (ASCII approximation):
```
Amount Distribution (5 bins):
[10.00 - 207.99]  ████████████████████████████ 312
[208.00 - 405.99] ████████████████████ 241
[406.00 - 603.99] ██████████ 152
[604.00 - 801.99] █████ 78
[802.00 - 999.99] ███ 45
```

### Example 4: Interactive mode

```bash
python3 scripts/main.py interactive sales.csv
```

Interactive mode guides you through:
1. File loading and preview
2. Column selection and filtering
3. Statistical analysis
4. Visualization options
5. Export results

## Requirements

- Python 3.x
- `pandas` library for data manipulation (installed automatically or via pip)
- `matplotlib` library for visualizations (optional, for enhanced charts)

Install missing dependencies:
```bash
pip3 install pandas matplotlib
```

## Limitations

- Large files (>100MB) may be slow to process
- Visualizations are ASCII-based or simple terminal plots
- No support for Excel files or other formats (CSV only)
- Limited to basic statistical functions (not advanced analytics)
- No support for time series analysis or complex aggregations
- Memory usage scales with file size
- No built-in support for database connections
- No support for streaming/processing very large datasets
- Visualizations limited to terminal capabilities
- No support for geographic data or maps
- Limited error handling for malformed CSV files
- No built-in data cleaning or transformation functions
- Performance may be slower than specialized tools like R or specialized libraries

## Directory Structure

The tool works with CSV files in the current directory or specified paths. No special configuration directories are required.

## Error Handling

- Invalid CSV files show helpful error messages with line numbers
- Missing columns suggest available column names
- Type conversion errors show expected vs actual types
- Memory errors suggest using smaller files or filtering first
- File not found errors suggest checking path and permissions

## Contributing

This is a skill built by the Skill Factory. Issues and improvements should be reported through the OpenClaw project.