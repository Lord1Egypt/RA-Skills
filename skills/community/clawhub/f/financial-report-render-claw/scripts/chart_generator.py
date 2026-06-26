#!/usr/bin/env python3
"""专业图表生成器 — financial-report-render-claw"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd


def load_theme(theme_path=None):
    """加载图表主题配置。"""
    candidates = [
        theme_path,
        Path(__file__).resolve().parent.parent / "assets" / "chart_theme.json",
    ]
    for p in candidates:
        if p and Path(p).exists():
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    return None


def apply_theme(ax, theme):
    """将主题样式应用到坐标轴。"""
    if not theme:
        return
    c = theme.get("chart", {})
    ax.grid(True, alpha=c.get("grid_alpha", 0.15), linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(theme.get("colors", {}).get("text_light", "#7F8C8D"))
    ax.spines["bottom"].set_color(theme.get("colors", {}).get("text_light", "#7F8C8D"))
    ax.tick_params(labelsize=c.get("label_size", 11))
    ax.xaxis.label.set_fontsize(c.get("font_size", 12))
    ax.yaxis.label.set_fontsize(c.get("font_size", 12))


def setup_font(theme):
    """配置中文字体。"""
    if theme and "font" in theme:
        font_family = theme["font"].get("family_cn", "")
        plt.rcParams["font.sans-serif"] = [f.strip() for f in font_family.split(",")]
        plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


def save_fig(fig, output, theme):
    """保存图表。"""
    exp = theme.get("export", {}) if theme else {}
    fig.savefig(
        output,
        dpi=exp.get("dpi", 300),
        bbox_inches=exp.get("bbox_inches", "tight"),
        facecolor="white",
    )
    plt.close(fig)
    print(f"[OK] 图表已保存: {output}")


def line_chart(args, theme, palette):
    """折线图。"""
    df = pd.read_csv(args.input)
    setup_font(theme)

    fig, ax = plt.subplots(figsize=(theme["export"]["width"], theme["export"]["height"]) if theme else (10, 6))
    y_cols = args.y if len(args.y) > 1 else args.y[0]
    styles = ["-", "--", "-.", ":"]

    if isinstance(y_cols, list):
        for i, col in enumerate(y_cols):
            style = styles[i % len(styles)]
            ax.plot(df[args.x], df[col], marker="o", linewidth=theme["chart"]["line_width"] if theme else 2.5,
                    markersize=theme["chart"]["marker_size"] if theme else 6,
                    color=palette[i % len(palette)], linestyle=style, label=col)
        ax.legend(frameon=False, fontsize=11)
    else:
        ax.plot(df[args.x], df[y_cols], marker="o", linewidth=2.5, markersize=6,
                color=palette[0])

    ax.set_title(args.title, fontsize=theme["chart"]["title_size"] if theme else 14, fontweight="bold", pad=15)
    ax.set_xlabel(args.xlabel or args.x)
    ax.set_ylabel(args.ylabel or y_cols[0] if isinstance(y_cols, list) else y_cols)
    apply_theme(ax, theme)

    if args.yaxis_pct:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0%}"))

    save_fig(fig, args.output, theme)


def bar_chart(args, theme, palette):
    """柱状图。"""
    df = pd.read_csv(args.input)
    setup_font(theme)

    fig, ax = plt.subplots(figsize=(theme["export"]["width"], theme["export"]["height"]) if theme else (10, 6))
    y_cols = args.y if len(args.y) > 1 else args.y[0]

    if isinstance(y_cols, list):
        x = range(len(df))
        width = theme["chart"]["bar_width"] if theme else 0.6
        n = len(y_cols)
        single_w = width / n
        for i, col in enumerate(y_cols):
            offset = (i - n / 2 + 0.5) * single_w
            bars = ax.bar([xi + offset for xi in x], df[col], width=single_w,
                          color=palette[i % len(palette)], label=col)
            if args.value_label:
                for bar in bars:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                            f"{bar.get_height():,.1f}", ha="center", va="bottom", fontsize=9)
        ax.set_xticks(list(x))
        ax.set_xticklabels(df[args.x])
        ax.legend(frameon=False, fontsize=11)
    else:
        orient = "h" if args.horizontal else "v"
        bars = ax.barh(df[args.x], df[y_cols], color=palette[0]) if args.horizontal else \
               ax.bar(df[args.x], df[y_cols], color=palette[0])
        if args.value_label:
            for bar in bars:
                if args.horizontal:
                    ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                            f"{bar.get_width():,.1f}", ha="left", va="center", fontsize=9)
                else:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                            f"{bar.get_height():,.1f}", ha="center", va="bottom", fontsize=9)

    ax.set_title(args.title, fontsize=14, fontweight="bold", pad=15)
    apply_theme(ax, theme)

    save_fig(fig, args.output, theme)


def pie_chart(args, theme, palette):
    """饼图。"""
    df = pd.read_csv(args.input)
    setup_font(theme)

    fig, ax = plt.subplots(figsize=(8, 8))
    values = df[args.y[0]]
    labels = df[args.x]

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=palette[:len(values)],
        autopct=lambda pct: f"{pct:.1f}%" if pct > 3 else "",
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2),
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    for t in texts:
        t.set_fontsize(11)

    ax.set_title(args.title, fontsize=14, fontweight="bold", pad=20)

    save_fig(fig, args.output, theme)


def combo_chart(args, theme, palette):
    """组合图（柱+线）。"""
    df = pd.read_csv(args.input)
    setup_font(theme)

    fig, ax1 = plt.subplots(figsize=(theme["export"]["width"], theme["export"]["height"]) if theme else (10, 6))

    # 柱状
    bar_cols = args.y_bar if isinstance(args.y_bar, list) else [args.y_bar]
    x = range(len(df))
    n = len(bar_cols)
    width = 0.6
    for i, col in enumerate(bar_cols):
        offset = (i - n / 2 + 0.5) * (width / n)
        ax1.bar([xi + offset for xi in x], df[col], width=width / n,
                color=palette[i % len(palette)], label=col)

    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df[args.x])
    ax1.set_ylabel(args.y_bar if isinstance(args.y_bar, str) else args.y_bar[0])

    # 折线（右轴）
    line_cols = args.y_line if isinstance(args.y_line, list) else [args.y_line]
    ax2 = ax1.twinx()
    for i, col in enumerate(line_cols):
        ax2.plot(df[args.x], df[col], marker="s", linewidth=2.5, color=palette[(i + n) % len(palette)],
                 linestyle="--", label=col)
    ax2.set_ylabel(args.y_line if isinstance(args.y_line, str) else args.y_line[0])

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False, fontsize=11)

    ax1.set_title(args.title, fontsize=14, fontweight="bold", pad=15)
    apply_theme(ax1, theme)
    ax2.spines["top"].set_visible(False)

    save_fig(fig, args.output, theme)


def main():
    parser = argparse.ArgumentParser(description="专业图表生成器")
    sub = parser.add_subparsers(dest="chart_type", required=True)

    # 通用参数
    def add_common(p):
        p.add_argument("-i", "--input", required=True, help="数据文件路径（CSV）")
        p.add_argument("-o", "--output", required=True, help="输出图片路径")
        p.add_argument("--title", default="", help="图表标题")
        p.add_argument("--theme", help="主题 JSON 路径")

    # 折线图
    p_line = sub.add_parser("line")
    add_common(p_line)
    p_line.add_argument("-x", required=True, help="X 轴列名")
    p_line.add_argument("-y", nargs="+", required=True, help="Y 轴列名（支持多列）")
    p_line.add_argument("--xlabel", help="X 轴标签")
    p_line.add_argument("--ylabel", help="Y 轴标签")
    p_line.add_argument("--yaxis-pct", action="store_true", help="Y 轴显示为百分比")

    # 柱状图
    p_bar = sub.add_parser("bar")
    add_common(p_bar)
    p_bar.add_argument("-x", required=True, help="分类列名")
    p_bar.add_argument("-y", nargs="+", required=True, help="数值列名（支持多列）")
    p_bar.add_argument("--horizontal", action="store_true", help="水平柱状图")
    p_bar.add_argument("--stacked", action="store_true", help="堆叠柱状图")
    p_bar.add_argument("--value-label", action="store_true", help="显示数值标签")

    # 饼图
    p_pie = sub.add_parser("pie")
    add_common(p_pie)
    p_pie.add_argument("-x", required=True, help="分类列名")
    p_pie.add_argument("-y", nargs="+", required=True, help="数值列名")

    # 组合图
    p_combo = sub.add_parser("combo")
    add_common(p_combo)
    p_combo.add_argument("-x", required=True, help="X 轴列名")
    p_combo.add_argument("--y-bar", required=True, help="柱状图列名")
    p_combo.add_argument("--y-line", required=True, help="折线图列名")

    args = parser.parse_args()
    theme = load_theme(args.theme)
    palette = theme.get("palette", []) if theme else ["#2E86C1", "#27AE60", "#F39C12", "#E74C3C"]

    chart_fn = {"line": line_chart, "bar": bar_chart, "pie": pie_chart, "combo": combo_chart}
    chart_fn[args.chart_type](args, theme, palette)


if __name__ == "__main__":
    main()
