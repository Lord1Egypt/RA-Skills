#!/usr/bin/env python3
"""FK-Bench Skill — 打分脚本(版权保护)。

© 2026 FK-Bench Skill 作者。保留所有权利。未经授权禁止复制、分发、修改。

读入预测文件 {item_id: [{"kind": ..., "params": {...}}, ...]}, 对数据集
对应题目跑三层打分引擎, 输出汇总 + 逐题明细 JSON。

用法:
    python score.py --predictions pred.json --output scores.json
    python score.py --predictions pred.json --all --output scores.json   # 全量 722 题(未预测按空计划 0 分)
    python score.py --predictions pred.json --human                      # 打印易读汇总

预测未覆盖的题默认不计入总分(并报告覆盖率); --all 时全部计入。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parent.parent
BENCH = SKILL_ROOT / "assets" / "benchmark"
DATA_DIR = BENCH / "data" / "v2.0"
PACK_PATH = BENCH / "data.bin"
OWNER = "FK-Bench Skill"

sys.path.insert(0, str(BENCH))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsl import Item  # noqa: E402
from dsl.actions import Action  # noqa: E402
from scorer.aggregate import score_dataset  # noqa: E402
from _datapack import load_pack  # noqa: E402


def _load_all_items() -> list[Item]:
    if PACK_PATH.exists():
        raw = load_pack(PACK_PATH)
        return [Item.from_json(raw[name]) for name in sorted(raw)]
    return [Item.from_json(p.read_text(encoding="utf-8"))
            for p in sorted(DATA_DIR.glob("fk-*.json"))]


def _load_predictions(path: Path) -> dict[str, list[Action]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, list[Action]] = {}
    for k, v in raw.items():
        try:
            out[str(k)] = [Action.from_dict(a) for a in v]
        except Exception as e:  # noqa: BLE001
            print(f"error: bad prediction for {k}: {e}", file=sys.stderr)
            return {}
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="forklift-score")
    parser.add_argument("--predictions", type=Path, required=True,
                        help="预测文件: {item_id: [ {kind, params}, ... ]}")
    parser.add_argument("--output", type=Path, default=None, help="写 JSON 报告")
    parser.add_argument("--all", action="store_true",
                        help="对全部 722 题打分(未覆盖的题按空预测 0 分)")
    parser.add_argument("--human", action="store_true", help="打印易读汇总")
    args = parser.parse_args(argv)

    if not args.predictions.exists():
        print(f"error: prediction file not found: {args.predictions}", file=sys.stderr)
        return 2

    preds = _load_predictions(args.predictions)
    if not preds:
        print("error: no valid predictions", file=sys.stderr)
        return 2

    items = _load_all_items()

    if args.all:
        scored = items
    else:
        pred_ids = set(preds.keys())
        scored = [it for it in items if it.item_id in pred_ids]

    reports = score_dataset(scored, preds)

    by_mod: dict[str, list[float]] = defaultdict(list)
    by_diff: dict[str, list[float]] = defaultdict(list)
    rl_passes = 0
    rl_total = 0
    details: list[dict[str, Any]] = []
    for r in reports:
        it = next(i for i in scored if i.item_id == r.item_id)
        by_mod[it.meta.module].append(r.total)
        by_diff[it.meta.difficulty].append(r.total)
        if r.red_line_violated_item:
            rl_total += 1
            if r.red_line >= 1.0:
                rl_passes += 1
        details.append({
            "item_id": r.item_id,
            "module": it.meta.module,
            "scene_type": it.meta.scene_type,
            "difficulty": it.meta.difficulty,
            "red_line": r.red_line,
            "lcs": r.lcs,
            "iou": r.iou,
            "total": r.total,
        })

    summary: dict[str, Any] = {
        "owner": OWNER,
        "predicted_items": len(preds),
        "scored_items": len(reports),
        "coverage": round(len(reports) / len(items), 4) if items else 0,
        "macro_total": round(sum(r.total for r in reports) / max(1, len(reports)), 2),
        "red_line_total": rl_total,
        "red_line_pass": rl_passes,
        "red_line_pass_rate": round(rl_passes / max(1, rl_total), 4) if rl_total else None,
        "by_module": {m: round(sum(v) / len(v), 2) for m, v in sorted(by_mod.items())},
        "by_difficulty": {d: round(sum(v) / len(v), 2) for d, v in sorted(by_diff.items())},
        "details": details,
    }

    if args.output:
        args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.human or not args.output:
        print(f"Predicted {summary['predicted_items']} items, scored {summary['scored_items']} "
              f"(coverage {summary['coverage'] * 100:.1f}%)")
        print(f"Macro total: {summary['macro_total']} / 100")
        if summary["red_line_total"]:
            print(f"Red-line pass: {summary['red_line_pass']} / {summary['red_line_total']} "
                  f"({summary['red_line_pass_rate'] * 100:.1f}%)")
        for m, v in summary["by_module"].items():
            print(f"  {m}: {v}")
    if args.output:
        print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
