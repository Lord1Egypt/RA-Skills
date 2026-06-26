# python-pptx 原生图表 API

python-pptx 图表是**真正的 Office 图表对象**（非手绘），支持 PowerPoint/WPS 内编辑。

## Table of Contents
- [基本流程](#basic)
- [柱状图 / 条形图](#bar)
- [折线图](#line)
- [饼图 / 环形图](#pie)
- [散点图](#scatter)
- [多系列图表](#multi-series)
- [样式设置](#styling)
- [图表位置与大小](#layout)

---

## 基本流程 {#basic}

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import ChartData, CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.dml.color import RGBColor

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# 1. 准备数据
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Sales', (120, 185, 210, 175))

# 2. 添加图表到幻灯片
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,   # 图表类型
    Inches(1), Inches(1),             # left, top
    Inches(8), Inches(4.5),           # width, height
    chart_data,
).chart

prs.save('output.pptx')
```

---

## 柱状图 / 条形图 {#bar}

```python
from pptx.enum.chart import XL_CHART_TYPE

# 常用类型
XL_CHART_TYPE.COLUMN_CLUSTERED       # 簇状柱形图（最常用）
XL_CHART_TYPE.COLUMN_STACKED         # 堆积柱形图
XL_CHART_TYPE.COLUMN_STACKED_100     # 百分比堆积柱形图
XL_CHART_TYPE.BAR_CLUSTERED          # 簇状条形图（横向）
XL_CHART_TYPE.BAR_STACKED            # 堆积条形图
```

```python
chart_data = CategoryChartData()
chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
chart_data.add_series('Revenue', (320, 285, 410, 375, 490, 520))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.5), Inches(1), Inches(9), Inches(5),
    chart_data,
).chart

# 显示数据标签
plot = chart.plots[0]
plot.has_data_labels = True
data_labels = plot.data_labels
data_labels.font.size = Pt(10)
data_labels.font.bold = True
```

---

## 折线图 {#line}

```python
XL_CHART_TYPE.LINE                   # 折线图
XL_CHART_TYPE.LINE_MARKERS           # 带数据点的折线图
XL_CHART_TYPE.LINE_STACKED           # 堆积折线图
```

```python
chart_data = CategoryChartData()
chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
chart_data.add_series('Product A', (50, 65, 80, 72, 95, 110))
chart_data.add_series('Product B', (30, 42, 55, 61, 78, 85))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.LINE_MARKERS,
    Inches(0.5), Inches(1), Inches(9), Inches(5),
    chart_data,
).chart

# 设置折线粗细
from pptx.util import Pt
series = chart.series[0]
series.format.line.width = Pt(2.5)
series.format.line.color.rgb = RGBColor(0x4B, 0x9F, 0xFF)
```

---

## 饼图 / 环形图 {#pie}

```python
XL_CHART_TYPE.PIE                    # 饼图
XL_CHART_TYPE.PIE_EXPLODED           # 分离型饼图
XL_CHART_TYPE.DOUGHNUT               # 环形图
XL_CHART_TYPE.DOUGHNUT_EXPLODED      # 分离型环形图
```

```python
from pptx.chart.data import ChartData

# 饼图用 ChartData（不是 CategoryChartData）
chart_data = ChartData()
chart_data.categories = ['Asia', 'Europe', 'Americas', 'Others']
chart_data.add_series('Market Share', (0.45, 0.28, 0.20, 0.07))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.PIE,
    Inches(1), Inches(1), Inches(7), Inches(5),
    chart_data,
).chart

# 显示百分比标签
plot = chart.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = '0%'
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END

# 显示图例
chart.has_legend = True
from pptx.enum.chart import XL_LEGEND_POSITION
chart.legend.position = XL_LEGEND_POSITION.RIGHT
chart.legend.include_in_layout = False
```

---

## 散点图 {#scatter}

```python
from pptx.chart.data import XyChartData
XL_CHART_TYPE.XY_SCATTER             # 散点图
XL_CHART_TYPE.XY_SCATTER_LINES       # 带直线的散点图
XL_CHART_TYPE.XY_SCATTER_SMOOTH      # 带平滑线的散点图
```

```python
chart_data = XyChartData()
series = chart_data.add_series('Group A')
for x, y in [(1, 2.1), (2, 3.5), (3, 2.8), (4, 4.2), (5, 3.9)]:
    series.add_data_point(x, y)

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.XY_SCATTER,
    Inches(1), Inches(1), Inches(8), Inches(5),
    chart_data,
).chart
```

---

## 多系列图表 {#multi-series}

```python
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('2023', (100, 120, 140, 130))
chart_data.add_series('2024', (130, 155, 170, 190))
chart_data.add_series('2025 (Forecast)', (160, 185, 210, 230))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.5), Inches(1), Inches(9), Inches(5),
    chart_data,
).chart

# 逐系列设置颜色
colors = [RGBColor(0x4B,0x9F,0xFF), RGBColor(0xF5,0xA6,0x23), RGBColor(0x4A,0xDE,0x80)]
for i, series in enumerate(chart.series):
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = colors[i]
```

---

## 样式设置 {#styling}

```python
# 图表标题
chart.has_title = True
chart.chart_title.text_frame.text = '季度收入趋势'
chart.chart_title.text_frame.paragraphs[0].font.size = Pt(16)
chart.chart_title.text_frame.paragraphs[0].font.bold = True

# 隐藏图表背景（透明，适合深色幻灯片）
chart.plot_area.format.fill.background()
chart.chart_area.format.fill.background()

# 坐标轴标签字体
from pptx.enum.chart import XL_AXIS_CROSSES
value_axis = chart.value_axis
value_axis.tick_labels.font.size = Pt(9)
value_axis.tick_labels.font.color.rgb = RGBColor(0xAA, 0xBB, 0xCC)
value_axis.major_gridlines.format.line.color.rgb = RGBColor(0x33, 0x44, 0x55)

category_axis = chart.category_axis
category_axis.tick_labels.font.size = Pt(9)
category_axis.tick_labels.font.color.rgb = RGBColor(0xAA, 0xBB, 0xCC)

# 数字格式
value_axis.tick_labels.number_format = '#,##0'    # 千位分隔
value_axis.tick_labels.number_format = '0.0%'     # 百分比
value_axis.tick_labels.number_format = '$#,##0'   # 美元

# 图例
chart.has_legend = True
chart.legend.font.size = Pt(9)
```

---

## 图表位置与大小 {#layout}

```python
from pptx.util import Inches, Emu

# 用 Inches（更直观）
left   = Inches(0.5)
top    = Inches(1.2)
width  = Inches(9.0)
height = Inches(4.8)

# 用 EMU（精确对齐其他元素时）
left   = Emu(457200)
top    = Emu(1097280)

# 添加后修改位置
graphic_frame = slide.shapes.add_chart(chart_type, left, top, width, height, chart_data)
graphic_frame.left   = Inches(1)    # 重新定位
graphic_frame.width  = Inches(10)   # 调整大小
```

---

## 注意事项

1. **`CategoryChartData` vs `ChartData`**：柱/折/条用 `CategoryChartData`，饼图用 `ChartData`，散点用 `XyChartData`
2. **透明背景**：深色幻灯片上要同时设置 `plot_area` 和 `chart_area` 为透明
3. **数据更新**：图表创建后数据保存在嵌入的 xlsx 内；重新设置数据需重建图表或操作内部 xlsx
4. **WPS 兼容性**：原生图表对象在 WPS 中完全支持，无兼容性问题
