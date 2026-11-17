"""FK-Bench v2 — Scoring CLI.

Usage:
    python -m scorer.run --prediction predictions.json --gold data/v2.0 --output scores.json

``predictions.json`` format::

    {
        "FK-500-MOD1-000": [ {"kind": "NAVIGATE", "params": {...}}, ... ],
        ...
    }
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from dsl import Item
from dsl.actions import Action

from .aggregate import score_dataset


def _load_predictions(path: Path) -> Dict[str, List[Action]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: Dict[str, List[Action]] = {}
    for k, v in raw.items():
        out[k] = [Action.from_dict(a) for a in v]
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scorer.run")
    parser.add_argument("--prediction", type=Path, required=True)
    parser.add_argument("--gold", type=Path, required=True, help="path to data/v2.0")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)

    if not args.prediction.exists():
        print(f"error: prediction file not found: {args.prediction}", file=sys.stderr)
        return 2
    if not args.gold.exists():
        print(f"error: gold dir not found: {args.gold}", file=sys.stderr)
        return 2

    items: List[Item] = []
    for p in sorted(args.gold.glob("fk-500-*.json")):
        items.append(Item.from_json(p.read_text(encoding="utf-8")))
    if not items:
        print("error: no gold items found", file=sys.stderr)
        return 2

    preds = _load_predictions(args.prediction)

    reports = score_dataset(items, preds)
    by_mod: dict[str, list[float]] = defaultdict(list)
    rl_passes = 0
    rl_total = 0
    for r in reports:
        by_mod[r.item_id.split("-")[2] + "-" + r.item_id.split("-")[3].rstrip("0123456789")].append(r.total)
        # Bucket by module prefix (MOD1, MOD2, ...)
        m = r.item_id.split("-")[2]  # MOD1, MOD2, ...
        by_mod[m].append(r.total)
        if r.red_line_violated_item:
            rl_total += 1
            if r.red_line >= 1.0:
                rl_passes += 1

    summary = {
        "total_items": len(reports),
        "macro_total": round(sum(r.total for r in reports) / max(1, len(reports)), 2),
        "red_line_pass_rate": round(rl_passes / max(1, rl_total), 4) if rl_total else None,
        "by_module": {m: round(sum(v) / len(v), 2) for m, v in sorted(by_mod.items())},
        "scores": [r.to_dict() for r in reports],
    }
    if args.output:
        args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scored {len(reports)} items.")
    print(f"  macro total:    {summary['macro_total']}")
    print(f"  red-line pass:  {summary['red_line_pass_rate']}")
    print(f"  by module:")
    for m, v in summary["by_module"].items():
        print(f"    {m}: {v}")
    if args.output:
        print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
