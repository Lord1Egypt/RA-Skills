# Segmentation Analysis Reference

## When to Use
Data has categorical groupings — region, product category, team, channel, customer segment, etc.
Keywords: 分类, 分组, 对比, 排名, 渠道, 地区, 品类, segment, category, group, breakdown, ranking, channel.

## Core Operations

```python
import pandas as pd

# Group and aggregate
summary = df.groupby('category').agg(
    total=('value', 'sum'),
    average=('value', 'mean'),
    count=('value', 'count'),
    max=('value', 'max'),
    min=('value', 'min')
).reset_index()

# Share of total
summary['share_pct'] = summary['total'] / summary['total'].sum() * 100

# Rank
summary['rank'] = summary['total'].rank(ascending=False).astype(int)
summary = summary.sort_values('total', ascending=False)

# Cumulative (Pareto)
summary['cumulative_pct'] = summary['share_pct'].cumsum()
pareto_80 = summary[summary['cumulative_pct'] <= 80]  # 80% of value
```

## Chart 1: Ranked Bar Chart

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 7))
top15 = summary.head(15).sort_values('total')
colors = ['#F18F01' if i >= len(top15)-3 else '#2E86AB' for i in range(len(top15))]
bars = ax.barh(top15['category'], top15['total'], color=colors)
ax.bar_label(bars, fmt='%.0f', padding=5, fontsize=9)
ax.set_title('Ranking by Total Value', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Value')
fig.tight_layout()
fig.savefig('chart_ranking.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 2: Pareto Chart (80/20 analysis)

```python
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

# Bar: individual values
ax1.bar(summary['category'], summary['total'], color='#2E86AB', alpha=0.8, label='Value')
ax1.set_ylabel('Value', color='#2E86AB')
ax1.tick_params(axis='x', rotation=45)

# Line: cumulative %
ax2.plot(summary['category'], summary['cumulative_pct'], color='#C73E1D',
         marker='o', linewidth=2, label='Cumulative %')
ax2.axhline(y=80, color='#F18F01', linestyle='--', linewidth=1.5, label='80% line')
ax2.set_ylabel('Cumulative %', color='#C73E1D')
ax2.set_ylim(0, 110)

ax1.set_title("Pareto Analysis (80/20)", fontsize=14, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')

fig.tight_layout()
fig.savefig('chart_pareto.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 3: Multi-Category Comparison (Grouped Bar)

```python
# Use when comparing multiple metrics across categories
fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(summary.head(8)))
width = 0.35

ax.bar([i - width/2 for i in x], summary.head(8)['metric1'],
       width, label='Metric 1', color='#2E86AB')
ax.bar([i + width/2 for i in x], summary.head(8)['metric2'],
       width, label='Metric 2', color='#F18F01')

ax.set_xticks(x)
ax.set_xticklabels(summary.head(8)['category'], rotation=30, ha='right')
ax.set_title('Comparison by Category', fontsize=14, fontweight='bold')
ax.legend()
fig.tight_layout()
fig.savefig('chart_grouped.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 4: Scatter (if two numeric dimensions per segment)

```python
# E.g., Revenue vs Volume per category — find outliers
fig, ax = plt.subplots(figsize=(10, 7))
sc = ax.scatter(df['revenue'], df['volume'], s=df['count']*5,
                c=range(len(df)), cmap='viridis', alpha=0.7)

for _, row in df.iterrows():
    ax.annotate(row['category'], (row['revenue'], row['volume']),
                fontsize=8, ha='center', va='bottom')

ax.set_xlabel('Revenue')
ax.set_ylabel('Volume')
ax.set_title('Revenue vs Volume by Category', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig('chart_scatter.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Narrative Template

**Key insights for segmentation:**
- 头部集中度：前 [X] 个类别贡献了总量的 [X%]（帕累托效应）
- 最优类别：[category] 表现最佳，占比 [X%]
- 末尾分析：后 [X] 个类别合计仅占 [X%]，建议评估资源分配
- 类别差异：最高 vs 最低相差 [X] 倍

**Section headings:**
- `## 分类排名` / `## Category Ranking`
- `## 帕累托分析` / `## Pareto Analysis`
- `## 多维对比` / `## Multi-Metric Comparison`
