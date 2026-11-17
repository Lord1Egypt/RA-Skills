#!/usr/bin/env python3
"""
Excel2Insights — Chart Generator
Generate visualization charts from structured data.
Supports: histogram, boxplot, bar, line, pie, correlation heatmap, scatter, pairplot.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    print(json.dumps({"error": "Missing dependencies. Install: pandas, matplotlib, seaborn"}))
    sys.exit(1)


# Theme configuration
THEME_CLEAN = {
    "figure.dpi": 150,
    "figure.figsize": (10, 6),
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.sans-serif": ["Arial", "DejaVu Sans", "sans-serif"],
}

sns.set_style("whitegrid")


def load_data(filepath, sheet=None, encoding="utf-8"):
    ext = Path(filepath).suffix.lower()
    if ext in (".xlsx", ".xls"):
        if sheet:
            return pd.read_excel(filepath, sheet_name=sheet)
        xls = pd.ExcelFile(filepath)
        return pd.read_excel(filepath, sheet_name=xls.sheet_names[0])
    elif ext == ".tsv":
        return pd.read_csv(filepath, sep="\t", encoding=encoding)
    else:
        return pd.read_csv(filepath, encoding=encoding)


def generate_charts(df, chart_types, columns=None, output_dir="output/charts",
                    theme="clean"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    charts = []
    plt.rcParams.update(THEME_CLEAN)

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    date_cols = [c for c in df.columns if df[c].dtype.kind == "M"]

    if columns:
        col_filter = [c for c in columns if c in df.columns]
    else:
        col_filter = None

    target_num = col_filter if col_filter else num_cols
    target_cat = col_filter if col_filter else cat_cols

    chart_map = {
        "histogram": lambda: _histogram(df, target_num, output_dir),
        "boxplot": lambda: _boxplot(df, target_num, output_dir),
        "bar": lambda: _bar(df, target_cat, output_dir),
        "line": lambda: _line(df, num_cols, date_cols, output_dir),
        "pie": lambda: _pie(df, target_cat, output_dir),
        "heatmap": lambda: _heatmap(df, num_cols, output_dir),
        "scatter": lambda: _scatter(df, target_num, output_dir),
        "pairplot": lambda: _pairplot(df, target_num, output_dir),
    }

    for ct in chart_types:
        ct = ct.strip().lower()
        if ct in chart_map:
            try:
                result = chart_map[ct]()
                if result:
                    charts.extend(result)
            except Exception as e:
                print(f"  [WARN] Chart '{ct}' failed: {e}", file=sys.stderr)

    return charts


def _histogram(df, columns, out):
    charts = []
    for col in columns[:8]:
        vals = df[col].dropna()
        if len(vals) < 3:
            continue
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(vals, bins=min(50, int(np.sqrt(len(vals)) * 2)),
                color="#2b6af6", edgecolor="white", alpha=0.85)
        ax.set_title(f"Distribution: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        path = Path(out) / f"{col}_histogram.png"
        fig.savefig(path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        charts.append(str(path))
    return charts


def _boxplot(df, columns, out):
    charts = []
    vals_list = [(c, df[c].dropna()) for c in columns[:10] if len(df[c].dropna()) > 3]
    if not vals_list:
        return charts
    fig, ax = plt.subplots(figsize=(10, max(5, len(vals_list) * 0.5)))
    data = [v[1].values for v in vals_list]
    labels = [v[0] for v in vals_list]
    bp = ax.boxplot(data, labels=labels, patch_artist=True)
    for patch in bp["boxes"]:
        patch.set_facecolor("#2b6af6")
        patch.set_alpha(0.7)
    ax.set_title("Boxplot — Numeric Columns")
    ax.set_ylabel("Value")
    plt.xticks(rotation=45, ha="right")
    path = Path(out) / "boxplot_all.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    charts.append(str(path))
    return charts


def _bar(df, columns, out):
    charts = []
    for col in columns[:6]:
        vals = df[col].dropna().astype(str).value_counts().head(15)
        if len(vals) < 2:
            continue
        fig, ax = plt.subplots(figsize=(9, 5))
        colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(vals)))
        vals.plot(kind="bar", ax=ax, color=colors, edgecolor="white")
        ax.set_title(f"Top {len(vals)} Values: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        path = Path(out) / f"{col}_bar.png"
        fig.savefig(path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        charts.append(str(path))
    return charts


def _line(df, num_cols, date_cols, out):
    charts = []
    if not date_cols or not num_cols:
        return charts
    date_col = date_cols[0]
    df_temp = df[[date_col] + num_cols[:3]].dropna(subset=[date_col]).copy()
    df_temp[date_col] = pd.to_datetime(df_temp[date_col])
    df_sorted = df_temp.sort_values(date_col)
    fig, ax = plt.subplots(figsize=(11, 5))
    for col in num_cols[:3]:
        ax.plot(df_sorted[date_col], df_sorted[col], label=col, linewidth=1.5)
    ax.set_title("Trend Over Time")
    ax.set_xlabel(str(date_col))
    ax.set_ylabel("Value")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    path = Path(out) / "trend_line.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    charts.append(str(path))
    return charts


def _pie(df, columns, out):
    charts = []
    for col in columns[:3]:
        vals = df[col].dropna().astype(str).value_counts().head(8)
        if len(vals) < 2:
            continue
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = plt.cm.Set2(np.linspace(0, 1, len(vals)))
        wedges, texts, autotexts = ax.pie(
            vals.values, labels=vals.index, autopct="%1.1f%%",
            colors=colors, startangle=90
        )
        ax.set_title(f"Proportion: {col}")
        path = Path(out) / f"{col}_pie.png"
        fig.savefig(path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        charts.append(str(path))
    return charts


def _heatmap(df, columns, out):
    if len(columns) < 2:
        return []
    corr = df[columns].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, square=True, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap")
    path = Path(out) / "correlation_heatmap.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [str(path)]


def _scatter(df, columns, out):
    charts = []
    num = [c for c in columns if len(df[c].dropna()) > 10]
    if len(num) >= 2:
        pairs = [(num[i], num[j]) for i in range(min(len(num), 5))
                 for j in range(i + 1, min(len(num), 5))]
        for x_col, y_col in pairs[:6]:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(df[x_col], df[y_col], alpha=0.5, s=20,
                       c="#2b6af6", edgecolors="white", linewidth=0.3)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{x_col} vs {y_col}")
            path = Path(out) / f"scatter_{x_col}_vs_{y_col}.png"
            fig.savefig(path, bbox_inches="tight", dpi=150)
            plt.close(fig)
            charts.append(str(path))
    return charts


def _pairplot(df, columns, out):
    num = [c for c in columns[:6] if len(df[c].dropna()) > 10]
    if len(num) < 2 or len(num) > 6:
        return []
    # Sample if too large
    df_plot = df[num].dropna()
    if len(df_plot) > 3000:
        df_plot = df_plot.sample(3000, random_state=42)
    path = Path(out) / "pairplot.png"
    try:
        g = sns.pairplot(df_plot, diag_kind="kde", plot_kws={"alpha": 0.5, "s": 10})
        g.fig.savefig(str(path), bbox_inches="tight", dpi=150)
        plt.close(g.fig)
        return [str(path)]
    except Exception:
        return []


def main():
    parser = argparse.ArgumentParser(description="Excel2Insights — Chart Generator")
    parser.add_argument("--file", required=True, help="Path to data file")
    parser.add_argument("--sheet", help="Sheet name")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--charts", default="histogram,bar,correlation",
                        help="Comma-separated chart types")
    parser.add_argument("--columns", help="Comma-separated column filter")
    parser.add_argument("--output", default="output/charts", help="Output directory")
    parser.add_argument("--theme", default="clean", help="Chart theme")
    args = parser.parse_args()

    try:
        df = load_data(args.file, args.sheet, args.encoding)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    chart_types = [c.strip() for c in args.charts.split(",")]
    col_filter = args.columns.split(",") if args.columns else None

    charts = generate_charts(df, chart_types, col_filter, args.output, args.theme)

    result = {
        "charts_generated": len(charts),
        "chart_files": charts,
        "output_dir": args.output
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
