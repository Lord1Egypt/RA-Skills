#!/usr/bin/env python3
"""
独孤九剑 · 可视化模块
生成 K 线图 + 均线 + 布林带 + 成交量 + 指标副图
支持保存为 PNG 供 AI 视觉分析
"""

import sys
import os
from datetime import datetime

import numpy as np
import pandas as pd

# mplfinance 使用非交互式后端
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
import mplfinance as mpf

# ── 中文字体配置 ────────────────────────────────────────

def _setup_cjk_font():
    """检测并配置 CJK 字体，支持 Windows/macOS/Linux"""
    # 按优先级搜索可用字体
    candidates = [
        "Microsoft YaHei", "SimHei", "SimSun", "KaiTi", "FangSong",     # Windows
        "PingFang SC", "Heiti SC", "STHeiti", "Hiragino Sans GB",       # macOS
        "Noto Sans CJK SC", "WenQuanYi Micro Hei", "Droid Sans Fallback", # Linux
    ]
    available = {f.name: f for f in fm.fontManager.ttflist}

    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            plt.rcParams["font.family"] = "sans-serif"
            return name

    # 如果都不行，尝试搜索任何 CJK 字体
    for f in fm.fontManager.ttflist:
        if any(kw in f.name.lower() for kw in ["cjk", "hei", "ming", "song", "kai", "chinese", "japan"]):
            plt.rcParams["font.sans-serif"] = [f.name, "DejaVu Sans"]
            plt.rcParams["font.family"] = "sans-serif"
            return f.name

    return None

_cjk_font = _setup_cjk_font()
if _cjk_font is None:
    # 如果没有 CJK 字体，禁用中文 warning，使用 ASCII 标记
    import warnings
    warnings.filterwarnings("ignore", message="Glyph.*missing from font")

plt.rcParams["axes.unicode_minus"] = False


# ── 配色方案 ────────────────────────────────────────────

COLORS = {
    "bg": "#1a1a2e",
    "panel_bg": "#16213e",
    "text": "#e0e0e0",
    "up": "#ef5350",        # 红色（A股习惯）
    "down": "#26a69a",      # 绿色（A股习惯）
    "ma5": "#ffd54f",
    "ma8": "#ff8a65",
    "ma13": "#ce93d8",
    "ma21": "#64b5f6",
    "ma55": "#81c784",
    "bb": "#4fc3f7",
    "volume": "#78909c",
    "grid": "#2a2a4a",
    "signal_bg": "#0d1b2a",
    "highlight": "#ffd54f",
}


def make_custom_style():
    """自定义 mplfinance 样式"""
    return mpf.make_mpf_style(
        base_mpf_style="charles",
        marketcolors=mpf.make_marketcolors(
            up=COLORS["up"],
            down=COLORS["down"],
            edge="inherit",
            wick="inherit",
            volume={"up": COLORS["up"], "down": COLORS["down"]},
        ),
        facecolor=COLORS["bg"],
        edgecolor=COLORS["grid"],
        figcolor=COLORS["bg"],
        gridcolor=COLORS["grid"],
        gridstyle=":",
        y_on_right=False,
    )


# ── 主图绘制 ────────────────────────────────────────────

def plot_analysis_chart(
    df: pd.DataFrame,
    signals: dict,
    zong_jue: dict,
    code: str,
    name: str = "",
    save_path: str = None,
) -> str:
    """
    绘制综合分析图

    布局：
      Panel 1: K线 + 均线(5/8/21/55) + 布林带
      Panel 2: 成交量 + 5日均量
      Panel 3: RSI(14)

    Args:
        df: 带特征的日K线 DataFrame
        signals: 九式信号字典
        zong_jue: 总诀式研判
        code: 股票代码
        name: 股票名称
        save_path: 保存路径（默认自动生成）

    Returns:
        保存的图片路径
    """
    if save_path is None:
        charts_dir = os.path.join(os.path.dirname(__file__), "..", "charts")
        os.makedirs(charts_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(charts_dir, f"{code}_{timestamp}.png")

    # 准备数据（取最近60天）
    plot_df = df.tail(60).copy()
    if "date" in plot_df.columns:
        plot_df.index = pd.DatetimeIndex(plot_df["date"])

    # 构建 mplfinance 需要的附加图
    add_plots = []

    # 均线
    for ma, color, label in [
        ("ma5", COLORS["ma5"], "MA5"),
        ("ma8", COLORS["ma8"], "MA8"),
        ("ma21", COLORS["ma21"], "MA21"),
        ("ma55", COLORS["ma55"], "MA55"),
    ]:
        if ma in plot_df.columns:
            add_plots.append(mpf.make_addplot(
                plot_df[ma], color=color, width=0.8, label=label
            ))

    # 布林带
    for bb, color in [("bb_upper", COLORS["bb"]), ("bb_lower", COLORS["bb"])]:
        if bb in plot_df.columns:
            add_plots.append(mpf.make_addplot(
                plot_df[bb], color=color, width=0.5, linestyle="--", alpha=0.5
            ))

    # RSI 副图
    if "rsi" in plot_df.columns:
        rsi_plot = mpf.make_addplot(
            plot_df["rsi"],
            panel=2,
            color="#ce93d8",
            width=1.0,
            label="RSI(14)",
            ylabel="RSI",
        )
        add_plots.append(rsi_plot)

        # RSI 超买超卖线
        for level, ls, lw in [(70, "--", 0.5), (30, "--", 0.5)]:
            hline = mpf.make_addplot(
                np.full(len(plot_df), level),
                panel=2,
                color="#ef5350" if level == 70 else "#26a69a",
                linestyle=ls,
                width=lw,
                alpha=0.5,
            )
            add_plots.append(hline)

    # 成交量副图
    if "volume" in plot_df.columns:
        colors_vol = [COLORS["up"] if plot_df.iloc[i]["close"] >= plot_df.iloc[i]["open"]
                      else COLORS["down"] for i in range(len(plot_df))]
        vol_plot = mpf.make_addplot(
            plot_df["volume"],
            panel=1,
            type="bar",
            color=colors_vol,
            alpha=0.7,
            ylabel="Volume",
            width=0.8,
        )
        add_plots.append(vol_plot)

        if "volume_ma5" in plot_df.columns:
            vol_ma = mpf.make_addplot(
                plot_df["volume_ma5"],
                panel=1,
                color=COLORS["highlight"],
                width=0.8,
                alpha=0.7,
            )
            add_plots.append(vol_ma)

    # 计算实际 panel 数量（基于 addplot 中的最大 panel 编号）
    max_panel = 1  # 默认至少有 main(0) + volume(1)
    for ap in add_plots:
        if hasattr(ap, '__dict__') and '_panel' in ap.__dict__:
            max_panel = max(max_panel, ap.__dict__['_panel'])
    n_panels = max_panel + 1
    # 构建动态 panel_ratios: 主图占3份，其余各1份
    ratios = [3] + [1] * (n_panels - 1)

    # 绘图
    style = make_custom_style()
    fig, axes = mpf.plot(
        plot_df,
        type="candle",
        style=style,
        addplot=add_plots,
        volume=False,
        figsize=(16, 10),
        title=f"\n独孤九剑 · {name}({code})",
        returnfig=True,
        panel_ratios=tuple(ratios),
        tight_layout=True,
    )

    # 添加图例
    main_ax = axes[0]
    main_ax.legend(loc="upper left", fontsize=7, framealpha=0.3)

    # 在图下方添加信号文字
    fig.text(
        0.50, 0.02,
        _build_signal_text(signals, zong_jue),
        ha="center", va="bottom",
        fontsize=7.5, family="monospace",
        color=COLORS["text"],
        bbox=dict(boxstyle="round,pad=0.8", facecolor=COLORS["signal_bg"], alpha=0.9, edgecolor=COLORS["grid"]),
        transform=fig.transFigure,
    )

    plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig)

    return save_path


def plot_simple_kline(df: pd.DataFrame, code: str, name: str = "", days: int = 90,
                      save_path: str = None) -> str:
    """
    简单 K 线图（快速预览，不需要完整特征）
    """
    if save_path is None:
        charts_dir = os.path.join(os.path.dirname(__file__), "..", "charts")
        os.makedirs(charts_dir, exist_ok=True)
        save_path = os.path.join(charts_dir, f"{code}_quick.png")

    plot_df = df.tail(days).copy()
    if "date" in plot_df.columns:
        plot_df.index = pd.DatetimeIndex(plot_df["date"])

    # 计算简单均线
    for p in [5, 8, 21]:
        if f"ma{p}" not in plot_df.columns:
            plot_df[f"ma{p}"] = plot_df["close"].rolling(p).mean()

    add_plots = []
    for p, color in [(5, COLORS["ma5"]), (8, COLORS["ma8"]), (21, COLORS["ma21"])]:
        add_plots.append(mpf.make_addplot(plot_df[f"ma{p}"], color=color, width=0.8))

    style = make_custom_style()

    mpf.plot(
        plot_df,
        type="candle",
        style=style,
        addplot=add_plots,
        volume=True,
        figsize=(14, 8),
        title=f"\n{name}({code}) - {days}日K线",
        savefig=save_path,
        tight_layout=True,
    )

    return save_path


def _build_signal_text(signals: dict, zong_jue: dict) -> str:
    """构建图表上的信号标注文字"""
    lines = []

    # 触发的招式
    triggered = [k for k, v in signals.items() if v["triggered"]]
    if triggered:
        sword_map = {
            "po_jian": "破剑式(起爆)", "po_dao": "破刀式(空中加油)",
            "po_qiang": "破枪式(主力跟踪)", "po_bian": "破鞭式(上下画线)",
            "po_suo": "破索式(底部吃货)", "po_zhang": "破掌式(短线打墙)",
            "po_jian_2": "破箭式(缺口策略)", "po_qi": "破气式(消息判别)",
        }
        triggered_names = [sword_map.get(k, k) for k in triggered]
        lines.append(f"触发: {' | '.join(triggered_names)}")

    # 总诀式
    lines.append(f"置信度: {zong_jue['confidence']:.0f}/100  |  风险: {zong_jue['risk_level']}")
    lines.append(f"建议: {zong_jue['recommendation']}")

    if zong_jue.get("synergies"):
        for s in zong_jue["synergies"][:2]:
            lines.append(s)

    return "\n".join(lines)


# ── CLI 入口 ────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python plot_charts.py <股票代码>")
        sys.exit(1)

    code = sys.argv[1]

    from fetch_data import fetch_all
    from compute_features import compute_all_features
    from nine_swords_rules import match_all_swords

    print(f"📊 正在获取 {code} 数据...")
    raw = fetch_all(code, days=120)
    if not raw["success"]:
        print(f"❌ 数据获取失败: {raw.get('errors')}")
        sys.exit(1)

    print("🔬 计算特征...")
    features = compute_all_features(raw["daily_kline"], raw.get("fund_flow"))

    print("⚔️ 匹配九式...")
    result = match_all_swords(features)

    print("🎨 绘制图表...")
    path = plot_analysis_chart(
        features["data"],
        result["signals"],
        result["zong_jue"],
        code,
        raw["name"],
    )

    print(f"✅ 图表已保存: {path}")
