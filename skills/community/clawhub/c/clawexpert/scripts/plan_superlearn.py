#!/usr/bin/env python3
"""Build a round plan for multi-round superlearn runs."""

from __future__ import annotations

import argparse
import json
import pathlib

from clawexpert_common import iso_now, knowledge_dir, load_json, meta_path


def load_gaps(path: pathlib.Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("breadth_tasks", [])
    data.setdefault("depth_tasks", [])
    return data


def pick_tasks(items: list[dict], limit: int | None, priority_key: str | None = None) -> list[dict]:
    ranked = list(items)
    if priority_key:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        ranked.sort(key=lambda item: (priority_order.get(item.get(priority_key), 9), item.get("label", "")))
    if limit is None or limit <= 0:
        return ranked
    return ranked[:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--gaps-file", required=True)
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--max-hours", type=float, default=0)
    parser.add_argument("--elapsed-hours", type=float, default=0)
    parser.add_argument("--breadth-limit", type=int, default=4)
    parser.add_argument("--depth-limit", type=int, default=6)
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    meta = load_json(meta_path(kb, args.slug), default={}) or {}
    gaps = load_gaps(pathlib.Path(args.gaps_file).expanduser().resolve())

    selected_breadth = pick_tasks(gaps["breadth_tasks"], args.breadth_limit)
    selected_depth = pick_tasks(gaps["depth_tasks"], args.depth_limit, priority_key="priority")
    completed_rounds = max(0, args.round - 1)
    rounds_satisfied = args.max_rounds <= 0 or completed_rounds >= args.max_rounds
    hours_satisfied = args.max_hours <= 0 or args.elapsed_hours >= args.max_hours
    minimum_budget_met = rounds_satisfied and hours_satisfied
    should_continue = not minimum_budget_met

    remaining_hours = None
    if args.max_hours > 0:
        remaining_hours = max(0.0, args.max_hours - args.elapsed_hours)
    remaining_rounds = None
    if args.max_rounds > 0:
        remaining_rounds = max(0, args.max_rounds - completed_rounds)

    payload = {
        "slug": args.slug,
        "topic": meta.get("topic", args.slug),
        "generated_at": iso_now(),
        "round": args.round,
        "budget_mode": infer_budget_mode(args.max_rounds, args.max_hours),
        "budget_contract": "minimum_required",
        "max_rounds": args.max_rounds,
        "max_hours": args.max_hours,
        "minimum_rounds_required": args.max_rounds,
        "minimum_hours_required": args.max_hours,
        "completed_rounds": completed_rounds,
        "elapsed_hours": args.elapsed_hours,
        "remaining_hours": remaining_hours,
        "remaining_rounds": remaining_rounds,
        "rounds_satisfied": rounds_satisfied,
        "hours_satisfied": hours_satisfied,
        "minimum_budget_met": minimum_budget_met,
        "should_continue": should_continue,
        "stop_reason": None if should_continue else infer_stop_reason(args, rounds_satisfied, hours_satisfied),
        "continue_reason": infer_continue_reason(minimum_budget_met, args, rounds_satisfied, hours_satisfied),
        "selected_breadth_tasks": selected_breadth,
        "selected_depth_tasks": selected_depth,
        "coverage_snapshot": gaps.get("summary", {}),
        "recommended_parallelism": max(1, min(len(selected_breadth) + len(selected_depth), 6)),
        "hard_stop_prohibited_until_minimum_met": not minimum_budget_met,
    }

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def infer_budget_mode(max_rounds: int, max_hours: float) -> str:
    if max_rounds > 0 and max_hours > 0:
        return "combined_minimum"
    if max_rounds > 0:
        return "rounds_minimum"
    if max_hours > 0:
        return "hours_minimum"
    return "default_rounds_minimum"


def infer_continue_reason(
    minimum_budget_met: bool,
    args: argparse.Namespace,
    rounds_satisfied: bool,
    hours_satisfied: bool,
) -> str:
    if minimum_budget_met:
        return "minimum_budget_met"
    missing: list[str] = []
    if args.max_rounds > 0 and not rounds_satisfied:
        missing.append("minimum_rounds_not_met")
    if args.max_hours > 0 and not hours_satisfied:
        missing.append("minimum_hours_not_met")
    if not missing:
        return "default_minimum_rounds_not_met"
    return "+".join(missing)


def infer_stop_reason(args: argparse.Namespace, rounds_satisfied: bool, hours_satisfied: bool) -> str:
    if args.max_rounds > 0 and args.max_hours > 0 and rounds_satisfied and hours_satisfied:
        return "minimum_rounds_and_hours_satisfied"
    if args.max_rounds > 0 and rounds_satisfied and args.max_hours <= 0:
        return "minimum_rounds_satisfied"
    if args.max_hours > 0 and hours_satisfied and args.max_rounds <= 0:
        return "minimum_hours_satisfied"
    if rounds_satisfied and hours_satisfied:
        return "default_minimum_rounds_satisfied"
    return "minimum_budget_not_met"


if __name__ == "__main__":
    raise SystemExit(main())
