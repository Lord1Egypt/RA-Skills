#!/usr/bin/env python3
"""Build book-derived examples as PNG, vector PDF/SVG, and Bokeh HTML."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure, output_file, save
from bokeh.resources import CDN
from matplotlib.colors import LinearSegmentedColormap

from storytelling_style import (
    BLUE,
    CONTEXT,
    GRID,
    INK,
    MUTED,
    ORANGE,
    SEQUENTIAL_BLUE,
    VERMILLION,
    add_source,
    apply_style,
    clean_axes,
    save_figure,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "assets" / "data"
BOOK_SOURCE = "Source: Knaflic, Storytelling with Data (2015); values transcribed from printed figures."


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


def build_employee_survey(output_dir: Path) -> list[Path]:
    df = read_csv("employee_survey.csv")
    years = [2014, 2015]
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for row in df.itertuples(index=False):
        values = [row.score_2014, row.score_2015]
        color = BLUE if row.topic in {"Peers", "Culture"} else CONTEXT
        width = 2.4 if color == BLUE else 1.3
        ax.plot(years, values, color=color, linewidth=width, marker="o", markersize=5, zorder=2)
        ax.text(2014 - 0.025, row.score_2014, f"{row.topic}  {row.score_2014}%", ha="right", va="center", color=INK, fontsize=9)
        ax.text(2015 + 0.025, row.score_2015, f"{row.score_2015}%  {row.topic}", ha="left", va="center", color=INK, fontsize=9)
    ax.set_xlim(2013.58, 2015.42)
    ax.set_ylim(25, 101)
    ax.set_xticks(years)
    ax.set_yticks([])
    ax.set_title("Peers and culture scores improved most", loc="left", pad=16)
    ax.text(2013.58, 103.5, "Employee survey favorable responses", color=MUTED, fontsize=10)
    clean_axes(ax, grid=None)
    add_source(fig, BOOK_SOURCE)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    return save_figure(fig, output_dir, "employee_survey_slopegraph")


def build_heatmap(output_dir: Path) -> list[Path]:
    df = read_csv("category_heatmap.csv")
    matrix = df.pivot(index="category", columns="series", values="percent")
    row_order = [f"Category {i}" for i in range(1, 7)]
    matrix = matrix.reindex(index=row_order, columns=["A", "B", "C"])
    cmap = LinearSegmentedColormap.from_list("story_blue", SEQUENTIAL_BLUE)
    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    sns.heatmap(
        matrix,
        ax=ax,
        cmap=cmap,
        vmin=0,
        vmax=60,
        annot=True,
        fmt=".0f",
        linewidths=1.5,
        linecolor="white",
        cbar_kws={"label": "Percent"},
    )
    ax.set_title("Category 5 has the highest combined score", loc="left", pad=16)
    ax.set_xlabel("Series")
    ax.set_ylabel("")
    ax.tick_params(axis="y", rotation=0)
    add_source(fig, BOOK_SOURCE)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    return save_figure(fig, output_dir, "category_heatmap")


def build_supplier_share(output_dir: Path) -> list[Path]:
    df = read_csv("supplier_market_share.csv").sort_values("share", ascending=False)
    colors = [BLUE] + [CONTEXT] * (len(df) - 1)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    bars = ax.barh(df["supplier"], df["share"], color=colors, height=0.62)
    ax.invert_yaxis()
    ax.set_xlim(0, 40)
    ax.set_xlabel("Market share (%)")
    ax.set_title("Supplier A leads, but only narrowly", loc="left", pad=16)
    ax.bar_label(bars, labels=[f"{v:.0f}%" for v in df["share"]], padding=5, color=INK)
    clean_axes(ax, grid="x")
    add_source(fig, BOOK_SOURCE)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    outputs = save_figure(fig, output_dir, "supplier_market_share")
    outputs.append(build_supplier_bokeh(df, output_dir))
    return outputs


def build_supplier_bokeh(df: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    bokeh_df = df.copy()
    bokeh_df["label"] = bokeh_df["share"].map(lambda value: f"{value:.0f}%")
    bokeh_df["color"] = [BLUE] + [CONTEXT] * (len(bokeh_df) - 1)
    source = ColumnDataSource(bokeh_df)
    p = figure(
        y_range=list(reversed(bokeh_df["supplier"].tolist())),
        x_range=(0, 40),
        width=760,
        height=420,
        title="Supplier A leads, but only narrowly",
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )
    p.hbar(y="supplier", right="share", height=0.62, color="color", source=source)
    p.add_tools(HoverTool(tooltips=[("Supplier", "@supplier"), ("Share", "@share{0}%")]))
    p.add_layout(LabelSet(x="share", y="supplier", text="label", x_offset=7, text_baseline="middle", source=source, text_color=INK))
    p.xaxis.axis_label = "Market share (%)"
    p.ygrid.grid_line_color = None
    p.xgrid.grid_line_color = GRID
    p.outline_line_color = None
    p.title.text_font_size = "16px"
    p.title.text_color = INK
    path = output_dir / "supplier_market_share.html"
    output_file(path, title="Supplier market share")
    save(p, resources=CDN)
    return path


def build_waterfall(output_dir: Path) -> list[Path]:
    df = read_csv("headcount_waterfall.csv")
    start = float(df.loc[df["step"] == "Start", "value"].iloc[0])
    stated_end = float(df.loc[df["step"] == "End", "value"].iloc[0])
    deltas = df.loc[df["kind"] == "delta", "value"]
    calculated_end = start + deltas.sum()
    if abs(calculated_end - stated_end) > 1e-9:
        raise ValueError(f"Waterfall does not reconcile: calculated {calculated_end}, stated {stated_end}")

    bottoms: list[float] = []
    heights: list[float] = []
    colors: list[str] = []
    running = 0.0
    for row in df.itertuples(index=False):
        if row.step == "Start":
            running = float(row.value)
            bottoms.append(0)
            heights.append(running)
            colors.append(INK)
        elif row.step == "End":
            bottoms.append(0)
            heights.append(float(row.value))
            colors.append(INK)
        else:
            change = float(row.value)
            bottoms.append(running if change >= 0 else running + change)
            heights.append(abs(change))
            colors.append(BLUE if change >= 0 else VERMILLION)
            running += change

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    positions = list(range(len(df)))
    bars = ax.bar(positions, heights, bottom=bottoms, color=colors, width=0.68)
    for i in range(len(df) - 1):
        if df.iloc[i]["step"] == "End":
            continue
        level = start if i == 0 else start + df.loc[1:i, "value"].sum()
        ax.plot([i + 0.34, i + 1 - 0.34], [level, level], color=CONTEXT, linewidth=1)
    labels = []
    for row in df.itertuples(index=False):
        if row.kind == "delta":
            labels.append(f"{row.value:+.0f}")
        else:
            labels.append(f"{row.value:.0f}")
    ax.bar_label(bars, labels=labels, padding=4, color=INK)
    ax.set_xticks(positions, df["step"])
    ax.set_ylim(0, 150)
    ax.set_ylabel("Employees")
    ax.set_title("Hiring lifted headcount from 100 to 116", loc="left", pad=16)
    clean_axes(ax, grid="y")
    add_source(fig, BOOK_SOURCE)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    return save_figure(fig, output_dir, "headcount_waterfall")


def build_tax_rates(output_dir: Path) -> list[Path]:
    df = read_csv("tax_rates.csv")
    fig, ax = plt.subplots(figsize=(5.8, 4.5))
    bars = ax.bar(df["period"], df["rate"], color=[CONTEXT, BLUE], width=0.58)
    ax.set_ylim(0, 45)
    ax.set_ylabel("Tax rate (%)")
    ax.set_title("The proposed rate is 4.6 points higher", loc="left", pad=16)
    ax.bar_label(bars, labels=[f"{value:.1f}%" for value in df["rate"]], padding=4, color=INK)
    clean_axes(ax, grid="y")
    add_source(fig, BOOK_SOURCE)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    return save_figure(fig, output_dir, "tax_rate_zero_baseline")


def build_small_multiples(output_dir: Path) -> list[Path]:
    df = read_csv("revenue_sales_staff.csv")
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 5.8), sharex=True)
    x = range(len(df))
    axes[0].plot(x, df["revenue_millions"], color=BLUE, linewidth=2.4)
    axes[0].scatter(x, df["revenue_millions"], color=BLUE, s=22, zorder=3)
    axes[0].set_ylabel("Revenue ($M)")
    axes[0].set_ylim(0, 1.1)
    axes[1].plot(x, df["sales_employees"], color=ORANGE, linewidth=2.4)
    axes[1].scatter(x, df["sales_employees"], color=ORANGE, s=22, zorder=3)
    axes[1].set_ylabel("Sales employees")
    axes[1].set_ylim(75, 120)
    axes[1].set_xticks(list(x), df["quarter"])
    axes[1].tick_params(axis="x", rotation=35)
    axes[0].set_title("In 2014, revenue rose while sales staffing stayed flat", loc="left", pad=16)
    for ax in axes:
        clean_axes(ax, grid="y")
    axes[0].annotate("$1.0M", (7, 1.0), xytext=(5, 8), textcoords="offset points", color=BLUE, weight="bold")
    axes[1].annotate("110", (7, 110), xytext=(5, 8), textcoords="offset points", color=ORANGE, weight="bold")
    add_source(fig, BOOK_SOURCE)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    return save_figure(fig, output_dir, "revenue_staff_small_multiples")


BUILDERS = {
    "employee-survey": build_employee_survey,
    "heatmap": build_heatmap,
    "supplier-share": build_supplier_share,
    "waterfall": build_waterfall,
    "tax-rates": build_tax_rates,
    "small-multiples": build_small_multiples,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=BASE_DIR / "assets" / "examples",
        help="Directory for generated PNG, PDF, SVG, and HTML files.",
    )
    parser.add_argument(
        "--only",
        choices=["all", *BUILDERS.keys()],
        default="all",
        help="Build one example or all examples.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    apply_style()
    selected = BUILDERS.items() if args.only == "all" else [(args.only, BUILDERS[args.only])]
    outputs: list[Path] = []
    for _, builder in selected:
        outputs.extend(builder(args.output_dir))
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
