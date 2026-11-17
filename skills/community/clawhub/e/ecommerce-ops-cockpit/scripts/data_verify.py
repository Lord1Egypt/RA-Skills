#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data_verify.py —— 交付关卡①：数据验真（程序化，对应 R1 / R10）

输入一份 bundle JSON，内含各模块脚本的真实输出（profit_roi / funnel / settlement 等），
程序化检查：
  V1 无 DATA_MISSING / null 残留（R1：真实数据是唯一经营事实）
  V2 无「假设 / 行业均值 / 经验值」来源（R1：禁止编造）
  V3 各模块 verdict 通过（settlement 非 FAIL-P0、funnel 非 DATA_MISSING、profit g_eff>0）
  V4 同一指标多来源时标记「待仲裁」（R5：禁跨源混算）
  V5 关键数值非空

用法：
  python data_verify.py --self-test
  python data_verify.py --bundle bundle.json [--json]
退出码：0 通过；1 未通过；2 输入错误。
"""

import argparse
import json
import sys


def verify(bundle: dict) -> dict:
    checks = []

    def add(cid, name, cond, detail=""):
        checks.append({"id": cid, "name": name, "pass": bool(cond), "detail": detail})

    raw = json.dumps(bundle, ensure_ascii=False)

    # V1 DATA_MISSING / null
    has_missing = ("DATA_MISSING" in raw) or ('"value": null' in raw)
    add("V1", "无 DATA_MISSING / null 残留", not has_missing,
        "" if not has_missing else "发现缺失数据标记")

    # V2 假设来源
    bad_marks = ["行业均值", "经验值", "假设值", "placeholder", "约", "大概"]
    bad_hit = [m for m in bad_marks if m in raw]
    add("V2", "无假设/行业均值来源", not bad_hit,
        "" if not bad_hit else "发现非真实数据来源: " + "/".join(bad_hit))

    # V3 模块 verdict
    modules = bundle.get("modules", {})
    verdict_ok = True
    vd = ""
    for m, out in modules.items():
        if not isinstance(out, dict):
            continue
        if m == "settlement" and out.get("verdict") == "FAIL-P0":
            verdict_ok = False
            vd += " settlement FAIL-P0"
        if m == "funnel" and out.get("verdict") == "DATA_MISSING":
            verdict_ok = False
            vd += " funnel DATA_MISSING"
        if m == "profit" and isinstance(out.get("cost"), dict):
            g = out["cost"].get("可投广告比例 g_eff")
            if g is not None and g <= 0:
                verdict_ok = False
                vd += " profit g_eff<=0"
    add("V3", "各模块 verdict 通过", verdict_ok, vd.strip())

    # V4 跨源混算
    cross = []
    for metric, sources in (bundle.get("cross_source", {}) or {}).items():
        if len(set(sources)) > 1:
            cross.append(metric)
    add("V4", "无跨源混算（待仲裁清单）", len(cross) == 0,
        "需仲裁: " + ",".join(cross) if cross else "无")

    # V5 关键数值非空
    keyvals = bundle.get("key_values", {})
    empty = [k for k, v in keyvals.items() if v is None]
    add("V5", "关键数值非空", len(empty) == 0,
        "空值: " + ",".join(empty) if empty else "无")

    ok = all(c["pass"] for c in checks)
    return {"ok": ok, "checks": checks, "cross_source_pending": cross}


def render(r):
    o = ["【数据验真关卡①】%s" % ("PASS" if r["ok"] else "FAIL")]
    for c in r["checks"]:
        line = "  [%s] %s %s" % (("√" if c["pass"] else "×"), c["id"], c["name"])
        if c["detail"]:
            line += " — " + c["detail"]
        o.append(line)
    if r["cross_source_pending"]:
        o.append("  待仲裁指标（综合任务须四位专家裁定）：" + ",".join(r["cross_source_pending"]))
    return "\n".join(o)


def self_test() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    clean = {"modules": {"settlement": {"verdict": "PASS"}, "funnel": {"verdict": "OK"},
                         "profit": {"cost": {"可投广告比例 g_eff": 0.2}}},
             "key_values": {"毛利率": 0.4, "保本ROI": 2.0}}
    chk("干净 bundle PASS", verify(clean)["ok"])

    bad = {"modules": {"settlement": {"verdict": "FAIL-P0"}}}
    chk("settlement FAIL-P0 → FAIL", not verify(bad)["ok"])

    miss = {"key_values": {"毛利率": None}}
    chk("空关键值 → FAIL", not verify(miss)["ok"])

    cross = {"cross_source": {"ROI": ["平台后台", "广告后台"]}}
    chk("跨源混算 → FAIL", not verify(cross)["ok"])

    print("data_verify self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="数据验真关卡")
    ap.add_argument("--bundle", help="验真 bundle JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.bundle:
        ap.error("需要 --bundle 或 --self-test")
    with open(a.bundle, "r", encoding="utf-8") as f:
        bundle = json.load(f)
    r = verify(bundle)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
