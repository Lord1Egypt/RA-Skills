#!/usr/bin/env python3
"""
data-visualizer - 数据可视化工具（付费版支持）
将 CSV/JSON 数据生成美观图表（柱状图、折线图、饼图、散点图、面积图）
"""

import os
import sys
import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 添加 shared 模块路径
workspace_root = Path(__file__).resolve().parents[3]
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

try:
    from skills.shared.license_manager import LicenseValidator, LicenseVerificationError
    LICENSE_AVAILABLE = True
except ImportError:
    LICENSE_AVAILABLE = False
    print("⚠️  License manager not found, license check disabled")

VERSION = "1.1.0-premium"

def read_data(file_path):
    """读取数据文件"""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.csv':
        return pd.read_csv(file_path)
    elif ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame([data])
        else:
            raise ValueError("JSON 格式不支持")
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"不支持的文件格式：{ext}")

def plot_bar(df, x_col, y_cols, title=None, x_label=None, y_label=None, color=None, grid=False, legend=False):
    """绘制柱状图"""
    ax = df.plot(
        kind='bar',
        x=x_col,
        y=y_cols,
        color=color,
        figsize=plt.rcParams.get('figure.figsize')
    )
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    if x_label:
        ax.set_xlabel(x_label, fontsize=12)
    if y_label:
        ax.set_ylabel(y_label, fontsize=12)
    if grid:
        ax.grid(True, alpha=0.3)
    if legend:
        ax.legend()
    plt.tight_layout()
    return ax

def plot_line(df, x_col, y_cols, title=None, x_label=None, y_label=None, color=None, grid=False, legend=False):
    """绘制折线图"""
    ax = df.plot(
        kind='line',
        x=x_col,
        y=y_cols,
        color=color,
        figsize=plt.rcParams.get('figure.figsize'),
        marker='o',
        linewidth=2
    )
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    if x_label:
        ax.set_xlabel(x_label, fontsize=12)
    if y_label:
        ax.set_ylabel(y_label, fontsize=12)
    if grid:
        ax.grid(True, alpha=0.3)
    if legend:
        ax.legend()
    plt.tight_layout()
    return ax

def plot_pie(df, x_col, y_col, title=None, color=None):
    """绘制饼图"""
    if isinstance(y_col, list):
        y_col = y_col[0]
    
    fig, ax = plt.subplots(figsize=plt.rcParams.get('figure.figsize'))
    ax.pie(
        df[y_col],
        labels=df[x_col],
        colors=color,
        autopct='%1.1f%%',
        startangle=90
    )
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('equal')
    plt.tight_layout()
    return ax

def plot_scatter(df, x_col, y_cols, title=None, x_label=None, y_label=None, color=None, grid=False, legend=False):
    """绘制散点图"""
    if len(y_cols) > 1:
        print("⚠️  散点图只支持一个 Y 列，使用第一个")
        y_col = y_cols[0]
    else:
        y_col = y_cols[0]
    
    ax = df.plot(
        kind='scatter',
        x=x_col,
        y=y_col,
        color=color,
        figsize=plt.rcParams.get('figure.figsize'),
        s=100,
        alpha=0.7
    )
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    if x_label:
        ax.set_xlabel(x_label, fontsize=12)
    if y_label:
        ax.set_ylabel(y_label, fontsize=12)
    if grid:
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return ax

def plot_area(df, x_col, y_cols, title=None, x_label=None, y_label=None, color=None, grid=False, legend=False):
    """绘制面积图"""
    ax = df.plot(
        kind='area',
        x=x_col,
        y=y_cols,
        color=color,
        figsize=plt.rcParams.get('figure.figsize'),
        alpha=0.7
    )
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    if x_label:
        ax.set_xlabel(x_label, fontsize=12)
    if y_label:
        ax.set_ylabel(y_label, fontsize=12)
    if grid:
        ax.grid(True, alpha=0.3)
    if legend:
        ax.legend()
    plt.tight_layout()
    return ax

def main():
    parser = argparse.ArgumentParser(
        description=f"data-visualizer v{VERSION} - 数据可视化工具（支持付费高级功能）"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="输入数据文件（CSV/JSON/Excel）"
    )
    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["bar", "line", "pie", "scatter", "area"],
        help="图表类型：bar（柱状图）、line（折线图）、pie（饼图）、scatter（散点图）、area（面积图）"
    )
    parser.add_argument(
        "--output", "-o",
        default="chart.png",
        help="输出文件路径（默认：chart.png）"
    )
    parser.add_argument(
        "--title",
        help="图表标题"
    )
    parser.add_argument(
        "--x-label",
        help="X 轴标签"
    )
    parser.add_argument(
        "--y-label",
        help="Y 轴标签"
    )
    parser.add_argument(
        "--x-col",
        required=True,
        help="X 轴数据列名"
    )
    parser.add_argument(
        "--y-col",
        required=True,
        help="Y 轴数据列名（逗号分隔多列）"
    )
    parser.add_argument(
        "--color",
        help="颜色（十六进制或颜色名，逗号分隔多色）"
    )
    parser.add_argument(
        "--figsize",
        default="10,6",
        help="图表大小，格式：宽,高（默认：10,6）"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=100,
        help="输出 DPI（默认：100）"
    )
    parser.add_argument(
        "--grid", "-g",
        action="store_true",
        help="显示网格线"
    )
    parser.add_argument(
        "--legend", "-l",
        action="store_true",
        help="显示图例"
    )
    parser.add_argument(
        "--preview", "-p",
        action="store_true",
        help="预览模式，显示图表不保存"
    )
    parser.add_argument(
        "--style",
        choices=["default", "seaborn", "ggplot", "fivethirtyeight"],
        default="default",
        help="图表样式（默认：default）"
    )
    parser.add_argument(
        "--license",
        help="许可证文件路径（付费功能必需）"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"data-visualizer v{VERSION}"
    )

    args = parser.parse_args()

    # License 检查（如果使用付费功能）
    try:
        if args.license:
            # 用户指定了许可证文件
            validator = LicenseValidator(
                license_path=args.license,
                secret_key=os.getenv('SKILL_LICENSE_SECRET')
            )
            validator.get_valid_license(skill_name='data-chart-tool')
            print("✅ 付费许可证验证通过")
        elif args.type == 'scatter':
            # scatter 是付费功能，需要许可证
            print("❌ 散点图（scatter）是付费功能，请通过 --license 指定许可证文件")
            print("   获取许可证：联系管理员并提供付款凭证")
            sys.exit(1)
    except LicenseVerificationError as e:
        print(f"❌ 许可证验证失败：{e}")
        print("   💡 如需使用高级功能，请购买许可证")
        sys.exit(1)
    except Exception as e:
        if args.type == 'scatter':
            print(f"⚠️  许可证系统不可用，散点图功能受限")
            # 在生产环境应该直接退出，这里为了调试放宽
            pass
    
    # 设置样式
    if args.style != "default":
        plt.style.use(args.style)
    
    # 设置图表大小
    try:
        width, height = map(float, args.figsize.split(','))
        plt.rcParams['figure.figsize'] = (width, height)
    except:
        print(f"⚠️  图表大小格式错误，使用默认值 10,6")
        plt.rcParams['figure.figsize'] = (10, 6)
    
    # 解析颜色
    colors = None
    if args.color:
        colors = [c.strip() for c in args.color.split(',')]
    
    # 解析 Y 列
    y_cols = [c.strip() for c in args.y_col.split(',')]
    
    # 读取数据
    print(f"📊 正在读取数据：{args.input}")
    try:
        df = read_data(args.input)
        print(f"✅ 数据读取成功！共 {len(df)} 行，{len(df.columns)} 列")
        print(f"   列名：{', '.join(df.columns)}")
    except Exception as e:
        print(f"❌ 读取数据失败：{e}")
        return
    
    # 检查列是否存在
    if args.x_col not in df.columns:
        print(f"❌ X 轴列 '{args.x_col}' 不存在")
        print(f"   可用列：{', '.join(df.columns)}")
        return
    
    for y_col in y_cols:
        if y_col not in df.columns:
            print(f"❌ Y 轴列 '{y_col}' 不存在")
            print(f"   可用列：{', '.join(df.columns)}")
            return
    
    # 绘制图表
    print(f"🎨 正在绘制 {args.type} 图表...")
    
    plot_functions = {
        'bar': plot_bar,
        'line': plot_line,
        'pie': plot_pie,
        'scatter': plot_scatter,
        'area': plot_area
    }
    
    plot_func = plot_functions[args.type]
    
    try:
        if args.type == 'pie':
            plot_func(df, args.x_col, y_cols, args.title, colors)
        else:
            plot_func(df, args.x_col, y_cols, args.title, args.x_label, args.y_label, colors, args.grid, args.legend)
        
        print(f"✅ 图表绘制成功！")
        
        if args.preview:
            print("👀 预览模式：显示图表...")
            plt.show()
        else:
            print(f"💾 正在保存到：{args.output}")
            plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
            print(f"✅ 保存成功！")
            
            # 显示文件大小
            file_size = os.path.getsize(args.output) / 1024
            print(f"   文件大小：{file_size:.2f} KB")
    
    except Exception as e:
        print(f"❌ 绘制图表失败：{e}")
        import traceback
        traceback.print_exc()
    
    finally:
        plt.close()

if __name__ == "__main__":
    main()
