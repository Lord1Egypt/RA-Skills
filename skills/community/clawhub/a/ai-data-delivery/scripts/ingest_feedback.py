#!/usr/bin/env python3
"""ingest_feedback.py — 评测资产段：用户反馈入 bad case 池（ai-data-delivery v0.0.4）

RULE-LOOP-01 的入口：试点期用户在群里说"这个答错了"，不能止于聊天记录——就地进池，
与 capture_case.py 的取证卡同构，统一走 triage → 修复 → promote_gold 闭环。

用法：
  python ingest_feedback.py --pool badcases/ --question "问句" --note "用户原话/场景" \
      [--source 用户反馈] [--id FB001]
同问句重复反馈：不重复建卡，次数 +1（热度即优先级信号）。
退出码：0 成功；2 用法错误。
"""
import argparse
import datetime
import glob
import os
import re
import sys

import yaml
from _contract import load


def next_id(pool):
    ids = []
    for p in glob.glob(os.path.join(pool, "*.yaml")):
        mm = re.match(r"FB(\d+)", os.path.basename(p))
        if mm:
            ids.append(int(mm.group(1)))
    return f"FB{(max(ids) + 1) if ids else 1:03d}"


def main():
    ap = argparse.ArgumentParser(description="用户反馈入 bad case 池")
    ap.add_argument("--pool", required=True, help="bad case 池目录")
    ap.add_argument("--question", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--source", default="用户反馈")
    ap.add_argument("--id", default=None)
    args = ap.parse_args()

    os.makedirs(args.pool, exist_ok=True)
    # 去重：同问句只累计次数
    for p in glob.glob(os.path.join(args.pool, "*.yaml")):
        c = load(p)
        if c and c.get("question") == args.question:
            c["feedback_count"] = c.get("feedback_count", 1) + 1
            c.setdefault("notes_log", []).append(
                {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
                 "note": args.note, "source": args.source})
            yaml.safe_dump(c, open(p, "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False)
            print(f"同问句已存在 → {p}（反馈次数 {c['feedback_count']}，优先级上调）")
            return 0

    cid = args.id or next_id(args.pool)
    card = {
        "id": cid,
        "captured_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "question": args.question,
        "note": args.note,
        "source": args.source,
        "feedback_count": 1,
        "evidence": None,          # 反馈卡无活引擎证据；取证请跑 capture_case.py
        "symptom": None, "layer": None, "fix": None, "verify": None,
        "expect": {"type": None, "value": None, "rows": None},
        "regression_before": None, "regression_after": None,
    }
    out = os.path.join(args.pool, f"{cid}.yaml")
    yaml.safe_dump(card, open(out, "w", encoding="utf-8"),
                   allow_unicode=True, sort_keys=False)
    print(f"反馈已入池 → {out}")
    print("提示：补 symptom/layer/expect 后可 promote_gold.py 回流评测集；"
              "需活引擎证据先跑 capture_case.py。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
