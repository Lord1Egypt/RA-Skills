#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v4.0 投行级量化研判层装配器（读 data.json → 写回顶层 gceo_quant 键）

用法（日更流水线第 ④ 步，接在 build_gceo_inputs.py 之后）：
    python3 "$SKILL/strategy/build_gceo_quant_inputs.py" "$D/data.json"

行为（强依赖，三层正交单向叠加）：
  * 仅当 data.v3.enabled 且 data.gceo.enabled 时 gceo_quant 才可能为 true；
    否则强制置 false，杜绝「引用不存在层」。
  * 复用 limitup_source.verify_covered() 的冻结闸门实跑结论喂给 DECIDE 步（只读引用，不重跑判定）。
  * 调 gceo_quant.build_gceo_quant_overlay(...) 生成真值研判 + 缺口台账；
  * 写 data["gceo_quant"] = overlay（含 blocks），并把 _framework_version 升 v4.0；
  * --disable 置 gceo_quant.enabled=false，回滚到 v3.1 的 18 页（前 18 页逐字不变）；
  * 六条口径 / KNOWLEDGE / v3 五模块 / gcceo 映射 / 冻结闸门 / pipeline 打分一律不改。

回滚：python3 build_gceo_quant_inputs.py "$D/data.json" --disable
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

from strategy import gceo_quant as Q          # noqa: E402
from strategy import limitup_source as LS     # noqa: E402


def _verify_from(data: dict) -> dict | None:
    """只读复用涨停源冻结闸门实跑结论（若当前为涨停源主口径）；否则 None。"""
    if data.get("selection_mode") != LS.MODE_LIMITUP:
        return None
    try:
        screen = LS.build_screen(data)
        return LS.verify_covered(data, screen)
    except Exception:
        # 闸门数据不齐时降级：研判页把相关标的标「未核验/非涨停源」，不伪造通过。
        return None


def assemble(data: dict, disable: bool = False) -> dict:
    v3 = data.get("v3") or {}
    gceo = data.get("gceo") or {}
    v3_on = bool(v3.get("enabled"))
    gceo_on = v3_on and bool(gceo.get("enabled"))
    # v4.0 强依赖 gceo⊂v3；任一关闭则本层一并关闭。
    enabled = bool(gceo_on and not disable)

    verify = _verify_from(data)
    ov = Q.build_gceo_quant_overlay(data, verify=verify, check_modules=True)
    ov["enabled"] = enabled
    ov["depends_on"] = {"v3.enabled": v3_on, "gceo.enabled": gceo_on}
    data["gceo_quant"] = ov
    data.setdefault("_caliber_version", "v2.3")
    # 框架版本随最外层开关升降：v4.0 / v3.1 / v3.0（回滚可逆）。
    data["_framework_version"] = "v4.0" if enabled else ("v3.1" if gceo_on else "v3.0")
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="装配 v4.0 投行级量化研判层（真值算 + 缺口标注）")
    ap.add_argument("data", help="data.json 路径（原地写回）")
    ap.add_argument("--disable", action="store_true",
                    help="置 gceo_quant.enabled=false，回滚到 v3.1 18 页")
    ap.add_argument("--print", action="store_true", help="打印装配摘要")
    args = ap.parse_args()

    p = pathlib.Path(args.data).expanduser().resolve()
    if not p.exists():
        sys.exit(f"[!] data.json 不存在：{p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    assemble(data, disable=args.disable)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    q = data["gceo_quant"]
    chk = q["non_invasive_check"]
    b = q["blocks"]
    if args.print or True:
        print("=" * 64)
        print(" v4.0 投行级量化研判层装配器 · 真值算 + 缺口标注")
        print("=" * 64)
        print(f" gceo_quant.enabled = {q['enabled']}  framework = {data['_framework_version']}")
        print(f" 依赖：v3={q['depends_on']['v3.enabled']} / gceo={q['depends_on']['gceo.enabled']}")
        print(f" 非侵入自检 {chk['passed']}/{chk['total']} all_ok={chk['all_ok']} "
              f"| 冻结口径 + KNOWLEDGE45 + v3.0 + GCCEO4.0 只读比对")
        print(f" 研判池 {b['universe_n']} 只（{b['universe_src']}）| "
              f"PE 中位 {b['dist']['pe_median']} / 亏损 {b['dist']['n_loss']} / "
              f"负增长 {b['dist']['n_neg_growth']}")
        print(f" 缺口台账 {b['counts']['gap_fields']} 穿透字段 + {b['counts']['extra_gaps']} 估值字段 全标注")
        print(f" 回滚：gceo_quant.enabled=false → v3.1 18 页；源码不编造 DCF/LBO/ROE/净现比")
        print(f" 写回：{p}")
        print("=" * 64)
    return 0 if chk["all_ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
