"""Aggregates and matplotlib chart export (dashboard-style, multi-chart)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.gridspec import GridSpec

from db import (
    aggregate_by_category,
    daily_totals,
    get_connection,
    monthly_totals,
    totals,
)

_CJK_FONT_CANDIDATES = (
    "PingFang SC",
    "Hiragino Sans GB",
    "Heiti SC",
    "STHeiti",
    "Songti SC",
    "Arial Unicode MS",
    "Microsoft YaHei",
    "SimHei",
    "Microsoft JhengHei",
    "Noto Sans CJK SC",
    "Noto Sans SC",
    "Source Han Sans SC",
    "WenQuanYi Micro Hei",
    "WenQuanYi Zen Hei",
    "Droid Sans Fallback",
)

# 与看板 dashboard 接近的配色
BG = "#080a0e"
PANEL = "#121822"
TEXT = "#e8ecf4"
MUTED = "#8b95a8"
ACCENT_TEAL = "#5eead4"
INCOME = "#34d399"
EXPENSE = "#fb923c"
PALETTE_EXP = [
    "#5eead4",
    "#a78bfa",
    "#fb923c",
    "#38bdf8",
    "#f472b6",
    "#facc15",
    "#4ade80",
    "#f87171",
    "#818cf8",
    "#94a3b8",
]
PALETTE_INC = [
    "#34d399",
    "#6ee7b7",
    "#2dd4bf",
    "#5eead4",
    "#a7f3d0",
    "#4ade80",
    "#22c55e",
    "#10b981",
]


def _configure_cjk_font() -> None:
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in _CJK_FONT_CANDIDATES:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            plt.rcParams["font.family"] = "sans-serif"
            plt.rcParams["axes.unicode_minus"] = False
            return
    for f in font_manager.fontManager.ttflist:
        n = f.name
        if "CJK" in n or "Han Sans" in n or "WenQuanYi" in n:
            plt.rcParams["font.sans-serif"] = [n, "DejaVu Sans"]
            plt.rcParams["font.family"] = "sans-serif"
            plt.rcParams["axes.unicode_minus"] = False
            return
    plt.rcParams["axes.unicode_minus"] = False


_configure_cjk_font()


def _style_axis_dark(ax: Any, *, panel: bool = True) -> None:
    ax.set_facecolor(PANEL if panel else BG)
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#2f3b4e")
    ax.title.set_color(TEXT)
    if hasattr(ax, "xaxis") and ax.get_xlabel():
        ax.xaxis.label.set_color(MUTED)
    if hasattr(ax, "yaxis") and ax.get_ylabel():
        ax.yaxis.label.set_color(MUTED)


def _donut(
    ax: Any,
    labels: list[str],
    sizes: list[float],
    title: str,
    colors: list[str],
    empty_msg: str,
) -> None:
    ax.set_facecolor(PANEL)
    if not sizes or sum(sizes) <= 0:
        ax.text(0.5, 0.5, empty_msg, ha="center", va="center", color=MUTED, fontsize=11)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title(title, color=TEXT, fontsize=12, fontweight="bold", pad=8)
        return
    cols = [colors[i % len(colors)] for i in range(len(sizes))]
    wedges, _texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        colors=cols,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5, edgecolor=PANEL, linewidth=1.5),
    )
    for t in autotexts:
        t.set_color(TEXT)
        t.set_fontsize(8)
    ax.legend(
        wedges,
        labels,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        fontsize=8,
        frameon=False,
        labelcolor=TEXT,
    )
    ax.set_title(title, color=TEXT, fontsize=12, fontweight="bold", pad=8)
    ax.axis("equal")


def _daily_trend(ax: Any, daily: list[dict[str, Any]]) -> None:
    ax.set_facecolor(PANEL)
    if not daily:
        ax.text(0.5, 0.5, "暂无每日数据", ha="center", va="center", color=MUTED)
        ax.axis("off")
        ax.set_title("每日收支", color=TEXT, fontsize=12, fontweight="bold", pad=8)
        return
    n = len(daily)
    xs = list(range(n))
    labels = [d["date"] for d in daily]
    inc = [d["income"] for d in daily]
    exp = [d["expense"] for d in daily]
    ax.fill_between(xs, inc, alpha=0.25, color=INCOME)
    ax.fill_between(xs, exp, alpha=0.22, color=EXPENSE)
    ax.plot(xs, inc, color=INCOME, linewidth=2, marker="o", markersize=3, label="收入")
    ax.plot(xs, exp, color=EXPENSE, linewidth=2, marker="o", markersize=3, label="支出")
    step = max(1, len(labels) // 12)
    ax.set_xticks(xs[::step])
    ax.set_xticklabels([labels[i] for i in range(0, len(labels), step)], rotation=45, ha="right")
    ax.legend(loc="upper right", frameon=False, labelcolor=TEXT, fontsize=9)
    ax.set_title("每日收支趋势", color=TEXT, fontsize=12, fontweight="bold", pad=8)
    ax.grid(True, alpha=0.15, color=MUTED)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"¥{v:,.0f}"))
    _style_axis_dark(ax)


def _monthly_bars(ax: Any, monthly: list[dict[str, Any]]) -> None:
    ax.set_facecolor(PANEL)
    if not monthly:
        ax.text(0.5, 0.5, "暂无按月数据", ha="center", va="center", color=MUTED)
        ax.axis("off")
        ax.set_title("按月汇总", color=TEXT, fontsize=12, fontweight="bold", pad=8)
        return
    months = [m["month"] for m in monthly]
    x = list(range(len(months)))
    w = 0.36
    inc = [m["income"] for m in monthly]
    exp = [m["expense"] for m in monthly]
    x_left = [i - w / 2 for i in x]
    x_right = [i + w / 2 for i in x]
    ax.bar(x_left, inc, width=w, label="收入", color=INCOME, edgecolor=PANEL, linewidth=0.5)
    ax.bar(x_right, exp, width=w, label="支出", color=EXPENSE, edgecolor=PANEL, linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.legend(loc="upper right", frameon=False, labelcolor=TEXT, fontsize=9)
    ax.set_title("按月汇总（收入 vs 支出）", color=TEXT, fontsize=12, fontweight="bold", pad=8)
    ax.grid(True, axis="y", alpha=0.15, color=MUTED)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"¥{v:,.0f}"))
    _style_axis_dark(ax)


def _save_single_charts(
    out_dir: Path,
    expense_rows: list[dict[str, Any]],
    income_rows: list[dict[str, Any]],
    daily: list[dict[str, Any]],
    monthly: list[dict[str, Any]],
    expense_total: float,
    income_total: float,
) -> dict[str, Path]:
    paths: dict[str, Path] = {}

    p_exp = out_dir / "expense_by_category.png"
    fig, ax = plt.subplots(figsize=(8, 7), facecolor=BG)
    labels_e = [r["category"] for r in expense_rows]
    sizes_e = [float(r["total"]) for r in expense_rows]
    _donut(ax, labels_e, sizes_e, "支出分类占比", PALETTE_EXP, "暂无支出数据")
    fig.patch.set_facecolor(BG)
    fig.savefig(p_exp, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    paths["expense_by_category"] = p_exp

    p_inc = out_dir / "income_by_category.png"
    fig, ax = plt.subplots(figsize=(8, 7), facecolor=BG)
    labels_i = [r["category"] for r in income_rows]
    sizes_i = [float(r["total"]) for r in income_rows]
    _donut(ax, labels_i, sizes_i, "收入分类占比", PALETTE_INC, "暂无收入数据")
    fig.patch.set_facecolor(BG)
    fig.savefig(p_inc, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    paths["income_by_category"] = p_inc

    p_daily = out_dir / "daily_trend.png"
    fig, ax = plt.subplots(figsize=(12, 4.5), facecolor=BG)
    _daily_trend(ax, daily)
    fig.patch.set_facecolor(BG)
    fig.savefig(p_daily, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    paths["daily_trend"] = p_daily

    p_mon = out_dir / "monthly_bar.png"
    fig, ax = plt.subplots(figsize=(12, 4.5), facecolor=BG)
    _monthly_bars(ax, monthly)
    fig.patch.set_facecolor(BG)
    fig.savefig(p_mon, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    paths["monthly_bar"] = p_mon

    return paths


def _save_dashboard_composite(
    out_dir: Path,
    *,
    date_from: str | None,
    date_to: str | None,
    t: dict[str, float],
    expense_rows: list[dict[str, Any]],
    income_rows: list[dict[str, Any]],
    daily: list[dict[str, Any]],
    monthly: list[dict[str, Any]],
) -> Path:
    path = out_dir / "report_dashboard.png"
    fig = plt.figure(figsize=(14, 18), facecolor=BG)
    gs = GridSpec(
        4,
        2,
        figure=fig,
        height_ratios=[0.14, 1.0, 1.15, 1.15],
        width_ratios=[1, 1],
        hspace=0.42,
        wspace=0.28,
        left=0.07,
        right=0.94,
        top=0.96,
        bottom=0.04,
    )

    ax_head = fig.add_subplot(gs[0, :])
    ax_head.set_facecolor(BG)
    ax_head.axis("off")
    rng = f"{date_from or '…'}  ~  {date_to or '…'}"
    ax_head.text(
        0.0,
        0.92,
        "BillClaw 收支报表",
        fontsize=18,
        color=TEXT,
        fontweight="bold",
        transform=ax_head.transAxes,
        va="top",
    )
    ax_head.text(
        0.0,
        0.55,
        f"统计区间：{rng}",
        fontsize=11,
        color=MUTED,
        transform=ax_head.transAxes,
        va="top",
    )
    kpi = (
        f"总收入  ¥{t['income']:,.2f}          "
        f"总支出  ¥{t['expense']:,.2f}          "
        f"净结余  ¥{t['balance']:,.2f}"
    )
    ax_head.text(
        0.0,
        0.12,
        kpi,
        fontsize=13,
        color=ACCENT_TEAL,
        transform=ax_head.transAxes,
        va="top",
        fontweight="bold",
    )

    ax_e = fig.add_subplot(gs[1, 0])
    labels_e = [r["category"] for r in expense_rows]
    sizes_e = [float(r["total"]) for r in expense_rows]
    _donut(ax_e, labels_e, sizes_e, "支出分类", PALETTE_EXP, "暂无支出")

    ax_i = fig.add_subplot(gs[1, 1])
    labels_i = [r["category"] for r in income_rows]
    sizes_i = [float(r["total"]) for r in income_rows]
    _donut(ax_i, labels_i, sizes_i, "收入分类", PALETTE_INC, "暂无收入")

    ax_d = fig.add_subplot(gs[2, :])
    _daily_trend(ax_d, daily)

    ax_m = fig.add_subplot(gs[3, :])
    _monthly_bars(ax_m, monthly)

    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return path


def build_report(
    *,
    db_path: Path | str | None,
    date_from: str | None,
    date_to: str | None,
    output_dir: Path | str | None = None,
) -> dict[str, Any]:
    out_dir = Path(output_dir) if output_dir else Path.cwd() / "billclaw_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    with get_connection(db_path) as conn:
        t = totals(conn, date_from=date_from, date_to=date_to)
        by_cat = aggregate_by_category(conn, date_from=date_from, date_to=date_to)
        daily = daily_totals(conn, date_from=date_from, date_to=date_to)
        monthly = monthly_totals(conn, date_from=date_from, date_to=date_to)

    expense_rows = [r for r in by_cat if r["type"] == "支出"]
    income_rows = [r for r in by_cat if r["type"] == "收入"]
    expense_total = t["expense"]
    income_total = t["income"]

    single = _save_single_charts(
        out_dir,
        expense_rows,
        income_rows,
        daily,
        monthly,
        expense_total,
        income_total,
    )
    composite = _save_dashboard_composite(
        out_dir,
        date_from=date_from,
        date_to=date_to,
        t=t,
        expense_rows=expense_rows,
        income_rows=income_rows,
        daily=daily,
        monthly=monthly,
    )

    top_expense = sorted(expense_rows, key=lambda x: x["total"], reverse=True)[:5]
    highlights = {
        "totals": t,
        "top_expense_categories": [
            {
                "category": r["category"],
                "total": float(r["total"]),
                "share_of_expense": float(r["total"] / expense_total)
                if expense_total > 0
                else 0.0,
                "count": int(r["cnt"]),
            }
            for r in top_expense
        ],
        "income_breakdown": [
            {"category": r["category"], "total": float(r["total"])} for r in income_rows
        ],
        "daily_points": len(daily),
        "months_in_range": len(monthly),
    }

    narrative_hints = _narrative_hints(highlights)

    charts_resolved = {k: str(v.resolve()) for k, v in single.items()}
    charts_resolved["report_dashboard"] = str(composite.resolve())
    # 兼容旧字段名（Agent / 文档可能仍引用）
    charts_resolved["expense_pie"] = charts_resolved["expense_by_category"]
    charts_resolved["trend"] = charts_resolved["daily_trend"]

    return {
        "charts": charts_resolved,
        "highlights": highlights,
        "narrative_hints": narrative_hints,
        "range": {"date_from": date_from, "date_to": date_to},
    }


def _narrative_hints(highlights: dict[str, Any]) -> list[str]:
    hints: list[str] = []
    te = highlights.get("top_expense_categories") or []
    if te:
        top = te[0]
        hints.append(
            f"支出第一大类是「{top['category']}」，约 {top['share_of_expense']*100:.1f}% 的支出来自这里。"
        )
    tot = highlights.get("totals") or {}
    bal = tot.get("balance")
    if bal is not None:
        if bal >= 0:
            hints.append(f"期内净结余为正（约 {bal:.2f} 元），可以夸一句会过日子。")
        else:
            hints.append(f"期内净结余为负（约 {bal:.2f} 元），适合温柔提醒控制大额支出。")
    return hints


def highlights_json_for_agent(report: dict[str, Any]) -> str:
    return json.dumps(
        {
            "totals": report["highlights"]["totals"],
            "top_expense": report["highlights"]["top_expense_categories"],
            "narrative_hints": report["narrative_hints"],
            "charts": report["charts"],
            "primary_chart": report["charts"].get("report_dashboard"),
        },
        ensure_ascii=False,
        indent=2,
    )
