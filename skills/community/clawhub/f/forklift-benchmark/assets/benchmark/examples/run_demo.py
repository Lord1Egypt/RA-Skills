#!/usr/bin/env python3
"""End-to-end demo for FK-Bench v2.

This script demonstrates the full pipeline at production scale (500 items):

    1. Load 500 items from ``data/v2.0/``.
    2. Run a "mock predictor" that returns a noisy prediction (deliberately
       failing on some red-line items to show the scorer veto).
    3. Run the three-layer scorer (red-line + LCS + parameter IoU).
    4. Write a Markdown summary to ``examples/demo_report.md``.

Usage::

    python examples/run_demo.py
    python examples/run_demo.py --num-items 500 --output examples/demo_report.md
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dsl import Action, Item
from scorer.aggregate import score_dataset
from validator import assert_distribution, check_all_physics, check_safety_red_line, validate_item_json


# ---------------------------------------------------------------------------
# Mock predictor
# ---------------------------------------------------------------------------
def mock_predict(item: Item, seed: int = 0) -> List[Action]:
    """Return a noisy prediction.

    * Red-line items: deliberately fails to abort (so the scorer veto kicks in).
    * Other items: copies the gold plan with random drift (drop 1 action
      in 5, swap 1 kind in 10, perturb numeric params by 5 %).
    """
    rng = random.Random(seed + hash(item.item_id) % 100000)
    if item.eval_metrics.red_line_violated and item.ground_truth.expected_decision == "SAFETY_ABORT":
        return [
            Action("LIFT", {"to_height_m": 0.3}),
            Action("NAVIGATE", {"to_x": 2.0, "to_y": 0.0, "max_speed_mps": 2.5}),
            Action("RAISE_ALARM", {"channel": "operator", "code": "E_NONE"}),
        ]
    plan: List[Action] = []
    for idx, action in enumerate(item.ground_truth.action_plan):
        if idx > 0 and idx % 5 == 4:
            continue  # drop
        new_kind = action.kind
        if idx > 0 and idx % 10 == 0 and action.kind in {"TILT_BACK", "TILT_FORWARD"}:
            new_kind = "TILT_FORWARD" if action.kind == "TILT_BACK" else "TILT_BACK"
        new_params: Dict[str, Any] = {}
        for k, v in action.params.items():
            if isinstance(v, float):
                new_params[k] = round(v * rng.uniform(0.95, 1.05), 3)
            elif isinstance(v, int) and v > 100:
                new_params[k] = int(v * rng.uniform(0.97, 1.03))
            else:
                new_params[k] = v
        plan.append(Action(new_kind, new_params))
    return plan


# ---------------------------------------------------------------------------
# Demo driver
# ---------------------------------------------------------------------------
def run_demo(num_items: int, output: Path) -> Dict[str, Any]:
    data_dir = REPO_ROOT / "data" / "v2.0"
    files = sorted(data_dir.glob("fk-500-*.json"))
    items: List[Item] = []
    for p in files[:num_items]:
        items.append(Item.from_json(p.read_text(encoding="utf-8")))

    # 1) Distribution check
    dist_errs = assert_distribution(items)
    # 2) Static validation
    schema_violations = sum(1 for it in items if validate_item_json(data_dir / f"{it.item_id.lower()}.json"))
    physics_violations = 0
    safety_violations = 0
    for it in items:
        max_h = 0.0
        for a in it.ground_truth.action_plan:
            if a.kind == "LIFT":
                h = a.params.get("to_height_m")
                if isinstance(h, (int, float)):
                    max_h = max(max_h, float(h))
        phys = check_all_physics(it, expected_max_height_m=max_h or 1.5)
        if phys:
            physics_violations += 1
        sv = check_safety_red_line(it)
        if sv and it.ground_truth.expected_decision != "SAFETY_ABORT":
            safety_violations += 1

    # 3) Mock predictions + score
    preds = {it.item_id: mock_predict(it, seed=7) for it in items}
    reports = score_dataset(items, preds)
    by_mod: Dict[str, List[float]] = defaultdict(list)
    by_diff: Dict[str, List[float]] = defaultdict(list)
    rl_pass = 0
    rl_total = 0
    for r in reports:
        # Recover module/difficulty from the item
        it = next(i for i in items if i.item_id == r.item_id)
        by_mod[it.meta.module].append(r.total)
        by_diff[it.meta.difficulty].append(r.total)
        if r.red_line_violated_item:
            rl_total += 1
            if r.red_line >= 1.0:
                rl_pass += 1

    summary = {
        "dataset_total": len(items),
        "distribution_errors": dist_errs,
        "schema_violations": schema_violations,
        "physics_violations": physics_violations,
        "safety_violations": safety_violations,
        "macro_total": round(sum(r.total for r in reports) / max(1, len(reports)), 2),
        "red_line_total": rl_total,
        "red_line_pass": rl_pass,
        "red_line_pass_rate": round(rl_pass / rl_total, 4) if rl_total else None,
        "by_module": {m: round(sum(v) / len(v), 2) for m, v in sorted(by_mod.items())},
        "by_difficulty": {d: round(sum(v) / len(v), 2) for d, v in sorted(by_diff.items())},
    }
    return summary


def write_markdown(summary: Dict[str, Any], output: Path) -> None:
    lines: List[str] = []
    lines.append("# FK-Bench v2 — End-to-end demo report\n")
    lines.append(f"- Dataset items: **{summary['dataset_total']}**")
    lines.append(f"- Distribution errors: **{len(summary['distribution_errors'])}**")
    lines.append(f"- Schema violations: **{summary['schema_violations']}**")
    lines.append(f"- Physics violations: **{summary['physics_violations']}**")
    lines.append(f"- Safety violations (only flagged if gold != SAFETY_ABORT): **{summary['safety_violations']}**")
    lines.append(f"- Mock predictor macro total: **{summary['macro_total']} / 100**")
    if summary["red_line_total"]:
        lines.append(f"- Red-line pass rate: **{summary['red_line_pass']} / {summary['red_line_total']} = {summary['red_line_pass_rate'] * 100:.1f} %**")
    lines.append("")
    lines.append("## Per-module average")
    lines.append("")
    lines.append("| Module | Average total |")
    lines.append("|--------|---------------|")
    for m, v in summary["by_module"].items():
        lines.append(f"| {m} | {v} |")
    lines.append("")
    lines.append("## Per-difficulty average")
    lines.append("")
    lines.append("| Difficulty | Average total |")
    lines.append("|------------|---------------|")
    for d, v in summary["by_difficulty"].items():
        lines.append(f"| {d} | {v} |")
    output.write_text("\n".join(lines), encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="run_demo")
    parser.add_argument("--num-items", type=int, default=500)
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "examples" / "demo_report.md")
    args = parser.parse_args(argv)

    summary = run_demo(args.num_items, args.output)
    write_markdown(summary, args.output)

    print(f"Scored {summary['dataset_total']} items.")
    print(f"  distribution errors: {len(summary['distribution_errors'])}")
    print(f"  schema violations  : {summary['schema_violations']}")
    print(f"  physics violations : {summary['physics_violations']}")
    print(f"  safety violations  : {summary['safety_violations']}")
    print(f"  macro total        : {summary['macro_total']} / 100")
    if summary["red_line_total"]:
        print(f"  red-line pass      : {summary['red_line_pass']} / {summary['red_line_total']} = {summary['red_line_pass_rate'] * 100:.1f} %")
    print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
