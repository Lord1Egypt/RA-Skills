# Statistical Analysis Reference

## When to Use
Data has multiple numeric columns with no obvious business label. Research data, survey data, scientific measurements, multi-variable datasets.
Keywords: 相关性, 分布, 回归, 异常值, correlation, distribution, regression, outlier, statistical.

## Correlation Analysis

```python
import pandas as pd
import numpy as np

numeric_cols = df.select_dtypes(include='number').columns.tolist()

# Correlation matrix
corr = df[numeric_cols].corr()

# Find strongest correlations
corr_pairs = []
for i in range(len(numeric_cols)):
    for j in range(i+1, len(numeric_cols)):
        val = corr.iloc[i, j]
        corr_pairs.append({
            'col1': numeric_cols[i],
            'col2': numeric_cols[j],
            'correlation': round(val, 3)
        })

corr_df = pd.DataFrame(corr_pairs).sort_values('correlation', key=abs, ascending=False)
strong_corr = corr_df[abs(corr_df['correlation']) > 0.7]
```

## Outlier Detection

```python
# IQR method
def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = series[(series < lower) | (series > upper)]
    return outliers, lower, upper

# Z-score method (for normally distributed data)
from scipy import stats
def detect_outliers_zscore(series, threshold=3):
    z_scores = np.abs(stats.zscore(series.dropna()))
    return series[z_scores > threshold]
```

## Distribution Testing

```python
from scipy import stats

def describe_distribution(series):
    clean = series.dropna()
    skewness = clean.skew()
    kurtosis = clean.kurtosis()
    
    # Normality test (Shapiro-Wilk, best for n<5000)
    if len(clean) < 5000:
        stat, p_value = stats.shapiro(clean.sample(min(len(clean), 500)))
        is_normal = p_value > 0.05
    else:
        is_normal = abs(skewness) < 0.5  # Rough heuristic
    
    return {
        'skewness': round(skewness, 3),
        'kurtosis': round(kurtosis, 3),
        'is_normal': is_normal,
        'distribution': 'Normal' if is_normal else ('Right-skewed' if skewness > 0 else 'Left-skewed')
    }
```

## Chart 1: Correlation Heatmap

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(max(8, len(numeric_cols)), max(7, len(numeric_cols)-1)))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, ax=ax, square=True,
            cbar_kws={'shrink': 0.8, 'label': 'Correlation Coefficient'})
ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig('chart_correlation.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 2: Distribution Histograms with KDE

```python
import math

cols = df.select_dtypes(include='number').columns[:6]
n = len(cols)
ncols = min(3, n)
nrows = math.ceil(n / ncols)

fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4 * nrows))
axes = axes.flatten() if n > 1 else [axes]

for i, col in enumerate(cols):
    data = df[col].dropna()
    axes[i].hist(data, bins=30, color='#2E86AB', edgecolor='white', alpha=0.7, density=True)
    
    # KDE overlay
    try:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(data)
        x_range = np.linspace(data.min(), data.max(), 200)
        axes[i].plot(x_range, kde(x_range), color='#C73E1D', linewidth=2)
    except:
        pass
    
    axes[i].set_title(col, fontsize=11)
    axes[i].set_xlabel('Value')
    axes[i].set_ylabel('Density')

for j in range(i+1, len(axes)):
    axes[j].set_visible(False)

fig.suptitle('Variable Distributions', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig('chart_distributions.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 3: Box Plot (Outlier Detection)

```python
fig, ax = plt.subplots(figsize=(12, 5))
bp = ax.boxplot([df[col].dropna() for col in numeric_cols[:8]],
                labels=numeric_cols[:8],
                patch_artist=True,
                boxprops=dict(facecolor='#2E86AB', alpha=0.6),
                medianprops=dict(color='#F18F01', linewidth=2.5),
                flierprops=dict(marker='o', color='#C73E1D', alpha=0.5, markersize=4))
ax.set_title('Distribution & Outliers (Box Plot)', fontsize=14, fontweight='bold')
plt.xticks(rotation=30, ha='right')
fig.tight_layout()
fig.savefig('chart_boxplot.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 4: Scatter Matrix (Pair Plot, max 4 variables)

```python
cols_to_plot = numeric_cols[:4]
fig, axes = plt.subplots(len(cols_to_plot), len(cols_to_plot),
                          figsize=(12, 10))

for i, col_i in enumerate(cols_to_plot):
    for j, col_j in enumerate(cols_to_plot):
        ax = axes[i][j]
        if i == j:
            ax.hist(df[col_i].dropna(), bins=20, color='#2E86AB', alpha=0.7)
        else:
            ax.scatter(df[col_j], df[col_i], alpha=0.4, s=10, color='#2E86AB')
        if j == 0:
            ax.set_ylabel(col_i, fontsize=8)
        if i == len(cols_to_plot)-1:
            ax.set_xlabel(col_j, fontsize=8)

fig.suptitle('Scatter Matrix', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig('chart_scatter_matrix.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Narrative Template

**Key statistical findings:**
- 最强正相关：[col1] 与 [col2]，r = [X.XX]（[强/中/弱]相关）
- 最强负相关：[col1] 与 [col2]，r = [X.XX]
- 分布形态：[col] 呈右偏分布，均值 > 中位数，存在高值异常点
- 异常值：[col] 检测到 [N] 个离群值（IQR方法），最大值为均值的 [X] 倍

**Section headings:**
- `## 变量分布` / `## Variable Distributions`
- `## 相关性分析` / `## Correlation Analysis`
- `## 异常值检测` / `## Outlier Detection`
