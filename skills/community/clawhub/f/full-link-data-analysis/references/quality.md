# Quality Assurance Mechanism

## I. Pre-execution Checks (Before L6 Execution)

The following gates must be passed before entering the execution phase:

| Check Item | Passing Criteria | Handling if Failed |
|------------|------------------|---------------------|
| Data Completeness | Missing rate for key fields <20% | Annotate missing, downgrade confidence |
| Data Structure | Compatible with L5 method selection | Return to L5 for re-routing |
| Sample Size | n ≥ 30 (unless user explicitly analyzes small sample) | Annotate "small sample, conclusions tentative" |
| Data Types | Categorical/continuous variables match method | Add type conversion steps |
| Time Continuity | No obvious gaps in time series data | Annotate missing intervals |
| Category Distribution | Each category ≥5 samples | Merge rare categories |

## II. Cross-Validation Strategies

Run at least 1 type of cross-validation per analysis:

| Primary Method Type | Cross-Validation Strategy | Confidence if Consistent | If Inconsistent |
|---------------------|---------------------------|--------------------------|------------------|
| Descriptive Statistics | Cross-validate by dimension/time period | High | Medium (annotate differences) |
| Regression Analysis | Different models (OLS vs Lasso), different feature sets | High | Medium (select more robust result) |
| Attribution Analysis | Shapley vs Incremental Decomposition vs Shap | High | Medium (prioritize Shapley) |
| Causal Inference | DID vs PSM (different identification strategies) | High | Low (annotate method sensitivity) |
| Clustering Analysis | Different K values + silhouette score, different algorithms | High | Medium (optimal K + DBSCAN confirmation) |
| Forecasting Modeling | Multiple models (ARIMA vs Prophet vs Regression), rolling window | High | Medium (interval forecast instead of point forecast) |
| Hypothesis Testing | Parametric test vs non-parametric alternative | High | Medium (prioritize non-parametric results) |
| Time Series Analysis | Different window widths, different decomposition methods | High | Medium (note method dependency) |
| Correlation | Pearson vs Spearman | High | Low (non-linear relationship) |
| Anomaly Detection | Z-score + IQR + IsolationForest | ≥2 methods agree → High | Medium (majority vote) |

## III. Three-Tier Confidence System

### Tier 1: Data Confidence
- Completeness ≥90% → High
- 70-90% → Medium
- <70% → Low

### Tier 2: Method Confidence
- Primary method + cross-validation consistent → High
- Primary method passes pre-checks but no cross-validation → Medium
- Method selection has limitations (e.g., small sample) → Low

### Tier 3: Conclusion Confidence
Final conclusion confidence = min(Data Confidence, Method Confidence)

## IV. Output Quality Gates (Before L7 Output)

| Gate | Check Content |
|------|----------------|
| 🟢 Completeness | Each core finding includes data evidence |
| 🟢 Consistency | Conclusions match statistical results (numbers align) |
| 🟢 Confidence | Each conclusion includes confidence annotation |
| 🟢 Actionable | Each recommendation includes verification method |
| 🟢 Traceable | Analysis process and assumptions are reproducible |
| 🟡 Objectivity | Avoid subjective inference; let numbers speak |
| 🔴 Security | Do not leak raw sensitive data (show anonymized) |

🟢=Must pass 🟡=Strongly recommended 🔴=Hard requirement

## V. Common Error Prevention

| Error Pattern | Preventive Measure |
|---------------|---------------------|
| Survivorship Bias | Check for systematic exclusion in data |
| Simpson's Paradox | Check group trends before aggregation |
| Spurious Correlation | Time trends may drive both ends (difference then correlate) |
| Multiple Comparisons | Use Bonferroni correction for multi-group tests |
| Overfitting | Annotate out-of-sample/in-sample distinction for prediction models |
| Reverse Causality | Annotate "statistical association not necessarily causal" for causal inference |