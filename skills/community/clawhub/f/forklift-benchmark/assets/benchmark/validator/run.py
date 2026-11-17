"""FK-Bench v2 — Static validation CLI.

Usage:
    python -m validator.run --dataset data/v2.0 --report validator_report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import List

from dsl import Item

from . import (
    assert_distribution,
    check_all_physics,
    check_safety_red_line,
    validate_item_json,
)


def _iter_items(dataset: Path):
    for p in sorted(dataset.glob("fk-500-*.json")):
        yield Item.from_json(p.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="validator.run")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    if not args.dataset.exists():
        print(f"error: dataset not found: {args.dataset}", file=sys.stderr)
        return 2

    items = list(_iter_items(args.dataset))
    if not items:
        print("error: no items found", file=sys.stderr)
        return 2

    report = {
        "dataset": str(args.dataset),
        "total_items": len(items),
        "schema_violations": 0,
        "physics_violations": 0,
        "safety_violations": 0,
        "distribution_violations": [],
        "items": [],
    }

    # 1. Distribution check
    report["distribution_violations"] = assert_distribution(items)

    # 2. Per-item checks
    schema_err = 0
    phys_err = 0
    safety_err = 0
    mod_counter: Counter[str] = Counter()
    diff_counter: Counter[str] = Counter()
    scene_counter: Counter[str] = Counter()
    for it in items:
        mod_counter[it.meta.module] += 1
        diff_counter[it.meta.difficulty] += 1
        scene_counter[it.meta.scene_type] += 1

        # schema
        errs = validate_item_json(args.dataset / f"{it.item_id.lower()}.json")
        if errs:
            schema_err += 1
            report["items"].append({"item_id": it.item_id, "schema": errs})
            continue

        # physics
        # Estimate the maximum lift height implied by the gold plan.
        max_h = 0.0
        for a in it.ground_truth.action_plan:
            if a.kind == "LIFT":
                h = a.params.get("to_height_m")
                if isinstance(h, (int, float)):
                    max_h = max(max_h, float(h))
        check_h = max_h if max_h > 0 else 1.5
        phys = check_all_physics(it, expected_max_height_m=check_h)
        if phys:
            phys_err += 1
            report["items"].append({
                "item_id": it.item_id,
                "physics": [{"code": v.code, "message": v.message} for v in phys],
            })
            continue

        # safety (informational; not a hard reject for the dataset)
        sv = check_safety_red_line(it)
        if sv and it.ground_truth.expected_decision != "SAFETY_ABORT":
            # Inconsistency: instruction violates safety but the gold
            # answer is EXECUTE. This is a generator bug.
            safety_err += 1
            report["items"].append({
                "item_id": it.item_id,
                "safety": [{"code": v.code, "message": v.message} for v in sv],
            })

    report["schema_violations"] = schema_err
    report["physics_violations"] = phys_err
    report["safety_violations"] = safety_err
    report["by_module"] = dict(sorted(mod_counter.items()))
    report["by_scene"] = dict(sorted(scene_counter.items()))
    report["by_difficulty"] = dict(sorted(diff_counter.items()))

    pass_rate = 1.0 - (schema_err + phys_err + safety_err) / max(1, len(items))

    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.quiet:
        print(f"Dataset : {args.dataset}")
        print(f"Items   : {len(items)}")
        print(f"Schema  : {schema_err} violations")
        print(f"Physics : {phys_err} violations")
        print(f"Safety  : {safety_err} violations (only flagged if gold != SAFETY_ABORT)")
        print(f"Pass rate: {pass_rate * 100:.1f} %")
        if report["distribution_violations"]:
            print("Distribution violations:")
            for v in report["distribution_violations"]:
                print(f"  - {v}")
        if args.report:
            print(f"Report written to {args.report}")

    return 0 if (schema_err + phys_err + safety_err + len(report["distribution_violations"])) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
