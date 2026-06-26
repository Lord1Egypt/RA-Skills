#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Chart Generator - 数据可视化图表生成器
支持：折线图、柱状图、饼图、散点图、面积图、多系列对比图
"""

import argparse
import sys
import os
import json

# 使用 conda 环境中的 matplotlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))

import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt

# 配色方案
COLORS = {
    'blue': '#2196F3',
    'red': '#F44336',
    'green': '#4CAF50',
    'orange': '#FF9800',
    'purple': '#9C27B0',
    'cyan': '#00BCD4',
    'lime': '#CDDC39',
    'pink': '#E91E63',
    'teal': '#009688',
    'amber': '#FFC107'
}

COLOR_PALETTE = list(COLORS.values())

def parse_data(data_str):
    """解析数据字符串"""
    data_str = data_str.strip('[]').replace(' ', '')
    return [float(x) for x in data_str.split(',')]

def parse_labels(labels_str):
    """解析标签字符串"""
    labels_str = labels_str.strip('[]')
    if "'" in labels_str:
        return [x.strip().strip("'") for x in labels_str.split(',')]
    elif '"' in labels_str:
        return [x.strip().strip('"') for x in labels_str.split(',')]
    else:
        return [x.strip() for x in labels_str.split(',')]

def parse_datasets(datasets_json):
    """解析多系列数据集"""
    return json.loads(datasets_json)

def generate_line_chart(data, labels=None, title="Data Trend", output="/tmp/chart.png", 
                        width=10, height=6, color="#2196F3"):
    """生成折线图"""
    if labels is None:
        labels = [f'Day {i+1}' for i in range(len(data))]
    
    plt.figure(figsize=(width, height))
    plt.plot(labels, data, marker='o', linewidth=2, markersize=8, color=color)
    plt.fill_between(range(len(data)), data, alpha=0.3, color=color)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, max(data) * 1.2 if max(data) > 0 else 10)
    
    if len(labels) > 5:
        plt.xticks(rotation=45)
    
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output

def generate_bar_chart(data, labels=None, title="Data Overview", output="/tmp/chart.png",
                       width=10, height=6, color="#2196F3"):
    """生成柱状图"""
    if labels is None:
        labels = [f'Item {i+1}' for i in range(len(data))]
    
    plt.figure(figsize=(width, height))
    bars = plt.bar(range(len(data)), data, color=color, edgecolor='white', linewidth=1.5)
    
    # 在柱子上方添加数值标签
    for i, (bar, val) in enumerate(zip(bars, data)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(data)*0.01,
                f'{val:.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.xticks(range(len(data)), labels, rotation=45 if len(labels) > 5 else 0)
    plt.grid(True, alpha=0.3, axis='y')
    plt.ylim(0, max(data) * 1.2 if max(data) > 0 else 10)
    
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output

def generate_pie_chart(data, labels=None, title="Distribution", output="/tmp/chart.png",
                       width=8, height=8):
    """生成饼图"""
    if labels is None:
        labels = [f'Item {i+1}' for i in range(len(data))]
    
    # 如果数据太多，合并小项
    if len(data) > 10:
        sorted_indices = sorted(range(len(data)), key=lambda i: data[i], reverse=True)
        top_9 = sorted_indices[:9]
        others_sum = sum(data[i] for i in sorted_indices[9:])
        data = [data[i] for i in top_9] + [others_sum]
        labels = [labels[i] for i in top_9] + ['Others']
    
    plt.figure(figsize=(width, height))
    wedges, texts, autotexts = plt.pie(data, labels=labels, autopct='%1.1f%%',
                                        colors=COLOR_PALETTE[:len(data)],
                                        startangle=90, explode=[0.02]*len(data))
    
    # 美化字体
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output

def generate_scatter_chart(data_x, data_y, labels=None, title="Scatter Plot", 
                           output="/tmp/chart.png", width=10, height=6, color="#2196F3"):
    """生成散点图"""
    if labels is None:
        labels = [f'Point {i+1}' for i in range(len(data_x))]
    
    plt.figure(figsize=(width, height))
    plt.scatter(data_x, data_y, s=100, c=color, alpha=0.6, edgecolors='white', linewidth=2)
    
    # 添加点的标签
    for i, (x, y) in enumerate(zip(data_x, data_y)):
        plt.annotate(f'{i+1}', (x, y), textcoords="offset points", xytext=(5,5), 
                    fontsize=9, alpha=0.7)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('X Axis', fontsize=12)
    plt.ylabel('Y Axis', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output

def generate_area_chart(data, labels=None, title="Area Chart", output="/tmp/chart.png",
                        width=10, height=6, color="#2196F3"):
    """生成面积图"""
    if labels is None:
        labels = [f'Day {i+1}' for i in range(len(data))]
    
    plt.figure(figsize=(width, height))
    plt.fill_between(range(len(data)), data, alpha=0.7, color=color)
    plt.plot(labels, data, linewidth=2, color=color, marker='o', markersize=6)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, max(data) * 1.2 if max(data) > 0 else 10)
    
    if len(labels) > 5:
        plt.xticks(rotation=45)
    
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output

def generate_multi_line_chart(datasets, labels=None, title="Comparison", 
                              output="/tmp/chart.png", width=12, height=7):
    """生成多系列对比折线图"""
    if labels is None:
        # 假设所有数据集长度相同
        first_dataset = list(datasets.values())[0]
        labels = [f'Day {i+1}' for i in range(len(first_dataset))]
    
    plt.figure(figsize=(width, height))
    
    # 为每个数据集使用不同颜色
    colors = list(COLOR_PALETTE)
    
    for i, (name, data) in enumerate(datasets.items()):
        color = colors[i % len(colors)]
        plt.plot(labels, data, marker='o', linewidth=2, markersize=6, 
                label=name, color=color)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # 自动调整 y 轴范围
    all_values = [v for data in datasets.values() for v in data]
    plt.ylim(0, max(all_values) * 1.2 if max(all_values) > 0 else 10)
    
    if len(labels) > 5:
        plt.xticks(rotation=45)
    
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output

def generate_bar_compare_chart(datasets, labels=None, title="Comparison", 
                               output="/tmp/chart.png", width=12, height=7):
    """生成多系列对比柱状图"""
    if labels is None:
        first_dataset = list(datasets.values())[0]
        labels = [f'Item {i+1}' for i in range(len(first_dataset))]
    
    plt.figure(figsize=(width, height))
    
    n_series = len(datasets)
    n_items = len(list(datasets.values())[0])
    bar_width = 0.8 / n_series
    colors = list(COLOR_PALETTE)
    
    for i, (name, data) in enumerate(datasets.items()):
        offset = (i - n_series/2 + 0.5) * bar_width
        color = colors[i % len(colors)]
        bars = plt.bar([j + offset for j in range(n_items)], data, 
                      bar_width, label=name, color=color, edgecolor='white', linewidth=1)
        
        # 添加数值标签
        for j, (bar, val) in enumerate(zip(bars, data)):
            if val > 0:
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(data)*0.01,
                        f'{val:.1f}', ha='center', va='bottom', fontsize=8)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.xticks([j + 0.4 - bar_width/2 for j in range(n_items)], labels, 
               rotation=45 if len(labels) > 5 else 0)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    
    all_values = [v for data in datasets.values() for v in data]
    plt.ylim(0, max(all_values) * 1.2 if max(all_values) > 0 else 10)
    
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output

def main():
    parser = argparse.ArgumentParser(description="数据可视化图表生成器")
    parser.add_argument("--data", help="数据数组，如：[2,4,3,7,8,8]")
    parser.add_argument("--data-x", help="散点图 X 轴数据")
    parser.add_argument("--data-y", help="散点图 Y 轴数据")
    parser.add_argument("--datasets", help="多系列数据 JSON，如：{\"系列 1\":[1,2,3],\"系列 2\":[4,5,6]}")
    parser.add_argument("--labels", help="X 轴标签，如：['周一','周二','周三']")
    parser.add_argument("--type", "-t", default="line", 
                       choices=["line", "bar", "pie", "scatter", "area", "multi-line", "bar-compare"],
                       help="图表类型")
    parser.add_argument("--title", default="Data Chart", help="图表标题")
    parser.add_argument("--output", default="/tmp/chart.png", help="输出文件路径")
    parser.add_argument("--width", type=float, default=10, help="图表宽度（英寸）")
    parser.add_argument("--height", type=float, default=6, help="图表高度（英寸）")
    parser.add_argument("--color", default="#2196F3", help="颜色（hex）")
    
    args = parser.parse_args()
    
    output = None
    
    try:
        if args.type == "line":
            data = parse_data(args.data)
            labels = parse_labels(args.labels) if args.labels else None
            output = generate_line_chart(data, labels, args.title, args.output, 
                                        args.width, args.height, args.color)
        
        elif args.type == "bar":
            data = parse_data(args.data)
            labels = parse_labels(args.labels) if args.labels else None
            output = generate_bar_chart(data, labels, args.title, args.output,
                                       args.width, args.height, args.color)
        
        elif args.type == "pie":
            data = parse_data(args.data)
            labels = parse_labels(args.labels) if args.labels else None
            output = generate_pie_chart(data, labels, args.title, args.output,
                                       args.width, args.height)
        
        elif args.type == "scatter":
            data_x = parse_data(args.data_x)
            data_y = parse_data(args.data_y)
            labels = parse_labels(args.labels) if args.labels else None
            output = generate_scatter_chart(data_x, data_y, labels, args.title,
                                           args.output, args.width, args.height, args.color)
        
        elif args.type == "area":
            data = parse_data(args.data)
            labels = parse_labels(args.labels) if args.labels else None
            output = generate_area_chart(data, labels, args.title, args.output,
                                        args.width, args.height, args.color)
        
        elif args.type == "multi-line":
            datasets = parse_datasets(args.datasets)
            labels = parse_labels(args.labels) if args.labels else None
            output = generate_multi_line_chart(datasets, labels, args.title,
                                              args.output, args.width, args.height)
        
        elif args.type == "bar-compare":
            datasets = parse_datasets(args.datasets)
            labels = parse_labels(args.labels) if args.labels else None
            output = generate_bar_compare_chart(datasets, labels, args.title,
                                               args.output, args.width, args.height)
        
        print(f"✅ 图表已生成：{output}")
        return 0
        
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
