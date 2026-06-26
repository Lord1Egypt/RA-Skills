# General Analysis Reference

## When to Use
Data type is unknown, mixed, or doesn't fit a specific template. Use as fallback when other references don't match.

## Universal Data Profiling

```python
import pandas as pd
import numpy as np

def full_profile(df):
    profile = {}
    
    # Basic shape
    profile['rows'] = len(df)
    profile['columns'] = len(df.columns)
    
    # Column classification
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Try to detect date columns in string format
    for col in categorical_cols:
        try:
            pd.to_datetime(df[col], infer_datetime_format=True)
            datetime_cols.append(col)
            categorical_cols.remove(col)
        except:
            pass
    
    profile['numeric_cols'] = numeric_cols
    profile['categorical_cols'] = categorical_cols
    profile['datetime_cols'] = datetime_cols
    
    # Missing values
    missing = df.isnull().sum()
    profile['missing'] = missing[missing > 0].to_dict()
    profile['missing_pct'] = (missing / len(df) * 100)[missing > 0].round(1).to_dict()
    
    # Duplicates
    profile['duplicate_rows'] = df.duplicated().sum()
    
    # Numeric summary
    if numeric_cols:
        profile['numeric_stats'] = df[numeric_cols].describe().round(2).to_dict()
    
    # Categorical summary
    for col in categorical_cols[:5]:  # Limit to first 5
        profile[f'top_{col}'] = df[col].value_counts().head(5).to_dict()
    
    return profile
```

## Decision Tree: What Charts to Generate

```
Has datetime column?
├── YES → Use time-series.md as primary
└── NO  →
    Has categorical + numeric?
    ├── YES →
    │   Categories < 10?
    │   ├── YES → Bar chart (category comparison) + Pie chart (composition)
    │   └── NO  → Horizontal bar (top 15) only
    └── NO  →
        Multiple numeric columns?
        ├── YES → Correlation heatmap + Distribution histograms
        └── NO  → Single column → Histogram + Box plot
```

## Universal Chart Set (for unknown data)

### Chart 1: Numeric Distributions
```python
import matplotlib.pyplot as plt
import math

numeric_cols = df.select_dtypes(include='number').columns[:6]  # Max 6
n = len(numeric_cols)
cols_per_row = 3
rows = math.ceil(n / cols_per_row)

fig, axes = plt.subplots(rows, cols_per_row, figsize=(14, 4 * rows))
axes = axes.flatten() if n > 1 else [axes]

for i, col in enumerate(numeric_cols):
    axes[i].hist(df[col].dropna(), bins=25, color='#2E86AB', edgecolor='white', alpha=0.8)
    axes[i].set_title(col, fontsize=11)
    axes[i].set_xlabel('Value')
    axes[i].set_ylabel('Frequency')

# Hide unused subplots
for j in range(i+1, len(axes)):
    axes[j].set_visible(False)

fig.suptitle('Variable Distributions', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig('chart_distributions.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

### Chart 2: Categorical Frequency
```python
for col in df.select_dtypes(include='object').columns[:3]:
    top = df[col].value_counts().head(12)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(top.index[::-1], top.values[::-1], color='#2E86AB')
    ax.bar_label(bars, padding=3)
    ax.set_title(f'Top Values: {col}', fontsize=13, fontweight='bold')
    fig.tight_layout()
    fig.savefig(f'chart_freq_{col}.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
```

### Chart 3: Correlation Heatmap (if ≥3 numeric cols)
```python
import seaborn as sns

numeric_cols = df.select_dtypes(include='number').columns
if len(numeric_cols) >= 3:
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))  # Show lower triangle only
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, ax=ax, square=True, cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
    fig.tight_layout()
    fig.savefig('chart_correlation.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
```

### Chart 4: Box Plot (outlier visibility)
```python
numeric_cols = df.select_dtypes(include='number').columns[:5]
fig, ax = plt.subplots(figsize=(10, 5))
df[numeric_cols].boxplot(ax=ax, patch_artist=True,
    boxprops=dict(facecolor='#2E86AB', alpha=0.6),
    medianprops=dict(color='#F18F01', linewidth=2))
ax.set_title('Variable Distribution & Outliers', fontsize=14, fontweight='bold')
plt.xticks(rotation=30)
fig.tight_layout()
fig.savefig('chart_boxplot.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Generic Narrative Template

```
## 数据概览 / Data Overview

本报告基于 [数据文件名] 数据集生成，包含 [X] 行记录、[X] 个字段。
数据时间范围：[start] 至 [end]（如适用）。

**数据质量：**
- 缺失值：[列名] 存在 [X%] 缺失（共 [N] 条）
- 重复记录：[X] 条
- 数据建议：[如需清洗，说明问题]

## 核心发现 / Key Findings

1. [Finding 1 — most important metric or trend]
2. [Finding 2 — notable pattern or outlier]
3. [Finding 3 — actionable insight]

## 建议 / Recommendations

- [Recommendation 1]
- [Recommendation 2]
```

## Data Quality Flags to Report

```python
issues = []

# Missing values
for col, pct in profile['missing_pct'].items():
    if pct > 20:
        issues.append(f"⚠️ {col}: {pct}% missing — consider imputation or exclusion")
    elif pct > 5:
        issues.append(f"ℹ️ {col}: {pct}% missing — minor gaps")

# Duplicates
if profile['duplicate_rows'] > 0:
    issues.append(f"⚠️ {profile['duplicate_rows']} duplicate rows detected")

# Constant columns (no variance)
for col in df.select_dtypes(include='number').columns:
    if df[col].std() == 0:
        issues.append(f"ℹ️ {col}: constant value — no analytical value")

# Report issues in "Data Overview" section
```
