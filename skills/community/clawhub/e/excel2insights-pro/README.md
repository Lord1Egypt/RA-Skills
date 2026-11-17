# Excel2Insights 📊

Excel / CSV / TSV 数据分析与可视化工具。自动加载结构化数据，执行统计分析，生成高质量图表，输出结构化洞察报告。

## 快速使用

```bash
# 一键全流程（扫描 + 分析 + 图表 + 报告）
python3 scripts/auto-pipeline.py --file data.csv

# 只看概览
python3 scripts/excel-reader.py --file data.xlsx

# 完整分析
python3 scripts/data-analyzer.py --file data.csv --correlation --outliers

# 指定图表类型
python3 scripts/chart-generator.py --file data.csv --charts histogram,bar,heatmap

# 生成报告（配合已生成的图表）
python3 scripts/report-generator.py --file data.csv --charts output/charts
```

## 功能

- **数据加载** — 支持 CSV, XLSX, XLS, TSV 格式
- **统计概要** — 数值列的均值/中位数/标准差/分位数，类别列的频次分布
- **数据质量** — 缺失值、重复行、异常值检测
- **可视化** — 直方图、箱线图、柱状图、折线图、饼图、热力图、散点图
- **结构化报告** — Markdown/HTML 报告，含摘要、逐列分析、图表、洞察
- **Auto Pipeline** — 一条命令完成全流程

## 脚本列表

| 脚本 | 功能 |
|------|------|
| `excel-reader.py` | 加载文件，输出元数据和预览 |
| `data-analyzer.py` | 统计分析，含数据质量检查 |
| `chart-generator.py` | 生成多种可视化图表 |
| `report-generator.py` | 生成结构化洞察报告 |
| `auto-pipeline.py` | 自动完成全流程 |

## 依赖

Python 3.9+, pandas, numpy, matplotlib, seaborn, openpyxl

## 许可

MIT-0 — 无需署名
