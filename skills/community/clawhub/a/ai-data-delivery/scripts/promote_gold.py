#!/usr/bin/env python3
"""promote_gold.py — 闭环段：修过的 bad case 沉淀进 gold 集（ai-data-delivery v0.0.4）

铁律：gold 集单调增长，修 A 坏 B 的防线。从 bad case 登记卡生成 gold 用例并落盘。

用法：
  python promote_gold.py --card badcases/bc-001.yaml --gold cases_merged.json
  python promote_gold.py --card badcases/bc-001.yaml --gold gold.yaml --fmt expect

幂等：同 id 已存在则更新期望（口径修正），不重复追加。
登记卡要求已填 expect（type: scalar/rows/refusal + value/rows）——没定期望不许进 gold。
"""
import os
import argparse
import json
import sys

import yaml
from _contract import load


def load_cases(path):
    if not os.path.exists(path):
        # 自动初始化空 gold 集（merged 为 list；expect 格式亦为 list）
        # 注意：data 与 lst 必须是同一对象，否则首条追加会写丢（v0.0.4 实测 bug）
        print(f"提示：{path} 不存在，自动初始化为空 gold 集")
        data = []
        return data, None, data
    with open(path, encoding="utf-8") as f:
        data = json.load(f) if path.endswith(".json") else yaml.safe_load(f)
    wrapper = None
    if isinstance(data, dict):
        for k in ("cases", "gold_results"):
            if k in data:
                wrapper, lst = (data, k), data[k]
                break
        if wrapper is None:
            raise ValueError("gold 文件缺少 cases/gold_results 键")
    else:
        lst = data
    return data, wrapper, lst


def save(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        if path.endswith(".json"):
            json.dump(data, f, ensure_ascii=False, indent=1)
        else:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def to_case(card, fmt):
    e = card.get("expect") or {}
    etype = e.get("type")
    if etype not in ("scalar", "rows", "refusal"):
        raise ValueError("登记卡 expect.type 未填或非法（scalar/rows/refusal）——先定验收期望再入库")
    if fmt == "expect":
        case = {"id": card["id"], "question": card["question"],
                "expect": {"type": etype}}
        if etype == "scalar":
            case["expect"]["value"] = e.get("value")
        elif etype == "rows":
            case["expect"]["rows"] = e.get("rows")
    else:  # merged 格式
        case = {"id": card["id"], "type": "badcase回流", "question": card["question"],
                "expect_reject": etype == "refusal"}
        if etype == "scalar":
            case["gold_rows"] = [[e.get("value")]]
        elif etype == "rows":
            case["gold_rows"] = e.get("rows")
    case["note"] = f"bad case 回流：{card.get('note') or card.get('fix') or ''}"
    return case


def main():
    ap = argparse.ArgumentParser(description="bad case → gold 集")
    ap.add_argument("--card", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--fmt", choices=["merged", "expect"], default="merged")
    args = ap.parse_args()

    card = load(args.card)
    try:
        case = to_case(card, args.fmt)
    except ValueError as e:
        print(f"错误：{e}\n  去这里补：{args.card} 的 expect 段"
              f"（type: scalar/rows/refusal + value/rows）", file=sys.stderr)
        return 2

    data, wrapper, lst = load_cases(args.gold)
    existing = next((i for i, c in enumerate(lst) if c.get("id") == case["id"]), None)
    if existing is None:
        lst.append(case)
        print(f"gold 新增 {case['id']}（{case['question'][:24]}）")
    else:
        lst[existing] = case
        print(f"gold 更新 {case['id']}（同 id 覆盖期望，不重复追加）")
    save(args.gold, data)
    print(f"gold 集现有 {len(lst)} 条；提示：追加后先跑 gold_lint.py 体检，再全量回归")
    return 0


if __name__ == "__main__":
    sys.exit(main())
