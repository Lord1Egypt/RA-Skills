# Excel2Insights 功能演示

> 以下演示基于 `assets/sample_sales_data.csv`（26行销售数据样本）。

## 一、快速扫描

```bash
python3 scripts/excel-reader.py --file assets/sample_sales_data.csv
```

预期输出：

```json
{
  "file": "assets/sample_sales_data.csv",
  "rows": 26,
  "columns": 7,
  "column_names": ["date", "product", "category", "region", "revenue", "quantity", "customer_segment"],
  "column_types": {
    "numeric": ["revenue", "quantity"],
    "categorical": ["product", "category", "region", "customer_segment"],
    "datetime": ["date"]
  },
  "quality_flags": [],
  "preview": {
    "head": [
      {"date": "2024-01-05", "product": "Widget A", "category": "Electronics", "region": "North", "revenue": 12500.0, "quantity": 45, "customer_segment": "Enterprise"},
      {"date": "2024-01-12", "product": "Widget B", "category": "Electronics", "region": "South", "revenue": 8900.0, "quantity": 32, "customer_segment": "SMB"},
      {"date": "2024-01-19", "product": "Gadget X", "category": "Accessories", "region": "East", "revenue": 3200.0, "quantity": 18, "customer_segment": "Enterprise"}
    ]
  }
}
```

## 二、统计分析

```bash
python3 scripts/data-analyzer.py --file assets/sample_sales_data.csv --correlation --outliers
```

预期输出节选：

```
=== Dataset Summary ===
  26 rows x 7 columns
  Numeric: 2 | Categorical: 4 | Datetime: 1
  Missing cells: 0 | Duplicate rows: 0

=== Numeric Columns ===

Revenue (26 non-null):
  Mean:   8,315   Median: 5,700
  Min:    2,100   Max:    17,200
  Std:    5,174   Skewness: 0.31
  Q1:     3,025   Q3:     12,875
  Outliers: 0

Quantity (26 non-null):
  Mean:   31.5    Median: 29.0
  Min:    11      Max:    62
  Std:    16.3
  Outliers: 0

=== Key Findings ===
  - Top product: Widget A (7 occurrences)
  - Top region: North (7 occurrences)
  - Correlation (revenue vs quantity): 0.997 (very strong)
  - Revenue range: $2,100 - $17,200
```

## 三、图表生成

```bash
python3 scripts/chart-generator.py --file assets/sample_sales_data.csv --charts histogram,bar,boxplot,heatmap,line
```

预期输出：

```
Charts generated: 5
  output/charts/revenue_histogram.png
  output/charts/quantity_histogram.png
  -- 两张直方图展示 revenue 和 quantity 的分布形状

  output/charts/product_bar.png
  output/charts/region_bar.png
  -- 柱状图展示 product 和 region 的频率分布

  output/charts/boxplot_all.png
  -- 箱线图显示数据分布和离群点

  output/charts/correlation_heatmap.png
  -- 热力图显示 revenue 与 quantity 高度相关 (0.997)

  output/charts/trend_line.png
  -- 折线图按月份展示 revenue 趋势
```

## 四、完整报告

```bash
python3 scripts/auto-pipeline.py --file assets/sample_sales_data.csv --charts histogram,bar,boxplot,heatmap,line
```

一键运行后，`output/` 目录下会产出：

```
output/
├── analysis.json         # 完整统计分析结果
├── charts/
│   ├── revenue_histogram.png
│   ├── quantity_histogram.png
│   ├── product_bar.png
│   ├── region_bar.png
│   ├── boxplot_all.png
│   ├── correlation_heatmap.png
│   └── trend_line.png
└── report.html           # 结构化洞察报告（含嵌入图表）
```

## 五、Agent 使用示例

在 Codex 中安装该 Skill 后，用户可以这样说：

```
"帮我分析这份销售数据"
"这个 CSV 文件有哪些列？看个大概"
"对数据做个完整的统计分析并出报告"
"生成 revenue 的直方图和 region 的柱状图"
"看看有没有异常数据"
```

Agent 会根据 SKILL.md 中的指令自动编排管线，调用对应脚本完成分析。

---

## 使用场景

| 场景 | 推荐命令 |
|------|---------|
| 快速了解新数据集 | `python3 scripts/excel-reader.py --file data.csv` |
| 深入分析 | `python3 scripts/data-analyzer.py --file data.csv --correlation --outliers` |
| 制作报告图表 | `python3 scripts/chart-generator.py --file data.csv --charts histogram,bar,heatmap` |
| 一键搞定 | `python3 scripts/auto-pipeline.py --file data.csv` |
