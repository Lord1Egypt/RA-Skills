# Chart Toolkit
## 完整图表生成工具箱 | Python数据可视化解决方案

<p align="center">
  <a href="https://pypi.org/project/chart-toolkit/">
    <img src="https://img.shields.io/pypi/v/chart-toolkit" alt="PyPI">
  </a>
  <img src="https://img.shields.io/github/stars/XiLi/chart-toolkit" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/chart-toolkit" alt="License">
  <img src="https://img.shields.io/pypi/pyversions/chart-toolkit" alt="Python">
</p>

---

## 📦 项目简介

**Chart Toolkit** (图表工具箱) 是一套完整的Python数据可视化库,支持30+种图表类型,覆盖从基础统计到高级可视化的全部需求!

无论你是数据分析师、开发者还是运营人员,都能快速创建专业的图表!

> **让数据可视化变得简单高效!**

---

## ✨ 核心特性

### 🚀 30+图表类型

| 类别 | 图表类型 | 方法 |
|------|----------|------|
| 📈 基础图表 | 折线图 | `line_chart()` |
| 📊 | 柱状图 | `bar_chart()` |
| 🥧 | 饼图 | `pie_chart()` |
| ⚪ | 散点图 | `scatter_chart()` |
| 🔥 统计图表 | 热力图 | `plot_heatmap()` |
| 📉 | 直方图 | `plot_histogram()` |
| 🔢 | 相关性矩阵 | `plot_corr_matrix()` |
| 📶 时间序列 | 时间线 | `plot_timeline()` |
| 🎯 高级图表 | 仪表盘 | `plot_gauge()` |
| 🔻 | 漏斗图 | `plot_funnel()` |
| ☁️ | 词云 | `plot_wordcloud()` |
| 🗺️ | 地图 | `plot_map()` |
| 📦 批量 | 批量生成 | `batch_charts()` |
| 📊 | 仪表盘 | `dashboard()` |

### 🎨 多种渲染引擎

- **Matplotlib** - 传统静态图表
- **Plotly** - 交互式图表(HTML)

### 🌍 多风格支持

- 默认配色
- 柔和粉彩色 (Pastel)
- 霓虹色 (Neon)
- 自定义颜色

---

## 📦 安装

### 基础安装

```bash
pip install matplotlib pandas
```

### 完整安装 (推荐)

```bash
pip install matplotlib pandas plotly wordcloud folium
```

### 开发安装

```bash
git clone https://github.com/XiLi/chart-toolkit.git
cd chart-toolkit
pip install -e .
```

---

## 💡 快速开始

### 示例1: 一行代码生成折线图

```python
from chart_generator import ChartGenerator

data = {
    'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
    'sales': [10000, 15000, 12000, 18000],
    'profit': [2000, 3500, 2800, 4200]
}

chart = ChartGenerator()
chart.line_chart(data, 'date', ['sales', 'profit'], title='Sales & Profit')
chart.save('chart.png')
print("图表已保存到 chart.png")
```

### 示例2: 柱状图

```python
from chart_generator import ChartGenerator

data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'sales': [10000, 15000, 12000, 18000]
}

chart = ChartGenerator()
chart.bar_chart(data, 'month', 'sales', title='Monthly Sales')
chart.save('bar_chart.png')
```

### 示例3: 饼图

```python
from chart_generator import ChartGenerator

data = {
    'category': ['手机', '电脑', '平板', '配件'],
    'sales': [3500, 3000, 2000, 1500]
}

chart = ChartGenerator()
chart.pie_chart(data, 'category', 'sales', title='Sales by Category')
chart.save('pie_chart.png')
```

### 示例4: 批量生成

```python
import pandas as pd
from chart_generator import batch_charts

# 创建数据
data = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [5, 4, 3, 2, 1],
    'C': [2, 3, 4, 5, 6]
})

# 批量生成
results = batch_charts(data, output_dir='charts')
print(f"生成了 {len(results)} 个图表")
```

### 示例5: 交互式图表

```python
from chart_generator import PlotlyChart
import pandas as pd

data = pd.DataFrame({
    'date': ['2026-01', '2026-02', '2026-03'],
    'sales': [10000, 15000, 12000]
})

fig = PlotlyChart.line(data, 'date', 'sales', title='Interactive Chart')
html = PlotlyChart.to_html(fig)

with open('chart.html', 'w') as f:
    f.write(html)
```

### 示例6: 热力图

```python
import numpy as np
from chart_generator import plot_heatmap
import matplotlib.pyplot as plt

# 创建数据
data = np.random.rand(10, 10)

fig = plot_heatmap(data, '', '', title='Heatmap')
plt.savefig('heatmap.png')
```

### 示例7: 仪表盘HTML

```python
import pandas as pd
from chart_generator import dashboard

data = pd.DataFrame({
    'date': ['2026-01', '2026-02', '2026-03'],
    'sales': [1000, 1500, 1200],
    'profit': [200, 350, 280]
})

output = dashboard(data, output_path='dashboard.html')
print(f"仪表盘已保存到 {output}")
```

---

## 📋 完整API参考

### ChartGenerator 核心类

| 方法 | 参数 | 功能 |
|------|------|------|
| `__init__` | - | 初始化 |
| `line_chart` | data, x, y, title | 折线图 |
| `bar_chart` | data, x, y, title | 柱状图 |
| `pie_chart` | data, labels, values, title | 饼图 |
| `scatter_chart` | data, x, y, title | 散点图 |
| `save` | path | 保存图表 |
| `to_base64` | - | 转为Base64 |
| `show` | - | 显示图表 |

### 独立函数

| 函数 | 功能 |
|------|------|
| `plot_heatmap()` | 热力图 |
| `plot_histogram()` | 直方图 |
| `plot_corr_matrix()` | 相关性矩阵 |
| `plot_stacked_bar()` | 堆叠柱状图 |
| `plot_timeline()` | 时间线 |
| `plot_gauge()` | 仪表盘 |
| `plot_funnel()` | 漏斗图 |
| `plot_wordcloud()` | 词云 |
| `plot_map()` | 地图 |
| `batch_charts()` | 批量生成 |
| `dashboard()` | HTML仪表盘 |
| `get_color_scheme()` | 获取颜色方案 |

### Plotly图表 (交互式)

| 方法 | 功能 |
|------|------|
| `PlotlyChart.line()` | 交互折线图 |
| `PlotlyChart.bar()` | 交互柱状图 |
| `PlotlyChart.scatter()` | 交互散点图 |
| `PlotlyChart.pie()` | 交互饼图 |
| `PlotlyChart.to_html()` | 转为HTML |

---

## 🎨 颜色方案

```python
from chart_generator import get_color_scheme

# 获取颜色方案
colors = get_color_scheme('default')   # 默认
colors = get_color_scheme('pastel')  # 柔和
colors = get_color_scheme('neon')  # 霓虹
```

---

## 📊 数据格式

### 字典格式

```python
data = {
    'x_column': ['A', 'B', 'C'],
    'y_column': [100, 200, 300]
}
```

### DataFrame格式

```python
import pandas as pd
data = pd.DataFrame({
    'x': ['A', 'B', 'C'],
    'y': [100, 200, 300]
})
```

---

## 🛠️ 依赖

```txt
matplotlib>=3.4.0
pandas>=1.3.0

# 可选
plotly>=5.0.0      # 交互图表
wordcloud>=1.8.0   # 词云
folium>=0.12.0    # 地图
```

---

## 📝 示例代码

运行示例:

```bash
python examples.py
```

将在 `examples/` 目录生成所有图表!

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 许可证

MIT License - 免费商用

---

## ⭐ 支持

**如果对你有帮助,欢迎 ⭐ Star 支持!**

---

<div align="center">

**让数据可视化变得简单高效!**

Made with ❤️ by [XiLi](https://github.com/XiLi)

</div>

---

## 🔧 OpenClaw / Claude Code 使用

本技能已集成到 OpenClaw 技能系统,可直接使用:

`python
# 在 OpenClaw 或 Claude Code 中使用
from ai_workflow import run_workflow
from chart_generator import ChartGenerator
from data_parser import DataParser
from database_ops import DatabaseOps
from excel_parser import ExcelParser
from feishu_sheets import FeishuSheets
`

或通过 skills 目录调用:

`python
import sys
sys.path.insert(0, 'path/to/skills')
`

