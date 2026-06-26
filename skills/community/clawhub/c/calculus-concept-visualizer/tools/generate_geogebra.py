#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeoGebra 动态演示生成器
作者: 代国兴
功能: 生成可交互的数学概念可视化
"""

import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class GeoGebraConfig:
    """GeoGebra 配置类"""
    concept: str
    function: str
    params: Dict
    interactive_elements: List[Dict]

class GeoGebraGenerator:
    """生成 GeoGebra 动态演示"""

    def __init__(self):
        self.templates = {
            "limit_epsilon_delta": self._limit_epsilon_delta,
            "derivative_definition": self._derivative_definition,
            "integral_riemann": self._integral_riemann,
            "taylor_approximation": self._taylor_approximation,
            "continuity_types": self._continuity_types
        }

    def generate(self, concept: str, params: Dict) -> Dict:
        """生成指定概念的 GeoGebra 配置"""
        if concept in self.templates:
            return self.templates[concept](params)
        return self._generic_visualization(concept, params)

    def _limit_epsilon_delta(self, params: Dict) -> Dict:
        """
        ε-δ 极限定义的动态演示
        核心交互: 学生拖动 ε，观察 δ 的变化
        """
        function = params.get("function", "sin(x)/x")
        point = params.get("point", 0)
        limit_val = params.get("limit", 1)

        return {
            "type": "geogebra",
            "appName": "classic",
            "width": 900,
            "height": 650,
            "showToolBar": False,
            "enableShiftDragZoom": True,
            "showResetIcon": True,

            "parameters": {
                "epsilon": {
                    "type": "slider",
                    "min": 0.01,
                    "max": 1.0,
                    "increment": 0.01,
                    "default": 0.5,
                    "label": "ε (误差范围)",
                    "position": [10, 10]
                },
                "delta": {
                    "type": "slider",
                    "min": 0.001,
                    "max": 2.0,
                    "increment": 0.001,
                    "default": 0.3,
                    "label": "δ (自变量范围)",
                    "dependent": True,
                    "formula": "epsilon / 2"  # 自动计算建议值
                },
                "show_proof": {
                    "type": "boolean",
                    "default": False,
                    "label": "显示证明过程"
                }
            },

            "elements": [
                {
                    "type": "function",
                    "expression": function,
                    "color": "#2196F3",
                    "lineWidth": 3,
                    "domain": [-5, 5]
                },
                {
                    "type": "point",
                    "x": point,
                    "y": limit_val,
                    "color": "#FF5722",
                    "size": 6,
                    "label": "L"
                },
                {
                    "type": "interval",
                    "axis": "y",
                    "low": f"{limit_val} - epsilon",
                    "high": f"{limit_val} + epsilon",
                    "color": "#FF5722",
                    "opacity": 0.15,
                    "label": "目标误差带 (L±ε)"
                },
                {
                    "type": "interval",
                    "axis": "x",
                    "low": f"{point} - delta",
                    "high": f"{point} + delta",
                    "color": "#4CAF50",
                    "opacity": 0.15,
                    "label": "自变量范围 (a±δ)"
                },
                {
                    "type": "text",
                    "content": "任务：拖动 ε 滑块，然后调整 δ 使函数图像完全落在红色区域内",
                    "position": [50, 30],
                    "fontSize": 14,
                    "color": "#333"
                }
            ],

            "validation": {
                "check": f"abs({function.replace('x', '(x)')} - {limit_val}) < epsilon",
                "domain": [f"{point} - delta", f"{point} + delta"],
                "feedback": {
                    "success": {
                        "message": "✓ 完美！当前 δ 满足 ε-δ 条件",
                        "color": "#4CAF50",
                        "action": "highlight_interval"
                    },
                    "failure": {
                        "message": "✗ 需要调整 δ，确保函数值全部落在红色误差带内",
                        "color": "#FF5722",
                        "hint": "尝试减小 δ 的值"
                    }
                }
            },

            "tutorial_steps": [
                {"step": 1, "action": "set_epsilon", "value": 0.5, "description": "第一步：设定误差范围 ε"},
                {"step": 2, "action": "adjust_delta", "target": "epsilon/2", "description": "第二步：寻找合适的 δ"},
                {"step": 3, "action": "verify", "description": "第三步：验证 |f(x)-L|<ε"}
            ]
        }

    def _derivative_definition(self, params: Dict) -> Dict:
        """导数定义：割线→切线的演变动画"""
        function = params.get("function", "x^2")
        point = params.get("point", 1)

        return {
            "type": "geogebra",
            "appName": "classic",
            "width": 800,
            "height": 600,
            "animation": {
                "sequence": [
                    {
                        "step": 1,
                        "description": "固定点 P",
                        "elements": ["point_p", "tangent_preview"],
                        "duration": 1000
                    },
                    {
                        "step": 2,
                        "description": "移动割线点 Q 靠近 P",
                        "animate": {
                            "element": "point_q",
                            "property": "x",
                            "from": 3,
                            "to": f"{point} + 0.01",
                            "duration": 3000
                        }
                    },
                    {
                        "step": 3,
                        "description": "观察 Δx→0 时割线斜率变化",
                        "show_trace": "secant_line",
                        "display_values": ["delta_x", "delta_y", "slope"]
                    },
                    {
                        "step": 4,
                        "description": "极限位置：割线变为切线",
                        "highlight": "tangent_line",
                        "show_formula": "f\'(x) = lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x}"
                    }
                ],
                "controls": ["play", "pause", "reset", "step_forward", "step_backward"]
            },

            "interactive": {
                "draggable": ["point_q"],
                "constraints": {
                    "point_q": {"min_x": -5, "max_x": 5, "exclude": [point]}
                },
                "real_time_display": {
                    "secant_slope": "(y_q - y_p) / (x_q - x_p)",
                    "delta_x": "x_q - x_p",
                    "delta_y": "y_q - y_p"
                }
            },

            "elements": [
                {
                    "type": "function",
                    "expression": function,
                    "color": "#1976D2",
                    "lineWidth": 2
                },
                {
                    "type": "point",
                    "x": point,
                    "y": f"{function.replace('x', str(point))}",
                    "label": "P",
                    "color": "#D32F2F",
                    "size": 7
                },
                {
                    "type": "point",
                    "x": 3,
                    "y": f"{function.replace('x', '3')}",
                    "label": "Q",
                    "color": "#388E3C",
                    "size": 7,
                    "draggable": True
                },
                {
                    "type": "line",
                    "type_line": "secant",
                    "through": ["P", "Q"],
                    "color": "#757575",
                    "style": "dashed"
                },
                {
                    "type": "tangent",
                    "at": "P",
                    "color": "#D32F2F",
                    "lineWidth": 3,
                    "show_equation": True
                }
            ]
        }

    def _integral_riemann(self, params: Dict) -> Dict:
        """黎曼和动态构建"""
        function = params.get("function", "x^2")
        a = params.get("a", 0)
        b = params.get("b", 2)

        return {
            "type": "geogebra",
            "appName": "classic",
            "width": 900,
            "height": 600,
            "parameters": {
                "n": {
                    "type": "slider",
                    "min": 1,
                    "max": 100,
                    "increment": 1,
                    "default": 4,
                    "label": "分割份数 n"
                },
                "method": {
                    "type": "dropdown",
                    "options": ["left", "right", "midpoint", "trapezoid"],
                    "default": "left",
                    "label": "取点方法"
                }
            },

            "elements": [
                {
                    "type": "function",
                    "expression": function,
                    "color": "#1976D2",
                    "domain": [a, b]
                },
                {
                    "type": "riemann_sum",
                    "function": function,
                    "interval": [a, b],
                    "n": "n",
                    "method": "method",
                    "fill_color": "#4CAF50",
                    "fill_opacity": 0.3,
                    "show_area_value": True
                }
            ],

            "animation": {
                "sequence": [
                    {"step": 1, "n": 1, "description": "n=1：粗略估计"},
                    {"step": 2, "n": 4, "description": "n=4：改进估计"},
                    {"step": 3, "n": 20, "description": "n=20：接近精确值"},
                    {"step": 4, "n": 100, "description": "n=100：极限思想"}
                ]
            },

            "real_time_display": {
                "riemann_sum": "计算当前分割的近似值",
                "exact_integral": "精确积分值",
                "error": "误差分析"
            }
        }

    def _taylor_approximation(self, params: Dict) -> Dict:
        """泰勒展开逐步逼近"""
        function = params.get("function", "sin(x)")
        center = params.get("center", 0)

        return {
            "type": "geogebra",
            "parameters": {
                "order": {
                    "type": "slider",
                    "min": 1,
                    "max": 10,
                    "increment": 1,
                    "default": 1,
                    "label": "泰勒阶数 n"
                },
                "x_range": {
                    "type": "slider",
                    "min": 0.1,
                    "max": 5,
                    "increment": 0.1,
                    "default": 3,
                    "label": "观察范围"
                }
            },

            "elements": [
                {
                    "type": "function",
                    "expression": function,
                    "color": "#1976D2",
                    "lineWidth": 3,
                    "label": "原函数 f(x)"
                },
                {
                    "type": "taylor_polynomial",
                    "function": function,
                    "center": center,
                    "order": "order",
                    "color": "#D32F2F",
                    "lineWidth": 2,
                    "style": "dashed",
                    "label": "Pn(x)"
                },
                {
                    "type": "error_band",
                    "function": function,
                    "approximation": "taylor",
                    "color": "#FF9800",
                    "opacity": 0.2
                }
            ],

            "display": {
                "taylor_formula": True,
                "remainder_term": True,
                "convergence_radius": True
            }
        }

    def _continuity_types(self, params: Dict) -> Dict:
        """连续性与间断点类型对比"""
        return {
            "type": "geogebra",
            "comparison_mode": True,
            "scenes": [
                {
                    "name": "连续",
                    "function": "x^2",
                    "description": "极限值 = 函数值"
                },
                {
                    "name": "可去间断",
                    "function": "(x^2-1)/(x-1)",
                    "hole_at": 1,
                    "description": "极限存在 ≠ 函数值（或函数值不存在）"
                },
                {
                    "name": "跳跃间断",
                    "function": "floor(x)",
                    "jump_at": 1,
                    "description": "左右极限存在但不相等"
                },
                {
                    "name": "无穷间断",
                    "function": "1/x",
                    "asymptote_at": 0,
                    "description": "极限为无穷大"
                }
            ]
        }

    def _generic_visualization(self, concept: str, params: Dict) -> Dict:
        """通用可视化模板"""
        return {
            "type": "geogebra",
            "message": f"概念 '{concept}' 的专用可视化正在开发中，使用通用模板",
            "elements": [
                {
                    "type": "text",
                    "content": f"正在可视化: {concept}",
                    "position": [10, 10]
                }
            ]
        }

# 导出函数供 OpenClaw 调用
def generate_geogebra(concept: str, **params) -> str:
    """生成 GeoGebra 配置的入口函数"""
    generator = GeoGebraGenerator()
    config = generator.generate(concept, params)
    return json.dumps(config, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试生成
    print(generate_geogebra("limit_epsilon_delta", function="sin(x)/x", point=0, limit=1))
