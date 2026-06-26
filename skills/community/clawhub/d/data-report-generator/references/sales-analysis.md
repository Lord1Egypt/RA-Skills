# Sales & Performance Analysis Reference

## When to Use
Data contains sales, revenue, orders, GMV, conversion rate, or similar business performance metrics.
Keywords: 销售额, 营收, 订单, GMV, 转化率, 客单价, sales, revenue, orders, conversion, KPI, performance.

## Common Column Patterns to Detect

```python
SALES_KEYWORDS = ['sales', 'revenue', 'gmv', 'amount', 'price', '销售', '营收', '金额', '收入']
VOLUME_KEYWORDS = ['orders', 'count', 'qty', 'quantity', 'units', '订单', '数量', '件数']
REGION_KEYWORDS = ['region', 'city', 'area', 'store', 'channel', '地区', '城市', '门店', '渠道']
PRODUCT_KEYWORDS = ['product', 'sku', 'category', 'brand', '产品', '品类', '品牌', 'SKU']
PERSON_KEYWORDS = ['salesperson', 'rep', 'agent', 'staff', '销售员', '业务员', '负责人']
```

## Key KPIs to Calculate

```python
import pandas as pd

# Average order value
df['aov'] = df['revenue'] / df['orders']

# Conversion rate (if traffic/leads data available)
df['conversion_rate'] = df['orders'] / df['leads'] * 100

# Revenue per category %
total_rev = df['revenue'].sum()
df['revenue_share'] = df['revenue'] / total_rev * 100

# Ranking
df['rank'] = df['revenue'].rank(ascending=False).astype(int)

# Top/Bottom N
top10 = df.nlargest(10, 'revenue')
bottom10 = df.nsmallest(10, 'revenue')

# Target achievement (if target column exists)
if 'target' in df.columns:
    df['achievement_rate'] = df['revenue'] / df['target'] * 100
    df['gap_to_target'] = df['target'] - df['revenue']
```

## Chart 1: Top N Performers (Horizontal Bar)

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 7))
top_n = df.nlargest(10, 'revenue').sort_values('revenue')
colors = ['#2E86AB'] * 8 + ['#F18F01'] * 2  # Highlight top 2
bars = ax.barh(top_n['category'], top_n['revenue'], color=colors)
ax.bar_label(bars, fmt='%.0f', padding=5, fontsize=9)
ax.set_title('Top 10 by Revenue', fontsize=14, fontweight='bold')
ax.set_xlabel('Revenue')
fig.tight_layout()
fig.savefig('chart_top10.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 2: Revenue Mix (Treemap or Stacked Bar)

```python
# Stacked bar if time dimension exists; pie/treemap if snapshot
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 6))
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#44BBA4', '#3B1F2B']

# Pie with percentage labels
wedges, texts, autotexts = ax.pie(
    df['revenue_share'],
    labels=df['category'],
    autopct=lambda p: f'{p:.1f}%' if p > 3 else '',
    colors=COLORS[:len(df)],
    startangle=90,
    pctdistance=0.8
)
ax.set_title('Revenue Mix by Category', fontsize=14, fontweight='bold')
fig.savefig('chart_mix.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 3: Target Achievement (if target data exists)

```python
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(df))
width = 0.35
bars1 = ax.bar([i - width/2 for i in x], df['revenue'], width, label='Actual', color='#2E86AB')
bars2 = ax.bar([i + width/2 for i in x], df['target'], width, label='Target',
               color='#CCCCCC', alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels(df['category'], rotation=45, ha='right')
ax.set_title('Actual vs Target', fontsize=14, fontweight='bold')
ax.legend()
fig.tight_layout()
fig.savefig('chart_vs_target.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Chart 4: Funnel (if funnel stages available)

```python
# Detect funnel: impressions → clicks → leads → orders → payments
FUNNEL_STAGES = ['曝光', '点击', '加购', '下单', '支付',
                 'impressions', 'clicks', 'add_to_cart', 'orders', 'payments']

fig, ax = plt.subplots(figsize=(8, 6))
stages = [s for s in FUNNEL_STAGES if s in df.columns]
values = [df[s].sum() for s in stages]
y_pos = range(len(stages))

bars = ax.barh(y_pos, values, color='#2E86AB', alpha=0.85)
ax.set_yticks(y_pos)
ax.set_yticklabels(stages)
ax.bar_label(bars, padding=5)
ax.set_title('Conversion Funnel', fontsize=14, fontweight='bold')
ax.invert_yaxis()
fig.tight_layout()
fig.savefig('chart_funnel.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Narrative Template

**Executive Summary bullets (Chinese):**
- 总销售额：[X]，环比 [增长/下降] [X%]
- 最佳表现：[category/region] 贡献 [X%] 收入
- 客单价：平均 [X]，较上期 [变化]
- 达标情况：[X/total] 个业务线达成目标，整体达标率 [X%]

**Section headings:**
- `## 销售概览` / `## Sales Overview`
- `## 分类表现` / `## Category Performance`
- `## 地区分析` / `## Regional Analysis`
- `## 人员排名` / `## Sales Rep Ranking`
- `## 目标达成` / `## Target Achievement`
