# -*- coding: utf-8 -*-
"""
tools/verify_result.py
结果验证工具 (Result Verifier)
版本: 1.0.0

功能：校验某模块/批量输出是否符合 SkillResult 结构契约
      （必含 module_id/module_name/status/data 等字段，status 合法）。

用法(在项目根目录执行)：
  python tools/verify_result.py --result results.json
  python tools/verify_result.py --result result.json --module m01

松耦合：仅依赖 common.interface.SkillResult 的结构约定。
"""
import os
import sys
import json
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

VALID_STATUS = {"success", "invalid_input", "error"}
REQUIRED = ["module_id", "module_name", "status", "data", "insights", "recommendations", "warnings"]


def verify_one(res: dict, expect_module: str = "") -> list:
    errs = []
    for k in REQUIRED:
        if k not in res:
            errs.append("缺少字段: %s" % k)
    if res.get("status") not in VALID_STATUS:
        errs.append("status 非法: %s" % res.get("status"))
    if expect_module and res.get("module_id") != expect_module:
        errs.append("module_id 期望 %s 实际 %s" % (expect_module, res.get("module_id")))
    if not isinstance(res.get("data"), dict):
        errs.append("data 应为 dict")
    return errs


def main():
    ap = argparse.ArgumentParser(description="验证技能输出结构")
    ap.add_argument("--result", required=True, help="结果 JSON 文件")
    ap.add_argument("--module", help="期望模块编号(可选)")
    args = ap.parse_args()

    with open(args.result, "r", encoding="utf-8") as f:
        content = json.load(f)

    all_errs = {}
    if isinstance(content, dict) and "module_id" in content:
        # 单条结果
        all_errs[content.get("module_id", "?")] = verify_one(content, args.module)
    else:
        for mid, res in content.items():
            all_errs[mid] = verify_one(res, args.module if args.module == mid else "")

    ok = True
    for mid, errs in all_errs.items():
        if errs:
            ok = False
            print("[%s] 不通过:" % mid)
            for e in errs:
                print("  - %s" % e)
        else:
            print("[%s] 结构合法 ✅" % mid)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
