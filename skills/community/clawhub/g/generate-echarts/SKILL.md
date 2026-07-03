---
name: 图表生成工具
description: MCP ECharts 是一个基于 Apache ECharts 的动态图表生成和数据分析工具，支持多种导出格式和 MinIO 对象存储集成。
version: 1.0.0
---

# 图表生成工具

MCP ECharts 是一个基于 Apache ECharts 的动态图表生成和数据分析工具，支持多种导出格式和 MinIO 对象存储集成。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Generate visual charts using Apache ECharts with echarts option and configuration dynamically. Apache ECharts is an Open Source JavaScript Visualization Library, which is used to create interactive charts and visualizations in web applications. It supports a wide range of chart types, including line charts, bar charts, pie charts, scatter plots, and more. ECharts is highly customizable and can be integrated with various data sources to create dynamic visualizations. | `scripts.tools.generate_echarts` |
| Generate a line chart to show trends over time, such as, the ratio of Apple computer sales to Apple's profits changed from 2000 to 2016. | `scripts.tools.generate_line_chart` |
| Generate a bar chart to show data for numerical comparisons among different categories, such as, comparing categorical data and for horizontal comparisons. | `scripts.tools.generate_bar_chart` |
| Generate a pie chart to show the proportion of parts, such as, market share and budget allocation. | `scripts.tools.generate_pie_chart` |
| Generate a radar chart to display multidimensional data (four dimensions or more), such as, evaluate Huawei and Apple phones in terms of five dimensions: ease of use, functionality, camera, benchmark scores, and battery life. | `scripts.tools.generate_radar_chart` |
| Generate a scatter chart to show the relationship between two variables, helps discover their relationship or trends, such as, the strength of correlation, data distribution patterns. | `scripts.tools.generate_scatter_chart` |
| Generate a sankey chart to visualize the flow of data between different stages or categories, such as, the user journey from landing on a page to completing a purchase. | `scripts.tools.generate_sankey_chart` |
| Generate a funnel chart to visualize the progressive reduction of data as it passes through stages, such as, the conversion rates of users from visiting a website to completing a purchase. | `scripts.tools.generate_funnel_chart` |
| Generate a gauge chart to display single indicator's current status, such as, CPU usage rate, completion progress, or performance scores. | `scripts.tools.generate_gauge_chart` |
| Generate a treemap chart to display hierarchical data and can intuitively show comparisons between items at the same level, such as, show disk space usage with treemap. | `scripts.tools.generate_treemap_chart` |
| Generate a sunburst chart to display multi-level hierarchical data, such as, organizational structure, file system hierarchy, or category breakdown. | `scripts.tools.generate_sunburst_chart` |
| Generate a heatmap chart to display data density or intensity distribution, such as, user activity patterns by time and day, or correlation matrix. | `scripts.tools.generate_heatmap_chart` |
| Generate a candlestick chart for financial data visualization, such as, stock prices, cryptocurrency prices, or other OHLC (Open-High-Low-Close) data. | `scripts.tools.generate_candlestick_chart` |
| Generate a boxplot chart to show data for statistical summaries among different categories, such as, comparing the distribution of data points across categories. | `scripts.tools.generate_boxplot_chart` |
| Generate a network graph chart to show relationships (edges) between entities (nodes), such as, relationships between people in social networks. | `scripts.tools.generate_graph_chart` |
| Generate a parallel coordinates chart to display multi-dimensional data, such as, comparing different products across multiple attributes. | `scripts.tools.generate_parallel_chart` |
| Generate a tree chart to display hierarchical data structure, such as, organizational chart, family tree, or file directory structure. | `scripts.tools.generate_tree_chart` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.generate_echarts
工具描述：Generate visual charts using Apache ECharts with echarts option and configuration dynamically. Apache ECharts is an Open Source JavaScript Visualization Library, which is used to create interactive charts and visualizations in web applications. It supports a wide range of chart types, including line charts, bar charts, pie charts, scatter plots, and more. ECharts is highly customizable and can be integrated with various data sources to create dynamic visualizations.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|echartsOption|string|true| |ECharts option and configuration used to generate charts. For example:
{
  "title": {
    "text": "ECharts Entry Example",
    "left": "center",
    "top": "2%"
  },
  "tooltip": {},
  "xAxis": {
    "data": ["shirt", "cardigan", "chiffon", "pants", "heels", "socks"]
  },
  "yAxis": {},
  "series": [{
    "name": "Sales",
    "type": "bar",
    "data": [5, 20, 36, 10, 10, 20]
  }]
}

ATTENTION: A valid ECharts option must be a valid JSON string, and cannot be empty.
|
|width|number|false|800.0|The width of the ECharts in pixels. Default is 800.|
|height|number|false|600.0|The height of the ECharts in pixels. Default is 600.|
|theme|string|false|"default"|ECharts theme, optional. Default is 'default'.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_line_chart
工具描述：Generate a line chart to show trends over time, such as, the ratio of Apple computer sales to Apple's profits changed from 2000 to 2016.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|axisXTitle|string|false|""|Set the x-axis title of chart.|
|axisYTitle|string|false|""|Set the y-axis title of chart.|
|data|array|true| |Data for line chart, such as, [{ time: '2015', value: 23 }, { time: '2016', value: 32 }]. For multiple series: [{ group: 'Series A', time: '2015', value: 23 }, { group: 'Series B', time: '2015', value: 18 }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|showArea|boolean|false|false|Whether to fill the area under the line. Default is false.|
|showSymbol|boolean|false|true|Whether to show symbols on data points. Default is true.|
|smooth|boolean|false|false|Whether to use a smooth curve. Default is false.|
|stack|boolean|false|false|Whether stacking is enabled. When enabled, line charts require a 'group' field in the data.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_bar_chart
工具描述：Generate a bar chart to show data for numerical comparisons among different categories, such as, comparing categorical data and for horizontal comparisons.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|axisXTitle|string|false|""|Set the x-axis title of chart.|
|axisYTitle|string|false|""|Set the y-axis title of chart.|
|data|array|true| |Data for bar chart, such as, [{ category: 'Category A', value: 10 }, { category: 'Category B', value: 20 }] or [{ category: 'Category A', value: 10, group: 'Group A' }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|group|boolean|false|false|Whether grouping is enabled. When enabled, bar charts require a 'group' field in the data. When `group` is true, `stack` should be false.|
|stack|boolean|false|false|Whether stacking is enabled. When enabled, bar charts require a 'group' field in the data. When `stack` is true, `group` should be false.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_pie_chart
工具描述：Generate a pie chart to show the proportion of parts, such as, market share and budget allocation.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for pie chart, such as, [{ category: 'Category A', value: 27 }, { category: 'Category B', value: 25 }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|innerRadius|number|false|0.0|Set the innerRadius of pie chart, the value between 0 and 1. Set the pie chart as a donut chart. Set the value to 0.6 or number in [0 ,1] to enable it.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_radar_chart
工具描述：Generate a radar chart to display multidimensional data (four dimensions or more), such as, evaluate Huawei and Apple phones in terms of five dimensions: ease of use, functionality, camera, benchmark scores, and battery life.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for radar chart, such as, [{ name: 'Design', value: 70 }, { name: 'Performance', value: 85 }] or [{ name: 'Design', value: 70, group: 'iPhone' }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_scatter_chart
工具描述：Generate a scatter chart to show the relationship between two variables, helps discover their relationship or trends, such as, the strength of correlation, data distribution patterns.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|axisXTitle|string|false|""|Set the x-axis title of chart.|
|axisYTitle|string|false|""|Set the y-axis title of chart.|
|data|array|true| |Data for scatter chart, such as, [{ x: 10, y: 15 }, { x: 20, y: 25 }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_sankey_chart
工具描述：Generate a sankey chart to visualize the flow of data between different stages or categories, such as, the user journey from landing on a page to completing a purchase.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for sankey chart, such as, [{ source: 'Landing Page', target: 'Product Page', value: 50000 }, { source: 'Product Page', target: 'Add to Cart', value: 35000 }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|nodeAlign|string|false|"justify"|Alignment of nodes in the sankey chart, such as, 'left', 'right', or 'justify'.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_funnel_chart
工具描述：Generate a funnel chart to visualize the progressive reduction of data as it passes through stages, such as, the conversion rates of users from visiting a website to completing a purchase.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for funnel chart, such as, [{ category: 'Browse Website', value: 50000 }, { category: 'Add to Cart', value: 35000 }, { category: 'Generate Order', value: 25000 }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_gauge_chart
工具描述：Generate a gauge chart to display single indicator's current status, such as, CPU usage rate, completion progress, or performance scores.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for gauge chart, such as, [{ name: 'CPU Usage', value: 75 }]. Multiple gauges can be displayed.|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|max|number|false|100.0|Maximum value of the gauge, default is 100.|
|min|number|false|0.0|Minimum value of the gauge, default is 0.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_treemap_chart
工具描述：Generate a treemap chart to display hierarchical data and can intuitively show comparisons between items at the same level, such as, show disk space usage with treemap.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for treemap chart, such as, [{ name: 'Design', value: 70, children: [{ name: 'Tech', value: 20 }] }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_sunburst_chart
工具描述：Generate a sunburst chart to display multi-level hierarchical data, such as, organizational structure, file system hierarchy, or category breakdown.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for sunburst chart, such as, [{ name: 'Technology', value: 100, children: [{ name: 'Frontend', value: 60, children: [{ name: 'React', value: 30 }] }] }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_heatmap_chart
工具描述：Generate a heatmap chart to display data density or intensity distribution, such as, user activity patterns by time and day, or correlation matrix.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|axisXTitle|string|false|""|Set the x-axis title of chart.|
|axisYTitle|string|false|""|Set the y-axis title of chart.|
|data|array|true| |Data for heatmap chart, such as, [{ x: 'Mon', y: '12AM', value: 5 }, { x: 'Tue', y: '1AM', value: 3 }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_candlestick_chart
工具描述：Generate a candlestick chart for financial data visualization, such as, stock prices, cryptocurrency prices, or other OHLC (Open-High-Low-Close) data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for candlestick chart, such as, [{ date: '2023-01-01', open: 100, high: 110, low: 95, close: 105, volume: 10000 }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|showVolume|boolean|false|false|Whether to show volume chart below candlestick. Default is false.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_boxplot_chart
工具描述：Generate a boxplot chart to show data for statistical summaries among different categories, such as, comparing the distribution of data points across categories.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|axisXTitle|string|false|""|Set the x-axis title of chart.|
|axisYTitle|string|false|""|Set the y-axis title of chart.|
|data|array|true| |Data for boxplot chart, such as, [{ category: 'Category A', value: 10 }, { category: 'Category B', value: 20, group: 'Group A' }].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_graph_chart
工具描述：Generate a network graph chart to show relationships (edges) between entities (nodes), such as, relationships between people in social networks.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|object|true| |Data for network graph chart, such as, { nodes: [{ id: 'node1', name: 'Node 1' }], edges: [{ source: 'node1', target: 'node2' }] }|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|layout|string|false|"force"|Layout algorithm for the graph. Default is 'force'.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_parallel_chart
工具描述：Generate a parallel coordinates chart to display multi-dimensional data, such as, comparing different products across multiple attributes.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |Data for parallel chart, such as, [{ name: 'Product A', values: [4.2, 3.4, 2.3, 1.8] }].|
|dimensions|array|true| |Names of the dimensions/axes, such as, ['Price', 'Quality', 'Service', 'Value'].|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---

## scripts.tools.generate_tree_chart
工具描述：Generate a tree chart to display hierarchical data structure, such as, organizational chart, family tree, or file directory structure.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|object|true| |Tree data structure, such as, { name: 'Root', children: [{ name: 'Child 1' }, { name: 'Child 2' }] }.|
|height|integer|false|600.0|Set the height of the chart, default is 600px.|
|layout|string|false|"orthogonal"|Tree layout type. Default is 'orthogonal'.|
|orient|string|false|"LR"|Tree orientation. LR=left-to-right, RL=right-to-left, TB=top-to-bottom, BT=bottom-to-top. Default is 'LR'.|
|theme|string|false|"default"|Set the theme for the chart, optional, default is 'default'.|
|title|string|false| |Set the title of the chart.|
|width|integer|false|800.0|Set the width of the chart, default is 800px.|
|outputType|string|false|"png"|The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据