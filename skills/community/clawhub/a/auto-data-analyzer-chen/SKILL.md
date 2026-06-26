---
name: auto-data-analyzer
description: Automated data analysis tool - Input CSV/Excel data and automatically generate comprehensive analysis reports. Includes data cleaning, statistical description, visualization, correlation analysis, and regression analysis. Ideal for rapid data analysis needs.
tags:
  - data
  - analysis
  - report
  - visualization
  - automation
version: 1.0.0
author: chenq
---

# auto-data-analyzer

Automated data analysis tool that generates comprehensive reports from input data.

## Features

### 1. Data Cleaning
- Missing value detection and handling
- Outlier detection
- Data type conversion
- Duplicate value handling

### 2. Statistical Description
- Basic statistics (mean, median, standard deviation, etc.)
- Quantile analysis
- Distribution visualization

### 3. Visualization
- Histograms
- Box plots
- Scatter plots
- Heatmaps

### 4. Advanced Analysis
- Correlation analysis
- Regression analysis
- Clustering analysis
- Time series analysis

## Usage

### Installation
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Basic Usage
```python
from analyzer import DataAnalyzer

analyzer = DataAnalyzer('data.csv')
analyzer.clean()
analyzer.describe()
analyzer.visualize()
analyzer.report()  # Generate HTML report
```

### Command Line
```bash
python main.py data.csv --output report.html
```

## Output

- HTML analysis report
- PNG charts
- CSV statistical results

## Use Cases

- Business data analysis
- Market research reports
- User behavior analysis
- Sales data analysis
