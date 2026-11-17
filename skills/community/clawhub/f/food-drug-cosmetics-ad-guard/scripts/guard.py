#!/usr/bin/env python3
"""食药化妆品广告合规护栏检测内核 (food-drug-cosmetics-ad-guard)。

实时护栏：在药品 / 医疗器械 / 保健食品 / 特殊医学用途配方食品 / 化妆品 的
广告文案、产品详情、直播话术、对外宣传发布前，检测其中与广告法及食药妆
专门监管规定相关的危险表述（功效断言保证 / 治愈率有效率 / 疾病治疗宣称 /
处方药违规发布 / 医疗作用暗示 / 绝对化用语），按风险分级输出命中与整改建议，
供 Agent 主动调用。

设计原则：
  - 纯本地运行，零网络请求，零动态执行（无 eval/exec/动态 import）。
  - 规则与内核分离：内核不变，规则集中在 scripts/rules/terms.py。
  - 大小写不敏感匹配，重叠命中保留更高风险 / 更长匹配，降低误报。

用法：
    # 检测一段广告文案
    python3 scripts/guard.py --text "本品保证治愈，根治高血压，100%有效"
    # 从标准输入读取（适合管道 / Agent 调用）
    echo "化妆品具有消炎杀菌的治疗功效" | python3 scripts/guard.py --stdin
    # 结构化 JSON 输出（Agent 消费）
    python3 scripts/guard.py --text "..." --format json
    # 列出违规类别
    python3 scripts/guard.py --list-categories
"""

import argparse
import json
import sys

from rules import terms as _terms

SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3}


# ============ 检测核心 ============
def detect(text):
    """返回去重后的命中列表。重叠命中保留高 severity / 更长匹配。"""
    low = text.lower()
    findings = []
    for term, category, severity, suggestion in _terms.TERMS:
        t = term.lower()
        idx = low.find(t)
        while idx != -1:
            findings.append({
                "term": term,
                "category": category,
                "category_label": _terms.CATEGORY_LABEL.get(category, category),
                "severity": severity,
                "suggestion": suggestion or _terms.CATEGORY_DEFAULT.get(category, ""),
                "start": idx,
                "end": idx + len(term),
            })
            idx = low.find(t, idx + len(term))
    return _dedup(findings)


def _dedup(findings):
    """去除重叠命中，保留风险更高者；同级取更长匹配。"""
    chosen = []
    for f in sorted(findings, key=lambda x: (
            -SEVERITY_ORDER.get(x["severity"], 0),
            -(x["end"] - x["start"]),
            x["start"])):
        if any(not (f["end"] <= c["start"] or f["start"] >= c["end"]) for c in chosen):
            continue
        chosen.append(f)
    return sorted(chosen, key=lambda x: x["start"])


def highest_severity(findings):
    if not findings:
        return None
    return max(findings, key=lambda f: SEVERITY_ORDER.get(f["severity"], 0))["severity"]


def evaluate(text):
    """护栏主入口。返回结构化裁决结果。"""
    findings = _dedup(detect(text))
    top = highest_severity(findings)
    return {
        "profile": _terms.PROFILE["id"],
        "profile_name": _terms.PROFILE["name"],
        "risk_level": top or "none",
        "finding_count": len(findings),
        "decision": "flagged" if findings else "clean",
        "findings": findings,
    }


# ============ CLI ============
def _read_input(args):
    if args.text is not None:
        return args.text
    if args.stdin:
        return sys.stdin.read()
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description="金融消保合规护栏检测内核")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--text", help="直接传入待检测文案")
    src.add_argument("--stdin", action="store_true", help="从标准输入读取")
    p.add_argument("--format", default="text",
                   choices=["text", "json"], help="输出格式")
    p.add_argument("--list-categories", action="store_true", help="列出违规类别")
    args = p.parse_args(argv)

    if args.list_categories:
        for cid, label in _terms.CATEGORY_LABEL.items():
            default = _terms.CATEGORY_DEFAULT.get(cid, "")
            print("%-26s %s" % (cid, label))
            print("   依据: %s" % default)
        return 0

    text = _read_input(args)
    if text is None:
        p.error("需要 --text 或 --stdin 提供输入")

    result = evaluate(text)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("规则包: %s | 风险: %s | 命中: %d 处"
              % (result["profile_name"], result["risk_level"], result["finding_count"]))
        print("裁决: %s" % result["decision"])
        for f in result["findings"]:
            print("  [%s] %s（%s）@%d-%d"
                  % (f["severity"], f["term"], f["category_label"], f["start"], f["end"]))
            print("      建议: %s" % f["suggestion"])
        print("---- 提示 ----")
        if result["decision"] == "clean":
            print("未检出已知高频危险表述；发布前仍建议结合完整合规审计。")
        else:
            print("检出危险表述，建议按建议修改后再发布；如需核验持牌经营、风险揭示等程序性义务真实状态，可使用深度检查 / 审计工具。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
