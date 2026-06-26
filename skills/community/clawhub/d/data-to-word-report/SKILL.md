---
name: data-to-word-report
description: Automatically generate a professional Word analysis report from user-provided data files, including data overview, key metric statistics and trend analysis, key findings and conclusions. 
---

# Data to Word Analysis Report

Automatically generate a professionally formatted analysis report (.docx) from data files, ready for presentation.

## Use Cases

Use when users need to "generate analysis report", "convert data to Word", or "produce a report".

## Workflow

### 1. Read Data

Read the user-uploaded data file, automatically detect the format (CSV/JSON/Excel/TXT), extract the data, and confirm the structure.

### 2. Analyze Data

Perform the following analysis on the data:
- **Data Overview**: Row count, column count, field types, missing value statistics, time range
- **Key Metrics**: Mean/median/max/min/standard deviation for key numeric columns
- **Trend Analysis**: If a time column exists, calculate trends by time dimension
- **Key Findings**: Outliers, significant changes, critical conclusions

### 3. Generate Report

Call the script to generate the Word report:

```bash
python3 scripts/gen_report.py '<output_path>' '<report_json>'
```

- `output_path`: Output path, e.g., `/root/.openclaw/workspace/analysis_report.docx`
- `report_json`: JSON string, see structure below

### report_json Structure

```json
{
  "title": "Data Analysis Report",
  "sections": [
    {
      "heading": "I. Data Overview",
      "paragraphs": ["This analysis covers 1,234 records...", "Time range: 2024-01 to 2024-12"],
      "table": {
        "headers": ["Metric", "Value"],
        "rows": [["Total Records", "1,234"], ["Fields", "8"], ["Missing Rate", "2.1%"]]
      }
    },
    {
      "heading": "II. Key Metrics",
      "paragraphs": ["Average sales: 456K, median: 382K..."],
      "table": {
        "headers": ["Metric", "Mean", "Median", "Max", "Min"],
        "rows": [["Sales (10K)", "45.6", "38.2", "120.5", "5.3"]]
      }
    },
    {
      "heading": "III. Trend Analysis",
      "paragraphs": ["Overall upward trend, Q4 grew 23% QoQ..."],
      "table": null
    },
    {
      "heading": "IV. Key Findings & Recommendations",
      "paragraphs": ["1. East China region accounts for the highest share (38%)...", "2. December return rate abnormally rose to 5.7%..."],
      "table": null
    }
  ]
}
```

The `table` field in each section is optional; pass `null` to output only paragraphs.

### 4. Output Results

Inform the user of the file save location and display an overview of the report structure.