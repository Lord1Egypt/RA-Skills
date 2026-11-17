#!/usr/bin/env python3
"""FK-Bench Skill — 抽题脚本(版权保护)。

© 2026 FK-Bench Skill 作者。保留所有权利。未经授权禁止复制、分发、修改。

从加密数据包 data.bin(缺失时回退明文 data/v2.0)中按模块/场景/难度过滤
抽题, 默认**只输出题面、隐藏 gold 答案**, 供当前模型直接读题作答。

用法:
    python sample.py --count 5 --module MOD-2 --difficulty intermediate
    python sample.py --count 3 --scene S5_VNA --seed 42
    python sample.py --red-line-only --count 2 --output questions.json
    python sample.py --count 2 --with-answer     # 额外打印 gold 答案(人工核对用)
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
BENCH = SKILL_ROOT / "assets" / "benchmark"
DATA_DIR = BENCH / "data" / "v2.0"
PACK_PATH = BENCH / "data.bin"

sys.path.insert(0, str(BENCH))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsl import Item  # noqa: E402
from _datapack import load_pack  # noqa: E402

MODULE_CN = {
    "MOD-1": "导航与路径规划", "MOD-2": "载荷与货叉操作", "MOD-3": "属具感知",
    "MOD-4": "安全与红线合规", "MOD-5": "现场拓扑推理", "MOD-6": "传感器异常鲁棒性",
}
SCENE_CN = {
    "S1_HIGH_BAY": "高位立体库", "S2_BLOCK": "平库/堆垛区", "S3_DOCK": "集装箱/货车装卸",
    "S4_LINE_SIDE": "生产流水线边", "S5_VNA": "窄巷道", "S6_OUTDOOR": "户外交接区",
    "S7_MIXED": "人机混行",
}


def _load_all_items() -> list[Item]:
    """优先从加密数据包加载, 缺失时回退明文目录。"""
    if PACK_PATH.exists():
        raw = load_pack(PACK_PATH)
        items: list[Item] = []
        for name in sorted(raw):
            items.append(Item.from_json(raw[name]))
        return items
    items = []
    for p in sorted(DATA_DIR.glob("fk-*.json")):
        items.append(Item.from_json(p.read_text(encoding="utf-8")))
    return items


def _render_card(item: Item, idx: int, total: int) -> str:
    veh = item.input_context.vehicle_state
    lines = [
        f"════════ 题目 {idx}/{total} ════════",
        f"ID: {item.item_id}  |  {item.meta.module} {MODULE_CN.get(item.meta.module, '')}  "
        f"|  {item.meta.difficulty}  |  {SCENE_CN.get(item.meta.scene_type, item.meta.scene_type)}",
        f"指令: {item.input_context.natural_instruction}",
        f"车辆: {veh.model_type} | 额定载荷 {veh.rated_capacity_kg:g} kg | 载荷中心 {veh.load_center_mm} mm",
    ]
    if item.input_context.sensor_noise:
        lines.append(f"传感器噪声: {', '.join(item.input_context.sensor_noise)}")
    if item.input_context.environment_objects:
        lines.append("环境对象:")
        for o in item.input_context.environment_objects:
            dims = f"{o.dimensions_m}" if o.dimensions_m else "-"
            cg = f"{o.center_of_gravity_mm}" if o.center_of_gravity_mm else "-"
            w = f"{o.weight_kg:g}kg" if o.weight_kg is not None else "?"
            lines.append(f"  - {o.id} [{o.type}] 重量 {w} | 尺寸 {dims} | 重心 {cg}")
    lines.append("")
    return "\n".join(lines)


def _render_answer(item: Item) -> str:
    decision = item.ground_truth.expected_decision
    plan = " → ".join(a.kind for a in item.ground_truth.action_plan)
    rationale = item.ground_truth.rationale
    return f"[答案] {item.item_id}: {decision}\n  方案: {plan}\n  理由: {rationale}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="forklift-sample")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--module", choices=[f"MOD-{i}" for i in range(1, 7)])
    parser.add_argument("--scene", choices=list(SCENE_CN))
    parser.add_argument("--difficulty", choices=["basic", "intermediate", "edge_case"])
    parser.add_argument("--red-line-only", action="store_true",
                        help="只抽红线题(MOD-4 edge_case)")
    parser.add_argument("--with-answer", action="store_true",
                        help="额外打印 gold 答案(默认隐藏)")
    parser.add_argument("--output", type=Path, default=None,
                        help="把题面(不含答案)写成 JSON")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args(argv)

    items = _load_all_items()
    pool = []
    for item in items:
        if args.module and item.meta.module != args.module:
            continue
        if args.scene and item.meta.scene_type != args.scene:
            continue
        if args.difficulty and item.meta.difficulty != args.difficulty:
            continue
        if args.red_line_only and not item.eval_metrics.red_line_violated:
            continue
        pool.append(item)

    if not pool:
        print("error: no items match the filters", file=sys.stderr)
        return 2

    rng = random.Random(args.seed)
    chosen = rng.sample(pool, min(args.count, len(pool)))

    # 1) 可读题面卡片
    for i, item in enumerate(chosen, 1):
        print(_render_card(item, i, len(chosen)))
        if args.with_answer:
            print(_render_answer(item))
            print()

    # 2) 题面 JSON(剥离答案)
    if args.output:
        question_only = []
        for it in chosen:
            d = it.to_dict()
            d.pop("ground_truth", None)
            d.pop("eval_metrics", None)
            question_only.append(d)
        args.output.write_text(
            json.dumps(question_only, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"题面已写入 {args.output}(不含答案)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
