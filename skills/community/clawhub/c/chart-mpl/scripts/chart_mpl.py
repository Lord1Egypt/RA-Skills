#!/usr/bin/env python3
import argparse
import csv
import math
import os
import re
import sys
from datetime import datetime

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except Exception:
    print("Missing dependency: matplotlib. Install with: python3 -m pip install matplotlib", file=sys.stderr)
    raise SystemExit(3)


def parse_args():
    p = argparse.ArgumentParser(description="Generate clean BI charts (PNG/SVG) from a CSV file.")
    p.add_argument("--csv", required=True, help="Path to CSV file")
    p.add_argument("--xcol", required=True, help="Column name for X axis")
    p.add_argument("--ycol", required=True, help="Column name(s) for Y axis (comma-separated for multi-series)")
    p.add_argument("--kind", choices=["line", "bar", "hbar", "pie", "stacked", "scatter", "area"], default="line", help="Chart type")
    p.add_argument("--title", default="", help="Chart title")
    p.add_argument("--xlabel", default="", help="X axis label")
    p.add_argument("--ylabel", default="", help="Y axis label")
    p.add_argument("--delim", default="", help="CSV delimiter (auto-detect if omitted)")
    p.add_argument("--out", default="", help="Output path — PNG or SVG (default: workspace/exports/images/...)")
    p.add_argument("--top", type=int, default=0, help="Show only top N categories (bar, hbar, pie, stacked). Multi-series ranks by row total.")
    p.add_argument("--sort", choices=["x-asc", "x-desc", "y-desc", "none"], default="none", help="Sort data before plotting (useful for line/area)")
    p.add_argument("--numfmt", choices=["fr", "en"], default="fr", help="Number format on Y axis: fr (1,5M) or en (1.5M)")
    return p.parse_args()


def default_out(name_hint: str) -> str:
    base = os.path.expanduser("~/.openclaw/workspace/exports/images")
    os.makedirs(base, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in (name_hint or "chart"))
    return os.path.join(base, f"{safe}_{stamp}.png")


def detect_dialect(path: str, delim: str):
    if delim:
        dialect = csv.excel()
        dialect.delimiter = delim
        return dialect
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        try:
            return csv.Sniffer().sniff(sample, delimiters=";,\t|")
        except csv.Error:
            dialect = csv.excel()
            dialect.delimiter = ";"
            return dialect


def read_csv(path: str, delim: str):
    dialect = detect_dialect(path, delim)
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect)
        rows = list(reader)
    return reader.fieldnames or [], rows


def to_float(raw):
    s = str(raw or "").strip()
    if not s:
        return float("nan")

    # Normalize spaces and decimal separators (supports 1 234,56 and 1,234.56)
    s = s.replace("\u202f", "").replace("\xa0", "").replace(" ", "")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "")
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")

    # Accounting negatives: (1234.56) → -1234.56
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]

    # Keep numeric chars only where possible
    s = re.sub(r"[^0-9.+-eE]", "", s)
    return float(s)


PALETTE = ["#2E6F95", "#E8833A", "#4CA352", "#D94F4F", "#8E6DBF", "#C9A830", "#2AAFCF", "#E36BA0"]


def extract_series(rows, ycol_name):
    values = []
    bad = 0
    for r in rows:
        try:
            v = to_float(r.get(ycol_name, ""))
        except Exception:
            v = float("nan")
        if math.isnan(v):
            bad += 1
        values.append(v)
    if bad == len(values):
        raise SystemExit(f"All values in '{ycol_name}' are non-numeric")
    if bad > 0:
        print(f"Warning: {bad} non-numeric values in '{ycol_name}' converted to NaN", file=sys.stderr)
    return values


def human_tick_formatter(locale="fr"):
    """Return a matplotlib FuncFormatter that renders 1500000 as 1,5M (fr) or 1.5M (en)."""
    dec = "," if locale == "fr" else "."
    def fmt(val, _pos):
        aval = abs(val)
        sign = "-" if val < 0 else ""
        if aval >= 1_000_000_000:
            s = f"{aval / 1_000_000_000:.1f}".replace(".", dec) + "G"
        elif aval >= 1_000_000:
            s = f"{aval / 1_000_000:.1f}".replace(".", dec) + "M"
        elif aval >= 1_000:
            s = f"{aval / 1_000:.1f}".replace(".", dec) + "K"
        else:
            s = f"{aval:g}"
            if dec == "," and "." in s:
                s = s.replace(".", ",")
        # Strip trailing zero after decimal: 1,0M → 1M
        s = re.sub(r"[,.]0([KMG])", r"\1", s)
        return sign + s
    return fmt


def apply_top_n(x, series, ycols, top_n):
    """Keep only the top_n rows ranked by row total (sum across all Y columns)."""
    totals = []
    for i in range(len(x)):
        row_sum = sum(series[yc][i] for yc in ycols if not math.isnan(series[yc][i]))
        totals.append((row_sum, i))
    totals.sort(key=lambda t: t[0], reverse=True)
    keep = sorted([idx for _, idx in totals[:top_n]])
    x_new = [x[i] for i in keep]
    series_new = {yc: [series[yc][i] for i in keep] for yc in ycols}
    return x_new, series_new


def apply_top_n_pie(x, series, ycol, top_n):
    """Keep top_n rows by ycol value, aggregate the rest into 'Other'."""
    vals = series[ycol]
    indexed = [(vals[i] if not math.isnan(vals[i]) else 0.0, i) for i in range(len(x))]
    indexed.sort(key=lambda t: t[0], reverse=True)
    keep = [idx for _, idx in indexed[:top_n]]
    rest = [idx for _, idx in indexed[top_n:]]
    x_new = [x[i] for i in keep]
    series_new = {ycol: [vals[i] for i in keep]}
    other_total = sum(vals[i] for i in rest if not math.isnan(vals[i]) and vals[i] > 0)
    if other_total > 0:
        x_new.append("Other")
        series_new[ycol].append(other_total)
    return x_new, series_new


def apply_sort(x, series, ycols, mode):
    """Sort data rows by the given mode."""
    indices = list(range(len(x)))
    if mode == "x-asc":
        indices.sort(key=lambda i: x[i])
    elif mode == "x-desc":
        indices.sort(key=lambda i: x[i], reverse=True)
    elif mode == "y-desc":
        # Sort by first ycol descending
        indices.sort(key=lambda i: (series[ycols[0]][i] if not math.isnan(series[ycols[0]][i]) else float("-inf")), reverse=True)
    else:
        return x, series
    x_new = [x[i] for i in indices]
    series_new = {yc: [series[yc][i] for i in indices] for yc in ycols}
    return x_new, series_new


def main():
    a = parse_args()
    cols, rows = read_csv(a.csv, a.delim)

    if not rows:
        raise SystemExit("Empty dataset: CSV has 0 rows")

    ycols = [c.strip() for c in a.ycol.split(",")]

    if a.xcol not in cols:
        raise SystemExit(f"X column '{a.xcol}' not found. Available: {cols}")
    missing = [c for c in ycols if c not in cols]
    if missing:
        raise SystemExit(f"Y column(s) {missing} not found. Available: {cols}")

    if a.kind == "stacked" and len(ycols) < 2:
        raise SystemExit("Stacked chart requires at least 2 Y columns (comma-separated --ycol)")

    x = [r.get(a.xcol, "") for r in rows]
    series = {yc: extract_series(rows, yc) for yc in ycols}

    # Apply --top N (bar, hbar, pie, stacked)
    if a.top > 0 and a.kind in ("bar", "hbar", "pie", "stacked"):
        if a.kind == "pie":
            x, series = apply_top_n_pie(x, series, ycols[0], a.top)
        else:
            x, series = apply_top_n(x, series, ycols, a.top)

    # Apply --sort
    if a.sort != "none":
        x, series = apply_sort(x, series, ycols, a.sort)

    out = a.out.strip() or default_out(a.title or f"{'_'.join(ycols)}_by_{a.xcol}")
    out_dir = os.path.dirname(out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    multi = len(ycols) > 1

    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.figure(figsize=(10, 5), dpi=160)
    ax = plt.gca()

    if a.kind == "pie":
        y = series[ycols[0]]
        valid = [(lbl, v) for lbl, v in zip(x, y) if not math.isnan(v) and v > 0]
        if not valid:
            raise SystemExit("Pie chart requires at least one positive value")
        labels, values = zip(*valid)
        colors = [PALETTE[i % len(PALETTE)] for i in range(len(values))]
        ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
        ax.set_aspect("equal")
    elif a.kind == "hbar":
        if multi:
            positions = np.arange(len(x))
            bar_h = 0.8 / len(ycols)
            for i, yc in enumerate(ycols):
                offsets = positions + i * bar_h - 0.4 + bar_h / 2
                ax.barh(offsets, series[yc], height=bar_h, color=PALETTE[i % len(PALETTE)], label=yc)
            ax.set_yticks(positions)
            ax.set_yticklabels(x)
        else:
            ax.barh(x, series[ycols[0]], color=PALETTE[0])
        ax.set_xlabel(a.ylabel or ", ".join(ycols), fontsize=11)
        ax.set_ylabel(a.xlabel or a.xcol, fontsize=11)
        ax.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.5)
    elif a.kind == "stacked":
        bottom = [0.0] * len(x)
        for i, yc in enumerate(ycols):
            y = series[yc]
            safe_y = [v if not math.isnan(v) else 0.0 for v in y]
            color = PALETTE[i % len(PALETTE)]
            ax.bar(x, safe_y, bottom=bottom, color=color, label=yc)
            bottom = [b + v for b, v in zip(bottom, safe_y)]
        ax.set_xlabel(a.xlabel or a.xcol, fontsize=11)
        ax.set_ylabel(a.ylabel or ", ".join(ycols), fontsize=11)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.tick_params(axis="x", labelrotation=35)
    elif a.kind == "scatter":
        for i, yc in enumerate(ycols):
            color = PALETTE[i % len(PALETTE)]
            ax.scatter(x, series[yc], color=color, s=40, label=yc if multi else None)
        ax.set_xlabel(a.xlabel or a.xcol, fontsize=11)
        ax.set_ylabel(a.ylabel or ", ".join(ycols), fontsize=11)
        ax.grid(True, axis="both", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.tick_params(axis="x", labelrotation=35)
    elif a.kind == "area":
        for i, yc in enumerate(ycols):
            color = PALETTE[i % len(PALETTE)]
            ax.fill_between(range(len(x)), series[yc], alpha=0.35, color=color, label=yc)
            ax.plot(range(len(x)), series[yc], linewidth=1.5, color=color)
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x)
        ax.set_xlabel(a.xlabel or a.xcol, fontsize=11)
        ax.set_ylabel(a.ylabel or ", ".join(ycols), fontsize=11)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.tick_params(axis="x", labelrotation=35)
    elif a.kind == "bar":
        if multi:
            positions = np.arange(len(x))
            bar_w = 0.8 / len(ycols)
            for i, yc in enumerate(ycols):
                offsets = positions + i * bar_w - 0.4 + bar_w / 2
                ax.bar(offsets, series[yc], width=bar_w, color=PALETTE[i % len(PALETTE)], label=yc)
            ax.set_xticks(positions)
            ax.set_xticklabels(x)
        else:
            ax.bar(x, series[ycols[0]], color=PALETTE[0])
        ax.set_xlabel(a.xlabel or a.xcol, fontsize=11)
        ax.set_ylabel(a.ylabel or ", ".join(ycols), fontsize=11)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.tick_params(axis="x", labelrotation=35)
    else:  # line
        for i, yc in enumerate(ycols):
            color = PALETTE[i % len(PALETTE)]
            ax.plot(x, series[yc], marker="o", linewidth=2.2, color=color, label=yc if multi else None)
        ax.set_xlabel(a.xlabel or a.xcol, fontsize=11)
        ax.set_ylabel(a.ylabel or ", ".join(ycols), fontsize=11)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.tick_params(axis="x", labelrotation=35)

    if a.title:
        ax.set_title(a.title, fontsize=14, fontweight="bold")
    if multi or a.kind == "stacked":
        ax.legend(fontsize=10)

    # Human-readable tick formatting (skip pie)
    if a.kind != "pie":
        from matplotlib.ticker import FuncFormatter
        hfmt = FuncFormatter(human_tick_formatter(a.numfmt))
        if a.kind == "hbar":
            ax.xaxis.set_major_formatter(hfmt)
        else:
            ax.yaxis.set_major_formatter(hfmt)

    ax.margins(x=0.02)

    plt.tight_layout()
    plt.savefig(out, bbox_inches="tight")
    print(out)


if __name__ == "__main__":
    main()
