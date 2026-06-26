---
name: autoplot-skill
description: |
  Automatically visualize any data file (CSV/Excel/JSON) with one command. No coding required.
  
  Keywords: data visualization, chart generator, CSV plot, CSV visualization, Excel chart, JSON visualization, automatic graph, no-code visualization, data analysis, plot generator, 数据可视化, 图表生成, CSV画图, Excel转图表
  
  Use this skill when:
  - "Visualize this CSV file"
  - "Visualize CSV data"
  - "Create a chart from this data"
  - "Create chart from Excel"
  - "Plot these sales numbers"
  - "Plot my data without coding"
  - "Show me trends in this dataset"
  - "Make a bar chart from this Excel file"
  - "Generate an infographic from this JSON"
  - "Make a graph from JSON"
  - "Analyze and visualize this data"
  - "CSV转图表"
  - "数据可视化"
  - "Excel画图"
  
  Auto-detects data types, selects optimal chart type (line, bar, scatter, pie, histogram), and generates publication-ready visualizations in PNG, SVG, HTML, PDF formats.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      optional:
        - node  # For interactive HTML output
---

# AutoPlot - Automatic Data Visualization

Transform any data file into beautiful charts with one command. No Python, no coding, just results.

## When to Use

✅ **Use this skill when:**
- "Visualize this CSV file"
- "Create a chart from this data"
- "Plot these sales numbers"
- "Show me trends in this dataset"
- "Make a bar chart from this Excel file"
- "Generate an infographic from this JSON"
- "Analyze and visualize this data"

❌ **Don't use when:**
- Real-time streaming data visualization
- Complex statistical analysis (use dedicated tools)
- 3D visualization (not supported yet)

## Features

### 1. Auto-Detection
- **File format** - CSV, Excel (.xlsx/.xls), JSON
- **Data types** - Numeric, categorical, datetime, text
- **Relationships** - Correlations, trends, distributions

### 2. Smart Chart Selection
| Data Pattern | Auto-Selected Chart |
|-------------|---------------------|
| Time series | Line chart with trend |
| Categories + values | Bar chart |
| Distributions | Histogram / Box plot |
| Correlations | Scatter plot + regression |
| Proportions | Pie / Donut chart |
| Geographic | Map visualization |

### 3. Output Formats
- **PNG** - Static image, email-ready
- **SVG** - Scalable, web-ready
- **HTML** - Interactive, zoom/pan/hover
- **PDF** - Publication quality

### 4. Styling
- Professional themes (default, minimal, dark)
- Auto-color palettes
- Responsive sizing
- Annotations and labels

## Quick Start

### Check installation
```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py --version
```

### Visualize a file
```bash
# Auto-detect and visualize
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize data.csv

# Specify output format
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize sales.xlsx --format html

# Custom title and theme
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize metrics.json --title "Q4 Performance" --theme dark
```

## Commands

### visualize
Create visualization from data file.

```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize <file> [options]

Options:
  --chart-type    Override auto-detection (bar, line, scatter, pie, histogram, box)
  --x-column      Specify X-axis column
  --y-column      Specify Y-axis column
  --title         Chart title
  --theme         Visual theme (default, minimal, dark, colorful)
  --format        Output format (png, svg, html, pdf)
  --output        Output file path
  --width         Chart width in pixels (default: 1200)
  --height        Chart height in pixels (default: 800)
```

### analyze
Analyze data structure and suggest visualizations.

```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py analyze <file> [options]

Options:
  --detailed      Show detailed statistics
  --sample N      Show first N rows
```

### dashboard
Generate multi-chart dashboard.

```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py dashboard <file> [options]

Options:
  --charts N      Number of charts to include
  --layout        Layout style (grid, vertical, horizontal)
```

## Examples

### Example 1: Sales Data
Input: `sales.csv`
```csv
Month,Revenue,Profit,Customers
Jan,10000,3000,150
Feb,12000,4000,180
Mar,15000,5000,220
```

Command:
```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize sales.csv --title "Q1 Sales Performance"
```

Output:
- Line chart for Revenue/Profit trend
- Bar chart for Customers by month
- Correlation heatmap

### Example 2: Survey Results
Input: `survey.xlsx` with categorical data

Command:
```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize survey.xlsx --chart-type pie
```

Output: Pie chart showing response distribution

### Example 3: Interactive Dashboard
```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py dashboard metrics.json --format html
```

Output: `metrics_dashboard.html` - Open in browser for interactive exploration

## Supported Data Formats

### CSV
- Comma or tab delimited
- Headers auto-detected
- Date columns auto-parsed

### Excel
- .xlsx and .xls
- Multiple sheets (specify with --sheet)
- Formulas evaluated

### JSON
- Array of objects
- Nested objects flattened
- Metadata preserved

## Chart Types

### Available Charts
- **Line** - Time series, trends
- **Bar** - Comparisons, rankings
- **Scatter** - Correlations, clusters
- **Pie/Donut** - Proportions
- **Histogram** - Distributions
- **Box/Violin** - Statistical summaries
- **Heatmap** - Correlation matrices
- **Area** - Cumulative trends
- **Bubble** - Multi-dimensional

### Auto-Selection Logic
```
if datetime_column:
    -> Line chart
elif categorical + numeric:
    -> Bar chart
elif two_numeric:
    if correlation_detected:
        -> Scatter + regression
    else:
        -> Scatter
elif single_numeric:
    -> Histogram
elif categorical_only:
    -> Count plot / Pie
```

## Styling Options

### Themes
- **default** - Clean, professional
- **minimal** - No grid, minimal labels
- **dark** - Dark background, neon colors
- **colorful** - Vibrant palette
- **print** - B&W optimized

### Customization
```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize data.csv \
  --theme dark \
  --title "Revenue Analysis" \
  --width 1600 \
  --height 900
```

## Output Examples

### PNG (Static)
- Email attachments
- Documents
- Social media

### SVG (Vector)
- Scalable without quality loss
- Web embedding
- Print materials

### HTML (Interactive)
- Zoom and pan
- Hover tooltips
- Toggle data series
- Export to PNG

### PDF (Publication)
- Research papers
- Reports
- Presentations

## Advanced Usage

### Multi-Series Charts
```bash
# Plot multiple columns
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize data.csv \
  --y-column Revenue,Profit,Expenses \
  --chart-type line
```

### Aggregations
```bash
# Group by category and aggregate
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize data.csv \
  --group-by Category \
  --aggregate sum
```

### Filtering
```bash
# Filter data before plotting
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize data.csv \
  --filter "Year >= 2020" \
  --filter "Status = 'Active'"
```

## Integration with OpenClaw

### In conversation
```
User: "Show me the trend in sales.csv"
AI: [Uses autoplot to generate line chart]

User: "Create a dashboard from this Excel file"
AI: [Generates multi-chart HTML dashboard]
```

### Batch processing
```bash
# Visualize all CSV files in directory
for file in *.csv; do
    python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize "$file"
done
```

## Requirements

- Python 3.8+
- pandas
- plotly / matplotlib
- openpyxl (for Excel files)

## Installation

```bash
# Install dependencies
pip install -r ~/.openclaw/workspace/autoplot/requirements.txt

# Verify installation
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py --version
```

## Troubleshooting

### Large datasets (>100k rows)
Use sampling:
```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize big.csv --sample 10000
```

### Memory issues
Process in chunks or use aggregation.

### Date parsing errors
Specify date format:
```bash
python3 ~/.openclaw/workspace/autoplot/scripts/autoplot.py visualize data.csv --date-format "%Y-%m-%d"
```

## Roadmap

- [ ] 3D visualization support
- [ ] Animation/timelapse charts
- [ ] Real-time data streaming
- [ ] SQL database connections
- [ ] Custom chart templates
- [ ] API server mode

## License

MIT License - See LICENSE file

## Credits

Built with Plotly, Pandas, and OpenClaw
