---
name: csv-to-chart
description: >
  Use when (1) user pastes or uploads CSV data and asks to generate a chart, graph, or visualization. 
  (2) user wants to "plot" or "visualize" tabular data. (3) user provides data and says "make a chart", 
  "show this as a graph", or "visualize this". 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# CSV to Chart

Use when (1) user pastes or uploads CSV data and asks to generate a chart, graph, or visualization. (2) user wants to "plot" or "visualize" tabular data. (3) user provides data and says "make a chart", "show this as a graph", or "visualize this".

## Core Position

This skill solves the specific problem of: *user has tabular CSV data and needs a visual chart — not the raw numbers.*

This skill IS NOT:
- A data transformation tool (use csv-to-task for row-level operations)
- A reporting tool — it produces visual output, not written reports
- Activated by "analyze this data" alone — must involve chart/visualization intent

This skill IS activated ONLY when: chart/graph/visualization intent + CSV data are both present.

## Modes

### `/csv-to-chart`

**Default mode.** Reads CSV data and outputs a chart specification or renders the chart directly.

When to use: User provides CSV and explicitly asks for a chart, plot, graph, or visualization.

### `/csv-to-chart/suggest`

Suggests the most appropriate chart type based on data structure without generating the chart.

When to use: User is unsure which chart type fits their data.

## Execution Steps

### Step 1 — Parse the CSV

1. Receive CSV input (pasted text, file attachment, or path)
2. Detect header row — first row becomes column names
3. Detect column types:
   - Numeric → candidate for Y-axis / values
   - Date/datetime → candidate for X-axis / time series
   - Text/category → candidate for labels / categories
4. If CSV is malformed (uneven columns, no header), respond with specific fix request

### Step 2 — Select Chart Type

Choose the most appropriate chart based on data shape:

| Data Shape | Recommended Chart |
|---|---|
| 1 numeric col + 1 category col | Bar chart (vertical or horizontal) |
| 2+ numeric cols, 1 category col | Grouped/stacked bar, line |
| 1 time-series numeric col | Line chart |
| 2 numeric cols (correlation) | Scatter plot |
| Proportions summing to 100% | Pie / donut chart |
| Single numeric column | Histogram |
| 3+ numeric cols, many rows | Heatmap or radar |

If user specified a chart type, validate it makes sense for the data; warn if mismatched.

### Step 3 — Generate Chart

Produce chart using a library appropriate to context:
- Python: `matplotlib` or `plotly`
- JavaScript: `chart.js` or `plotly.js`
- Markdown/mermaid: `mermaid` flowchart for simple data

Output the complete, runnable code block with the chart. Include axis labels, title, and legend.

### Step 4 — Validate Output

- Verify chart renders without error
- Confirm X and Y axes match the data columns
- Ensure no data truncation or misordering

## Mandatory Rules

### Do not

- Do not assume column meaning from position — always use headers
- Do not强行 apply a pie chart to data with >7 categories
- Do not truncate data rows silently — warn if >500 rows
- Do not embed API keys in chart rendering code

### Do

- State the chart type being generated and why it fits the data
- Preserve original column names and data types
- Handle missing values explicitly (skip, zero-fill, or annotate)
- Add a clear title and axis labels

## Quality Bar

**A good output:**
- Chart type matches data shape and user intent
- All columns are correctly mapped to axes
- Code runs without modification and renders a visible chart
- Handles missing values and edge cases explicitly

**A bad output:**
- Renders a chart type unrelated to data (e.g., pie chart for 50 categories)
- Misplaces data on wrong axis (category on Y, numeric on X)
- Drops or reorders rows silently
- Code block missing dependencies or imports

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| Monthly sales data | Line chart with year as Y-axis | Line chart with month on X, sales on Y, labeled axes |
| Product categories | Pie chart with 20 slices | Horizontal bar chart, top 10 + "Other" |
| Two numeric columns | Static image without context | Scatter plot with axis labels and trend line |
| CSV with missing values | Drops rows silently | "Note: 3 rows omitted due to missing Q3 sales; treated as 0" |

## References

- `references/` — Chart type decision tree, code templates for plotly/matplotlib/chart.js