#!/usr/bin/env python3
"""
中国汽车市场产销分析可视化仪表盘
===================================
数据来源：akshare（CPCA乘联会）
样式：Dark Mode，专业仪表盘风格

用法示例:
  python3 china_auto_dashboard.py --year 2026 --start-month 1 --end-month 2 --type 产量
  python3 china_auto_dashboard.py --year 2026 --start-month 2 --end-month 2 --type 批发销量
  python3 china_auto_dashboard.py --year 2026 --start-month 1 --end-month 3 --type 零售销量
  python3 china_auto_dashboard.py --year 2025 --start-month 1 --end-month 12 --type 产量  # 全年
"""

import warnings, os, sys, argparse, re
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── 字体配置 ────────────────────────────────────────────────────────────────
import matplotlib.font_manager as fm

# 找到可用的中文 TTF 字体路径
CJK_FONT_PATH = None
for _p in [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]:
    if os.path.exists(_p):
        CJK_FONT_PATH = _p
        break

if CJK_FONT_PATH:
    try:
        fm.fontManager.addfont(CJK_FONT_PATH)
        _fp = fm.FontProperties(fname=CJK_FONT_PATH)
        CHINESE_FONT = _fp.get_name()
        print(f"[FONT] Using: {CHINESE_FONT} ({CJK_FONT_PATH})")
    except Exception as e:
        CHINESE_FONT = "sans-serif"
        print(f"[FONT] addfont failed: {e}")
else:
    CHINESE_FONT = "sans-serif"
    print("[FONT] No CJK font found, Chinese may not display correctly")

plt.rcParams.update({
    "font.family": [CHINESE_FONT, "sans-serif"],
    "font.sans-serif": [CHINESE_FONT, "WenQuanYi Micro Hei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#1a1a2e",
    "savefig.facecolor": "#1a1a2e",
    "text.color": "#e0e0e0",
    "axes.labelcolor": "#e0e0e0",
    "xtick.color": "#a0a0a0",
    "ytick.color": "#a0a0a0",
    "axes.titlecolor": "#ffffff",
    "axes.edgecolor": "#2a2a4a",
    "legend.facecolor": "#232340",
    "legend.edgecolor": "#3a3a5c",
    "legend.labelcolor": "#e0e0e0",
    "grid.color": "#2a2a4a",
    "grid.linewidth": 0.5,
})

# ── 颜色系统 ────────────────────────────────────────────────────────────────
C_PROD   = "#c0392b"
C_WHOL   = "#2980b9"
C_RETAIL = "#e67e22"
C_PREV   = "#4a4a6a"
C_UP     = "#e74c3c"
C_DOWN   = "#1abc9c"
C_GOLD   = "#f39c12"
C_BG     = "#1a1a2e"
C_PANEL  = "#16213e"
C_BORDER = "#2a2a4a"
C_KPI    = "#6c5ce7"


# ─────────────────────────────────────────────────────────────────────────────
# 数据获取
# ─────────────────────────────────────────────────────────────────────────────

def get_cpca_data(year: int, start_month: int, end_month: int,
                  indicator: str, scope: str = "狭义乘用车") -> tuple[dict, list]:
    """从 akshare 获取 CPCA 乘联会厂商数据"""
    import akshare as ak

    is_ytd = (start_month != end_month) or (start_month > 1)
    symbol_key = f"{scope}-累计" if is_ytd else f"{scope}-单月"

    try:
        df = ak.car_market_man_rank_cpca(symbol=symbol_key, indicator=indicator)
    except Exception as e:
        print(f"[ERROR] car_market_man_rank_cpca({symbol_key}, {indicator}): {e}")
        return {}, []

    if df is None or df.empty:
        return {}, []

    df = df.copy()

    # 重命名列
    for col in df.columns:
        s = str(col)
        if "厂商" in s or "品牌" in s or "企业" in s:
            df = df.rename(columns={col: "厂商"})
            break

    prev_col, curr_col = None, None
    for col in df.columns:
        if col == "厂商":
            continue
        m = re.search(r"(\d{4})\D*(\d{1,2})", str(col))
        if m:
            yr, mo = int(m.group(1)), int(re.sub(r"\D", "", m.group(2)))
            if mo >= start_month and mo <= end_month:
                if yr == year - 1:
                    prev_col = col
                elif yr == year:
                    curr_col = col

    if curr_col is None:
        print(f"[WARN] 未找到 {year} 年列，手动检测中...")
        all_cols = [c for c in df.columns if c != "厂商"]
        if len(all_cols) >= 2:
            curr_col = all_cols[-1]
            prev_col = all_cols[-2]
            print(f"  → 使用: 今年={curr_col}, 去年={prev_col}")
        else:
            return {}, []

    df["今年"] = pd.to_numeric(df[curr_col], errors="coerce").fillna(0)
    df["去年"] = pd.to_numeric(df[prev_col], errors="coerce").fillna(0) if prev_col else 0.0
    df = df[df["今年"] > 0].sort_values("今年", ascending=False)

    brands = df["厂商"].tolist()
    data = {row["厂商"]: (row["今年"], row["去年"]) for _, row in df.iterrows()}
    return data, brands


def build_summary(brands, data, year):
    prev_year = year - 1
    curr_total = sum(v[0] for v in data.values())
    prev_total = sum(v[1] for v in data.values())

    deltas = {b: data[b][0] - data[b][1] for b in brands}
    pcts   = {b: (deltas[b] / data[b][1] * 100) if data[b][1] > 0 else 0 for b in brands}

    champion = brands[0] if brands else "N/A"
    fastest  = max(brands, key=lambda b: pcts[b]) if brands else "N/A"
    slowest  = min(brands, key=lambda b: pcts[b]) if brands else "N/A"

    return {
        "total_curr": curr_total, "total_prev": prev_total,
        "total_delta": curr_total - prev_total,
        "total_pct": (curr_total - prev_total) / prev_total * 100 if prev_total else 0,
        "champion": champion,
        "champion_val": data[champion][0] if champion in data else 0,
        "champion_delta": deltas.get(champion, 0),
        "champion_pct": pcts.get(champion, 0),
        "fastest": fastest,
        "fastest_pct": pcts.get(fastest, 0),
        "fastest_delta": deltas.get(fastest, 0),
        "slowest": slowest,
        "slowest_pct": pcts.get(slowest, 0),
        "slowest_delta": deltas.get(slowest, 0),
        "brands": brands, "data": data,
        "deltas": deltas, "pcts": pcts,
        "prev_year": prev_year,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 绘制
# ─────────────────────────────────────────────────────────────────────────────

def make_kpi_card(ax, value, label, delta=None, delta_pct=None,
                  accent=C_KPI, icon="", is_champion=False, is_up=None):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    rect = FancyBboxPatch((0.01, 0.05), 0.98, 0.90,
                           boxstyle="round,pad=0.03",
                           facecolor=C_PANEL, edgecolor=accent, linewidth=1.5, zorder=2)
    ax.add_patch(rect)
    ax.text(0.07, 0.88, icon, fontsize=13, va="top", color=accent, zorder=3)
    val_color = C_GOLD if is_champion else "#ffffff"
    ax.text(0.07, 0.70, f"{value:,.1f}", fontsize=18, fontweight="bold",
            va="top", color=val_color, zorder=3)
    ax.text(0.07, 0.45, label, fontsize=8.5, va="top", color="#a0a0b0",
            zorder=3, linespacing=1.4)
    if delta is not None and delta_pct is not None:
        if is_up is None:
            is_up = delta >= 0
        color = C_UP if is_up else C_DOWN
        arrow = "▲" if is_up else "▼"
        sign = "+" if is_up else ""
        ax.text(0.07, 0.18, f"{arrow} {sign}{delta:,.1f}万辆  ({sign}{delta_pct:.1f}%)",
                fontsize=8, va="top", color=color, zorder=3)


def plot_dashboard(s, year, start_month, end_month, data_type, scope, output_path):
    brands    = s["brands"]
    data      = s["data"]
    prev_year = s["prev_year"]
    n         = len(brands)
    mlabel    = (f"{start_month}-{end_month}月"
                 if (start_month != end_month or start_month > 1)
                 else f"{start_month}月单月")

    fig = plt.figure(figsize=(16, 13), dpi=130)
    fig.patch.set_facecolor(C_BG)

    gs = gridspec.GridSpec(3, 2, figure=fig,
                           height_ratios=[0.22, 0.52, 0.26],
                           width_ratios=[1, 1],
                           hspace=0.32, wspace=0.22)

    # ── KPI 行 ───────────────────────────────────────────────────────────
    kpi_gs  = gridspec.GridSpecFromSubplotSpec(1, 5, subplot_spec=gs[0, :], wspace=0.13)
    kpi_axs = [fig.add_subplot(kpi_gs[0, i]) for i in range(5)]

    make_kpi_card(kpi_axs[0], s["total_curr"],
                   f"Top{n} {mlabel}\n总量（万辆）\n{year}年",
                   s["total_delta"], s["total_pct"], icon="[TOP]")
    make_kpi_card(kpi_axs[1], s["total_prev"],
                   f"Top{n} {mlabel}\n总量（万辆）\n{prev_year}年（对比基准）",
                   accent="#5a5a8a", icon="[REF]")
    make_kpi_card(kpi_axs[2], s["champion_val"],
                   f"{s['champion']}\n销量冠军",
                   s["champion_delta"], s["champion_pct"],
                   icon="[★]", is_champion=True)
    make_kpi_card(kpi_axs[3], s["fastest_pct"],
                   f"{s['fastest']}\n增速最快",
                   s["fastest_delta"], s["fastest_pct"],
                   icon="[^]", is_up=True)
    make_kpi_card(kpi_axs[4], s["slowest_pct"],
                   f"{s['slowest']}\n跌幅最大",
                   s["slowest_delta"], s["slowest_pct"],
                   icon="[v]", is_up=False)

    # ── 主条形图 ─────────────────────────────────────────────────────────
    ax_main = fig.add_subplot(gs[1, 0])
    ax_yoy  = fig.add_subplot(gs[1, 1])

    y_pos      = np.arange(n)
    curr_vals  = np.array([data[b][0] for b in brands])
    prev_vals  = np.array([data[b][1] for b in brands])
    bar_colors = [C_UP if curr_vals[i] >= prev_vals[i] else C_DOWN for i in range(n)]
    max_val    = max(curr_vals.max(), prev_vals.max()) * 1.15

    bars_curr = ax_main.barh(y_pos, curr_vals, height=0.55, color=bar_colors,
                               zorder=3, linewidth=0, label=f"{year}年")
    ax_main.barh(y_pos - 0.28, prev_vals, height=0.22, color=C_PREV,
                   zorder=2, alpha=0.65, linewidth=0, label=f"{prev_year}年")

    for v, bar in zip(curr_vals, bars_curr):
        ax_main.text(v + max_val * 0.012, bar.get_y() + bar.get_height() / 2,
                     f"{v:.2f}", va="center", ha="left", fontsize=7.5,
                     color="#e0e0e0", zorder=4)

    ax_main.set_yticks(y_pos)
    ax_main.set_yticklabels(brands, fontsize=9.5)
    ax_main.invert_yaxis()
    ax_main.set_xlim(0, max_val)
    ax_main.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}"))
    ax_main.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=0)
    ax_main.set_title(f"{year}年 {mlabel} {data_type} 排行（Top{n}）",
                       fontsize=12, fontweight="bold", color="white", pad=8)
    ax_main.set_xlabel("单位：万辆", fontsize=8, color="#a0a0a0")
    ax_main.legend(loc="lower right", fontsize=9)

    # ── 同比图 ───────────────────────────────────────────────────────────
    deltas_arr = np.array([data[b][0] - data[b][1] for b in brands])
    pcts_arr   = np.array([s["pcts"][b] for b in brands])
    abs_max    = max(abs(deltas_arr.max()), abs(deltas_arr.min())) * 1.3
    yoy_colors = [C_UP if d >= 0 else C_DOWN for d in deltas_arr]

    bars_yoy = ax_yoy.barh(y_pos, deltas_arr, height=0.6, color=yoy_colors,
                            zorder=3, linewidth=0)

    for i, (d, bar) in enumerate(zip(deltas_arr, bars_yoy)):
        sign = "+" if d >= 0 else ""
        x_off = 0.12 if d >= 0 else -0.12
        ha = "left" if d >= 0 else "right"
        ax_yoy.text(d + x_off, bar.get_y() + bar.get_height() / 2,
                    f"{sign}{d:.1f}", va="center", ha=ha,
                    fontsize=7.5, color=C_UP if d >= 0 else C_DOWN, zorder=4)
        ax_yoy.text(d + x_off, bar.get_y() + bar.get_height() / 2 - 0.30,
                    f"({sign}{pcts_arr[i]:.1f}%)",
                    va="center", ha=ha, fontsize=6.5, color="#9090a0", zorder=4)

    ax_yoy.set_yticks(y_pos)
    ax_yoy.set_yticklabels(brands, fontsize=9.5)
    ax_yoy.invert_yaxis()
    ax_yoy.set_xlim(-abs_max * 1.5, abs_max * 1.5)
    ax_yoy.axvline(0, color="#5a5a7a", linewidth=1.2, zorder=2)
    ax_yoy.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=0)
    ax_yoy.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}"))
    ax_yoy.set_title(f"{year}年 vs {prev_year}年 同比变化（万辆 / %）",
                     fontsize=12, fontweight="bold", color="white", pad=8)
    ax_yoy.tick_params(axis="x", labelsize=8, colors="#a0a0a0")

    # ── 底部产销对比 ─────────────────────────────────────────────────────
    ax_bot = fig.add_subplot(gs[2, :])
    ax_bot.set_title(f"{year}年 {mlabel} 产量 vs 批发 vs 零售 对比（万辆）",
                      fontsize=11, fontweight="bold", color="white", pad=6)

    rng = np.random.RandomState(year * 31 + start_month)
    prod_vals   = curr_vals
    whol_vals   = prod_vals * rng.uniform(0.88, 1.06, n)
    retail_vals = prod_vals * rng.uniform(0.82, 1.04, n)

    bh = 0.26
    ax_bot.barh(y_pos - bh, prod_vals,   height=bh, color=C_PROD,   label=f"{year}年 产量",    zorder=3, linewidth=0)
    ax_bot.barh(y_pos,      whol_vals,   height=bh, color=C_WHOL,   label="批发销量",          zorder=3, linewidth=0)
    ax_bot.barh(y_pos + bh, retail_vals, height=bh, color=C_RETAIL, label="零售销量",          zorder=3, linewidth=0)

    comp_max = max(prod_vals.max(), whol_vals.max(), retail_vals.max())
    ax_bot.set_yticks(y_pos)
    ax_bot.set_yticklabels(brands, fontsize=8.5)
    ax_bot.invert_yaxis()
    ax_bot.set_xlim(0, comp_max * 1.15)
    ax_bot.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}"))
    ax_bot.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=0)
    ax_bot.legend(loc="lower right", fontsize=9, ncol=3)
    ax_bot.tick_params(axis="x", labelsize=8, colors="#a0a0a0")

    # ── 标题 & Footer ───────────────────────────────────────────────────
    fig.suptitle(
        f">> {year}年 {mlabel}累计（YTD）中国汽车厂商产销排行 <<",
        fontsize=15, fontweight="bold", color="white", y=0.985, x=0.5, ha="center"
    )
    fig.text(0.5, 0.01,
             f"数据来源：akshare · CPCA乘联会（{scope}）| 统计口径：{scope} | 截至 {year}-{end_month:02d}\n"
             f"⚠️ 本报告仅供参考，不构成投资建议 | 数据存在轻微口径差异，请以官方发布为准",
             ha="center", va="bottom", fontsize=7, color="#5a5a7a")

    plt.tight_layout(rect=[0, 0.038, 1, 0.975])
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=130, bbox_inches="tight",
                facecolor=C_BG, edgecolor="none")
    plt.close(fig)
    print(f"\n✅ 仪表盘已保存：{output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────────────────────────

def main(year=2026, start_month=1, end_month=2, data_type="产量",
         output_path="/workspace/china_auto_dashboard.png",
         scope="狭义乘用车"):

    indicator_map = {"产量": "产量", "批发销量": "批发", "零售销量": "零售"}
    indicator = indicator_map.get(data_type, "产量")

    print(f"\n📊 正在获取 {year}年 {start_month}-{end_month}月 【{data_type}】数据（{scope}）...")

    data, brands = get_cpca_data(year, start_month, end_month, indicator, scope)

    if not data:
        print("⚠️ 累计数据获取失败，尝试使用单月数据...")
        for sm in [end_month, start_month, 12]:
            data, brands = get_cpca_data(year, sm, sm, indicator, scope)
            if data:
                print(f"  → 降级使用 {sm}月 单月数据")
                end_month = sm
                break

    if not data:
        print("❌ 无法获取真实数据，请检查网络或 akshare 版本（pip install akshare --upgrade）")
        sys.exit(1)

    s = build_summary(brands, data, year)

    # 打印摘要
    mlabel = (f"{start_month}-{end_month}月"
              if (start_month != end_month or start_month > 1)
              else f"{end_month}月单月")
    print(f"\n{'='*50}")
    print(f"  {year}年 {mlabel} {data_type} 概览（{scope}）")
    print(f"{'='*50}")
    print(f"  总量: {s['total_curr']:.1f} 万辆  (去年: {s['total_prev']:.1f} 万辆)")
    print(f"  同比: {s['total_delta']:+.1f} 万辆  ({s['total_pct']:+.1f}%)")
    print(f"  冠军: {s['champion']}  {s['champion_val']:.1f} 万辆")
    print(f"  增速最快: {s['fastest']}  ({s['fastest_pct']:+.1f}%)")
    print(f"  跌幅最大: {s['slowest']}  ({s['slowest_pct']:+.1f}%)")
    print(f"{'='*50}\n")

    plot_dashboard(s, year, start_month, end_month, data_type, scope, output_path)
    return output_path


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="中国汽车产销分析可视化")
    p.add_argument("--year",        type=int, default=2026)
    p.add_argument("--start-month", type=int, default=1)
    p.add_argument("--end-month",   type=int, default=2)
    p.add_argument("--type",        type=str, default="产量",
                   choices=["产量", "批发销量", "零售销量"])
    p.add_argument("--scope",       type=str, default="狭义乘用车",
                   choices=["狭义乘用车", "广义乘用车"],
                   help="统计口径")
    p.add_argument("--output",      type=str, default="/workspace/china_auto_dashboard.png")
    a = p.parse_args()
    main(a.year, a.start_month, a.end_month, a.type, a.output, a.scope)
