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

## 依赖要求

- Python 3.8+
- plotly >= 5.0
- matplotlib >= 3.5
- seaborn >= 0.11
- pandas >= 1.3
- numpy >= 1.21
- kaleido >= 0.2 (静态图片导出)

## 快速开始

### 基础图表

```python
from scripts.chart_engine import ChartEngine

engine = ChartEngine(backend='plotly')

# 创建折线图
data = {'月份': ['1月', '2月', '3月', '4月'], '销售额': [100, 150, 200, 180]}
fig = engine.line_chart(data, x='月份', y='销售额', title='月度销售趋势')
fig.write_html('sales.html')
```

### 多种图表类型

```python
# 柱状图
fig = engine.bar_chart(data, x='产品', y='销量', color='分类')

# 饼图
fig = engine.pie_chart(data, values='销售额', names='区域')

# 散点图
fig = engine.scatter_chart(data, x='价格', y='销量', size='库存', color='类别')

# 热力图
fig = engine.heatmap(correlation_matrix, title='相关性矩阵')
```

### 交互式仪表盘

```python
from scripts.dashboard import Dashboard

dash = Dashboard(title='业务监控大屏', theme='dark')
dash.add_chart('sales', engine.line_chart(sales_data, x='日期', y='金额'))
dash.add_chart('users', engine.bar_chart(user_data, x='渠道', y='新增'))
dash.add_kpi('总销售额', 1250000, change=+12.5)
dash.save('dashboard.html')
```

### 数据报表

```python
from scripts.report_generator import ReportGenerator

report = ReportGenerator()
report.add_section('销售分析', charts=[fig1, fig2])
report.add_table('明细数据', dataframe=df)
report.export('report.pdf')
```

## API 文档

### ChartEngine

```python
ChartEngine(backend='plotly', theme='light')
```

| 参数 | 类型 | 说明 |
|------|------|------|
| backend | str | 'plotly', 'matplotlib', 'seaborn' |
| theme | str | 'light', 'dark', 'corporate' |

### Dashboard

```python
Dashboard(title='仪表盘', layout='grid', theme='light')
```

| 方法 | 说明 |
|------|------|
| add_chart(id, fig) | 添加图表 |
| add_kpi(title, value, change) | 添加KPI指标 |
| add_table(title, df) | 添加数据表 |
| save(path) | 保存HTML |

## 示例

见 `examples/basic_usage.py`

## 测试

```bash
python -m pytest tests/ -v
```

## 许可证

MIT License
