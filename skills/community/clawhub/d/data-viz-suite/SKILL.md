---
name: data-viz-suite
description: 数据可视化套件 - 企业级BI工具，支持图表生成、数据报表、交互式仪表盘。支持 Plotly/Matplotlib/Seaborn 多种引擎。
homepage: https://github.com/openclaw/skills/tree/main/data-viz-suite
category: data-processing
tags:
  - visualization
  - plotly
  - matplotlib
  - seaborn
  - dashboard
  - bi
  - charts
  - analytics
---

# Data Viz Suite - 数据可视化套件

专业的数据可视化解决方案，支持静态图表、交互式仪表盘和企业级报表。

## 功能特性

- 📊 **多种图表类型**：折线图、柱状图、饼图、散点图、热力图、箱线图
- 🎨 **三大可视化引擎**：Plotly(交互式)、Matplotlib(静态)、Seaborn(统计)
- 📈 **交互式仪表盘**：支持拖拽布局、实时数据更新
- 📄 **报表导出**：支持 PDF、PNG、HTML、Excel 格式
- 🔗 **数据源支持**：CSV、Excel、JSON、SQL 数据库
- 🌐 **Web 展示**：生成交互式 HTML 报告

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 基础图表

```python
from scripts.chart_engine import ChartEngine

engine = ChartEngine(backend='plotly')

# 创建折线图
data = {'月份': ['1月', '2月', '3月'], '销售额': [100, 150, 200]}
fig = engine.line_chart(data, x='月份', y='销售额', title='月度销售趋势')
fig.write_html('sales.html')
```

### 2. 交互式仪表盘

```python
from scripts.dashboard import Dashboard

dash = Dashboard(title='业务监控大屏')
dash.add_chart('sales', engine.line_chart(data, x='月份', y='销售额'))
dash.add_chart('users', engine.bar_chart(users, x='日期', y='新增用户'))
dash.save('dashboard.html')
```

### 3. 数据报表

```python
from scripts.report_generator import ReportGenerator

report = ReportGenerator()
report.add_section('销售分析', charts=[fig1, fig2])
report.add_table('明细数据', dataframe=df)
report.export('report.pdf')
```

## 目录结构

```
data-viz-suite/
├── SKILL.md                  # 本文件
├── README.md                 # 详细文档
├── requirements.txt          # 依赖
├── examples/                 # 示例
│   └── basic_usage.py
├── scripts/                  # 核心脚本
│   ├── chart_engine.py
│   ├── dashboard.py
│   ├── report_generator.py
│   └── data_connector.py
└── tests/                    # 测试
    ├── test_chart_engine.py
    ├── test_dashboard.py
    └── test_report_generator.py
```

## 配置说明

### 主题配置

```python
from scripts.chart_engine import Theme

engine = ChartEngine(theme=Theme.DARK)  # DARK, LIGHT, CORPORATE
```

### 数据源配置

```python
# CSV/Excel
conn = DataConnector()
df = conn.load_csv('data.csv')
df = conn.load_excel('data.xlsx', sheet='Sheet1')

# SQL
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'pass',
    'database': 'analytics'
}
df = conn.load_sql('SELECT * FROM sales', config)
```

## 许可证

MIT License
