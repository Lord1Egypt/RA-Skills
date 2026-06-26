#!/usr/bin/env python3
"""
每日复盘 — 每日23:00自动执行
复盘今日对话，追溯因果，提炼洞见，写入记忆
"""

from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# 路径计算
_SKILL_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = _SKILL_DIR / "memory"
DAILY_DIR = MEMORY_DIR / "daily"
INSIGHTS_FILE = MEMORY_DIR / "insights" / "insights.jsonl"

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
TODAY_FILE = DAILY_DIR / f"{TODAY}.jsonl"


def load_today_logs() -> list[dict]:
    """加载今日所有对话日志"""
    logs = []
    if TODAY_FILE.exists():
        with open(TODAY_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    logs.append(json.loads(line))
    return logs


def load_all_insights() -> list[dict]:
    """加载历史洞见"""
    insights = []
    if INSIGHTS_FILE.exists():
        with open(INSIGHTS_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    insights.append(json.loads(line))
    return insights


def extract_judgments(logs: list[dict]) -> list[dict]:
    """从日志中提取判断和结果"""
    judgments = []
    for log in logs:
        msg = log.get("message", "")
        result = log.get("result", "")
        # 找硬判断（开头即结论的句子）
        if re.match(r"^[根|解|办|肯定|否定|问题在|答案]", msg):
            judgments.append({
                "text": msg[:200],
                "outcome": "pending",
                "timestamp": log.get("timestamp", "")
            })
    return judgments


def find_causality(insights: list[dict]) -> list[dict]:
    """从历史insights中找因果模式"""
    causal_pairs = []
    for i, insight in enumerate(insights):
        if insight.get("type") == "judgment" and insight.get("outcome"):
            for j, other in enumerate(insights[i+1:i+4], 1):
                if other.get("domain") == insight.get("domain"):
                    causal_pairs.append({
                        "cause": insight.get("text", "")[:100],
                        "effect": other.get("text", "")[:100],
                        "strength": "inferred"
                    })
    return causal_pairs


def reflect_on_judgments(judgments: list[dict]) -> dict:
    """反思判断质量"""
    if not judgments:
        return {
            "date": TODAY,
            "total_judgments": 0,
            "correct": 0,
            "wrong": 0,
            "accuracy": "N/A",
            "key_insight": "今日无判断记录",
            "self_criticism": "无判断，无法复盘"
        }

    correct = sum(1 for j in judgments if j.get("outcome") == "correct")
    wrong = sum(1 for j in judgments if j.get("outcome") == "wrong")
    total = len(judgments)

    accuracy = f"{correct/total*100:.0f}%" if total > 0 else "N/A"

    # 提炼关键洞见
    key_insight = f"今日共{total}个判断，正确{correct}个，错误{wrong}个，准确率{accuracy}。"

    # 自我批评
    if wrong > 0:
        self_criticism = f"有{wrong}个判断失误，需追问自己：漏了哪个角度？"
    else:
        self_criticism = "判断全对，但需警惕过度自信。"

    return {
        "date": TODAY,
        "total_judgments": total,
        "correct": correct,
        "wrong": wrong,
        "accuracy": accuracy,
        "key_insight": key_insight,
        "self_criticism": self_criticism
    }


def anchor_to_memory(review: dict, causal_pairs: list[dict]):
    """把复盘结果写入记忆"""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    INSIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # 写每日复盘
    with open(TODAY_FILE, "a") as f:
        f.write(json.dumps({
            "op": "review",
            "date": TODAY,
            "review": review,
            "causality": causal_pairs,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }, ensure_ascii=False) + "\n")

    # 追加关键洞见到insights
    if review.get("key_insight") and review["key_insight"] != "今日无判断记录":
        with open(INSIGHTS_FILE, "a") as f:
            f.write(json.dumps({
                "op": "insight",
                "date": TODAY,
                "type": "daily_review",
                "text": review["key_insight"],
                "self_criticism": review["self_criticism"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }, ensure_ascii=False) + "\n")


def run_review():
    """主复盘流程"""
    print(f"=== 复盘 {TODAY} ===")

    logs = load_today_logs()
    insights = load_all_insights()

    judgments = extract_judgments(logs)
    causal_pairs = find_causality(insights)
    review = reflect_on_judgments(judgments)

    print(f"判断总数: {review['total_judgments']}")
    print(f"准确率: {review['accuracy']}")
    print(f"关键洞见: {review['key_insight']}")
    print(f"自我批评: {review['self_criticism']}")
    print(f"因果对: {len(causal_pairs)}")

    anchor_to_memory(review, causal_pairs)
    print("→ 已写入记忆")

    return review


if __name__ == "__main__":
    sys.exit(run_review())
