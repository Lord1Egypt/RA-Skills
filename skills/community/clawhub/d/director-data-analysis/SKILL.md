---
name: data-analysis
description: Analyze CSV/Excel files to extract insights, generate statistics, create charts, and produce summaries. Use when user wants to (1) upload or analyze spreadsheet data, (2) get insights from data files, (3) generate charts or visualizations, (4) calculate statistics or trends, (5) clean or transform data.
---

# Data Analysis Skill

Analyze data files (CSV, Excel) and produce actionable insights.

## Quick Start

1. **Read the file** - Use appropriate library:
   - CSV: `csv` module or `pandas.read_csv()`
   - Excel: `pandas.read_excel()` with openpyxl engine

2. **Explore the data** - Get shape, columns, dtypes, missing values

3. **Generate insights** - Calculate:
   - Descriptive stats (mean, median, mode, std, min, max)
   - Correlations between numeric columns
   - Value counts for categorical columns
   - Trends over time if date column exists

4. **Create visualizations** - Use matplotlib:
   - Bar charts for categorical data
   - Line charts for time series
   - Histograms for distributions
   - Scatter plots for correlations

5. **Summarize** - Write findings in plain English

## Common Patterns

### Sales Data
```python
import pandas as pd

df = pd.read_csv('sales.csv')
summary = {
    'total_revenue': df['amount'].sum(),
    'avg_order': df['amount'].mean(),
    'top_products': df['product'].value_counts().head(5),
    'monthly_trend': df.groupby(pd.to_datetime(df['date']).dt.month)['amount'].sum()
}
```

### Customer Data
```python
demographics = df.groupby('segment').agg({
    'age': ['mean', 'median'],
    'income': ['mean', 'std'],
    'id': 'count'
})
```

### Time Series
```python
df['date'] = pd.to_datetime(df['date'])
monthly = df.resample('M', on='date')['value'].sum()
```

## Output Format

Always include:
1. **Overview** - What the data contains (rows, columns, date range)
2. **Key Metrics** - Top 5-10 actionable numbers
3. **Insights** - 3-5 bullet points of what the data reveals
4. **Visualizations** - At least 2 charts for any dataset with 100+ rows
5. **Recommendations** - Suggested next steps based on findings

## Error Handling

- Handle missing values: `df.fillna(0)` or `df.dropna()`
- Handle date parsing: Use `pd.to_datetime(..., errors='coerce')`
- Handle large files: Process in chunks for files >100MB
