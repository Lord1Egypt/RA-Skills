#!/usr/bin/env python3
"""Run one incremental refresh from a baseline and emit evidence changes."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from research_outputs import compare


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=Path("competitive-intelligence-monitor"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    baseline = args.baseline
    baseline_state = baseline if baseline.name == "state.json" else baseline / "state.json"
    state = json.loads(baseline_state.read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = args.output_root / stamp
    run_dir.mkdir(parents=True, exist_ok=False)
    for action in state["actions"]:
        action["status"] = "pending"
        action["output"] = None
        action["error"] = None
        action["attempts"] = 0
    new_state = run_dir / "state.json"
    new_state.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    runner = Path(__file__).with_name("run_research.py")
    command = [sys.executable, str(runner), "--resume", str(run_dir), "--autopilot"]
    if args.dry_run:
        command.append("--dry-run")
    result = subprocess.run(command, check=False)
    if result.returncode != 0 or args.dry_run:
        return result.returncode
    old_evidence = baseline_state.parent / "evidence.json"
    new_evidence = run_dir / "evidence.json"
    if not old_evidence.exists():
        print("Baseline evidence.json is missing; cannot compute changes.", file=sys.stderr)
        return 2
    changes = compare(old_evidence, new_evidence)
    changes_path = run_dir / "changes.json"
    changes_path.write_text(json.dumps(changes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run": str(run_dir), "changes": str(changes_path), "change_count": len(changes)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
