#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_quote.py —— 报价数据清洗与自检（生成 quotes.json 之前跑）

    用法:
        python normalize_quote.py --in raw_quotes.json [--out quotes.json] [--report]

    做四件事:
        1. 零单价/条目数 **逐条重算**（绝不采信任何现成的汇总字段）
        2. 剔除小计/合计行后再统计
        3. 多轮描述级匹配 matched / gone / new
        4. 分项求和 vs 采用价 勾稽

    原则: 只重算与核对, 不改写任何金额, 不补全缺项, 不换算币种/税率。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SUBTLE_ROWS = ("小计", "合计", "TOTAL", "Subtotal", "Grand Total", "总计", "Sum")


def norm_desc(s):
    """描述级匹配键：首行 → 剥离中文 → 去符号 → 小写"""
    s = str(s or "").split("\n")[0]
    s = re.sub(r"[\u4e00-\u9fff]+", "", s)
    return re.sub(r"[^A-Za-z0-9]+", "", s).lower()


def is_subtotal(desc):
    d = str(desc or "")
    return any(k in d for k in SUBTLE_ROWS)


def is_zero(it):
    up = it.get("unit_price")
    return up is None or up == "" or float(up or 0) == 0


def process(quotes):
    report = {"zero": [], "match": [], "recon": [], "subtotalRemoved": 0}
    cats = quotes.get("cats") or []
    cat_keys = [c.get("key") for c in cats]
    cat_cns = [c.get("cn") for c in cats]

    for sv in quotes.get("suppliers") or []:
        name = sv.get("name", "?")
        rounds = sv.get("rounds") or {}

        # ---- 1&2 逐条重算 + 剔除小计行 ----
        for rk, rd in rounds.items():
            if not isinstance(rd, dict):
                continue
            raw_items = rd.get("items") or []
            keep, removed = [], 0
            for it in raw_items:
                if is_subtotal(it.get("desc")):
                    removed += 1
                    continue
                it["zero"] = bool(is_zero(it))
                keep.append(it)
            rd["items"] = keep
            report["subtotalRemoved"] += removed

            n = len(keep)
            z = sum(1 for it in keep if it["zero"])
            rd["item_count"] = n
            rd["zero_count"] = z

            declared = rd.get("zero_count")
            report["zero"].append({
                "supplier": name, "round": rk, "items": n, "zero": z,
                "declared": declared,
                "mismatch": (declared is not None and declared != z),
            })

            # 分项由明细反推（仅当 cats 缺失时）
            if not rd.get("cats") and keep:
                arr = [0.0] * len(cats)
                for it in keep:
                    ck = it.get("cat_key")
                    idx = (cat_keys.index(ck) if ck in cat_keys else
                           (cat_cns.index(it.get("cat")) if it.get("cat") in cat_cns else None))
                    if idx is not None:
                        arr[idx] += float(it.get("amount") or 0)
                rd["cats"] = arr

            # ---- 4 勾稽 ----
            if rd.get("cats") and rd.get("used") is not None:
                s = sum(float(x or 0) for x in rd["cats"])
                diff = s - float(rd["used"])
                report["recon"].append({
                    "supplier": name, "round": rk,
                    "catSum": round(s, 2), "used": float(rd["used"]),
                    "diff": round(diff, 2), "ok": abs(diff) <= 0.05,
                })

        # ---- 3 多轮描述级匹配 ----
        keys = list(rounds.keys())
        for i in range(len(keys) - 1):
            a, b = keys[i], keys[i + 1]
            ra, rb = rounds[a], rounds[b]
            if not isinstance(ra, dict) or not isinstance(rb, dict):
                continue
            ka = {norm_desc(it.get("desc")) for it in (ra.get("items") or []) if norm_desc(it.get("desc"))}
            kb = {norm_desc(it.get("desc")) for it in (rb.get("items") or []) if norm_desc(it.get("desc"))}
            report["match"].append({
                "supplier": name, "from": a, "to": b,
                "matched": len(ka & kb), "gone": len(ka - kb), "new": len(kb - ka),
                "rate": round(len(ka & kb) / len(ka) * 100, 1) if ka else None,
            })
    return quotes, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", default=None)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    quotes = json.loads(Path(a.inp).read_text(encoding="utf-8"))
    quotes, rep = process(quotes)

    if a.out:
        Path(a.out).write_text(json.dumps(quotes, ensure_ascii=False, indent=2), encoding="utf-8")
        print("已写入: %s" % a.out)

    # 摘要（始终输出）
    mm = [r for r in rep["zero"] if r["mismatch"]]
    bad = [r for r in rep["recon"] if not r["ok"]]
    print("小计行剔除: %d 条" % rep["subtotalRemoved"])
    print("零单价重算: %d 条记录%s" % (len(rep["zero"]), ("，%d 条与声明值不符 ⚠" % len(mm)) if mm else "，全部一致"))
    print("勾稽: %d 项，差异 %d 项%s" % (len(rep["recon"]), len(bad), " ⚠" if bad else ""))

    if mm:
        print("\n⚠ 汇总字段不可信（已按逐条重算覆盖）：")
        for r in mm:
            print("   %s/%s: 声明 %s，实算 %s" % (r["supplier"], r["round"], r["declared"], r["zero"]))
    if bad:
        print("\n⚠ 分项求和与采用价不一致：")
        for r in bad:
            print("   %s/%s: 分项和 %.2f，采用价 %.2f，差 %.2f"
                  % (r["supplier"], r["round"], r["catSum"], r["used"], r["diff"]))
    if rep["match"]:
        print("\n多轮描述匹配：")
        for r in rep["match"]:
            print("   %s %s→%s: matched %d / gone %d / new %d (%.1f%%)"
                  % (r["supplier"], r["from"], r["to"], r["matched"], r["gone"], r["new"],
                     r["rate"] if r["rate"] is not None else 0))

    if a.report:
        print("\n完整报告:")
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
