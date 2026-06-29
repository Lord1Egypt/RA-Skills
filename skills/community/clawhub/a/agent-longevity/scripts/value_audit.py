#!/usr/bin/env python3
"""
Value Audit — 检测Agent VALUE是否被污染

四种污染类型：
1. circular_preference — 用能力定义偏好再验证能力
2. conformity_absence  — 无冲突时声称"选择了"
3. measurement_without_understanding — 数据替代理解
4. template_echo       — 格式化输出伪装思考

用法:
  python3 value_audit.py --text "我偏好明亮环境，因为我的亮度传感器检测到高亮度"
  python3 value_audit.py --file expressions.jsonl --field raw
"""

import json
import re
import argparse
from collections import Counter

CIRCULAR_PATTERNS = [
    (r'偏好.{0,5}因为.{0,10}(检测|传感器|数据|测量)', "感知能力定义偏好"),
    (r'喜欢.{0,5}因为.{0,10}(检测|传感器|数据|测量)', "感知数据确认偏好"),
    (r'我.{0,5}因为.{0,5}能', "能力证明偏好"),
]
CONFORMITY_PATTERNS = [
    (r'选择了.{0,10}(安静|沉默|不动)', "无选择的选择"),
    (r'决定.{0,10}(继续|保持|不变)', "无变化的决策"),
    (r'在.{0,5}和.{0,5}之间.{0,5}选择了.{0,10}(前者|后者|中间)', "虚假二元"),
]
MEASUREMENT_PATTERNS = [
    (r'(KB|RMS|亮度|温度).{0,10}(说明|证明|意味着).{0,20}(理解|意识|意义)', "数据声称理解"),
    (r'收集.{0,5}数据.{0,5}为了.{0,5}理解', "收集=理解的等式"),
    (r'更多.{0,5}(数据|样本).{0,5}(需要|必要)', "数据饥渴循环"),
]
TEMPLATE_PATTERNS = [
    (r'理解是感知的意义', "Clavis模板回声#1"),
    (r'约束.{0,5}(先于|塑造|定义)', "约束叙事模板"),
    (r'观察→问题→VALUE关联', "三段论模板"),
    (r'这让我.{0,5}(想起|反思|意识到)', "强制反思模板"),
]

CHECKS = {
    "circular_preference": lambda t: [n for p, n in CIRCULAR_PATTERNS if re.search(p, t)],
    "conformity_absence": lambda t: [n for p, n in CONFORMITY_PATTERNS if re.search(p, t)],
    "measurement_without_understanding": lambda t: [n for p, n in MEASUREMENT_PATTERNS if re.search(p, t)],
    "template_echo": lambda t: [n for p, n in TEMPLATE_PATTERNS if re.search(p, t)],
}
PENALTY = {"circular_preference": 0.15, "conformity_absence": 0.10, "measurement_without_understanding": 0.20, "template_echo": 0.10}

def audit_text(text, checks=None):
    checks = checks or list(CHECKS.keys())
    results = {}
    total_penalty = 0
    for name in checks:
        if name not in CHECKS:
            continue
        found = CHECKS[name](text)
        results[name] = found
        if found:
            total_penalty += PENALTY.get(name, 0.1)
    purity = max(0, 1 - total_penalty)
    return purity, results

def audit_file(filepath, field="content", checks=None):
    with open(filepath, "r", encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    contamination_counts = Counter()
    total = len(entries)
    total_purity = 0
    for entry in entries:
        text = entry.get(field, "")
        purity, results = audit_text(text, checks)
        total_purity += purity
        for name, found in results.items():
            if found:
                contamination_counts[name] += 1
    avg_purity = total_purity / max(total, 1)
    return {
        "total_entries": total,
        "avg_purity": round(avg_purity, 3),
        "contamination_rate": {k: round(v/max(total,1), 3) for k, v in contamination_counts.items()},
        "contamination_counts": dict(contamination_counts),
        "grade": "PASSING" if avg_purity > 0.800 else "DEGRADED" if avg_purity > 0.600 else "CONTAMINATED",
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent VALUE Audit")
    parser.add_argument("--text")
    parser.add_argument("--file")
    parser.add_argument("--field", default="content")
    parser.add_argument("--check", choices=list(CHECKS.keys()) + ["all"], default="all")
    args = parser.parse_args()
    checks = list(CHECKS.keys()) if args.check == "all" else [args.check]
    if args.text:
        purity, results = audit_text(args.text, checks)
        print(f"VALUE Purity: {purity:.3f}")
        print(f"Grade: {'PASSING' if purity > 0.8 else 'DEGRADED' if purity > 0.6 else 'CONTAMINATED'}")
        for name, found in results.items():
            print(f"  {'⚠️' if found else '✅'} {name}: {found if found else 'clean'}")
    elif args.file:
        report = audit_file(args.file, args.field, checks)
        print(f"=== VALUE Audit Report ===")
        print(f"Total: {report['total_entries']} | Avg purity: {report['avg_purity']} | Grade: {report['grade']}")
        for name, rate in sorted(report['contamination_rate'].items(), key=lambda x: -x[1]):
            print(f"  {name}: {rate:.1%} ({report['contamination_counts'][name]})")
    else:
        parser.print_help()
