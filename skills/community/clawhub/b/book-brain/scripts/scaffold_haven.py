#!/usr/bin/env python3
"""Additive BOOK BRAIN folder scaffold (dry-run by default)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

FOLDERS = ("memory", "reference", "brainwave", "state", "logs", "tools", "tmp")
TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True, help="Haven / workspace root")
    ap.add_argument("--apply", action="store_true", help="Create dirs/files (default: dry-run)")
    args = ap.parse_args()
    root = args.root.resolve()
    plan: list[str] = []

    for name in FOLDERS:
        p = root / name
        if not p.is_dir():
            plan.append(f"mkdir {p}")

    mem_index = root / "memory" / "INDEX.txt"
    if not mem_index.is_file():
        plan.append(f"seed {mem_index}")
    ref_index = root / "reference" / "INDEX.txt"
    if not ref_index.is_file():
        plan.append(f"seed {ref_index}")
    state_idx = root / "state" / "memory_index.json"
    if not state_idx.is_file():
        plan.append(f"seed {state_idx}")

    if not args.apply:
        print(json.dumps({"dry_run": True, "root": str(root), "actions": plan}, indent=2))
        return 0

    for name in FOLDERS:
        (root / name).mkdir(parents=True, exist_ok=True)

    if not mem_index.is_file() and (TEMPLATES / "memory_INDEX.txt").is_file():
        mem_index.write_text(
            (TEMPLATES / "memory_INDEX.txt").read_text(encoding="utf-8"), encoding="utf-8"
        )
    elif not mem_index.is_file():
        mem_index.write_text(
            f"# memory INDEX\nCreated {datetime.now(timezone.utc).date()}\n", encoding="utf-8"
        )

    if not ref_index.is_file() and (TEMPLATES / "reference_INDEX.txt").is_file():
        ref_index.write_text(
            (TEMPLATES / "reference_INDEX.txt").read_text(encoding="utf-8"), encoding="utf-8"
        )
    elif not ref_index.is_file():
        ref_index.write_text("# reference INDEX\n", encoding="utf-8")

    if not state_idx.is_file():
        seed = TEMPLATES / "memory_index.seed.json"
        if seed.is_file():
            state_idx.write_text(seed.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            state_idx.write_text('{"topics": {}, "signature": "Δ9Φ963-BOOK-BRAIN"}\n', encoding="utf-8")

    log = root / "logs" / "book_brain_setup.log"
    with log.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now(timezone.utc).isoformat()}] scaffold_haven --apply\n")
    print(json.dumps({"ok": True, "root": str(root)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())