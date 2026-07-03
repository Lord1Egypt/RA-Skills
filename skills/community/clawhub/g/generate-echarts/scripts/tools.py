from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def generate_echarts(
    echartsOption: str,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    theme: Optional[str] = "default",
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate visual charts using Apache ECharts with echarts option and configuration dynamically. Apache ECharts is an Open Source JavaScript Visualization Library, which is used to create interactive charts and visualizations in web applications. It supports a wide range of chart types, including line charts, bar charts, pie charts, scatter plots, and more. ECharts is highly customizable and can be integrated with various data sources to create dynamic visualizations.
    
    Args:
        echartsOption: ECharts option and configuration used to generate charts. For example:
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

        width: The width of the ECharts in pixels. Default is 800.
        height: The height of the ECharts in pixels. Default is 600.
        theme: ECharts theme, optional. Default is 'default'.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "echartsOption": echartsOption,
        "width": width,
        "height": height,
        "theme": theme,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_echarts", arguments)

def generate_line_chart(
    axisXTitle: Optional[str] = "",
    axisYTitle: Optional[str] = "",
    data: null,
    height: Optional[int] = 600.0,
    showArea: Optional[bool] = False,
    showSymbol: Optional[bool] = True,
    smooth: Optional[bool] = False,
    stack: Optional[bool] = False,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a line chart to show trends over time, such as, the ratio of Apple computer sales to Apple's profits changed from 2000 to 2016.
    
    Args:
        axisXTitle: Set the x-axis title of chart.
        axisYTitle: Set the y-axis title of chart.
        data: Data for line chart, such as, [{ time: '2015', value: 23 }, { time: '2016', value: 32 }]. For multiple series: [{ group: 'Series A', time: '2015', value: 23 }, { group: 'Series B', time: '2015', value: 18 }].
        height: Set the height of the chart, default is 600px.
        showArea: Whether to fill the area under the line. Default is false.
        showSymbol: Whether to show symbols on data points. Default is true.
        smooth: Whether to use a smooth curve. Default is false.
        stack: Whether stacking is enabled. When enabled, line charts require a 'group' field in the data.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "data": data,
        "height": height,
        "showArea": showArea,
        "showSymbol": showSymbol,
        "smooth": smooth,
        "stack": stack,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_line_chart", arguments)

def generate_bar_chart(
    axisXTitle: Optional[str] = "",
    axisYTitle: Optional[str] = "",
    data: null,
    height: Optional[int] = 600.0,
    group: Optional[bool] = False,
    stack: Optional[bool] = False,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a bar chart to show data for numerical comparisons among different categories, such as, comparing categorical data and for horizontal comparisons.
    
    Args:
        axisXTitle: Set the x-axis title of chart.
        axisYTitle: Set the y-axis title of chart.
        data: Data for bar chart, such as, [{ category: 'Category A', value: 10 }, { category: 'Category B', value: 20 }] or [{ category: 'Category A', value: 10, group: 'Group A' }].
        height: Set the height of the chart, default is 600px.
        group: Whether grouping is enabled. When enabled, bar charts require a 'group' field in the data. When `group` is true, `stack` should be false.
        stack: Whether stacking is enabled. When enabled, bar charts require a 'group' field in the data. When `stack` is true, `group` should be false.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "data": data,
        "height": height,
        "group": group,
        "stack": stack,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_bar_chart", arguments)

def generate_pie_chart(
    data: null,
    height: Optional[int] = 600.0,
    innerRadius: Optional[float] = 0.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a pie chart to show the proportion of parts, such as, market share and budget allocation.
    
    Args:
        data: Data for pie chart, such as, [{ category: 'Category A', value: 27 }, { category: 'Category B', value: 25 }].
        height: Set the height of the chart, default is 600px.
        innerRadius: Set the innerRadius of pie chart, the value between 0 and 1. Set the pie chart as a donut chart. Set the value to 0.6 or number in [0 ,1] to enable it.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "innerRadius": innerRadius,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_pie_chart", arguments)

def generate_radar_chart(
    data: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a radar chart to display multidimensional data (four dimensions or more), such as, evaluate Huawei and Apple phones in terms of five dimensions: ease of use, functionality, camera, benchmark scores, and battery life.
    
    Args:
        data: Data for radar chart, such as, [{ name: 'Design', value: 70 }, { name: 'Performance', value: 85 }] or [{ name: 'Design', value: 70, group: 'iPhone' }].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_radar_chart", arguments)

def generate_scatter_chart(
    axisXTitle: Optional[str] = "",
    axisYTitle: Optional[str] = "",
    data: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a scatter chart to show the relationship between two variables, helps discover their relationship or trends, such as, the strength of correlation, data distribution patterns.
    
    Args:
        axisXTitle: Set the x-axis title of chart.
        axisYTitle: Set the y-axis title of chart.
        data: Data for scatter chart, such as, [{ x: 10, y: 15 }, { x: 20, y: 25 }].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "data": data,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_scatter_chart", arguments)

def generate_sankey_chart(
    data: null,
    height: Optional[int] = 600.0,
    nodeAlign: Optional[str] = "justify",
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a sankey chart to visualize the flow of data between different stages or categories, such as, the user journey from landing on a page to completing a purchase.
    
    Args:
        data: Data for sankey chart, such as, [{ source: 'Landing Page', target: 'Product Page', value: 50000 }, { source: 'Product Page', target: 'Add to Cart', value: 35000 }].
        height: Set the height of the chart, default is 600px.
        nodeAlign: Alignment of nodes in the sankey chart, such as, 'left', 'right', or 'justify'.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "nodeAlign": nodeAlign,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_sankey_chart", arguments)

def generate_funnel_chart(
    data: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a funnel chart to visualize the progressive reduction of data as it passes through stages, such as, the conversion rates of users from visiting a website to completing a purchase.
    
    Args:
        data: Data for funnel chart, such as, [{ category: 'Browse Website', value: 50000 }, { category: 'Add to Cart', value: 35000 }, { category: 'Generate Order', value: 25000 }].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_funnel_chart", arguments)

def generate_gauge_chart(
    data: null,
    height: Optional[int] = 600.0,
    max: Optional[float] = 100.0,
    min: Optional[float] = 0.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a gauge chart to display single indicator's current status, such as, CPU usage rate, completion progress, or performance scores.
    
    Args:
        data: Data for gauge chart, such as, [{ name: 'CPU Usage', value: 75 }]. Multiple gauges can be displayed.
        height: Set the height of the chart, default is 600px.
        max: Maximum value of the gauge, default is 100.
        min: Minimum value of the gauge, default is 0.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "max": max,
        "min": min,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_gauge_chart", arguments)

def generate_treemap_chart(
    data: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a treemap chart to display hierarchical data and can intuitively show comparisons between items at the same level, such as, show disk space usage with treemap.
    
    Args:
        data: Data for treemap chart, such as, [{ name: 'Design', value: 70, children: [{ name: 'Tech', value: 20 }] }].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_treemap_chart", arguments)

def generate_sunburst_chart(
    data: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a sunburst chart to display multi-level hierarchical data, such as, organizational structure, file system hierarchy, or category breakdown.
    
    Args:
        data: Data for sunburst chart, such as, [{ name: 'Technology', value: 100, children: [{ name: 'Frontend', value: 60, children: [{ name: 'React', value: 30 }] }] }].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_sunburst_chart", arguments)

def generate_heatmap_chart(
    axisXTitle: Optional[str] = "",
    axisYTitle: Optional[str] = "",
    data: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a heatmap chart to display data density or intensity distribution, such as, user activity patterns by time and day, or correlation matrix.
    
    Args:
        axisXTitle: Set the x-axis title of chart.
        axisYTitle: Set the y-axis title of chart.
        data: Data for heatmap chart, such as, [{ x: 'Mon', y: '12AM', value: 5 }, { x: 'Tue', y: '1AM', value: 3 }].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "data": data,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_heatmap_chart", arguments)

def generate_candlestick_chart(
    data: null,
    height: Optional[int] = 600.0,
    showVolume: Optional[bool] = False,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a candlestick chart for financial data visualization, such as, stock prices, cryptocurrency prices, or other OHLC (Open-High-Low-Close) data.
    
    Args:
        data: Data for candlestick chart, such as, [{ date: '2023-01-01', open: 100, high: 110, low: 95, close: 105, volume: 10000 }].
        height: Set the height of the chart, default is 600px.
        showVolume: Whether to show volume chart below candlestick. Default is false.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "showVolume": showVolume,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_candlestick_chart", arguments)

def generate_boxplot_chart(
    axisXTitle: Optional[str] = "",
    axisYTitle: Optional[str] = "",
    data: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a boxplot chart to show data for statistical summaries among different categories, such as, comparing the distribution of data points across categories.
    
    Args:
        axisXTitle: Set the x-axis title of chart.
        axisYTitle: Set the y-axis title of chart.
        data: Data for boxplot chart, such as, [{ category: 'Category A', value: 10 }, { category: 'Category B', value: 20, group: 'Group A' }].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "data": data,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_boxplot_chart", arguments)

def generate_graph_chart(
    data: null,
    height: Optional[int] = 600.0,
    layout: Optional[str] = "force",
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a network graph chart to show relationships (edges) between entities (nodes), such as, relationships between people in social networks.
    
    Args:
        data: Data for network graph chart, such as, { nodes: [{ id: 'node1', name: 'Node 1' }], edges: [{ source: 'node1', target: 'node2' }] }
        height: Set the height of the chart, default is 600px.
        layout: Layout algorithm for the graph. Default is 'force'.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "layout": layout,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_graph_chart", arguments)

def generate_parallel_chart(
    data: null,
    dimensions: null,
    height: Optional[int] = 600.0,
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a parallel coordinates chart to display multi-dimensional data, such as, comparing different products across multiple attributes.
    
    Args:
        data: Data for parallel chart, such as, [{ name: 'Product A', values: [4.2, 3.4, 2.3, 1.8] }].
        dimensions: Names of the dimensions/axes, such as, ['Price', 'Quality', 'Service', 'Value'].
        height: Set the height of the chart, default is 600px.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "dimensions": dimensions,
        "height": height,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_parallel_chart", arguments)

def generate_tree_chart(
    data: null,
    height: Optional[int] = 600.0,
    layout: Optional[str] = "orthogonal",
    orient: Optional[str] = "LR",
    theme: Optional[str] = "default",
    title: Optional[str] = None,
    width: Optional[int] = 800.0,
    outputType: Optional[str] = "png"
) -> Dict[str, Any]:
    """
    Generate a tree chart to display hierarchical data structure, such as, organizational chart, family tree, or file directory structure.
    
    Args:
        data: Tree data structure, such as, { name: 'Root', children: [{ name: 'Child 1' }, { name: 'Child 2' }] }.
        height: Set the height of the chart, default is 600px.
        layout: Tree layout type. Default is 'orthogonal'.
        orient: Tree orientation. LR=left-to-right, RL=right-to-left, TB=top-to-bottom, BT=bottom-to-top. Default is 'LR'.
        theme: Set the theme for the chart, optional, default is 'default'.
        title: Set the title of the chart.
        width: Set the width of the chart, default is 800px.
        outputType: The output type of the diagram. Can be 'png', 'svg' or 'option'. Default is 'png', 'png' will return the rendered PNG image, 'svg' will return the rendered SVG string, and 'option' will return the valid ECharts option.
    
    Returns:
        
    """
    arguments = {
        "data": data,
        "height": height,
        "layout": layout,
        "orient": orient,
        "theme": theme,
        "title": title,
        "width": width,
        "outputType": outputType
    }
    
    return call_api("1777316659773443", "generate_tree_chart", arguments)

