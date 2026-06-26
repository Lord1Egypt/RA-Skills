#!/usr/bin/env python3
"""
酒店P&L数据可视化脚本
使用ECharts生成交互式图表

依赖：pip install pyecharts
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

# 尝试导入pyecharts，如果不可用则使用替代方案
try:
    from pyecharts.charts import Bar, Line, Pie, Gauge, Radar
    from pyecharts import options as opts
    from pyecharts.globals import ThemeType
    HAS_PYECHARTS = True
except ImportError:
    HAS_PYECHARTS = False
    print("提示：pyecharts未安装，将生成JSON数据供前端渲染")


class HotelPLVisualizer:
    """酒店P&L数据可视化类"""
    
    def __init__(self, title: str = "酒店P&L分析"):
        self.title = title
        self.data = {}
    
    def add_revenue_data(self, data: Dict):
        """添加收入数据"""
        self.data['revenue'] = data
    
    def add_cost_data(self, data: Dict):
        """添加成本数据"""
        self.data['cost'] = data
    
    def add_profit_data(self, data: Dict):
        """添加利润数据"""
        self.data['profit'] = data
    
    def generate_kpi_dashboard(self) -> str:
        """生成KPI仪表盘JSON数据"""
        if 'revenue' not in self.data or 'profit' not in self.data:
            return "{}"
        
        # 提取关键指标
        total_revenue = self.data['revenue'].get('total', 0)
        gop = self.data['profit'].get('gop', 0)
        gop_margin = self.data['profit'].get('gop_margin', 0)
        occ = self.data['revenue'].get('occ', 0)
        adr = self.data['revenue'].get('adr', 0)
        revpar = self.data['revenue'].get('revpar', 0)
        
        # 生成ECharts配置
        chart_config = {
            "title": {
                "text": self.title,
                "subtext": datetime.now().strftime("%Y年%m月"),
                "left": "center"
            },
            "tooltip": {
                "trigger": "item",
                "formatter": "{b}: {c} ({d}%)"
            },
            "series": [
                {
                    "name": "GOP率仪表",
                    "type": "gauge",
                    "radius": "60%",
                    "center": ["25%", "50%"],
                    "startAngle": 180,
                    "endAngle": 0,
                    "min": 0,
                    "max": 50,
                    "splitNumber": 5,
                    "itemStyle": {
                        "color": "#5470C6"
                    },
                    "progress": {
                        "show": True,
                        "width": 18
                    },
                    "pointer": {
                        "show": True,
                        "length": "60%",
                        "width": 6
                    },
                    "axisLine": {
                        "lineStyle": {
                            "width": 18
                        }
                    },
                    "axisTick": {
                        "distance": -20,
                        "length": 5,
                        "lineStyle": {
                            "color": "auto",
                            "width": 1
                        }
                    },
                    "splitLine": {
                        "distance": -20,
                        "length": 14,
                        "lineStyle": {
                            "color": "auto",
                            "width": 2
                        }
                    },
                    "axisLabel": {
                        "distance": -40,
                        "color": "#999",
                        "fontSize": 10
                    },
                    "detail": {
                        "valueAnimation": True,
                        "formatter": "{value}%",
                        "color": "auto",
                        "fontSize": 20,
                        "offsetCenter": [0, "40%"]
                    },
                    "data": [{"value": round(gop_margin, 1), "name": "GOP率"}]
                },
                {
                    "name": "出租率仪表",
                    "type": "gauge",
                    "radius": "60%",
                    "center": ["75%", "50%"],
                    "startAngle": 180,
                    "endAngle": 0,
                    "min": 0,
                    "max": 100,
                    "splitNumber": 5,
                    "itemStyle": {
                        "color": "#91CC75"
                    },
                    "progress": {
                        "show": True,
                        "width": 18
                    },
                    "pointer": {
                        "show": True,
                        "length": "60%",
                        "width": 6
                    },
                    "axisLine": {
                        "lineStyle": {
                            "width": 18
                        }
                    },
                    "axisTick": {
                        "distance": -20,
                        "length": 5,
                        "lineStyle": {
                            "color": "auto",
                            "width": 1
                        }
                    },
                    "splitLine": {
                        "distance": -20,
                        "length": 14,
                        "lineStyle": {
                            "color": "auto",
                            "width": 2
                        }
                    },
                    "axisLabel": {
                        "distance": -40,
                        "color": "#999",
                        "fontSize": 10
                    },
                    "detail": {
                        "valueAnimation": True,
                        "formatter": "{value}%",
                        "color": "auto",
                        "fontSize": 20,
                        "offsetCenter": [0, "40%"]
                    },
                    "data": [{"value": round(occ, 1), "name": "出租率"}]
                }
            ]
        }
        
        return json.dumps(chart_config, ensure_ascii=False, indent=2)
    
    def generate_revenue_chart(self) -> str:
        """生成收入结构饼图"""
        if 'revenue' not in self.data:
            return "{}"
        
        revenue_data = self.data['revenue']
        
        chart_config = {
            "title": {
                "text": "收入结构分析",
                "left": "center"
            },
            "tooltip": {
                "trigger": "item",
                "formatter": "{b}: ¥{c}万 ({d}%)"
            },
            "legend": {
                "orient": "vertical",
                "left": "left"
            },
            "series": [
                {
                    "name": "收入构成",
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
                        "formatter": "{b}\n¥{c}万\n{d}%"
                    },
                    "emphasis": {
                        "label": {
                            "show": True,
                            "fontSize": 16,
                            "fontWeight": "bold"
                        }
                    },
                    "data": [
                        {"value": revenue_data.get('room', 0), "name": "客房收入", "itemStyle": {"color": "#5470C6"}},
                        {"value": revenue_data.get('fb', 0), "name": "餐饮收入", "itemStyle": {"color": "#91CC75"}},
                        {"value": revenue_data.get('other', 0), "name": "其他收入", "itemStyle": {"color": "#FAC858"}}
                    ]
                }
            ]
        }
        
        return json.dumps(chart_config, ensure_ascii=False, indent=2)
    
    def generate_cost_trend(self, monthly_data: List[Dict]) -> str:
        """生成成本趋势图"""
        months = [d.get('month', '') for d in monthly_data]
        labor_costs = [d.get('labor', 0) for d in monthly_data]
        utility_costs = [d.get('utility', 0) for d in monthly_data]
        marketing_costs = [d.get('marketing', 0) for d in monthly_data]
        
        chart_config = {
            "title": {
                "text": "成本趋势分析",
                "left": "center"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"}
            },
            "legend": {
                "data": ["人工成本", "能耗成本", "市场营销费"],
                "bottom": 0
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "15%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": months
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"formatter": "¥{value}万"}
            },
            "series": [
                {
                    "name": "人工成本",
                    "type": "bar",
                    "stack": "total",
                    "data": labor_costs,
                    "itemStyle": {"color": "#5470C6"}
                },
                {
                    "name": "能耗成本",
                    "type": "bar",
                    "stack": "total",
                    "data": utility_costs,
                    "itemStyle": {"color": "#91CC75"}
                },
                {
                    "name": "市场营销费",
                    "type": "bar",
                    "stack": "total",
                    "data": marketing_costs,
                    "itemStyle": {"color": "#FAC858"}
                }
            ]
        }
        
        return json.dumps(chart_config, ensure_ascii=False, indent=2)
    
    def generate_profit_analysis(self) -> str:
        """生成利润分析瀑布图数据"""
        if 'profit' not in self.data:
            return "{}"
        
        profit_data = self.data['profit']
        
        # 瀑布图数据
        waterfall_data = [
            {"name": "营业收入", "value": profit_data.get('total_revenue', 0)},
            {"name": "人工成本", "value": -abs(profit_data.get('labor', 0))},
            {"name": "能耗成本", "value": -abs(profit_data.get('utility', 0))},
            {"name": "营销成本", "value": -abs(profit_data.get('marketing', 0))},
            {"name": "管理费用", "value": -abs(profit_data.get('admin', 0))},
            {"name": "其他费用", "value": -abs(profit_data.get('other', 0))},
            {"name": "GOP", "value": profit_data.get('gop', 0)},
        ]
        
        chart_config = {
            "title": {
                "text": "利润形成分析",
                "left": "center"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b}: ¥{c}万"
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "10%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": [d['name'] for d in waterfall_data],
                "axisLabel": {"rotate": 15}
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"formatter": "¥{value}万"}
            },
            "series": [
                {
                    "type": "bar",
                    "data": [d['value'] for d in waterfall_data],
                    "itemStyle": {
                        "color": lambda params: "#5470C6" if params.value >= 0 else "#EE6666"
                    },
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": lambda params: f"¥{params.value:,.0f}万"
                    }
                }
            ]
        }
        
        return json.dumps(chart_config, ensure_ascii=False, indent=2)
    
    def generate_breakeven_chart(self, 
                                  breakeven_occ: float,
                                  current_occ: float,
                                  adr: float) -> str:
        """生成保本点分析图"""
        chart_config = {
            "title": {
                "text": "保本点分析",
                "subtext": f"保本出租率: {breakeven_occ:.1f}% | 当前: {current_occ:.1f}%",
                "left": "center"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"}
            },
            "legend": {
                "data": ["收入线", "成本线", "当前点"],
                "bottom": 0
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "15%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": ["0%", "20%", "40%", "60%", "80%", "100%"],
                "name": "出租率"
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"formatter": "¥{value}万"},
                "name": "金额"
            },
            "series": [
                {
                    "name": "收入线",
                    "type": "line",
                    "data": [0, 200, 400, 600, 800, 1000],
                    "itemStyle": {"color": "#5470C6"},
                    "areaStyle": {"color": "rgba(84, 112, 198, 0.2)"}
                },
                {
                    "name": "成本线",
                    "type": "line",
                    "data": [350, 350, 350, 350, 350, 350],
                    "itemStyle": {"color": "#EE6666"},
                    "linestyle": {"type": "dashed"}
                },
                {
                    "name": "当前点",
                    "type": "scatter",
                    "data": [[f"{current_occ:.1f}%", current_occ * 10]],
                    "symbolSize": 20,
                    "itemStyle": {"color": "#91CC75"}
                }
            ]
        }
        
        return json.dumps(chart_config, ensure_ascii=False, indent=2)
    
    def export_all_charts(self, output_dir: str = "./charts"):
        """导出所有图表配置为JSON文件"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        files = {
            "kpi_dashboard.json": self.generate_kpi_dashboard(),
            "revenue_chart.json": self.generate_revenue_chart(),
            "profit_analysis.json": self.generate_profit_analysis(),
        }
        
        for filename, content in files.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已生成: {filepath}")
        
        return list(files.keys())


def demo():
    """演示示例"""
    visualizer = HotelPLVisualizer("杭州开元名都大酒店")
    
    # 添加收入数据
    visualizer.add_revenue_data({
        'total': 2185,
        'room': 1420,
        'fb': 580,
        'other': 185,
        'occ': 72.5,
        'adr': 658,
        'revpar': 477
    })
    
    # 添加成本数据
    visualizer.add_cost_data({
        'labor': 612,
        'utility': 87,
        'marketing': 98,
        'admin': 65,
        'maintenance': 44,
        'other': 98,
        'total': 1004
    })
    
    # 添加利润数据
    visualizer.add_profit_data({
        'total_revenue': 2185,
        'labor': 612,
        'utility': 87,
        'marketing': 98,
        'admin': 65,
        'other': 98,
        'gop': 728,
        'gop_margin': 33.3
    })
    
    # 生成KPI仪表盘
    print("=== KPI仪表盘 ===")
    print(visualizer.generate_kpi_dashboard())
    
    # 导出图表
    print("\n=== 导出图表 ===")
    files = visualizer.export_all_charts()
    print(f"已生成 {len(files)} 个图表配置")


if __name__ == "__main__":
    demo()
