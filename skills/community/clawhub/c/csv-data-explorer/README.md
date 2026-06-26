# CSV Data Explorer

A CLI tool to explore, analyze, and visualize CSV data directly from the terminal. Load CSV files, filter rows, calculate statistics, generate summaries, and create basic visualizations.

## Installation

Install via ClawHub:

```bash
clawhub install csv-data-explorer
```

## Usage

### Basic Commands

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

### Interactive Mode

```bash
python3 scripts/main.py interactive data.csv
```

Interactive mode guides you through:
1. File loading and preview
2. Column selection and filtering
3. Statistical analysis
4. Visualization options
5. Export results

## Features

- Load and preview CSV files with automatic delimiter detection
- Explore data structure - view columns, data types, missing values
- Filter rows based on conditions (equality, inequality, contains, regex)
- Select columns - include/exclude specific columns
- Calculate statistics - mean, median, min, max, standard deviation, percentiles
- Generate summaries - count, unique values, frequency distributions
- Basic visualizations - histograms, bar charts, scatter plots (ASCII or simple terminal output)
- Export results - filtered data, statistics, summaries to new CSV/JSON files
- Interactive mode for step-by-step exploration

## Requirements

- Python 3.x
- `pandas` library (installed automatically or via pip)
- `matplotlib` library (optional, for enhanced charts)

Install missing dependencies:
```bash
pip3 install pandas matplotlib
```

## Limitations

- Large files (>100MB) may be slow to process
- Visualizations are ASCII-based or simple terminal plots
- No support for Excel files or other formats (CSV only)
- Limited to basic statistical functions
- Memory usage scales with file size

## Examples

### Filter and Calculate Statistics

```bash
python3 scripts/main.py filter sales.csv --where "Region == 'North' and Amount > 100" --stats
```

### Generate Histogram

```bash
python3 scripts/main.py histogram sales.csv --column Amount --bins 5
```

### Interactive Exploration

```bash
python3 scripts/main.py interactive sales.csv
```

## License

MIT