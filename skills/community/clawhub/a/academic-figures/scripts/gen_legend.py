#!/usr/bin/env python3
"""Generate journal-format figure legends from the same JSON used by gen_figure.py.

Produces copy-ready legend text ("Figure 1 | Title. ...") with per-panel
sentences, error-bar definitions, and n values inferred from the data.

Usage:
  python gen_legend.py -d data.json -t "Response to treatment" -f 1
  python gen_legend.py -d panels.json --type composite -t "Three-panel summary"
  python gen_legend.py -d data.json -o legend.txt
"""
import argparse
import json
import sys


def _fmt_n(series):
    ns = [len(v) for v in series.values() if isinstance(v, (list, tuple)) and v]
    if not ns:
        return ""
    if len(set(ns)) == 1:
        return f" (n = {ns[0]} per group)."
    return f" (n = {min(ns)}–{max(ns)} per group)."


def _names(names, limit=6):
    if not names:
        return ""
    shown = names[:limit]
    tail = f" and {len(names) - limit} more" if len(names) > limit else ""
    return "; ".join(shown) + tail


def legend_for(data, chart_type, title="", error_type="s.e.m."):
    """Return journal-format legend text for the given data dict."""
    series = data.get("series", data.get("datasets", {}))
    labels = data.get("labels", data.get("x", []))
    errors = data.get("errors", {})
    err_note = ""
    if isinstance(errors, dict) and errors:
        err_note = f" Error bars indicate {error_type.rstrip('.')}."

    if chart_type == "composite":
        panels = data.get("panels", [])
        body = []
        for i, p in enumerate(panels):
            desc = _describe_panel(p, error_type)
            if not desc.endswith("."):
                desc += "."
            body.append(f"{chr(ord('a') + i)}, {desc}")
        return "\n".join([f"Figure: {title + '.' if title else 'Composite figure.'}"] + body)

    if chart_type == "diagram":
        blocks = data.get("blocks", [])
        steps = [b.get("text", b.get("title", "")) for b in blocks if b.get("text") or b.get("title")]
        flow = " → ".join(steps[:8]) if steps else "schematic flow"
        return f"Figure: {title + '. ' if title else ''}Schematic diagram of {flow}."

    if chart_type == "prisma":
        ident = data.get("records_identified", 0)
        inc = data.get("studies_included", 0)
        n_reasons = len(data.get("exclusion_reasons", {}) or {})
        reason_note = (f" Reports were excluded for {n_reasons} prespecified reasons."
                       if n_reasons else "")
        return (f"Figure: {title + '. ' if title else ''}Flow of study identification, "
                f"screening, and inclusion following PRISMA 2020. Of {ident} records "
                f"identified, {inc} studies were included in the review."
                f"{reason_note}")

    if chart_type == "heatmap":
        matrix = data.get("matrix", data.get("data", data.get("values", [])))
        rows = len(matrix) if isinstance(matrix, list) else 0
        cols = len(matrix[0]) if rows and isinstance(matrix[0], list) else 0
        return (f"Figure: {title + '. ' if title else ''}Heatmap of {rows}×{cols} values."
                f"{err_note}")

    if chart_type == "scatter":
        x = data.get("x", data.get("xs", []))
        y = data.get("y", data.get("ys", []))
        n = len(x)
        return (f"Figure: {title + '. ' if title else ''}Scatter plot of y versus x"
                f" (n = {n} points).{err_note}")

    if chart_type in ("forest",):
        estimates = data.get("estimates", data.get("values", []))
        measure = data.get("measure", "effect size")
        het = data.get("heterogeneity", {})
        het_note = ""
        if isinstance(het, dict) and "I2" in het:
            het_note = f" Heterogeneity: I² = {het['I2'] * 100:.0f}%."
        return (f"Figure: {title + '. ' if title else ''}Forest plot of {measure} across "
                f"{len(estimates)} studies.{err_note}{het_note}")

    if chart_type in ("km", "survival"):
        groups = data.get("groups", data.get("series", {}))
        n_groups = len(groups)
        lr = data.get("log_rank", {})
        lr_note = ""
        if isinstance(lr, dict) and "p" in lr:
            lr_note = f" Log-rank P = {lr['p']:g}."
        return (f"Figure: {title + '. ' if title else ''}Kaplan–Meier survival curves for "
                f"{n_groups} group(s).{err_note}{lr_note}")

    if chart_type == "roc":
        curves = data.get("curves", [])
        if curves:
            aucs = [c.get("auc") for c in curves if c.get("auc") is not None]
            auc_note = (f" AUC values: {', '.join(f'{a:.3f}' for a in aucs)}." if aucs else "")
            return f"Figure: {title + '. ' if title else ''}ROC curves for {len(curves)} model(s).{err_note}{auc_note}"
        return f"Figure: {title + '. ' if title else ''}ROC curve.{err_note}"

    if chart_type == "dual_axis":
        left = data.get("left", data.get("y1", {}))
        right = data.get("right", data.get("y2", {}))
        l_names = _names(list(left.keys()))
        r_names = _names(list(right.keys()))
        return (f"Figure: {title + '. ' if title else ''}Dual-axis chart: left axis shows "
                f"{l_names or 'left series'}; right axis shows {r_names or 'right series'}.{err_note}")

    # bar / line / stacked / box / violin share the series-based form
    if series:
        n_series = len(series)
        chart_word = {"bar": "Grouped bar chart", "grouped_bar": "Grouped bar chart",
                      "hbar": "Horizontal bar chart", "horizontal_bar": "Horizontal bar chart",
                      "stacked_bar": "Stacked bar chart", "line": "Line chart",
                      "box": "Box plot", "boxplot": "Box plot", "violin": "Violin plot",
        "raincloud": "雨云图（密度云+箱线+原始点）"}.get(chart_type, "Chart")
        names = _names(list(series.keys()))
        return (f"Figure: {title + '. ' if title else ''}{chart_word} of {names or 'series'} "
                f"({n_series} series){_fmt_n(series)}{err_note}")

    return f"Figure: {title + '. ' if title else ''}{chart_type} chart{err_note}"


def _describe_panel(panel, error_type):
    if not isinstance(panel, dict):
        return "panel"
    ptype = panel.get("type", "")
    ptitle = panel.get("title", panel.get("label", ""))
    pdata = panel.get("data", {})
    if ptype == "bar":
        s = pdata.get("series", {})
        return f"{ptitle + ': ' if ptitle else ''}grouped bar chart of {_names(list(s.keys())) or 'values'}{_fmt_n(s)}"
    if ptype == "line":
        s = pdata.get("series", {})
        return f"{ptitle + ': ' if ptitle else ''}line chart of {_names(list(s.keys())) or 'values'}"
    if ptype == "scatter":
        n = len(pdata.get("x", []))
        return f"{ptitle + ': ' if ptitle else ''}scatter plot (n = {n} points)"
    if ptype == "heatmap":
        m = pdata.get("matrix", [])
        rows = len(m) if isinstance(m, list) else 0
        cols = len(m[0]) if rows and isinstance(m[0], list) else 0
        return f"{ptitle + ': ' if ptitle else ''}heatmap of {rows}×{cols} values"
    if ptype == "forest":
        n = len(pdata.get("estimates", []))
        return f"{ptitle + ': ' if ptitle else ''}forest plot of {n} studies"
    if ptype == "km":
        n = len(pdata.get("groups", {}))
        return f"{ptitle + ': ' if ptitle else ''}Kaplan–Meier curves for {n} group(s)"
    if ptype == "roc":
        n = len(pdata.get("curves", []))
        return f"{ptitle + ': ' if ptitle else ''}ROC curves for {n} model(s)"
    return ptitle or "panel"


def main():
    ap = argparse.ArgumentParser(description="Generate journal-format figure legends from data JSON")
    ap.add_argument("-d", "--data", required=True, help="Input data JSON (same format as gen_figure.py)")
    ap.add_argument("-t", "--title", default="", help="Legend title (e.g. 'Response to treatment')")
    ap.add_argument("-f", "--figure", type=int, default=1, help="Figure number (default: 1)")
    ap.add_argument("--type", default="bar", choices=["bar", "grouped_bar", "hbar", "horizontal_bar",
                                                      "stacked_bar", "line", "box", "boxplot", "violin",
                                                      "heatmap", "scatter", "forest", "km", "survival",
                                                      "roc", "dual_axis", "composite", "diagram",
                                                      "prisma"],
                    help="Chart type (default: bar)")
    ap.add_argument("--error-type", default="s.e.m.", help="Error-bar description (default: s.e.m.)")
    ap.add_argument("-o", "--out", default=None, help="Output file (default: stdout)")
    args = ap.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    text = legend_for(data, args.type, title=args.title, error_type=args.error_type)
    if args.figure > 0 and text.startswith("Figure:"):
        text = f"Figure {args.figure} |" + text[len("Figure:"):]
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Legend written to {args.out}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
