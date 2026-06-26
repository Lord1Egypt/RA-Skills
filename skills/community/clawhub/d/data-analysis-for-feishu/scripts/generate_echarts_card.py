#!/usr/bin/env python3
"""
生成飞书兼容的ECharts交互卡片JSON
支持图表类型：line(折线图), bar(柱状图), pie(饼图), gauge(仪表盘), radar(雷达图)
"""
import argparse
import json
from typing import List, Dict, Any

# 飞书卡片通用模板
CARD_TEMPLATE = {
    "config": {
        "wide_screen_mode": True
    },
    "elements": [
        {
            "tag": "markdown",
            "content": ""
        },
        {
            "tag": "echarts_chart",
            "option": {},
            "width": "100%",
            "height": "400px"
        }
    ]
}

# 默认配色方案
DEFAULT_COLORS = ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"]

def generate_line_chart(x_axis: List[str], y_axis: List[float], title: str, y_name: str = "") -> Dict[str, Any]:
    """生成折线图配置"""
    return {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": x_axis
        },
        "yAxis": {
            "type": "value",
            "name": y_name
        },
        "series": [
            {
                "name": y_name,
                "type": "line",
                "data": y_axis,
                "smooth": True,
                "itemStyle": {
                    "color": DEFAULT_COLORS[0]
                },
                "areaStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0,
                        "y": 0,
                        "x2": 0,
                        "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "rgba(84, 112, 198, 0.3)"},
                            {"offset": 1, "color": "rgba(84, 112, 198, 0.05)"}
                        ]
                    }
                }
            }
        ]
    }

def generate_bar_chart(x_axis: List[str], y_axis: List[float], title: str, y_name: str = "") -> Dict[str, Any]:
    """生成柱状图配置"""
    return {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": x_axis,
            "axisLabel": {
                "rotate": 30
            }
        },
        "yAxis": {
            "type": "value",
            "name": y_name
        },
        "series": [
            {
                "name": y_name,
                "type": "bar",
                "data": y_axis,
                "itemStyle": {
                    "color": DEFAULT_COLORS[0],
                    "borderRadius": [4, 4, 0, 0]
                }
            }
        ]
    }

def generate_pie_chart(labels: List[str], values: List[float], title: str) -> Dict[str, Any]:
    """生成饼图配置"""
    data = [{"name": label, "value": value} for label, value in zip(labels, values)]
    return {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "left": "left"
        },
        "series": [
            {
                "name": title,
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2
                },
                "label": {
                    "show": True,
                    "formatter": "{b}: {d}%"
                },
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": 16,
                        "fontWeight": "bold"
                    }
                },
                "data": data
            }
        ]
    }

def generate_gauge_chart(value: float, title: str, max_value: float = 100, unit: str = "%") -> Dict[str, Any]:
    """生成仪表盘配置"""
    return {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "formatter": "{a} <br/>{b} : {c}" + unit
        },
        "series": [
            {
                "name": title,
                "type": "gauge",
                "startAngle": 180,
                "endAngle": 0,
                "min": 0,
                "max": max_value,
                "splitNumber": 10,
                "itemStyle": {
                    "color": "#5470c6"
                },
                "progress": {
                    "show": True,
                    "width": 18
                },
                "pointer": {
                    "show": False
                },
                "axisLine": {
                    "lineStyle": {
                        "width": 18
                    }
                },
                "axisTick": {
                    "distance": -28,
                    "splitNumber": 5,
                    "lineStyle": {
                        "width": 2,
                        "color": "#999"
                    }
                },
                "splitLine": {
                    "distance": -35,
                    "length": 14,
                    "lineStyle": {
                        "width": 3,
                        "color": "#999"
                    }
                },
                "axisLabel": {
                    "distance": -20,
                    "color": "#999",
                    "fontSize": 12
                },
                "anchor": {
                    "show": False
                },
                "title": {
                    "show": False
                },
                "detail": {
                    "valueAnimation": True,
                    "width": "60%",
                    "lineHeight": 40,
                    "borderRadius": 8,
                    "offsetCenter": [0, "-15%"],
                    "fontSize": 32,
                    "fontWeight": "bolder",
                    "formatter": "{value}" + unit,
                    "color": "inherit"
                },
                "data": [
                    {
                        "value": value
                    }
                ]
            }
        ]
    }

def generate_radar_chart(indicators: List[Dict[str, Any]], values: List[float], title: str, series_name: str = "") -> Dict[str, Any]:
    """生成雷达图配置"""
    return {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "item"
        },
        "legend": {
            "left": "left"
        },
        "radar": {
            "indicator": indicators,
            "shape": "circle"
        },
        "series": [
            {
                "name": series_name,
                "type": "radar",
                "data": [
                    {
                        "value": values,
                        "name": series_name,
                        "areaStyle": {
                            "color": "rgba(84, 112, 198, 0.3)"
                        }
                    }
                ]
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="生成飞书ECharts交互卡片")
    parser.add_argument("--type", required=True, choices=["line", "bar", "pie", "gauge", "radar"], help="图表类型")
    parser.add_argument("--title", required=True, help="图表标题")
    parser.add_argument("--x-axis", nargs="+", help="X轴数据（折线图/柱状图用）")
    parser.add_argument("--y-axis", nargs="+", type=float, help="Y轴数据（折线图/柱状图用）")
    parser.add_argument("--y-name", default="", help="Y轴名称（折线图/柱状图用）")
    parser.add_argument("--labels", nargs="+", help="标签数据（饼图用）")
    parser.add_argument("--values", nargs="+", type=float, help="数值数据（饼图/雷达图用）")
    parser.add_argument("--value", type=float, help="单值数据（仪表盘用）")
    parser.add_argument("--max", type=float, default=100, help="最大值（仪表盘用）")
    parser.add_argument("--unit", default="%", help="单位（仪表盘用）")
    parser.add_argument("--indicators", type=json.loads, help="雷达图指标配置，JSON格式，例如：[{\"name\":\"指标1\",\"max\":100},...]")
    parser.add_argument("--series-name", default="", help="系列名称（雷达图用）")
    parser.add_argument("--height", default="400px", help="图表高度")
    parser.add_argument("--output", help="输出文件路径，不指定则打印到标准输出")
    
    args = parser.parse_args()
    
    # 生成对应图表配置
    option = {}
    if args.type == "line":
        if not args.x_axis or not args.y_axis:
            raise ValueError("折线图需要提供--x-axis和--y-axis参数")
        option = generate_line_chart(args.x_axis, args.y_axis, args.title, args.y_name)
    elif args.type == "bar":
        if not args.x_axis or not args.y_axis:
            raise ValueError("柱状图需要提供--x-axis和--y-axis参数")
        option = generate_bar_chart(args.x_axis, args.y_axis, args.title, args.y_name)
    elif args.type == "pie":
        if not args.labels or not args.values:
            raise ValueError("饼图需要提供--labels和--values参数")
        option = generate_pie_chart(args.labels, args.values, args.title)
    elif args.type == "gauge":
        if args.value is None:
            raise ValueError("仪表盘需要提供--value参数")
        option = generate_gauge_chart(args.value, args.title, args.max, args.unit)
    elif args.type == "radar":
        if not args.indicators or not args.values:
            raise ValueError("雷达图需要提供--indicators和--values参数")
        option = generate_radar_chart(args.indicators, args.values, args.title, args.series_name)
    
    # 构建卡片
    card = CARD_TEMPLATE.copy()
    card["elements"][0]["content"] = f"**{args.title}**"
    card["elements"][1]["option"] = option
    card["elements"][1]["height"] = args.height
    
    # 输出结果
    result = json.dumps(card, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        print(result)

if __name__ == "__main__":
    main()
