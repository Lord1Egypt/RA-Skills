#!/usr/bin/env python3
import json
from pathlib import Path

import matplotlib.pyplot as plt

RUNS = [
    ("sample-run", "Baseline"),
    ("repair-t7-run", "T+7"),
]
METRICS = [
    ("mention_rate", "Mention"),
    ("positive_mention_rate", "Positive"),
    ("capability_accuracy", "Capability"),
    ("ecosystem_accuracy", "Ecosystem"),
]
COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#7c3aed"]


def load_summary(root, run_id):
    return json.loads((root / run_id / "summary.json").read_text(encoding="utf-8"))


def main():
    root = Path("data/runs")
    out = Path("assets/repair-trend-sample.png")
    out.parent.mkdir(parents=True, exist_ok=True)

    summaries = [(label, load_summary(root, run_id)) for run_id, label in RUNS]
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    labels = [label for label, _ in summaries]

    for (metric, title), color in zip(METRICS, COLORS):
        values = [summary.get("metrics", {}).get(metric, 0) for _, summary in summaries]
        ax.plot(labels, values, marker="o", linewidth=2.2, color=color, label=title)
        for x, value in zip(labels, values):
            ax.text(x, value + 1.2, f"{value:.0f}", ha="center", va="bottom", fontsize=9, color=color)

    ax.set_ylim(0, 108)
    ax.set_ylabel("Score")
    ax.set_title("Repair Trend Snapshot", fontsize=16, pad=16)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.legend(ncols=2, frameon=False)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(json.dumps({"status": "ok", "image": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
