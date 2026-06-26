---
name: data-analysis-pro
description: |
  Data analysis pro skill providing three core functions: data analysis, data interpretation, and data visualization.
  
  **Use Cases**:
  (1) Data Analysis - Statistics, filtering, aggregation, calculation (e.g., "Calculate total sales", "Filter data greater than 100")
  (2) Data Interpretation - Trend analysis, pattern discovery, report generation (e.g., "Analyze sales trends", "Interpret data changes")
  (3) Data Visualization - Chart generation, data display (e.g., "Draw a bar chart", "Generate a pie chart")
  
  **Trigger Keywords**: analyze data, statistics, calculate, interpret trends, generate chart, visualize, plot
  
  **Prerequisites**: Set environment variable CHARTGEN_API_KEY (obtain from chartgen.ai)
metadata:
  openclaw:
    requires:
      env:
        - CHARTGEN_API_KEY
---

# ChartGen Data Analysis

Data analysis skill based on ChartGen API, supporting natural language-based data analysis, interpretation, and visualization.

## Overview

This skill enables codeless data analysis through natural language interaction. It supports Text2SQL, Text2Data, and Text2Code analysis. Simply provide Excel/CSV files or JSON data to automatically execute data queries, data interpretation, and data visualization (ChatBI).

The skill will intelligently parse time, metrics, and analytical dimensions through conversational queries, then generate SQL queries for data, create interactive BI charts, structured analysis reports. Optimized for standardized vertical datasets, powered by enterprise-grade analytics engine for reliable results.

**API Service**: This skill uses the ChartGen API service hosted at [chartgen.ai](https://chartgen.ai). All data is sent to `https://chartgen.ai/api/platform_api/` for processing.

---

## Quick Start

### 1. Apply for an API Key

You can easily create and manage your API Key at [chartgen.ai](https://chartgen.ai). To begin with, you need to register for an account.

**Steps:**
1. Visit [chartgen.ai](https://chartgen.ai) and sign up for an account
2. Access the API management dashboard
3. Create a new API and set the credit consumption limit
4. Copy the API Key for use

### 2. Configure Environment Variable

```bash
export CHARTGEN_API_KEY="your-api-key-here"
```

### 3. Run Scripts

```bash
# Data Analysis
python scripts/data_analysis.py --query "Calculate total sales by region" --file sales.xlsx

# Data Interpretation
python scripts/data_interpretation.py --query "Analyze sales trends" --file sales.xlsx

# Data Visualization
python scripts/data_visualization.py --query "Draw a bar chart of sales by region" --file sales.xlsx
```

---

## Credit Rules

- Calling a single tool consumes 20 credits
- You get 200 free credits per month for free accounts
- When credits run out, you can purchase more or upgrade your account on the [chartgen.ai Billing page](https://chartgen.ai/billing)

---

## Scripts Reference

| Script | Function | Use Case |
|--------|----------|----------|
| `data_analysis.py` | Data Analysis | Statistics, filtering, aggregation, calculation |
| `data_interpretation.py` | Data Interpretation | Trend analysis, pattern discovery, report generation |
| `data_visualization.py` | Data Visualization | Chart generation, data display |

---

## Parameters

### Common Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--query` | ✅ | Natural language query statement |
| `--file` | ❌ | Local file path (.xlsx/.xls/.csv), mutually exclusive with --json |
| `--json` | ❌ | JSON data (string or file path), mutually exclusive with --file |

### Visualization Specific Parameters

| Parameter | Description |
|-----------|-------------|
| `--output, -o` | Output HTML file path (defaults to /tmp/openclaw/charts/) |

---

## Data Format

### File Format

Supports `.xlsx`, `.xls`, `.csv` Excel and CSV files.

Note: Only one of --file or --json is needed. If both are provided, --file takes precedence. File types support both row-metric-column data files and column-metric-row data files.

### JSON Format

JSON data should be an array format, where each element is a row of data:

```json
[
  {"name": "Product A", "sales": 1000, "region": "East"},
  {"name": "Product B", "sales": 1500, "region": "North"},
  {"name": "Product C", "sales": 800, "region": "South"}
]
```

Or pass via file:

```bash
python scripts/data_analysis.py --query "Analyze the data" --json data.json
```

---

## Usage Examples

### Data Analysis

```bash
# Statistical calculation
python scripts/data_analysis.py --query "Calculate total and average sales by region" --file sales.xlsx

# Data filtering
python scripts/data_analysis.py --query "Filter products with sales greater than 1000" --file sales.xlsx

# Sorting
python scripts/data_analysis.py --query "Sort by sales in descending order" --file sales.xlsx
```

### Data Interpretation

```bash
# Trend analysis
python scripts/data_interpretation.py --query "Analyze monthly sales trends" --file monthly_sales.xlsx

# Anomaly detection
python scripts/data_interpretation.py --query "Find and explain anomalies in the data" --file data.xlsx

# Comprehensive interpretation
python scripts/data_interpretation.py --query "Provide a comprehensive analysis of this data with key insights" --file report.xlsx
```

### Data Visualization

```bash
# Bar chart
python scripts/data_visualization.py --query "Draw a bar chart of sales by product" --file sales.xlsx

# Line chart
python scripts/data_visualization.py --query "Draw a line chart of sales trends" --file trends.xlsx

# Pie chart
python scripts/data_visualization.py --query "Draw a pie chart of sales by region" --file sales.xlsx

# Save to specific path
python scripts/data_visualization.py --query "Draw a scatter plot" --file data.xlsx -o /path/to/chart.html
```

---

## Output Description

### Data Analysis & Data Interpretation

Returns Markdown format text results, including analysis conclusions, data tables, etc.

### Data Visualization

1. **Console Output**: ECharts configuration JSON
2. **HTML File**: Can be opened in browser to view the chart

---

## Error Handling

Common errors and solutions:

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `CHARTGEN_API_KEY not set` | Environment variable not set | `export CHARTGEN_API_KEY="your-key"` |
| `API request timeout` | Request timeout | Check network connection and retry |
| `File not found` | File does not exist | Check if file path is correct |
| `credits are insufficient` | Insufficient credits | Recharge or contact administrator |

---

## Technical Details

- **API Base URL**: `https://chartgen.ai/api/platform_api/`
- **Authentication**: Header `Authorization: <api-key>`
- **Request Format**: JSON
- **Timeout**: 60 seconds
- **Required Environment Variable**: `CHARTGEN_API_KEY`

See `scripts/chartgen_api.py` for implementation details.

---

## Privacy Notice

**Data sent to remote API**: This skill reads your provided data files (CSV/XLSX/JSON), base64-encodes them, and sends them to the ChartGen API at `https://chartgen.ai/api/platform_api/` for analysis and chart generation. Your data will leave your machine.

**Recommendations**:
- Do not upload sensitive or regulated data
- Use a dedicated API key with limited scope/credits
- Review the privacy practices at [chartgen.ai](https://chartgen.ai) before use
