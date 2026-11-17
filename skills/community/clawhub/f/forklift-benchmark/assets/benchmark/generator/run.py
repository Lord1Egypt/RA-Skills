"""FK-Bench v2 — Dataset generation entry point.

Usage:
    python -m generator.run --total 500 --seed 42 --output data/v2.0

Produces:
    data/v2.0/fk-500-mod{1-6}-{000-499}.json   (one item per file)
    data/v2.0/index.json                        (lookup index)
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from dsl import (
    DIFFICULTIES,
    MODULES,
    SCENES,
    validate_item_json,
)

from .combinatorial import generate_500


def _write_index(path: Path, items) -> None:
    by_mod: dict[str, int] = Counter()
    by_scene: dict[str, int] = Counter()
    by_diff: dict[str, int] = Counter()
    cross_mod_diff: dict[str, dict[str, int]] = {m: {d: 0 for d in DIFFICULTIES} for m in MODULES}
    cross_scene_diff: dict[str, dict[str, int]] = {s: {d: 0 for d in DIFFICULTIES} for s in SCENES}
    cross_mod_scene: dict[str, dict[str, int]] = {m: {s: 0 for s in SCENES} for m in MODULES}
    for it in items:
        m = it.meta.module
        s = it.meta.scene_type
        d = it.meta.difficulty
        by_mod[m] += 1
        by_scene[s] += 1
        by_diff[d] += 1
        cross_mod_diff[m][d] += 1
        cross_scene_diff[s][d] += 1
        cross_mod_scene[m][s] += 1
    index = {
        "dataset": "FK-Bench v2",
        "version": "2.0.0",
        "total_items": len(items),
        "by_module": dict(sorted(by_mod.items())),
        "by_scene": dict(sorted(by_scene.items())),
        "by_difficulty": dict(sorted(by_diff.items())),
        "cross_module_scene": {m: dict(sorted(v.items())) for m, v in cross_mod_scene.items()},
        "cross_module_difficulty": {m: v for m, v in cross_mod_diff.items()},
        "cross_scene_difficulty": {s: v for s, v in cross_scene_diff.items()},
        "items": [
            {
                "item_id": it.item_id,
                "module": it.meta.module,
                "scene_type": it.meta.scene_type,
                "difficulty": it.meta.difficulty,
                "expected_decision": it.ground_truth.expected_decision,
                "is_red_line": it.eval_metrics.red_line_violated,
            }
            for it in items
        ],
    }
    path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="generator.run")
    parser.add_argument("--total", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("data/v2.0"))
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    if args.total != 500:
        print(f"warning: this generator is tuned for total=500, got {args.total}", file=sys.stderr)

    items, stats = generate_500(seed=args.seed)
    if args.total != len(items):
        print(f"error: produced {len(items)} items, expected {args.total}", file=sys.stderr)
        return 1

    out_dir: Path = args.output
    out_dir.mkdir(parents=True, exist_ok=True)

    # Sanity: structural validation pass.
    bad = 0
    for it in items:
        d = it.to_dict()
        errs = []
        for k in ("item_id", "meta", "input_context", "ground_truth"):
            if k not in d:
                errs.append(f"missing {k}")
        if errs:
            bad += 1
    if bad:
        print(f"warning: {bad} items failed structural validation", file=sys.stderr)
        return 1

    for it in items:
        path = out_dir / f"{it.item_id.lower()}.json"
        path.write_text(it.to_json(indent=2), encoding="utf-8")

    _write_index(out_dir / "index.json", items)

    # Post-write disk check
    failures: list[str] = []
    for it in items:
        path = out_dir / f"{it.item_id.lower()}.json"
        errs = validate_item_json(path)
        if errs:
            failures.append(f"{it.item_id}: {errs}")
    if failures:
        print(f"error: {len(failures)} files failed re-load validation", file=sys.stderr)
        for f in failures[:5]:
            print(f"  {f}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"Generated {len(items)} items in {out_dir}")
        print(f"  by_module:    {dict(sorted(stats.__dict__.items()))}")
        # quick distribution
        mod_counter = Counter(it.meta.module for it in items)
        scene_counter = Counter(it.meta.scene_type for it in items)
        diff_counter = Counter(it.meta.difficulty for it in items)
        print(f"  module:    {dict(sorted(mod_counter.items()))}")
        print(f"  scene:     {dict(sorted(scene_counter.items()))}")
        print(f"  difficulty:{dict(sorted(diff_counter.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
