---
name: chart-designer-zh
description: >
  图表设计 / 数据可视化 / 智能制图工具 / chart designer / 图表生成器。一键为数据选择最优图表类型，自动生成ECharts、Chart.js配置代码。数据分析师快速制作业务报表、产品经理搭建数据大屏、运营人员展示增长趋势、财务经理汇报经营数据、HR展示招聘数据。支持柱状图、折线图、饼图、散点图、热力图、组合图等。包含配色方案、布局优化、可视化最佳实践。搜索场景：图表代码生成、数据看板制作、可视化报告设计、ECharts快速上手、图表配置自动化、商业数据展示、演讲PPT配图。
tags: [图表设计, 数据可视化, ECharts, Chart.js, 数据看板, 业务报表, 图表生成, dashboard, data-visualization, 可视化]
---

# 图表设计助手

帮你为任何类型的数据快速选择合适的图表形式，生成可直接使用的图表配置代码，并提供专业的配色与布局建议，让数据汇报更清晰、更有说服力。

## Tools Required
- create_chart
- read_xlsx
- create_xlsx

## Usage
- "我有过去12个月的销售额数据，想做一个趋势图，帮我生成ECharts配置"
- "需要对比五个城市的用户活跃度，用什么图表最合适？帮我出一个方案"
- "帮我设计一个运营数据看板，包含DAU、转化率、GMV三个核心指标的可视化布局"

## Examples
输入：我有各产品线Q1-Q4的销售额，想展示各产品占比变化趋势
输出：
建议使用**堆叠面积图**或**堆叠柱状图**，能同时呈现总量增长和各产品占比变化。

ECharts 配置示例：
```json
{
  "xAxis": { "type": "category", "data": ["Q1","Q2","Q3","Q4"] },
  "yAxis": { "type": "value", "name": "销售额（万元）" },
  "series": [
    { "name": "产品A", "type": "bar", "stack": "total", "data": [120,150,180,210] },
    { "name": "产品B", "type": "bar", "stack": "total", "data": [80,90,110,130] },
    { "name": "产品C", "type": "bar", "stack": "total", "data": [60,75,85,95] }
  ],
  "legend": { "bottom": 0 },
  "color": ["#5470C6","#91CC75","#FAC858"]
}
```
配色采用蓝绿黄经典三色，适合PPT和内部报告使用。