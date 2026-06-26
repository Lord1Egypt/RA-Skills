# Time Series Analysis Reference

## When to Use
Data has a date/datetime column + one or more numeric value columns.
Keywords: 日期, 时间, 月份, 日报, 周报, 月报, date, time, month, daily, weekly, trend.

## Step 1: Parse Dates

```python
import pandas as pd

# Try auto-parsing first
df['date'] = pd.to_datetime(df['date_col'], infer_datetime_format=True, errors='coerce')

# If auto-parse fails, try common Chinese formats
date_formats = ['%Y年%m月%d日', '%Y/%m/%d', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
for fmt in date_formats:
    try:
        df['date'] = pd.to_datetime(df['date_col'], format=fmt)
        break
    except:
        continue

# Sort by date
df = df.sort_values('date').reset_index(drop=True)
```

## Step 2: Resample to Common Periods

```python
df_ts = df.set_index('date')

# Daily → Weekly
weekly = df_ts.resample('W').sum()  # or .mean() for averages

# Daily → Monthly
monthly = df_ts.resample('M').sum()
```

## Step 3: Key Metrics to Calculate

```python
# Period-over-period growth
monthly['mom_growth'] = monthly['value'].pct_change() * 100  # Month-over-Month %
monthly['yoy_growth'] = monthly['value'].pct_change(12) * 100  # Year-over-Year %

# Rolling average (smooth noise)
df['7day_avg'] = df['value'].rolling(7).mean()
df['30day_avg'] = df['value'].rolling(30).mean()

# Cumulative
df['cumulative'] = df['value'].cumsum()

# Best/Worst period
best_period = monthly['value'].idxmax()
worst_period = monthly['value'].idxmin()
```

## Step 4: Charts for Time Series

### Chart 1: Overall Trend (Line)
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['date'], df['value'], color='#2E86AB', linewidth=2, alpha=0.8, label='Actual')
ax.plot(df['date'], df['7day_avg'], color='#F18F01', linewidth=2, linestyle='--', label='7-day avg')
ax.fill_between(df['date'], df['value'], alpha=0.1, color='#2E86AB')
ax.set_title('Value Trend Over Time', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig('chart_trend.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

### Chart 2: Monthly Bar Chart (Period Comparison)
```python
fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(monthly.index.strftime('%Y-%m'), monthly['value'], color='#2E86AB', width=0.6)
ax.bar_label(bars, fmt='%.0f', padding=3, fontsize=9)
ax.set_title('Monthly Performance', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig('chart_monthly.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

### Chart 3: Month-over-Month Growth Rate
```python
fig, ax = plt.subplots(figsize=(12, 4))
colors = ['#C73E1D' if x < 0 else '#44BBA4' for x in monthly['mom_growth'].dropna()]
ax.bar(monthly.index.dropna().strftime('%Y-%m'), monthly['mom_growth'].dropna(),
       color=colors, width=0.6)
ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_title('Month-over-Month Growth Rate (%)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig('chart_growth.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Step 5: Narrative Template

**Executive Summary bullets:**
- 总体趋势：[上升/下降/平稳]，整体 [增长/下降] X%
- 最高值：[period] 达到 [value]，最低值：[period] 为 [value]
- 环比增速：最近一期 [+X% / -X%]
- 关键转折点：[date] 出现明显 [上升/下降] 拐点

**Section heading:** `## 趋势分析` or `## Trend Analysis`

## Anomaly Detection (optional)

```python
# Flag values > 2 std devs from mean
mean = df['value'].mean()
std = df['value'].std()
df['is_anomaly'] = abs(df['value'] - mean) > 2 * std
anomalies = df[df['is_anomaly']]
if len(anomalies) > 0:
    # Note in report: "X anomalous data points detected on dates: ..."
    pass
```
