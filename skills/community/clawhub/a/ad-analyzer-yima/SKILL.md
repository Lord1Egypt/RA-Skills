---
name: ad-analyzer-yima
description: 广告投放数据分析。当用户上传 Excel/CSV 广告报表，或说"帮我分析投放数据/看看这个报表/哪个计划效果差/数据有没有问题"时触发。自动识别所有表头列，无需预设字段名，汇总全部指标，检测异常，生成可视化图表，输出分析报告和优化建议。支持巨量引擎、腾讯广告、Meta Ads、Google Ads、快手等平台导出格式。
homepage: https://clawhub.ai/ming0429/ad-analyzer-yima
version: 1.1.0
author: guojiaming
tags: [advertising, analytics, excel, csv, 广告分析, 投放优化, 数据可视化, chart]
metadata:
  clawdbot:
    emoji: 📊
    requires:
      bins: [python3]
      pip: [pandas, openpyxl, xlrd, matplotlib, seaborn]
      env: []
---

# 广告数据分析 Skill

分析用户上传的广告报表，自动识别所有列，汇总指标，检测异常，生成图表，输出优化建议。

## Setup

无需任何配置，开箱即用。支持 `.xlsx` / `.xls` / `.csv`，兼容 UTF-8 / GBK 编码。

## Usage

用户上传文件后，将完整分析脚本保存为文件再执行。**不要用 `-c` 内联方式运行**，内联模式不支持多行缩进代码。

正确执行方式：
```bash
# 第一步：把 scripts/analyze.py 脚本保存到本地
# 第二步：执行
python3 analyze.py --file /path/to/report.xlsx --out ./charts
```

## 分析脚本说明

脚本位于 `scripts/analyze.py`，执行后自动完成以下步骤：

1. **读取文件** — 自动识别 xlsx/xls/csv，自动尝试 utf-8/gbk 编码
2. **识别列类型** — 自动区分日期列、维度列（文字）、指标列（数值），不预设列名
3. **汇总指标** — 所有数值列的合计、均值、最大值、最小值
4. **分组分析** — 按每个维度列分组汇总，自动排序
5. **异常检测** — 均值 ±2 倍标准差自动标记异常行
6. **生成图表** — 输出 5 张 PNG 图表
7. **输出建议** — 基于数据给出具体优化方向

## 图表输出

| 文件名 | 内容 |
|--------|------|
| chart_1_totals.png | 各指标总量柱状图 |
| chart_2_dim_compare.png | 主维度横向对比图 |
| chart_3_trend.png | 指标趋势折线图（有日期列时） |
| chart_4_correlation.png | 指标相关性热力图（指标≥3时） |
| chart_5_pie.png | 主维度占比饼图 |

## Notes

- 必须保存为 `.py` 文件执行，不支持 `python3 -c` 内联模式
- 完全动态识别列名，表头是什么分析什么，一列不漏
- 数据不外传，完全本地处理
- 编码自动识别，兼容国内广告平台导出文件

## Examples

分析巨量引擎报表：
```bash
python3 analyze.py --file ~/Downloads/report.xlsx --out ~/Desktop/charts
```

分析腾讯广告 CSV：
```bash
python3 analyze.py --file ~/Downloads/tencent.csv --out ~/Desktop/charts
```
