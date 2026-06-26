#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 交互式可视化生成器
作者: 代国兴
功能: 使用 matplotlib/plotly 生成交互式图表
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import BytesIO
from typing import Dict, List

class InteractivePlotter:
    """生成交互式数学可视化"""

    def __init__(self):
        self.backend = "matplotlib"  # 或 "plotly"

    def generate(self, plot_type: str, params: Dict) -> str:
        """生成可视化并返回 base64 编码或配置"""
        if plot_type == "limit_demonstration":
            return self._plot_limit_demonstration(params)
        elif plot_type == "derivative_animation":
            return self._plot_derivative_animation(params)
        elif plot_type == "riemann_sum":
            return self._plot_riemann_sum(params)
        elif plot_type == "taylor_comparison":
            return self._plot_taylor_comparison(params)
        elif plot_type == "error_analysis":
            return self._plot_error_analysis(params)
        else:
            return self._generic_plot(params)

    def _plot_limit_demonstration(self, params: Dict) -> str:
        """ε-δ 极限演示图"""
        fig, ax = plt.subplots(figsize=(10, 6))

        function_str = params.get("function", "np.sin(x)/x")
        a = params.get("point", 0)
        L = params.get("limit", 1)
        epsilon = params.get("epsilon", 0.5)
        delta = params.get("delta", 0.5)

        # 定义函数
        x = np.linspace(a-2, a+2, 1000)
        x = x[x != a]  # 排除间断点

        try:
            f = eval(f"lambda x: {function_str}")
            y = f(x)
        except:
            y = np.sin(x)/x
            y[x == 0] = 1

        # 绘制函数
        ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {function_str}')

        # 绘制极限点
        ax.plot(a, L, 'ro', markersize=10, label=f'L = {L}')

        # 绘制 ε-带状区域
        ax.axhspan(L-epsilon, L+epsilon, alpha=0.2, color='red', label=f'L ± ε (ε={epsilon})')

        # 绘制 δ-区间
        ax.axvspan(a-delta, a+delta, alpha=0.2, color='green', label=f'a ± δ (δ={delta})')

        # 绘制虚线框
        rect = plt.Rectangle((a-delta, L-epsilon), 2*delta, 2*epsilon, 
                            fill=False, edgecolor='purple', linestyle='--', linewidth=2)
        ax.add_patch(rect)

        # 验证区域
        mask = (np.abs(x - a) < delta) & (np.abs(x - a) > 0)
        if np.any(mask):
            y_in_range = y[mask]
            violation = np.any(np.abs(y_in_range - L) >= epsilon)
            color = 'red' if violation else 'green'
            status = '不满足' if violation else '满足'
            ax.text(0.05, 0.95, f'ε-δ 条件: {status}', 
                   transform=ax.transAxes, fontsize=14, 
                   bbox=dict(boxstyle='round', facecolor=color, alpha=0.3),
                   verticalalignment='top')

        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('f(x)', fontsize=12)
        ax.set_title(f'ε-δ 极限定义演示: lim(x→{a}) f(x) = {L}', fontsize=14)
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(L-2*epsilon, L+2*epsilon)

        # 保存为 base64
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return json.dumps({
            "type": "image",
            "format": "base64_png",
            "data": img_base64,
            "description": f"ε-δ 定义可视化: ε={epsilon}, δ={delta}"
        })

    def _plot_derivative_animation(self, params: Dict) -> str:
        """导数定义的帧序列"""
        function_str = params.get("function", "x**2")
        a = params.get("point", 1)

        # 生成帧数据
        h_values = np.logspace(-1, -4, 20)
        frames = []

        for h in h_values:
            fig, ax = plt.subplots(figsize=(8, 6))

            x = np.linspace(-2, 4, 200)
            f = eval(f"lambda x: {function_str}")
            y = f(x)

            ax.plot(x, y, 'b-', linewidth=2, label='f(x)')
            ax.plot(a, f(a), 'ro', markersize=10, label='P')

            # 割线
            if h > 0:
                x_q = a + h
                y_q = f(x_q)
                ax.plot(x_q, y_q, 'go', markersize=8, label='Q')
                ax.plot([a, x_q], [f(a), y_q], 'g--', linewidth=2, label='割线')

                slope = (y_q - f(a)) / h
                ax.text(0.05, 0.95, f'h = {h:.4f}\n割线斜率 = {slope:.4f}',
                       transform=ax.transAxes, fontsize=11,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       verticalalignment='top')

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('割线→切线的演变过程')
            ax.legend()
            ax.grid(True, alpha=0.3)

            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()

            frames.append({
                "h": float(h),
                "image": img_base64
            })

        return json.dumps({
            "type": "animation",
            "frames": frames,
            "description": "割线斜率随 h→0 的演变过程",
            "final_slope": f"导数 f'({a}) = 极限值"
        })

    def _plot_riemann_sum(self, params: Dict) -> str:
        """黎曼和可视化"""
        function_str = params.get("function", "x**2")
        a = params.get("a", 0)
        b = params.get("b", 2)
        n = params.get("n", 10)
        method = params.get("method", "left")

        fig, ax = plt.subplots(figsize=(10, 6))

        f = eval(f"lambda x: {function_str}")

        # 绘制函数
        x_smooth = np.linspace(a, b, 200)
        ax.plot(x_smooth, f(x_smooth), 'b-', linewidth=2, label='f(x)')

        # 绘制矩形
        dx = (b - a) / n
        total_area = 0

        for i in range(n):
            x_left = a + i * dx
            x_right = a + (i + 1) * dx

            if method == "left":
                x_val = x_left
            elif method == "right":
                x_val = x_right
            else:  # midpoint
                x_val = (x_left + x_right) / 2

            height = f(x_val)
            total_area += height * dx

            color = 'green' if height >= 0 else 'red'
            ax.bar(x_val, height, width=dx, alpha=0.3, color=color, edgecolor='black')

        # 计算精确值对比
        from scipy import integrate
        exact, _ = integrate.quad(f, a, b)

        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'黎曼和近似 (n={n}, {method} endpoint)\n近似值: {total_area:.4f}, 精确值: {exact:.4f}')
        ax.legend()
        ax.grid(True, alpha=0.3)

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return json.dumps({
            "type": "image",
            "format": "base64_png",
            "data": img_base64,
            "approximation": total_area,
            "exact": exact,
            "error": abs(total_area - exact)
        })

    def _plot_taylor_comparison(self, params: Dict) -> str:
        """泰勒展开对比图"""
        function_str = params.get("function", "np.sin(x)")
        center = params.get("center", 0)
        max_order = params.get("max_order", 5)

        fig, ax = plt.subplots(figsize=(10, 6))

        x = np.linspace(-np.pi, np.pi, 200)

        try:
            f = eval(f"lambda x: {function_str}")
            y_exact = f(x)
        except:
            y_exact = np.sin(x)

        ax.plot(x, y_exact, 'k-', linewidth=3, label='f(x) = sin(x)')

        # 计算各阶泰勒展开
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for n in range(1, max_order + 1, 2):  # 奇数阶
            y_taylor = self._taylor_sin(x, center, n)
            ax.plot(x, y_taylor, '--', color=colors[(n-1)//2 % len(colors)], 
                   linewidth=2, label=f'P_{n}(x)')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'泰勒多项式逼近 (在 x={center} 处展开)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-2, 2)

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return json.dumps({
            "type": "image",
            "format": "base64_png",
            "data": img_base64
        })

    def _taylor_sin(self, x, center, n):
        """计算 sin(x) 的 n 阶泰勒展开"""
        result = 0
        for k in range((n+1)//2):
            term = ((-1)**k) * (x - center)**(2*k+1) / np.math.factorial(2*k+1)
            result += term
        return result

    def _plot_error_analysis(self, params: Dict) -> str:
        """误差分析图"""
        # 实现略
        return json.dumps({"type": "placeholder"})

    def _generic_plot(self, params: Dict) -> str:
        """通用绘图"""
        return json.dumps({"type": "generic", "message": "通用绘图功能"})

def plot_interactive(plot_type: str, **params) -> str:
    """供 OpenClaw 调用的入口函数"""
    plotter = InteractivePlotter()
    return plotter.generate(plot_type, params)

if __name__ == "__main__":
    # 测试
    print(plot_interactive("limit_demonstration", function="np.sin(x)/x", point=0, limit=1, epsilon=0.5, delta=0.3)[:200] + "...")
