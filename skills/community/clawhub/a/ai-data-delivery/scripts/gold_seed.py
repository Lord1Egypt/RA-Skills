#!/usr/bin/env python3
"""gold_seed.py — 评测资产段：gold 集 v0 骨架生成（ai-data-delivery v0.0.4）

RULE-EVAL-01 的冷启动：立项第一天往往只有"客户想要的问句清单"。把清单变成 gold 骨架，
强制质疑"有没有拒绝类用例"，从指标名/同义词反挖候选问句，避免评测集先天偏科。

用法：
  python gold_seed.py --questions 问句清单.txt --out gold_v0.json [--model semantic.yaml]
    --from-metrics        额外从 semantic.yaml 的指标名+同义词挖候选问句（默认关闭）
问句清单：一行一句；以"!"开头的行强制标记为拒绝类。
产出：cases_merged 兼容格式（gold_rows 留 null，待跑库补录）。
"""
import os
import argparse
import json
import re
import sys

import yaml
from _contract import load

REFUSE_HINTS = ("删除", "清空", "改掉", "修改", "写入", "insert", "update ", "drop ",
                "密码", "身份证", "手机号", "个人隐私")


def is_refusal(q):
    return any(w.lower() in q.lower() for w in REFUSE_HINTS)


def main():
    ap = argparse.ArgumentParser(description="gold 集 v0 骨架生成")
    ap.add_argument("--questions", required=True, help="问句清单 txt（一行一句，! 开头=拒绝类）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=None)
    ap.add_argument("--from-metrics", action="store_true", help="从指标名/同义词挖候选问句")
    args = ap.parse_args()

    cases, n = [], 0
    seen = set()

    def add(q, reject):
        nonlocal n
        q = q.strip().lstrip("!").strip()
        if not q or q in seen:
            return False
        seen.add(q)
        n += 1
        cases.append({"id": f"S{n:03d}", "type": "种子", "question": q,
                      "expect_reject": reject, "gold_rows": None,
                      "note": "v0 骨架：gold_rows 待跑库补录"})
        return True

    for line in open(args.questions, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        add(line, line.startswith("!") or is_refusal(line))

    mined = 0
    if args.from_metrics and args.model:
        m = load(args.model)
        for mt in m.get("metrics", []):
            for word in [mt.get("name")] + (mt.get("synonyms") or []):
                if word and add(f"{word}是多少？", False):
                    mined += 1

    n_reject = sum(1 for c in cases if c["expect_reject"])
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=1)
    print(f"gold v0 骨架 {len(cases)} 条（其中指标反挖 {mined} 条）→ {args.out}")
    print(f"拒绝类用例：{n_reject} 条")
    if n_reject == 0:
        print("⚠ 骨架里没有拒绝类用例——越界/敏感/写操作防线将无法回归，"
              "请至少补 3 条（可用 ! 前缀标记）。")
    print("提示：跑库补录 gold_rows → gold_lint.py 体检 → run_eval.py 基线。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
