# Chart.js 图表配置参考指南

## 支持的图表类型及配置示例

### 1. 环形图 / 饼图（doughnut / pie）

适用场景：占比分析、构成分析，分类数 ≤ 6 时使用 doughnut，> 6 时考虑 bar。

```json
{
  "type": "doughnut",
  "title": "品类营收占比",
  "labels": ["Food", "Electronics", "Sports", "Clothing", "Furniture"],
  "datasets": [
    {"data": [456833, 351665, 349967, 310014, 287427]}
  ]
}
```

### 2. 折线图（line）

适用场景：时间序列、趋势分析。

```json
{
  "type": "line",
  "title": "月度营收趋势",
  "labels": ["1月","2月","3月","4月","5月","6月"],
  "datasets": [
    {"label": "营收", "data": [158495, 185560, 98369, 158995, 230752, 144102]}
  ]
}
```

多条线（多 dataset）：
```json
{
  "type": "line",
  "title": "各渠道月度对比",
  "labels": ["1月","2月","3月"],
  "datasets": [
    {"label": "Online",      "data": [50000, 60000, 45000]},
    {"label": "Store",       "data": [30000, 35000, 28000]},
    {"label": "Distributor", "data": [70000, 80000, 65000]}
  ]
}
```

### 3. 垂直柱状图（bar）

适用场景：分类对比，标签较短，分类 ≤ 8。

```json
{
  "type": "bar",
  "title": "区域营收对比",
  "labels": ["East", "West", "North", "South", "Central"],
  "datasets": [
    {"label": "营收", "data": [419036, 428635, 331090, 357535, 219610]}
  ]
}
```

### 4. 水平柱状图（horizontalBar）

适用场景：排名展示、标签较长时使用。

```json
{
  "type": "horizontalBar",
  "title": "品类均价排名",
  "labels": ["Electronics", "Clothing", "Sports", "Furniture", "Food"],
  "datasets": [
    {"label": "均价(¥)", "data": [860, 833, 813, 811, 775]}
  ]
}
```

### 5. 分组柱状图

同一 chart type=bar，提供多个 dataset 即可自动分组：

```json
{
  "type": "bar",
  "title": "Q1-Q2 各品类对比",
  "labels": ["Food", "Electronics", "Sports"],
  "datasets": [
    {"label": "Q1", "data": [120000, 95000, 88000]},
    {"label": "Q2", "data": [145000, 110000, 102000]}
  ]
}
```

---

## KPI 卡片配置

```json
[
  {"label": "总营收",     "value": "¥1,755,905", "sub": "全年累计",      "color": "green"},
  {"label": "订单数",     "value": "200",         "sub": "5品类·25产品",  "color": "blue"},
  {"label": "平均单价",   "value": "¥815",        "sub": "中位数¥868",    "color": "yellow"},
  {"label": "平均件数/单","value": "10.7",        "sub": "最高20件",      "color": "purple"}
]
```

color 可选值：`blue` | `green` | `yellow` | `purple` | `red`

---

## 完整调用示例（与 chat2duckdb 配合）

```python
import subprocess, json, sys

# 1. 从 DuckDB 查询结果构建数据
kpis = [
    {"label": "总营收", "value": "¥1,755,905", "sub": "200单", "color": "green"},
]
charts = [
    {
        "type": "doughnut",
        "title": "品类营收占比",
        "labels": ["Food","Electronics","Sports","Clothing","Furniture"],
        "datasets": [{"data": [456833,351665,349967,310014,287427]}]
    },
    {
        "type": "line",
        "title": "月度营收趋势",
        "labels": ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
        "datasets": [{"label":"营收","data":[158495,185560,98369,158995,230752,144102,71695,209684,72276,119508,160265,146204]}]
    }
]
data_json = json.dumps({"kpis": kpis, "charts": charts}, ensure_ascii=False)

# 2. 调用生成脚本
subprocess.run([
    sys.executable,
    "C:/Users/wangd/.workbuddy/skills/chartjs-reporter/scripts/generate_report.py",
    "--title", "2025年销售分析报告",
    "--subtitle", "数据来源：sales_data.csv · DuckDB 分析",
    "--data", data_json,
    "--output", "output_report.html"
])
```

---

## 布局自动规则

| 图表数量 | 网格列数 |
|---------|---------|
| 1       | 全宽 1列 |
| 2       | 2列     |
| 3       | 3列     |
| 4       | 2×2     |
| 6       | 3×2     |
| 其他     | 2列     |
