---
name: data-analysis-plus
description: "Enhanced data analysis with Python/R code templates, visualization gallery, statistical tests, and automated report generation. Covers hypothesis testing, regression, clustering, time series, and more."
metadata:
  author: opencode
  version: 2.0
  tags: data-analysis, statistics, visualization, python, r
  compatibility: opencode
  license: MIT
---

# Data Analysis Plus

Enhanced data analysis with code templates, visualization gallery, and statistical methods.

## Features

- **Code Templates**: Python/R ready-to-use templates
- **Visualization Gallery**: Charts for every analysis type
- **Statistical Methods**: Hypothesis testing, regression, clustering
- **Automated Reports**: Decision-ready output formats
- **Data Validation**: Quality checks before analysis

## Quick Reference

| Analysis Type | Python Template | R Template |
|---------------|-----------------|------------|
| Descriptive | `df.describe()` | `summary(df)` |
| Hypothesis | `scipy.stats.ttest_ind()` | `t.test()` |
| Regression | `sklearn.linear_model` | `lm()` |
| Clustering | `sklearn.cluster.KMeans` | `kmeans()` |
| Time Series | `statsmodels.tsa` | `forecast::auto.arima()` |

## Python Templates

### Data Loading

```python
import pandas as pd
import numpy as np

# CSV
df = pd.read_csv("data.csv")

# Excel
df = pd.read_excel("data.xlsx")

# JSON
df = pd.read_json("data.json")

# Database
import sqlalchemy
engine = sqlalchemy.create_engine("sqlite:///data.db")
df = pd.read_sql("SELECT * FROM table", engine)
```

### Descriptive Statistics

```python
# Basic stats
df.describe()

# By group
df.groupby("category").agg({
    "value": ["mean", "median", "std", "count"]
})

# Correlation
df.corr()
```

### Data Cleaning

```python
# Missing values
df.isnull().sum()
df.fillna(df.mean())
df.dropna()

# Duplicates
df.duplicated().sum()
df.drop_duplicates()

# Outliers
Q1 = df["value"].quantile(0.25)
Q3 = df["value"].quantile(0.75)
IQR = Q3 - Q1
df = df[(df["value"] >= Q1 - 1.5*IQR) & (df["value"] <= Q3 + 1.5*IQR)]
```

### Hypothesis Testing

```python
from scipy import stats

# T-test
group1 = df[df["group"] == "A"]["value"]
group2 = df[df["group"] == "B"]["value"]
stat, p_value = stats.ttest_ind(group1, group2)

# Chi-square
contingency = pd.crosstab(df["cat1"], df["cat2"])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

# ANOVA
f_stat, p_value = stats.f_oneway(group1, group2, group3)
```

### Regression

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = df[["feature1", "feature2"]]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

print(f"R²: {model.score(X_test, y_test)}")
print(f"Coefficients: {model.coef_}")
```

### Clustering

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[["feature1", "feature2"]])

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)
```

### Time Series

```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# Parse dates
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# Decompose
decomposition = seasonal_decompose(df["value"], model="additive", period=12)
decomposition.plot()
```

## R Templates

### Data Loading

```r
library(readr)
library(readxl)

# CSV
df <- read_csv("data.csv")

# Excel
df <- read_excel("data.xlsx")

# JSON
library(jsonlite)
df <- fromJSON("data.json")
```

### Descriptive Statistics

```r
# Basic stats
summary(df)

# By group
library(dplyr)
df %>%
  group_by(category) %>%
  summarise(
    mean = mean(value, na.rm = TRUE),
    median = median(value, na.rm = TRUE),
    sd = sd(value, na.rm = TRUE),
    n = n()
  )

# Correlation
cor(df[, sapply(df, is.numeric)], use = "complete.obs")
```

### Hypothesis Testing

```r
# T-test
t.test(value ~ group, data = df)

# Chi-square
chisq.test(table(df$cat1, df$cat2))

# ANOVA
aov_result <- aov(value ~ group, data = df)
summary(aov_result)
```

### Regression

```r
# Linear regression
model <- lm(target ~ feature1 + feature2, data = df)
summary(model)

# Logistic regression
model <- glm(binary_target ~ feature1 + feature2, data = df, family = "binomial")
summary(model)
```

### Clustering

```r
# K-means
library(cluster)
df_scaled <- scale(df[, c("feature1", "feature2")])
kmeans_result <- kmeans(df_scaled, centers = 3)
df$cluster <- kmeans_result$cluster
```

## Visualization Gallery

### Chart Selection Guide

| Question Type | Chart | Python | R |
|---------------|-------|--------|---|
| Trend over time | Line | `matplotlib` | `ggplot2` |
| Comparison | Bar | `seaborn.barplot` | `ggplot2::geom_bar` |
| Distribution | Histogram | `seaborn.histplot` | `ggplot2::geom_histogram` |
| Relationship | Scatter | `seaborn.scatterplot` | `ggplot2::geom_point` |
| Composition | Pie/Stacked Bar | `matplotlib.pyplot.pie` | `ggplot2::geom_bar(position="fill")` |
| Correlation | Heatmap | `seaborn.heatmap` | `pheatmap` |

### Python Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Line plot
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="date", y="value", hue="category")
plt.title("Trend Over Time")
plt.savefig("trend.png", dpi=300, bbox_inches="tight")

# Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="feature1", y="feature2", hue="target")
plt.title("Feature Relationship")
plt.savefig("scatter.png", dpi=300, bbox_inches="tight")

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.savefig("heatmap.png", dpi=300, bbox_inches="tight")
```

### R Visualization

```r
library(ggplot2)

# Line plot
ggplot(df, aes(x = date, y = value, color = category)) +
  geom_line() +
  labs(title = "Trend Over Time") +
  theme_minimal()

# Scatter plot
ggplot(df, aes(x = feature1, y = feature2, color = target)) +
  geom_point() +
  labs(title = "Feature Relationship") +
  theme_minimal()

# Bar plot
ggplot(df, aes(x = category, fill = category)) +
  geom_bar() +
  labs(title = "Category Distribution") +
  theme_minimal()
```

## Statistical Methods

### Hypothesis Testing Decision Tree

```
Is the data categorical?
├── Yes → Chi-square test
└── No → Is the data normally distributed?
    ├── Yes → T-test (2 groups) / ANOVA (3+ groups)
    └── No → Mann-Whitney U (2 groups) / Kruskal-Wallis (3+ groups)
```

### Sample Size Calculator

```python
def sample_size计算器(effect_size, alpha=0.05, power=0.8):
    from statsmodels.stats.power import TTestIndPower
    analysis = TTestIndPower()
    n = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power)
    return int(np.ceil(n * 2))  # Total sample size
```

## Report Templates

### Executive Summary

```markdown
# [Analysis Title]

## Key Findings
1. [Finding 1 with evidence]
2. [Finding 2 with evidence]
3. [Finding 3 with evidence]

## Methodology
- Data: [source, timeframe, sample size]
- Methods: [statistical tests used]
- Limitations: [caveats]

## Recommendations
1. [Action 1]
2. [Action 2]
3. [Action 3]

## Appendix
- Charts: [list of visualizations]
- Statistical tables: [p-values, confidence intervals]
```

### Technical Report

```markdown
# [Analysis Title] - Technical Report

## Data
- Source: [database/file]
- Records: [count]
- Variables: [list with types]
- Missing values: [summary]

## Methods
- [Method 1]: [justification]
- [Method 2]: [justification]

## Results
### [Test 1]
- Statistic: [value]
- p-value: [value]
- Effect size: [value]
- Confidence interval: [range]

## Code
[Reproducible code]
```

## Best Practices

1. **Start with EDA** - Understand data before analysis
2. **Validate data** - Check quality, missing values, outliers
3. **Document assumptions** - State methodology choices
4. **Report uncertainty** - Confidence intervals, p-values
5. **Visualize results** - Charts communicate better
6. **Make reproducible** - Save code, set seeds
7. **Peer review** - Have someone check your work

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| P-hacking | Pre-register hypotheses |
| Correlation ≠ causation | Use experiments when possible |
| Selection bias | Random sampling |
| Survivorship bias | Include failures |
| Simpson's paradox | Stratify analysis |
