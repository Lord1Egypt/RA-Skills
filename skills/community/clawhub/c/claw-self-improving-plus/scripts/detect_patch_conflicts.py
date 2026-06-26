#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path


TARGETS = {"SOUL.md", "AGENTS.md", "TOOLS.md", "MEMORY.md"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def conflict_key(patch: dict):
    target = patch.get("target_file")
    anchor = patch.get("anchor") or "<append>"
    mode = patch.get("insert_mode") or "append"
    return target, anchor, mode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patches", help="Path to patch JSON")
    ap.add_argument("-o", "--output", help="Write conflict report JSON")
    args = ap.parse_args()

    data = load_json(Path(args.patches))
    patches = data.get("patch_candidates", [])

    buckets = defaultdict(list)
    invalid_targets = []
    duplicate_entries = []

    for patch in patches:
        if patch.get("target_file") not in TARGETS:
            invalid_targets.append({"id": patch.get("id"), "target_file": patch.get("target_file")})
            continue
        key = conflict_key(patch)
        buckets[key].append(patch)

    for (target, anchor, mode), group in buckets.items():
        seen_entries = {}
        for patch in group:
            entry = (patch.get("suggested_entry") or "").strip()
            if not entry:
                continue
            if entry in seen_entries:
                duplicate_entries.append({
                    "target_file": target,
                    "anchor": anchor,
                    "mode": mode,
                    "ids": [seen_entries[entry], patch.get("id")],
                    "entry": entry,
                })
            else:
                seen_entries[entry] = patch.get("id")

    anchor_conflicts = [
        {
            "target_file": target,
            "anchor": anchor,
            "mode": mode,
            "count": len(group),
            "ids": [p.get("id") for p in group],
        }
        for (target, anchor, mode), group in buckets.items()
        if len(group) > 1
    ]

    report = {
        "total_patches": len(patches),
        "invalid_targets": invalid_targets,
        "anchor_conflicts": anchor_conflicts,
        "duplicate_entries": duplicate_entries,
        "has_conflicts": bool(invalid_targets or anchor_conflicts or duplicate_entries),
    }

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
