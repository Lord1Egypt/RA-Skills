#!/usr/bin/env python3
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

METRICS = ["mention_rate", "positive_mention_rate", "capability_accuracy", "ecosystem_accuracy"]
METRIC_LABELS = {
    "mention_rate": "Mention",
    "positive_mention_rate": "Positive",
    "capability_accuracy": "Capability",
    "ecosystem_accuracy": "Ecosystem",
}
METRIC_COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#7c3aed"]


def load_summary(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def collect_rows(root):
    rows = []
    for path in sorted(Path(root).glob("*/summary.json")):
        summary = load_summary(path)
        for model_row in summary.get("by_model", []):
            rows.append({"run_id": summary["run_id"], "project": summary["project"], **model_row})
    return rows


def write_csv(rows, path):
    fields = ["run_id", "project", "model_id", *METRICS]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in fields})


def aggregate(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["model_id"]].append(row)
    output = []
    for model_id, items in grouped.items():
        latest = items[-1]
        prev = items[-2] if len(items) > 1 else None
        agg = {"model_id": model_id, "run_count": len(items)}
        for metric in METRICS:
            values = [r[metric] for r in items if r.get(metric) is not None]
            agg[f"avg_{metric}"] = round(sum(values) / len(values), 2) if values else None
            agg[f"latest_{metric}"] = latest.get(metric)
            agg[f"delta_{metric}"] = round(latest.get(metric, 0) - prev.get(metric, 0), 2) if prev and prev.get(metric) is not None else None
        output.append(agg)
    return sorted(output, key=lambda x: (x.get("latest_mention_rate") or 0), reverse=True)


def write_md(rows, path):
    if len(rows) == 1:
        row = rows[0]
        lines = [
            "# Single-Model DevTool Answer Monitor Snapshot",
            "",
            f"Default sample uses one enabled model: **{row['model_id']}**.",
            "",
            "| Metric | Latest Score | Δ vs Previous |",
            "|---|---:|---:|",
        ]
        for metric in METRICS:
            delta = row[f"delta_{metric}"]
            delta_text = "NA" if delta is None else f"{delta:+.2f}"
            lines.append(f"| {METRIC_LABELS[metric]} | {row[f'latest_{metric}']:.2f} | {delta_text} |")
    else:
        lines = [
            "# Model Leaderboard",
            "",
            "| Model | Runs | Latest Mention | Latest Positive | Latest Capability | Latest Ecosystem | Δ Mention |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
        for row in rows:
            delta = "NA" if row["delta_mention_rate"] is None else f"{row['delta_mention_rate']:+.2f}"
            lines.append(
                f"| {row['model_id']} | {row['run_count']} | {row['latest_mention_rate']:.2f} | {row['latest_positive_mention_rate']:.2f} | {row['latest_capability_accuracy']:.2f} | {row['latest_ecosystem_accuracy']:.2f} | {delta} |"
            )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_png(rows, path):
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    if len(rows) == 1:
        row = rows[0]
        values = [row[f"latest_{metric}"] for metric in METRICS]
        labels = [METRIC_LABELS[m] for m in METRICS]
        bars = ax.bar(labels, values, color=METRIC_COLORS, width=0.62)
        ax.set_ylabel("Score")
        ax.set_title("Single-Model DevTool Answer Monitor Snapshot", fontsize=16, pad=20)
        ax.text(0.5, 1.01, f"Model: {row['model_id']}", transform=ax.transAxes, ha="center", va="bottom", fontsize=10, color="#475569")
        ax.set_ylim(0, 108)
        for bar, value in zip(bars, values):
            label_y = value - 3 if value >= 98 else value + 1.2
            label_va = "top" if value >= 98 else "bottom"
            ax.text(bar.get_x() + bar.get_width() / 2, label_y, f"{value:.0f}", ha="center", va=label_va, fontsize=10, fontweight="semibold", color="#111827")
    else:
        labels = [row["model_id"] for row in rows]
        values = [row["latest_mention_rate"] for row in rows]
        bars = ax.bar(labels, values, color="#2563eb")
        ax.set_ylabel("Mention Rate")
        ax.set_title("Model Leaderboard Snapshot", fontsize=16, pad=18)
        ax.set_ylim(0, 108)
        for bar, value in zip(bars, values):
            label_y = value - 3 if value >= 98 else value + 1.2
            label_va = "top" if value >= 98 else "bottom"
            ax.text(bar.get_x() + bar.get_width() / 2, label_y, f"{value:.0f}", ha="center", va=label_va, fontsize=10, fontweight="semibold")
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-root", default="data/runs")
    ap.add_argument("--output-dir", default="data/leaderboards")
    ap.add_argument("--image-output", default="assets/leaderboard-sample.png")
    args = ap.parse_args()

    rows = collect_rows(args.runs_root)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    Path(args.image_output).parent.mkdir(parents=True, exist_ok=True)
    write_csv(rows, output_dir / "model_leaderboard.csv")
    aggregated = aggregate(rows)
    write_md(aggregated, output_dir / "model_leaderboard.md")
    write_png(aggregated, args.image_output)
    print(json.dumps({"rows": len(rows), "models": len(aggregated), "output_dir": str(output_dir), "image": args.image_output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
