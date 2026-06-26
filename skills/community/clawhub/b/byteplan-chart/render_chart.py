#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BytePlan Chart Renderer - Matplotlib 版本
功能：使用 matplotlib 渲染 AntV 格式的图表数据
支持：Line, Column, Bar, Area, Pie, Rose, Scatter, Box, Heatmap 等

用法：
    uv run python render_chart.py <antv_json> <output_path>

依赖：
    uv pip install matplotlib numpy
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Windows 命令行编码兼容
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# ==================== 字体检测与配置 ====================

def setup_chinese_fonts():
    """
    检测并配置中文字体
    解决 matplotlib 中文显示问题
    """
    import matplotlib.font_manager as fm
    from matplotlib import rcParams
    
    print("🔍 检测系统中文字体...")
    
    # 常见中文字体映射（按优先级）
    font_candidates = {
        'win32': [
            'Microsoft YaHei',      # 微软雅黑
            'SimHei',               # 黑体
            'SimSun',               # 宋体
            'KaiTi',                # 楷体
        ],
        'darwin': [
            'PingFang SC',          # 苹方
            'Heiti SC',             # 黑体 - 简
            'STHeiti',              # 华文黑体
        ],
        'linux': [
            'WenQuanYi Zen Hei',    # 文泉驿正黑
            'WenQuanYi Micro Hei',  # 文泉驿微米黑
            'Noto Sans CJK SC',     # Noto Sans CJK
        ],
    }
    
    platform = sys.platform
    candidates = font_candidates.get(platform, [])
    
    # 获取系统可用字体
    available_fonts = set()
    for font in fm.fontManager.ttflist:
        available_fonts.add(font.name)
    
    # 查找可用的中文字体
    found_font = None
    for candidate in candidates:
        if candidate in available_fonts:
            found_font = candidate
            print(f"✅ 找到中文字体：{candidate}")
            break
    
    if found_font:
        # 配置 matplotlib 使用找到的字体
        rcParams['font.sans-serif'] = [found_font] + rcParams['font.sans-serif']
        rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        print(f"✅ 字体配置成功：{found_font}")
        return True
    else:
        print("⚠️ 未找到系统预装中文字体")
        print("💡 如遇到中文乱码，请安装中文字体后重试")
        print("\nLinux 安装字体:")
        print("  Ubuntu/Debian: sudo apt-get install fonts-wqy-zenhei fonts-noto-cjk")
        print("  CentOS/RHEL: sudo yum install wqy-zenhei-fonts google-noto-sans-cjk-fonts")
        return False


# ==================== 图表绘制函数 ====================

def draw_line(data, config, output_path, safe_font=True):
    """绘制折线图"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    
    x_data = [str(item[x_field]) for item in data]
    y_data = [item[y_field] for item in data]
    
    ax.plot(x_data, y_data, marker='o', linewidth=2, markersize=6, color='#5B8FF9')
    
    # 添加数值标签
    for i, (x, y) in enumerate(zip(x_data, y_data)):
        ax.annotate(f'{y}', xy=(x, y), xytext=(0, 5), 
                   textcoords='offset points', ha='center', fontsize=9)
    
    ax.set_title(config.get('title', '折线图'), fontsize=14, fontweight='bold')
    ax.set_xlabel(x_field, fontsize=11)
    ax.set_ylabel(y_field, fontsize=11)
    
    # 旋转 x 轴标签
    plt.xticks(rotation=45, ha='right')
    
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_column(data, config, output_path, safe_font=True):
    """绘制柱状图（支持分组/堆叠）"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    group_field = config.get('groupField')
    is_stack = config.get('isStack', False)
    
    colors = ['#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E8684A', '#6DC8EC', '#945FB9', '#FF9845']
    
    if group_field:
        # 分组或堆叠柱状图
        groups = list(set(item[group_field] for item in data))
        categories = list(set(item[x_field] for item in data))
        
        if is_stack:
            # 堆叠柱状图
            bottom = np.zeros(len(categories))
            for i, group in enumerate(groups):
                values = [next((item[y_field] for item in data if item[x_field] == cat and item[group_field] == group), 0) 
                         for cat in categories]
                ax.bar(categories, values, bottom=bottom, label=group, color=colors[i % len(colors)])
                bottom += np.array(values)
        else:
            # 分组柱状图
            x = np.arange(len(categories))
            width = 0.8 / len(groups)
            for i, group in enumerate(groups):
                values = [next((item[y_field] for item in data if item[x_field] == cat and item[group_field] == group), 0) 
                         for cat in categories]
                offset = (i - len(groups) / 2 + 0.5) * width
                ax.bar(x + offset, values, width, label=group, color=colors[i % len(colors)])
            ax.set_xticks(x)
            ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
    else:
        # 普通柱状图
        x_data = [str(item[x_field]) for item in data]
        y_data = [item[y_field] for item in data]
        
        bars = ax.bar(x_data, y_data, color=colors[:len(data)])
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords='offset points',
                       ha='center', va='bottom', fontsize=9)
        
        plt.xticks(rotation=45, ha='right')
    
    ax.set_title(config.get('title', '柱状图'), fontsize=14, fontweight='bold')
    ax.set_ylabel(y_field, fontsize=11)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_bar(data, config, output_path, safe_font=True):
    """绘制条形图"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    
    x_data = [str(item[x_field]) for item in data]
    y_data = [item[y_field] for item in data]
    
    colors = ['#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E8684A', '#6DC8EC', '#945FB9', '#FF9845']
    
    bars = ax.barh(x_data, y_data, color=colors[:len(data)])
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{int(width)}',
                   xy=(width, bar.get_y() + bar.get_height() / 2),
                   xytext=(3, 0), textcoords='offset points',
                   va='center', fontsize=9)
    
    ax.set_title(config.get('title', '条形图'), fontsize=14, fontweight='bold')
    ax.set_xlabel(y_field, fontsize=11)
    ax.grid(True, alpha=0.3, axis='x', linestyle='--')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_pie(data, config, output_path, safe_font=True, is_rose=False):
    """绘制饼图/玫瑰图"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    
    labels = [str(item[x_field]) for item in data]
    sizes = [item[y_field] for item in data]
    
    colors = ['#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E8684A', '#6DC8EC', '#945FB9', '#FF9845']
    
    # 突出显示最大值
    explode = [0.05 if size == max(sizes) else 0 for size in sizes]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                       colors=colors, explode=explode, startangle=90)
    
    # 设置字体大小
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title(config.get('title', '饼图'), fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_scatter(data, config, output_path, safe_font=True):
    """绘制散点图"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    
    x_data = [item[x_field] for item in data]
    y_data = [item[y_field] for item in data]
    
    ax.scatter(x_data, y_data, c='#5B8FF9', alpha=0.6, s=100, edgecolors='white', linewidth=1.5)
    
    ax.set_title(config.get('title', '散点图'), fontsize=14, fontweight='bold')
    ax.set_xlabel(x_field, fontsize=11)
    ax.set_ylabel(y_field, fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_area(data, config, output_path, safe_font=True):
    """绘制面积图"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    
    x_data = [str(item[x_field]) for item in data]
    y_data = [item[y_field] for item in data]
    
    ax.fill_between(x_data, y_data, alpha=0.3, color='#5B8FF9')
    ax.plot(x_data, y_data, linewidth=2, color='#5B8FF9', marker='o', markersize=6)
    
    ax.set_title(config.get('title', '面积图'), fontsize=14, fontweight='bold')
    ax.set_xlabel(x_field, fontsize=11)
    ax.set_ylabel(y_field, fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_heatmap(data, config, output_path, safe_font=True):
    """绘制热力图"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    value_field = config.get('valueField', list(data[0].keys())[2])
    
    # 构建矩阵
    x_categories = list(set(item[x_field] for item in data))
    y_categories = list(set(item[y_field] for item in data))
    
    matrix = np.zeros((len(y_categories), len(x_categories)))
    for item in data:
        x_idx = x_categories.index(item[x_field])
        y_idx = y_categories.index(item[y_field])
        matrix[y_idx, x_idx] = item[value_field]
    
    # 绘制热力图
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    # 添加数值标签
    for i in range(len(y_categories)):
        for j in range(len(x_categories)):
            text = ax.text(j, i, f'{int(matrix[i, j])}',
                          ha='center', va='center', color='black', fontsize=9)
    
    ax.set_xticks(np.arange(len(x_categories)))
    ax.set_yticks(np.arange(len(y_categories)))
    ax.set_xticklabels(x_categories, rotation=45, ha='right')
    ax.set_yticklabels(y_categories)
    
    ax.set_title(config.get('title', '热力图'), fontsize=14, fontweight='bold')
    
    # 添加颜色条
    plt.colorbar(im, ax=ax, label=value_field)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_dual_axis(data, config, output_path, safe_font=True):
    """绘制双轴图（柱状图 + 折线图组合）"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field1 = config.get('yField1', list(data[0].keys())[1])
    y_field2 = config.get('yField2', list(data[0].keys())[2])
    
    x_data = [str(item[x_field]) for item in data]
    y1_data = [item[y_field1] for item in data]
    y2_data = [item[y_field2] for item in data]
    
    # 第一个 Y 轴（左侧）- 柱状图
    color1 = '#5B8FF9'
    ax1.set_xlabel(x_field, fontsize=11)
    ax1.set_ylabel(y_field1, color=color1, fontsize=11)
    bars = ax1.bar(x_data, y1_data, color=color1, alpha=0.7, label=y_field1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xticklabels(x_data, rotation=45, ha='right')
    
    # 添加数值标签（柱状图）
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8, color=color1)
    
    # 第二个 Y 轴（右侧）- 折线图
    ax2 = ax1.twinx()
    color2 = '#E8684A'
    ax2.set_ylabel(y_field2, color=color2, fontsize=11)
    line = ax2.plot(x_data, y2_data, color=color2, marker='o', 
                   linewidth=2, markersize=6, label=y_field2)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # 添加数值标签（折线图）
    for i, (x, y) in enumerate(zip(x_data, y2_data)):
        ax2.annotate(f'{y}', xy=(i, y), xytext=(0, 5),
                    textcoords='offset points', ha='center',
                    fontsize=8, color=color2)
    
    # 标题
    plt.title(config.get('title', '双轴图'), fontsize=14, fontweight='bold')
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_box(data, config, output_path, safe_font=True):
    """绘制箱型图"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    x_field = config.get('xField', list(data[0].keys())[0])
    y_field = config.get('yField', list(data[0].keys())[1])
    
    # 按 X 字段分组
    groups = {}
    for item in data:
        x_val = str(item.get(x_field, 'All'))
        y_val = item.get(y_field, 0)
        if x_val not in groups:
            groups[x_val] = []
        groups[x_val].append(y_val)
    
    # 准备数据
    data_to_plot = [groups[k] for k in sorted(groups.keys())]
    labels = sorted(groups.keys())
    
    # 绘制箱型图
    bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                    boxprops=dict(facecolor='#5B8FF9', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2),
                    whiskerprops=dict(color='gray', linewidth=1.5),
                    capprops=dict(color='gray', linewidth=1.5))
    
    ax.set_title(config.get('title', '箱型图'), fontsize=14, fontweight='bold')
    ax.set_ylabel(y_field, fontsize=11)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_detail_table(data, config, output_path, safe_font=True):
    """绘制明细表"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
    ax.axis('tight')
    ax.axis('off')
    
    # 获取字段
    fields = config.get('fields', list(data[0].keys()))
    
    # 准备表格数据
    table_data = []
    for item in data:
        row = [str(item.get(field, '')) for field in fields]
        table_data.append(row)
    
    # 创建表格
    table = ax.table(cellText=table_data,
                    colLabels=fields,
                    cellLoc='center',
                    loc='center',
                    colColours=['#5B8FF9'] * len(fields))
    
    # 设置表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)
    
    # 设置表头样式
    for i in range(len(fields)):
        table[(0, i)].set_facecolor('#5B8FF9')
        table[(0, i)].set_text_props(color='white', fontweight='bold')
    
    # 设置交替行颜色
    for i in range(1, len(table_data) + 1):
        for j in range(len(fields)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f8f9fa')
            else:
                table[(i, j)].set_facecolor('white')
    
    ax.set_title(config.get('title', '明细表'), fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def draw_pivot_table(data, config, output_path, safe_font=True):
    """绘制透视表"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
    ax.axis('tight')
    ax.axis('off')
    
    row_field = config.get('rowField', list(data[0].keys())[0])
    col_field = config.get('colField', list(data[0].keys())[1])
    value_field = config.get('valueField', list(data[0].keys())[2])
    
    # 构建透视数据
    rows = sorted(set(item[row_field] for item in data))
    cols = sorted(set(item[col_field] for item in data))
    
    # 创建矩阵
    matrix = [[''] * (len(cols) + 1) for _ in range(len(rows) + 1)]
    matrix[0][0] = row_field + '\\' + col_field
    
    # 填充表头
    for j, col in enumerate(cols):
        matrix[0][j + 1] = str(col)
    
    # 填充行头和数值
    for i, row in enumerate(rows):
        matrix[i + 1][0] = str(row)
        for j, col in enumerate(cols):
            item = next((d for d in data if d[row_field] == row and d[col_field] == col), None)
            matrix[i + 1][j + 1] = str(item[value_field]) if item else ''
    
    # 创建表格
    table = ax.table(cellText=matrix,
                    cellLoc='center',
                    loc='center',
                    colColours=['#5B8FF9'] * (len(cols) + 1))
    
    # 设置表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.3, 2.0)
    
    # 设置表头样式
    for j in range(len(cols) + 1):
        table[(0, j)].set_facecolor('#5B8FF9')
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    # 设置第一列样式
    for i in range(1, len(rows) + 1):
        table[(i, 0)].set_facecolor('#e8e8e8')
        table[(i, 0)].set_text_props(fontweight='bold')
    
    # 设置交替行颜色
    for i in range(1, len(rows) + 1):
        for j in range(1, len(cols) + 1):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f8f9fa')
            else:
                table[(i, j)].set_facecolor('white')
    
    ax.set_title(config.get('title', '透视表'), fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def render_chart(antv_json, output_path):
    """
    主渲染函数
    根据图表类型调用相应的绘制函数
    """
    # 配置中文字体
    setup_chinese_fonts()
    
    chart_type = antv_json.get('type', 'Column')
    config = antv_json.get('config', {})
    data = antv_json.get('data', [])
    
    print(f"📊 图表类型：{chart_type}")
    print(f"📝 数据量：{len(data)} 条")
    print(f"📄 标题：{config.get('title', 'N/A')}")
    
    # 图表类型映射 - 全部 12 种图表支持
    type_mapping = {
        'Line': draw_line,
        'Column': draw_column,
        'Bar': draw_bar,
        'Area': draw_area,
        'Pie': draw_pie,
        'Rose': lambda d, c, p: draw_pie(d, c, p, is_rose=True),
        'Scatter': draw_scatter,
        'Box': draw_box,  # ✅ 箱型图已支持
        'Heatmap': draw_heatmap,
        'DualAxisChart': draw_dual_axis,  # ✅ 双轴图已支持
        'DetailTable': draw_detail_table,  # ✅ 明细表已支持
        'PivotTable': draw_pivot_table,  # ✅ 透视表已支持
    }
    
    if chart_type not in type_mapping:
        print(f"⚠️ 不支持的图表类型：{chart_type}，使用柱状图代替")
        chart_type = 'Column'
    
    render_func = type_mapping[chart_type]
    
    try:
        render_func(data, config, output_path)
        print(f"✅ 图表已保存：{output_path}")
        return output_path
    except Exception as e:
        print(f"❌ 渲染失败：{e}")
        import traceback
        traceback.print_exc()
        return None


# ==================== 主程序入口 ====================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：uv run python render_chart.py <antv_json> <output_path>")
        print("示例：uv run python render_chart.py '{\"type\":\"Column\",\"data\":[{\"name\":\"A\",\"value\":100}]}' output.png")
        sys.exit(1)
    
    antv_json_str = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        antv_json = json.loads(antv_json_str)
        render_chart(antv_json, output_path)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 渲染失败：{e}")
        sys.exit(1)
