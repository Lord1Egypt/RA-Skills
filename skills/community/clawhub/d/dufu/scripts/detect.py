#!/usr/bin/env python3
"""Heuristic Chinese writing signals; never presents a probability of being AI-written."""

import argparse
import json
import re
import sys
from pathlib import Path

CONNECTIVES = ("首先", "其次", "最后", "此外", "然而", "因此", "综上所述", "值得注意的是", "总而言之")
ABSTRACT = ("赋能", "闭环", "抓手", "底层逻辑", "颗粒度", "全方位", "全面提升", "深刻")
SYMMETRY = ("不仅", "而且", "不是", "而是")


def split_sentences(text):
    return [s.strip() for s in re.split(r"[。！？!?；;\n]+", text) if s.strip()]


def analyze(text):
    sentences = split_sentences(text)
    hits = {"connectives": [w for w in CONNECTIVES if w in text],
            "abstract_terms": [w for w in ABSTRACT if w in text],
            "symmetric_patterns": [w for w in SYMMETRY if w in text]}
    lengths = [len(s) for s in sentences]
    anchors = re.findall(r"(?:\d+(?:\.\d+)?%?|20\d{2}年|[一二三四五六七八九十]+月|[北京上海广州深圳杭州成都])", text)
    flags = []
    if hits["connectives"]:
        flags.append("段落可能依赖模板连接词")
    if hits["abstract_terms"]:
        flags.append("存在需要具体化的抽象词")
    if len(hits["symmetric_patterns"]) >= 2:
        flags.append("存在对称句式，可检查是否过于工整")
    if lengths and max(lengths) > 45:
        flags.append("存在较长句子，可按语义拆分")
    if not anchors:
        flags.append("未发现明显时间、数字或地点锚点；不代表原文有问题")
    return {"sentence_count": len(sentences), "sentence_lengths": lengths,
            "hits": hits, "fact_anchor_examples": anchors[:10], "heuristic_flags": flags}


def main():
    parser = argparse.ArgumentParser(description="Detect common Chinese template signals")
    parser.add_argument("--file", type=Path, help="UTF-8 text file; omit to read stdin")
    parser.add_argument("--json", action="store_true", help="print JSON output")
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
    result = analyze(text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("启发式提示（不是 AI 概率）")
        for flag in result["heuristic_flags"]:
            print(f"- {flag}")


if __name__ == "__main__":
    main()
