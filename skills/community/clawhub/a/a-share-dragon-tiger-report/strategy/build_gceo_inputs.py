#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.1 GCCEO 全量整合层装配器（读 data.json → 写回顶层 gceo 键）

用法（日更流水线第 ③ 步，接在 build_v3_inputs.py 之后）：
    python3 "$SKILL/strategy/build_gceo_inputs.py" "$D/data.json"

行为：
  * 读 data.json，从既有 data.v3.non_invasive_check 取 v3 自检结果复用；
  * 调 gcceo_ext.build_gceo_overlay(...) 生成只读覆盖层；
  * 写 data["gceo"] = overlay，并把 data["gceo"]["blocks"] = gceo_report_blocks(overlay)；
  * 默认 gceo.enabled=true；--disable 置 false（回滚到 v3.0 16 页）；
  * 若 data.v3.enabled 非真，则给 gceo.enabled 也置 false（强依赖，避免引用断裂）；
  * 六条口径 / KNOWLEDGE / v3 五模块一字不改，仅新增顶层 gceo 键。

回滚：python3 build_gceo_inputs.py "$D/data.json" --disable
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

from strategy import gcceo_ext as G  # noqa: E402


def assemble(data: dict, disable: bool = False) -> dict:
    v3 = data.get("v3") or {}
    v3_on = bool(v3.get("enabled"))
    v3_check = v3.get("non_invasive_check")
    # GCCEO 强依赖 v3：v3 关闭时 GCCEO 一并关闭，杜绝「引用不存在层」。
    enabled = bool(v3_on and not disable)

    ov = G.build_gceo_overlay(data, check_modules=True, v3_check=v3_check)
    ov["enabled"] = enabled
    ov["blocks"] = G.gceo_report_blocks(ov)
    data["gceo"] = ov
    data.setdefault("_caliber_version", "v2.3")
    data["_framework_version"] = "v3.1" if enabled else "v3.0"
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="装配 v3.1 GCCEO 全量整合只读覆盖层")
    ap.add_argument("data", help="data.json 路径（原地写回）")
    ap.add_argument("--disable", action="store_true",
                    help="置 gceo.enabled=false，回滚到 v3.0 16 页")
    ap.add_argument("--print", action="store_true", help="打印装配摘要")
    args = ap.parse_args()

    p = pathlib.Path(args.data).expanduser().resolve()
    if not p.exists():
        sys.exit(f"[!] data.json 不存在：{p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    assemble(data, disable=args.disable)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    g = data["gceo"]
    chk = g["non_invasive_check"]
    if args.print or True:
        print("=" * 62)
        print(" v3.1 GCCEO 全量整合层装配器")
        print("=" * 62)
        print(f" gceo.enabled = {g['enabled']}  framework = {data['_framework_version']}")
        print(f" 十域 {g['source_counts']['domain_skills']} 技能 / 投行 {g['source_counts']['ib_pe']} / "
              f"出海 {g['source_counts']['globalization']} / AI 超能力 {g['source_counts']['ai_superpowers']} / "
              f"方法论 {g['source_counts']['method_tools']}")
        print(f" 非侵入自检 {chk['passed']}/{chk['total']} all_ok={chk['all_ok']} "
              f"| v3 复用 {str((chk.get('v3_recheck') or {}).get('passed', '—'))}/14")
        print(f" 回滚：gceo.enabled=false → v3.0 16 页；v3.enabled=false → v2.3 14 页")
        print(f" 写回：{p}")
        print("=" * 62)
    # 自检不全绿则非零退出，阻断出报告
    return 0 if chk["all_ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
