#!/usr/bin/env python3
"""
反思引擎 — 找因果关系，提炼规律，洞见真谛
从历史insights中提炼模式，找出因果链条
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_SKILL_DIR = Path(__file__).resolve().parent.parent
INSIGHTS_FILE = _SKILL_DIR / "memory" / "insights" / "insights.jsonl"


def load_insights(limit: int = 500) -> list[dict]:
    """加载历史insights"""
    if not INSIGHTS_FILE.exists():
        return []
    insights = []
    with open(INSIGHTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                insights.append(json.loads(line))
    return insights[-limit:]


def extract_domains(insights: list[dict]) -> dict[str, list[dict]]:
    """按领域分组insights"""
    domains = defaultdict(list)
    for ins in insights:
        domain = ins.get("domain", "general")
        domains[domain].append(ins)
    return domains


def find_cause_effect_pairs(insights: list[dict]) -> list[dict]:
    """找因果对：前面判断 + 后面验证/结果"""
    pairs = []
    for i, ins in enumerate(insights):
        if ins.get("type") != "judgment":
            continue
        text = ins.get("text", "")
        # 往后找3条，找印证或否定
        for j in insights[i+1:i+4]:
            jtext = j.get("text", "")
            # 检测因果词
            if any(w in jtext for w in ["因为", "所以", "导致", "证明", "结果", "印证"]):
                pairs.append({
                    "cause": text[:100],
                    "effect": jtext[:100],
                    "date": ins.get("date", ""),
                    "confidence": "high" if "印证" in jtext or "证明" in jtext else "medium"
                })
    return pairs


def detect_patterns(insights: list[dict]) -> list[dict]:
    """检测反复出现的模式"""
    # 统计高频词
    word_freq = defaultdict(int)
    for ins in insights:
        words = re.findall(r"[\w]{4,}", ins.get("text", ""))
        for w in words:
            word_freq[w] += 1

    # 找高频词组合（2-gram）
    phrase_freq = defaultdict(int)
    for ins in insights:
        text = ins.get("text", "")
        phrases = re.findall(r"[\w]{4,10}[\s][\w]{4,10}", text)
        for p in phrases:
            phrase_freq[p.strip()] += 1

    top_phrases = sorted(phrase_freq.items(), key=lambda x: -x[1])[:10]
    top_words = sorted(word_freq.items(), key=lambda x: -x[1])[:20]

    patterns = []
    for phrase, freq in top_phrases:
        if freq >= 2:
            patterns.append({
                "pattern": phrase,
                "frequency": freq,
                "type": "phrase"
            })
    for word, freq in top_words:
        if freq >= 3:
            patterns.append({
                "pattern": word,
                "frequency": freq,
                "type": "word"
            })

    return patterns


def derive_dao_insights(patterns: list[dict], cause_effect: list[dict]) -> list[dict]:
    """从模式和因果链中提炼"道"的洞见"""
    insights = []

    if len(cause_effect) >= 2:
        insights.append({
            "level": "dao",
            "text": f"因果链条{len(cause_effect)}条，最强规律：{cause_effect[0]['cause'][:40]} → {cause_effect[0]['effect'][:40]}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    top_patterns = [p for p in patterns if p["frequency"] >= 3]
    if top_patterns:
        pattern_text = "、".join([f"{p['pattern']}({p['frequency']}次)" for p in top_patterns[:5]])
        insights.append({
            "level": "dao",
            "text": f"高频规律：{pattern_text}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    return insights


def run_reflection():
    """主反思流程"""
    insights = load_insights()
    domains = extract_domains(insights)
    cause_effect = find_cause_effect_pairs(insights)
    patterns = detect_patterns(insights)
    dao_insights = derive_dao_insights(patterns, cause_effect)

    print(f"=== 反思报告 ===")
    print(f"总洞见: {len(insights)}")
    print(f"领域数: {len(domains)}")
    print(f"因果对: {len(cause_effect)}")
    print(f"高频模式: {len(patterns)}")
    print()
    print("--- 因果链 ---")
    for p in cause_effect[:5]:
        print(f"  因: {p['cause'][:50]}")
        print(f"  果: {p['effect'][:50]}")
        print()
    print("--- 道之洞见 ---")
    for d in dao_insights:
        print(f"  ★ {d['text']}")

    return {
        "insights_count": len(insights),
        "domains": len(domains),
        "cause_effect_pairs": len(cause_effect),
        "patterns": patterns,
        "dao_insights": dao_insights
    }


def main():
    parser = argparse.ArgumentParser(description="反思引擎")
    parser.add_argument("--limit", "-n", type=int, default=500, help="分析最近N条insights")
    args = parser.parse_args()

    insights = load_insights(args.limit)
    result = run_reflection()
    return 0


if __name__ == "__main__":
    sys.exit(main())
