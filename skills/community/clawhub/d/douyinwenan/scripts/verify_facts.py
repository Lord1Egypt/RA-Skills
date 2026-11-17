# -*- coding: utf-8 -*-
"""事实核验脚本 — 提取文案中的数字/年份/百分比/政策关键词，生成人工核验清单

用法:
  python verify_facts.py "文案文本"
  python verify_facts.py --file draft.txt
  python verify_facts.py --json "文案文本"

设计原则：脚本不信任模型记忆，只负责「找出需要核验的点」，
最终准确性由「搜索比对 + 人工核对」双轨保证。
"""
import argparse
import json
import re
import sys

# 数字/百分比/年份
NUM_RE = re.compile(r"\d+(?:\.\d+)?%?")
YEAR_RE = re.compile(r"(?:19|20)\d{2}\s*年?")
# 政策/考试相关关键词
POLICY_KEYWORDS = [
    "政策", "改革", "新规", "规定", "办法", "通知", "意见", "方案",
    "高考", "考研", "单招", "专升本", "分数线", "录取率", "报录比",
    "扩招", "缩招", "双减", "新课标", "教育部", "教育厅", "省考试院",
    "编制", "公务员", "事业编", "就业率", "薪资", "平均工资",
]
# 绝对化/承诺类（转给 compliance 处理，这里只提示）
ABSOLUTE_WORDS = ["第一", "最", "绝对", "一定", "100%", "百分百", "保证", "稳了"]


def extract_facts(text):
    facts = []
    # 数字（含上下文）
    for m in NUM_RE.finditer(text):
        start = max(0, m.start() - 12)
        end = min(len(text), m.end() + 12)
        context = text[start:end].replace("\n", " ")
        facts.append({"type": "number", "value": m.group(0), "context": context})
    # 年份
    for m in YEAR_RE.finditer(text):
        start = max(0, m.start() - 12)
        end = min(len(text), m.end() + 12)
        context = text[start:end].replace("\n", " ")
        facts.append({"type": "year", "value": m.group(0), "context": context})
    # 政策关键词
    for kw in POLICY_KEYWORDS:
        for m in re.finditer(kw, text):
            start = max(0, m.start() - 12)
            end = min(len(text), m.end() + 12)
            context = text[start:end].replace("\n", " ")
            facts.append({"type": "policy", "value": kw, "context": context})
    return facts


def dedupe(facts):
    seen = set()
    out = []
    for f in facts:
        key = (f["type"], f["value"], f["context"][:20])
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out


def main():
    parser = argparse.ArgumentParser(description="事实核验清单生成")
    parser.add_argument("text", nargs="?", help="文案文本")
    parser.add_argument("--file", help="从文件读取")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("用法: python verify_facts.py '文案' 或 --file draft.txt")
        sys.exit(1)

    facts = dedupe(extract_facts(text))
    if args.json:
        print(json.dumps({"facts": facts, "count": len(facts)}, ensure_ascii=False, indent=2))
        return

    print("--- 事实核验清单 ---")
    if not facts:
        print("未检测到数字/年份/政策关键词。注意：无数据支撑的文案传播力弱。")
        sys.exit(0)
    print(f"共 {len(facts)} 个事实点需要人工核对：\n")
    for i, f in enumerate(facts, 1):
        print(f"[{i}] ({f['type']}) {f['value']}")
        print(f"    上下文: ...{f['context']}...")
        print(f"    核对项: 来源? 年份? 口径? 是否过时?\n")
    print("提示: 每个数字/政策必须能给出来源（官方文件/权威媒体），")
    print("无法溯源的数据一律删除或改为模糊表述（如'近年'）。")
    sys.exit(0)


if __name__ == "__main__":
    main()
