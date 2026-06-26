#!/usr/bin/env python3
"""Record deepen/superlearn session metadata."""

from __future__ import annotations

import argparse
import json

from clawexpert_common import iso_now, knowledge_dir, load_json, meta_path, save_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--mode", choices=["deepen", "superlearn"], required=True)
    parser.add_argument("--phase", choices=["start", "finish"], required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--round", type=int, default=1)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--max-hours", type=float, default=0)
    parser.add_argument("--status")
    parser.add_argument("--breadth-tasks", type=int, default=0)
    parser.add_argument("--depth-tasks", type=int, default=0)
    parser.add_argument("--sources-added", type=int, default=0)
    parser.add_argument("--nodes-added", type=int, default=0)
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    path = meta_path(kb, args.slug)
    meta = load_json(path, default=None)
    if meta is None:
        raise SystemExit(f"Missing meta.json: {path}")

    key = f"{args.mode}_sessions"
    sessions = meta.setdefault(key, [])

    if args.phase == "start":
        sessions.append(
            {
                "session_id": args.session_id,
                "round": args.round,
                "started": iso_now(),
                "finished": None,
                "status": "running",
                "budget_contract": "minimum_required",
                "max_rounds": args.max_rounds,
                "max_hours": args.max_hours,
                "minimum_rounds_required": args.max_rounds,
                "minimum_hours_required": args.max_hours,
                "breadth_tasks": args.breadth_tasks,
                "depth_tasks": args.depth_tasks,
                "sources_added": 0,
                "nodes_added": 0,
            }
        )
    else:
        target = next((item for item in reversed(sessions) if item.get("session_id") == args.session_id), None)
        if target is None:
            target = {
                "session_id": args.session_id,
                "round": args.round,
                "started": None,
            }
            sessions.append(target)
        target["finished"] = iso_now()
        target["status"] = args.status or "complete"
        target["budget_contract"] = "minimum_required"
        target["max_rounds"] = args.max_rounds
        target["max_hours"] = args.max_hours
        target["minimum_rounds_required"] = args.max_rounds
        target["minimum_hours_required"] = args.max_hours
        target["breadth_tasks"] = args.breadth_tasks
        target["depth_tasks"] = args.depth_tasks
        target["sources_added"] = args.sources_added
        target["nodes_added"] = args.nodes_added

    if args.mode == "superlearn":
        meta["depth_level"] = "exhaustive" if args.max_rounds and args.max_rounds >= 3 else "deep"
    elif args.mode == "deepen":
        meta["depth_level"] = "deep"

    save_json(path, meta)
    print(
        json.dumps(
            {
                "slug": args.slug,
                "mode": args.mode,
                "phase": args.phase,
                "session_count": len(sessions),
                "depth_level": meta.get("depth_level"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
