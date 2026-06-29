#!/usr/bin/env python3
"""
cn-financial-deep-analysis 图表生成插件

从分析结果JSON生成PNG图表：营收趋势、净利润趋势、现金流趋势、资产负债结构。
macOS 默认使用 PingFang SC 中文字体。

用法：
    python3 charts.py --input analysis_result.json --output-dir ./charts/
"""

import argparse
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── 中文字体配置（macOS 优先 PingFang SC） ──
def _setup_chinese_font():
    """自动检测并配置中文字体。"""
    candidates = [
        "PingFang SC",
        "Heiti SC",
        "STHeiti",
        "Arial Unicode MS",
        "SimHei",
        "Microsoft YaHei",
        "WenQuanYi Micro Hei",
    ]
    for font_name in candidates:
        try:
            plt.rcParams["font.sans-serif"] = [font_name]
            plt.rcParams["axes.unicode_minus"] = False
            # 验证：尝试渲染一个中文字符
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.set_title("测")
            plt.close(fig)
            return font_name
        except Exception:
            continue
    print("警告：未找到中文字体，图表中文可能显示为方块", file=sys.stderr)
    plt.rcParams["axes.unicode_minus"] = False
    return None


FONT_NAME = _setup_chinese_font()


def load_data(input_path: str) -> dict:
    """加载分析结果JSON。"""
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _style_ax(ax, title: str, xlabel: str = "", ylabel: str = ""):
    """统一图表样式。"""
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.legend(fontsize=10, frameon=False)


def chart_revenue_trend(data: dict, output_dir: str):
    """营收与净利润趋势图（双Y轴）。"""
    years = data.get("years", [])
    revenue = data.get("revenue", [])
    net_profit = data.get("net_profit", [])

    if not years or not revenue:
        print("跳过营收趋势：数据不足")
        return

    revenue_unit = 100_000_000  # 亿元
    revenue_billion = [v / revenue_unit for v in revenue]
    net_profit_billion = [v / revenue_unit for v in net_profit] if net_profit else None

    fig, ax1 = plt.subplots(figsize=(10, 5))

    bars = ax1.bar(years, revenue_billion, width=0.5, color="#2563EB", alpha=0.85, label="营业收入")
    ax1.set_ylabel("营业收入（亿元）", fontsize=11)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}"))

    # 在柱上标数值
    for bar, val in zip(bars, revenue):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(revenue_billion) * 0.02,
                 f"{val/revenue_unit:.1f}亿", ha="center", va="bottom", fontsize=9, color="#1E3A5F")

    if net_profit_billion:
        ax2 = ax1.twinx()
        ax2.plot(years, net_profit_billion, "o-", color="#DC2626", linewidth=2, markersize=6, label="净利润")
        ax2.set_ylabel("净利润（亿元）", fontsize=11, color="#DC2626")
        ax2.tick_params(axis="y", colors="#DC2626")
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}"))

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels() if net_profit_billion else ([], [])
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=10, frameon=False, loc="upper left")

    _style_ax(ax1, data.get("company_name", "") + " 营收与净利润趋势", xlabel="年度")

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "营收与净利润趋势.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"已生成：{filepath}")


def chart_cashflow_trend(data: dict, output_dir: str):
    """经营/投资/筹资现金流趋势图。"""
    years = data.get("years", [])
    operating = data.get("operating_cf", [])
    investing = data.get("investing_cf", [])
    financing = data.get("financing_cf", [])

    if not years or not operating:
        print("跳过现金流趋势：数据不足")
        return

    unit = 100_000_000
    op = [v / unit for v in operating]
    inv = [v / unit for v in investing] if investing else []
    fin = [v / unit for v in financing] if financing else []

    fig, ax = plt.subplots(figsize=(10, 5))

    x = range(len(years))
    width = 0.25
    ax.bar([i - width for i in x], op, width, color="#059669", alpha=0.85, label="经营活动")
    if inv:
        ax.bar(x, inv, width, color="#D97706", alpha=0.85, label="投资活动")
    if fin:
        ax.bar([i + width for i in x], fin, width, color="#7C3AED", alpha=0.85, label="筹资活动")

    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("现金流（亿元）", fontsize=11)
    ax.axhline(y=0, color="black", linewidth=0.8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}"))

    _style_ax(ax, data.get("company_name", "") + " 现金流趋势", xlabel="年度")

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "现金流趋势.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"已生成：{filepath}")


def chart_balance_structure(data: dict, output_dir: str):
    """最新一期资产负债结构饼图。"""
    assets = data.get("latest_assets", {})
    liabilities = data.get("latest_liabilities", {})
    equity = data.get("latest_equity", {})

    if not assets:
        print("跳过资产负债结构：数据不足")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 资产结构
    asset_labels = list(assets.keys())
    asset_values = list(assets.values())
    colors_asset = ["#2563EB", "#60A5FA", "#93C5FD", "#BFDBFE", "#DBEAFE"][:len(asset_labels)]
    ax1.pie(asset_values, labels=asset_labels, autopct="%1.1f%%",
            colors=colors_asset, startangle=90, pctdistance=0.75)
    ax1.set_title("资产结构", fontsize=13, fontweight="bold", pad=12)

    # 负债与权益结构
    liab_labels = list(liabilities.keys()) + list(equity.keys())
    liab_values = list(liabilities.values()) + list(equity.values())
    colors_liab = (["#DC2626", "#F87171", "#FCA5A5", "#FECACA"][:len(liabilities)]
                   + ["#059669", "#34D399"][:len(equity)])
    ax2.pie(liab_values, labels=liab_labels, autopct="%1.1f%%",
            colors=colors_liab, startangle=90, pctdistance=0.75)
    ax2.set_title("负债与权益结构", fontsize=13, fontweight="bold", pad=12)

    fig.suptitle(data.get("company_name", "") + " 资产负债结构（最新一期）",
                 fontsize=14, fontweight="bold", y=1.02)

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "资产负债结构.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"已生成：{filepath}")


def chart_roe_dupont(data: dict, output_dir: str):
    """杜邦分析ROE拆解堆叠条形图。"""
    years = data.get("years", [])
    net_margin = data.get("net_margin", [])      # %
    asset_turnover = data.get("asset_turnover", [])
    equity_multiplier = data.get("equity_multiplier", [])

    if not years or not net_margin:
        print("跳过杜邦分析：数据不足")
        return

    fig, ax = plt.subplots(figsize=(10, 4.5))
    x = range(len(years))

    # 三因子条形图
    width = 0.5
    p1 = ax.bar(x, net_margin, width, color="#2563EB", alpha=0.85, label="净利率(%)")
    p2 = ax.bar(x, asset_turnover, width, bottom=net_margin, color="#059669", alpha=0.85, label="资产周转率")
    bottom2 = [a + b for a, b in zip(net_margin, asset_turnover)]
    p3 = ax.bar(x, equity_multiplier, width, bottom=bottom2, color="#D97706", alpha=0.85, label="权益乘数")
    totals = [a + b + c for a, b, c in zip(net_margin, asset_turnover, equity_multiplier)]

    # 标注ROE值
    for i, total in enumerate(totals):
        ax.text(i, total + max(totals) * 0.02, f"{total:.1f}%", ha="center", fontsize=10, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("ROE (%)", fontsize=11)
    _style_ax(ax, data.get("company_name", "") + " ROE 杜邦拆解", xlabel="年度")

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "ROE杜邦拆解.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"已生成：{filepath}")


def main():
    parser = argparse.ArgumentParser(description="生成财务报表图表")
    parser.add_argument("--input", "-i", required=True, help="分析结果JSON文件路径")
    parser.add_argument("--output-dir", "-o", required=True, help="图表输出目录")
    args = parser.parse_args()

    data = load_data(args.input)

    chart_revenue_trend(data, args.output_dir)
    chart_cashflow_trend(data, args.output_dir)
    chart_balance_structure(data, args.output_dir)
    chart_roe_dupont(data, args.output_dir)

    print(f"\n全部图表已生成至 {args.output_dir}/")


if __name__ == "__main__":
    main()
