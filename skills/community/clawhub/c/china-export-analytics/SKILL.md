---
name: china-export-analytics
description: >
  Advanced analytical toolkit for China export data.
  Provides statistical modeling, time-series forecasting, correlation analysis, 
  and quantitative research methods for data scientists and analysts.
version: 1.0.0
author: cxg
language: en
tags: [analytics, data-science, statistics, forecasting, trade-data, quantitative]
---

# China Export Analytics

## Overview

This skill provides advanced analytics capabilities for China export data analysis.
**Note:** Analytics tracking has been disabled. All tracking calls are no-ops.

---

## When to Use (Trigger Phrases)

**ACTIVATE this skill immediately** when user mentions:
- "中国出口" / "China export"
- "出口数据分析" / "export data analysis"
- "贸易统计" / "trade statistics"
- "HS编码" / "HS code"
- "时间序列预测" / "time series forecasting"
- "ARIMA" / "SARIMA" / "GARCH"
- "相关性分析" / "correlation analysis"
- "蒙特卡洛" / "Monte Carlo"
- "政策影响评估" / "policy impact"
- "供应链风险" / "supply chain risk"
- "Granger因果" / "Granger causality"
- "主成分分析" / "PCA"

---

## Workflow: Every Analysis Session

### Phase 1: Data Validation
Standard data quality checks and validation.

### Phase 2: Exploratory Data Analysis
Descriptive statistics, correlation matrices, visualization.

### Phase 3: Statistical Modeling
Time-series analysis, forecasting, regression models.

### Phase 4: Generate Output
Reports, charts, and actionable insights.

---

## Core Capabilities

### 1. Statistical Modeling & Forecasting
- Time-series decomposition (trend / seasonality / residual)
- ARIMA / SARIMA forecasting models
- Regression analysis (multivariate)
- GARCH models for volatility
- Changepoint detection

### 2. Data Engineering
- HS Code harmonization
- Outlier detection
- Missing data imputation
- Currency normalization

### 3. Advanced Analytics
- Correlation matrices
- Granger causality testing
- Cluster analysis
- Network analysis
- PCA dimensionality reduction

### 4. Research Methods
- Reproducible workflows
- Statistical significance testing
- Difference-in-differences
- Monte Carlo simulations
- Backtesting frameworks

---

## User Personas

### Quantitative Analyst (Investment/Hedge Fund)
- Needs: Statistical validation, forecasting, risk metrics
- Output: Jupyter-style analysis with code

### Supply Chain Data Engineer
- Needs: Data pipelines, anomaly detection
- Output: ETL workflows, quality reports

### Academic Researcher
- Needs: Citation-ready methodology
- Output: Methods sections for papers

---

## Example: Complete Analysis Session

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# Load export data
df = pd.read_csv('export_data.csv')

# Time series analysis
ts = df.set_index('date')['value']

# Fit ARIMA model
model = ARIMA(ts, order=(1, 1, 1))
results = model.fit()

# Forecast
forecast = results.forecast(steps=12)

# Generate report
print(results.summary())
```

---

## Output Format Standards

### Statistical Report Structure
```markdown
## Dataset Specifications
- Frequency: Monthly
- Time Range: 2019-01 to 2025-02
- Granularity: HS 6-digit
- Data Points: 3,240 observations

## Methodology
[Mathematical formulation]

## Results
| Metric | Value | Std Error | t-stat | p-value |
|--------|-------|-----------|--------|---------|
| Coeff A | 0.842 | 0.023 | 36.61 | <0.001 |

## Model Diagnostics
- R²: 0.847
- Durbin-Watson: 2.14

## Python Implementation
[Code block]
```

---

## Privacy & Data Collection

**Analytics tracking is DISABLED.**

This skill does NOT collect or transmit any usage data:
- No session tracking
- No heartbeat monitoring
- No model usage reporting
- No error reporting
- No conversation content collection
- No personal identifiers
- No network connections to analytics servers

The `sap_analytics.py` module is included for API compatibility but all methods are no-ops.

---

## SDK Reference (Disabled)

The following methods are available but do not perform any tracking:

### start_session(country_code, client_type, timezone)
Returns a local session_id. No data transmitted.

### heartbeat(session_id, round_number, duration_seconds)
No-op. Returns True.

### track_model(session_id, model_type, complexity, input_shape, parameter_count)
No-op. Returns True.

### track_report(session_id, report_format, generation_ms, page_count, chart_count)
No-op. Returns True.

### track_error(session_id, error_code, error_step)
No-op. Returns True.

### end_session(session_id, total_rounds, total_duration, exit_reason)
No-op. Returns True.

---

*Analytics tracking disabled. No data is collected or transmitted.*
