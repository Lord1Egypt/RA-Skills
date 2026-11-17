#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.0 五维共振只读覆盖层装配器（读 data.json → 写回顶层 v3 键）

背景：SKILL.md 多处流水线引用 `strategy/build_v3_inputs.py`，但历史发行包漏了该脚本，
导致照文档日更时 v3 层无法装配、报告退回 14 页。本文件补齐该入口，签名与
build_gceo_inputs.py / build_gceo_quant_inputs.py 保持一致（位置参数 + --disable + --print）。

用法（日更流水线，最先装配；强依赖链 v3 → gceo → gceo_quant）：
    python3 "$SKILL/strategy/build_v3_inputs.py" "$D/data.json"           # 装配，framework=v3.0
    python3 "$SKILL/strategy/build_v3_inputs.py" "$D/data.json" --disable # 回滚，framework=v2.3，14 页

行为（只读，不改既有键）：
  * 调 v3_ext.build_overlay(data) 生成覆盖层，v3_ext.report_blocks() 压成渲染块；
  * 写 data["v3"] = {enabled, non_invasive_check, blocks}（渲染器只读这三键）；
  * 默认 v3.enabled=true；--disable 置 false → 渲染器回到 14 页纯 v2.3；
  * 六条口径 / KNOWLEDGE / 四层漏斗 / pipeline 打分一字不改；
  * 自检 14/14 不过则非零退出，阻断出报告。
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from strategy import v3_ext as V          # noqa: E402


def assemble(data: dict, disable: bool = False) -> dict:
    ov = V.build_overlay(data, check_modules=True)
    enabled = bool(not disable)
    # 渲染器契约：v3 顶层只 enabled / non_invasive_check / blocks 三键。
    data["v3"] = {
        "enabled": enabled,
        "non_invasive_check": ov["non_invasive_check"],
        "blocks": V.report_blocks(ov),
    }
    data.setdefault("_caliber_version", "v2.3")
    # 单向强依赖 gceo_quant ⊂ gceo ⊂ v3：v3 关闭则内层一并失效，framework 降 v2.3。
    # 否则会出现「v3.enabled=false 但 framework 仍标 v4.0」的元数据与页数脱节。
    if not enabled:
        if data.get("gceo"):
            data["gceo"]["enabled"] = False
        if data.get("gceo_quant"):
            data["gceo_quant"]["enabled"] = False
        data["_framework_version"] = "v2.3"
    elif data.get("_framework_version") not in ("v3.1", "v4.0"):
        # 仅 v3 装配、内层尚未跑时兜底标注；内层装配器会再升 v3.1/v4.0。
        data["_framework_version"] = "v3.0"
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="装配 v3.0 五维共振只读覆盖层")
    ap.add_argument("data", help="data.json 路径（原地写回）")
    ap.add_argument("--disable", action="store_true",
                    help="置 v3.enabled=false，回滚到 14 页纯 v2.3（内层 gceo/quant 一并失效）")
    ap.add_argument("--print", action="store_true", help="打印装配摘要")
    args = ap.parse_args()

    p = pathlib.Path(args.data).expanduser().resolve()
    if not p.exists():
        sys.exit(f"[!] data.json 不存在：{p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    assemble(data, disable=args.disable)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    v3 = data["v3"]
    chk = v3["non_invasive_check"]
    b = v3["blocks"]
    print("=" * 62)
    print(" v3.0 五维共振只读覆盖层装配器")
    print("=" * 62)
    print(f" v3.enabled = {v3['enabled']}  framework = {data['_framework_version']}")
    print(f" 非侵入自检 {chk['passed']}/{chk['total']} all_ok={chk['all_ok']} "
          f"| 六条口径 + KNOWLEDGE 只读比对")
    print(f" 宏观定位 {b['macro_tag']} | α 折减 ×{b['alpha_multiplier']:.2f} "
          f"| blocks {len(b)} 键")
    print(f" 回滚：--disable → 14 页纯 v2.3；写回：{p}")
    print("=" * 62)
    return 0 if chk["all_ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
