# Data Visualization - 数据可视化工具箱

<p align="center">
  <img src="https://img.shields.io/pypi/v/chart-generator-toolkit?style=flat-square" alt="PyPI">
  <img src="https://img.shields.io/pypi/l/chart-generator-toolkit?style=flat-square" alt="License">
</p>

## 📖 简介

**Data Visualization** 是简洁强大的数据可视化工具,帮助快速生成各类统计图表。

### 🎯 适用场景

- 📊 数据分析报告
- 📈 业务Dashboard
- 📉 趋势分析
- 🥧 占比分析
- 🔍 相关性分析

## 🚀 功能特性

| 功能 | 说明 |
|------|------|
| 📈 **折线图** | 趋势变化 |
| 📊 **柱状图** | 类别对比 |
| 🥧 **饼图** | 占比分布 |
| ⚪ **散点图** | 相关性 |
| 🎨 **样式定制** | 颜色/标签/图例 |
| 💾 **多格式导出** | PNG/SVG/HTML |

## 📦 安装

```bash
# 基础
pip install matplotlib pandas

# 交互式图表 (可选)
pip install plotly
```

## 🎬 快速开始

```python
from chart_generator import ChartGenerator, quick_chart

# 准备数据
data = {
    '月份': ['1月', '2月', '3月', '4月'],
    '销售额': [10000, 15000, 12000, 18000],
    '利润': [2000, 3500, 2800, 4200]
}

# 方式1: 快速生成
chart = quick_chart(data, 'line', '月份', '销售额')
chart.save('chart.png')

# 方式2: 完整API
chart = ChartGenerator()
chart.line_chart(data, '月份', ['销售额', '利润'], title='月度业绩')
chart.save('sales.png')
```

## 📚 详细示例

### 折线图 - 趋势分析

```python
from chart_generator import ChartGenerator

data = {
    'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
    'sales': [1000, 1500, 1300, 1800],
    'profit': [200, 350, 250, 400]
}

chart = ChartGenerator()
chart.line_chart(
    data, 
    x='date', 
    y=['sales', 'profit'],  # 多条线
    title='2026年销售趋势',
    xlabel='月份',
    ylabel='金额(元)'
)
chart.save('trend.png')
```

### 柱状图 - 类别对比

```python
data = {
    'product': ['产品A', '产品B', '产品C', '产品D'],
    'sales': [1500, 2300, 1800, 2100],
    'target': [2000, 2000, 2000, 2000]
}

chart = ChartGenerator()
chart.bar_chart(
    data,
    x='product',
    y=['sales', 'target'],  # 对比
    title='产品销售 vs 目标'
)
chart.save('bar.png')
```

### 饼图 - 占比分析

```python
data = {
    'category': ['手机', '电脑', '平板', '配件'],
    'revenue': [35, 30, 20, 15]  # 百分比
}

chart = ChartGenerator()
chart.pie_chart(
    data,
    names='category',
    values='revenue',
    title='收入占比'
)
chart.save('pie.png')
```

### 散点图 - 相关性分析

```python
data = {
    'advertising': [100, 200, 300, 400, 500],
    'sales': [1200, 1800, 2400, 2900, 3800],
    'profit': [300, 500, 700, 800, 1100]
}

chart = ChartGenerator()
chart.scatter_chart(
    data,
    x='advertising',
    y='sales',
    size='profit',  # 气泡大小
    title='广告投入 vs 销售额'
)
chart.save('scatter.png')
```

### Plotly 交互式图表

```python
import pandas as pd
from chart_generator import PlotlyChart

df = pd.DataFrame(data)

# 交互式折线图
fig = PlotlyChart.line(df, 'date', 'sales', title='交互式折线图')
html = PlotlyChart.to_html(fig)

# 保存为HTML
PlotlyChart.save(fig, 'interactive.html')

# 保存为PNG
PlotlyChart.save(fig, 'chart.png', format='png')
```

## 📋 API 参考

### ChartGenerator (静态图表)

```python
chart = ChartGenerator()

# 图表类型
chart.line_chart(data, x, y)        # 折线图
chart.bar_chart(data, x, y)         # 柱状图
chart.pie_chart(data, names, values) # 饼图
chart.scatter_chart(data, x, y)     # 散点图

# 保存
chart.save('output.png', dpi=300)
chart.to_base64()  # Base64编码
```

### PlotlyChart (交互式)

```python
# 创建
fig = PlotlyChart.line(df, x, y)
fig = PlotlyChart.bar(df, x, y)
fig = PlotlyChart.scatter(df, x, y, color=category)
fig = PlotlyChart.pie(df, names, values)

# 导出
html = PlotlyChart.to_html(fig)
PlotlyChart.save(fig, 'output.html')
PlotlyChart.save(fig, 'output.png')
```

## 🎨 样式选项

```python
chart.line_chart(
    data, 'x', 'y',
    title='标题',
    xlabel='X轴标签',
    ylabel='Y轴标签',
    figsize=(12, 6),  # 图形大小
    color='#FF5733'   # 颜色
)
```

## 📊 图表选择指南

| 数据类型 | 推荐图表 |
|----------|----------|
| 随时间变化 | 折线图 |
| 类别比较 | 柱状图 |
| 部分占比 | 饼图 |
| 两变量关系 | 散点图 |
| 多维数据 | 气泡图 |

## 🔧 常见问题

### 中文显示乱码?
```python
# 设置中文字体
from chart_generator import setup_chinese_font
setup_chinese_font()
```

### 如何调整图形大小?
```python
chart.line_chart(data, x, y, figsize=(14, 8))
```

### 如何只显示部分数据?
```python
# 筛选数据
data = {k: v[:10] for k, v in data.items()}
```

## 📄 许可证

MIT License