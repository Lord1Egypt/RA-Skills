#!/usr/bin/env python3
"""
Local ECharts rendering + headless browser screenshot generation
Fully local operation, no third-party API dependencies, ensures normal image display
"""
import argparse
import json
import asyncio
from pyppeteer import launch
from typing import List, Dict, Any, Union

# ECharts CDN address
ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"

# Default color scheme
DEFAULT_COLORS = ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"]

async def render_echarts_to_image(option: dict, output_path: str, width: int = 1200, height: int = 750):
    """Use headless browser to render ECharts and take screenshot"""
    browser = await launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--force-device-scale-factor=2', '--high-dpi-support=1']
    )
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height, 'deviceScaleFactor': 2})
    
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="{ECHARTS_CDN}"></script>
        <style>
            body {{ margin: 0; padding: 0; background: #fff; }}
            #chart {{ width: {width}px; height: {height}px; }}
        </style>
    </head>
    <body>
        <div id="chart"></div>
        <script>
            var myChart = echarts.init(document.getElementById('chart'));
            var option = {json.dumps(option)};
            myChart.setOption(option);
        </script>
    </body>
    </html>
    """
    
    await page.setContent(html_content)
    # Wait for ECharts to load and render completely
    chart_element = await page.waitForSelector('#chart', {'visible': True})
    await asyncio.sleep(3)
    # Precisely capture the chart element, no extra content
    await chart_element.screenshot({
        'path': output_path, 
        'type': 'png', 
        'omitBackground': False,
        'quality': 100
    })
    await browser.close()
    print(f"Image generated: {output_path}")

def generate_chart_option(args) -> Dict[str, Any]:
    """Generate ECharts configuration"""
    # Support multi-series data
    is_multi_series = hasattr(args, 'multi_series') and args.multi_series
    y_axis_data = args.y_axis if is_multi_series and isinstance(args.y_axis[0], list) else [args.y_axis]
    series_names = args.series_names.split(",") if hasattr(args, 'series_names') and args.series_names else [f"Series {i+1}" for i in range(len(y_axis_data))]
    stack = args.stack if hasattr(args, 'stack') and args.stack else None
    
    if args.type == "line":
        series = []
        for i, (y_data, name) in enumerate(zip(y_axis_data, series_names)):
            series_item = {
                "name": name,
                "type": "line",
                "data": y_data,
                "smooth": True,
                "itemStyle": {"color": DEFAULT_COLORS[i % len(DEFAULT_COLORS)]}
            }
            if getattr(args, 'area', False):
                series_item["areaStyle"] = {
                    "color": {
                        "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": f"rgba{tuple(int(DEFAULT_COLORS[i%len(DEFAULT_COLORS)][1:][j:j+2], 16) for j in (0,2,4)) + (0.3,)}"},
                            {"offset": 1, "color": f"rgba{tuple(int(DEFAULT_COLORS[i%len(DEFAULT_COLORS)][1:][j:j+2], 16) for j in (0,2,4)) + (0.05,)}"}
                        ]
                    }
                }
            if stack:
                series_item["stack"] = stack
            series.append(series_item)
        
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "axis"},
            "legend": {"top": "10%"},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {"type": "category", "boundaryGap": False, "data": args.x_axis},
            "yAxis": {"type": "value", "name": args.y_name},
            "series": series
        }
    
    elif args.type == "area":
        args.area = True
        args.type = "line"
        return generate_chart_option(args)
    
    elif args.type == "bar":
        series = []
        for i, (y_data, name) in enumerate(zip(y_axis_data, series_names)):
            series_item = {
                "name": name,
                "type": "bar",
                "data": y_data,
                "itemStyle": {
                    "color": DEFAULT_COLORS[i % len(DEFAULT_COLORS)],
                    "borderRadius": [4, 4, 0, 0]
                }
            }
            if stack:
                series_item["stack"] = stack
            series.append(series_item)
        
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {"top": "10%"},
            "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
            "xAxis": {"type": "category", "data": args.x_axis, "axisLabel": {"rotate": 30}, "boundaryGap": True},
            "yAxis": {"type": "value", "name": args.y_name},
            "series": series
        }
    
    elif args.type == "stack_bar":
        args.stack = "total"
        args.type = "bar"
        return generate_chart_option(args)
    
    elif args.type == "pie":
        data = [{"name": label, "value": value} for label, value in zip(args.labels, args.values)]
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b}: {c} ({d}%)"},
            "legend": {"orient": "vertical", "left": "left"},
            "series": [{
                "name": args.title,
                "type": "pie",
                "radius": ["40%", "70%"],
                "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
                "label": {"show": True, "formatter": "{b}: {d}%"},
                "data": data
            }]
        }
    
    elif args.type == "donut":
        option = generate_chart_option(args)
        option["series"][0]["radius"] = ["30%", "70%"]
        return option
    
    elif args.type == "gauge":
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"formatter": "{a} <br/>{b} : {c}" + args.unit},
            "series": [{
                "name": args.title,
                "type": "gauge",
                "startAngle": 180,
                "endAngle": 0,
                "min": 0,
                "max": args.max,
                "splitNumber": 10,
                "itemStyle": {"color": "#5470c6"},
                "progress": {"show": True, "width": 18},
                "pointer": {"show": False},
                "axisLine": {"lineStyle": {"width": 18}},
                "axisTick": {"distance": -28, "splitNumber": 5, "lineStyle": {"width": 2, "color": "#999"}},
                "splitLine": {"distance": -35, "length": 14, "lineStyle": {"width": 3, "color": "#999"}},
                "axisLabel": {"distance": -20, "color": "#999", "fontSize": 14},
                "detail": {
                    "valueAnimation": True,
                    "width": "60%",
                    "lineHeight": 40,
                    "borderRadius": 8,
                    "offsetCenter": [0, "-15%"],
                    "fontSize": 40,
                    "fontWeight": "bolder",
                    "formatter": "{value}" + args.unit,
                    "color": "inherit"
                },
                "data": [{"value": args.value}]
            }]
        }
    
    elif args.type == "radar":
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "item"},
            "legend": {"left": "left"},
            "radar": {
                "indicator": args.indicators,
                "shape": "circle"
            },
            "series": [{
                "name": args.series_name,
                "type": "radar",
                "data": [{
                    "value": args.values,
                    "name": args.series_name,
                    "areaStyle": {"color": "rgba(84, 112, 198, 0.3)"}
                }]
            }]
        }
    
    elif args.type == "scatter":
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "item"},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {"type": "value", "name": args.x_name if hasattr(args, 'x_name') else "X"},
            "yAxis": {"type": "value", "name": args.y_name},
            "series": [{
                "type": "scatter",
                "data": list(zip(args.x_axis, args.y_axis)),
                "itemStyle": {"color": DEFAULT_COLORS[0]}
            }]
        }
    
    elif args.type == "funnel":
        data = [{"name": label, "value": value} for label, value in zip(args.labels, args.values)]
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "item", "formatter": "{b}: {c}"},
            "legend": {"left": "left"},
            "series": [{
                "name": args.title,
                "type": "funnel",
                "left": "10%",
                "top": "60",
                "width": "80%",
                "min": 0,
                "max": max(args.values) if args.values else 100,
                "minSize": "0%",
                "maxSize": "100%",
                "sort": "descending",
                "gap": 2,
                "label": {"show": True, "position": "inside"},
                "itemStyle": {"borderColor": "#fff", "borderWidth": 2},
                "data": data
            }]
        }
    
    elif args.type == "waterfall":
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {"type": "category", "data": args.x_axis, "axisLabel": {"rotate": 30}},
            "yAxis": {"type": "value", "name": args.y_name},
            "series": [
                {
                    "type": "bar",
                    "stack": "total",
                    "itemStyle": {"color": "transparent", "borderColor": "transparent"},
                    "emphasis": {"itemStyle": {"color": "transparent", "borderColor": "transparent"}},
                    "data": args.base_values if hasattr(args, 'base_values') else [0] * len(args.y_axis)
                },
                {
                    "type": "bar",
                    "stack": "total",
                    "itemStyle": {
                        "color": lambda params: "#ee6666" if params.data < 0 else "#91cc75",
                        "borderRadius": [4, 4, 0, 0]
                    },
                    "data": args.y_axis
                }
            ]
        }
    
    elif args.type == "dual_axis":
        return {
            "title": {"text": args.title, "left": "center", "textStyle": {"fontSize": 22, "fontWeight": "bold"}},
            "tooltip": {"trigger": "axis"},
            "legend": {"top": "10%"},
            "grid": {"left": "3%", "right": "20%", "bottom": "15%", "containLabel": True},
            "xAxis": {"type": "category", "boundaryGap": True, "data": args.x_axis, "axisLabel": {"rotate": 30}},
            "yAxis": [
                {"type": "value", "name": args.y1_name, "position": "left"},
                {"type": "value", "name": args.y2_name, "position": "right"}
            ],
            "series": [
                {
                    "name": args.y1_name,
                    "type": "line",
                    "data": args.y1_axis,
                    "smooth": True,
                    "itemStyle": {"color": DEFAULT_COLORS[0]}
                },
                {
                    "name": args.y2_name,
                    "type": "bar",
                    "yAxisIndex": 1,
                    "data": args.y2_axis,
                    "itemStyle": {"color": DEFAULT_COLORS[1]}
                }
            ]
        }
    
    return {}

def main():
    parser = argparse.ArgumentParser(description="Local ECharts rendering + screenshot generation")
    parser.add_argument("--type", required=True, choices=["line", "area", "bar", "stack_bar", "pie", "donut", "gauge", "radar", "scatter", "funnel", "waterfall", "dual_axis"], help="Chart type")
    parser.add_argument("--title", required=True, help="Chart title")
    parser.add_argument("--output", required=True, help="Output PNG file path")
    
    # Common data parameters
    parser.add_argument("--x-axis", nargs="+", help="X-axis data (line/bar/area/scatter/waterfall)")
    parser.add_argument("--y-axis", nargs="+", type=float, help="Y-axis data")
    parser.add_argument("--y-name", default="", help="Y-axis name")
    parser.add_argument("--labels", nargs="+", help="Labels (pie/donut/funnel)")
    parser.add_argument("--values", nargs="+", type=float, help="Values (pie/donut/funnel)")
    parser.add_argument("--value", type=float, help="Single value (gauge)")
    parser.add_argument("--max", type=float, default=100, help="Max value (gauge)")
    parser.add_argument("--unit", default="%", help="Unit (gauge)")
    parser.add_argument("--indicators", type=json.loads, help="Radar chart indicators JSON")
    parser.add_argument("--series-name", default="", help="Series name (radar)")
    
    # Multi-series parameters
    parser.add_argument("--multi-series", action="store_true", help="Enable multi-series mode")
    parser.add_argument("--series-names", default="", help="Comma-separated series names")
    parser.add_argument("--stack", default="", help="Stack name for stacked charts")
    parser.add_argument("--area", action="store_true", help="Enable area fill for line chart")
    
    # Dual axis parameters
    parser.add_argument("--y1-axis", nargs="+", type=float, help="Left Y-axis data (dual_axis)")
    parser.add_argument("--y2-axis", nargs="+", type=float, help="Right Y-axis data (dual_axis)")
    parser.add_argument("--y1-name", default="", help="Left Y-axis name")
    parser.add_argument("--y2-name", default="", help="Right Y-axis name")
    
    # Waterfall parameters
    parser.add_argument("--base-values", nargs="+", type=float, help="Base values for waterfall chart")
    
    # Scatter parameters
    parser.add_argument("--x-name", default="", help="X-axis name (scatter)")
    
    # Output options
    parser.add_argument("--width", type=int, default=1200, help="Image width")
    parser.add_argument("--height", type=int, default=750, help="Image height")
    
    args = parser.parse_args()
    option = generate_chart_option(args)
    asyncio.run(render_echarts_to_image(option, args.output, args.width, args.height))

if __name__ == "__main__":
    main()
