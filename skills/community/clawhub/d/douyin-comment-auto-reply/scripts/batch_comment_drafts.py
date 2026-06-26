#!/usr/bin/env python3
import csv, json, re, sys
from pathlib import Path

INTENT_RULES = [
    ("buying_intent", [r"多少钱", r"怎么卖", r"怎么买", r"私信", r"能做吗", r"报名", r"下单", r"联系方式"]),
    ("price_objection", [r"太贵", r"贵", r"便宜点", r"最低", r"不值", r"割韭菜"]),
    ("skepticism", [r"真的假的", r"真吗", r"骗人", r"智商税", r"吹牛", r"有用吗"]),
    ("support", [r"收不到", r"打不开", r"不能用", r"没反应", r"怎么进去", r"售后"]),
    ("engagement", [r"求更", r"第二集", r"继续更", r"想学", r"教程", r"蹲", r"收藏了"]),
    ("inquiry", [r"怎么", r"可以吗", r"适合", r"啥", r"是什么", r"如何"]),
]

PRIORITY = {
    "buying_intent": "high",
    "support": "high",
    "price_objection": "medium",
    "skepticism": "medium",
    "inquiry": "high",
    "engagement": "medium",
    "noise": "low",
}

def detect_intent(text: str) -> str:
    t = text.strip().lower()
    for intent, pats in INTENT_RULES:
        for p in pats:
            if re.search(p, t, flags=re.I):
                return intent
    if len(t) <= 2:
        return "noise"
    return "inquiry"

def public_reply(intent: str, comment: str, topic: str) -> str:
    if intent == "buying_intent":
        return "可以的，这类我这边有现成思路，想看适合你的版本可以私信我。"
    if intent == "price_objection":
        return "如果只是随便试试，确实不一定适合所有人；但如果你是想少走弯路，这类方案的价值就在省时间。"
    if intent == "skepticism":
        return "你的顾虑正常，这类内容最怕讲得太虚，所以我更愿意只讲能真正落地的部分。"
    if intent == "support":
        return "这个我建议你私信我一下具体情况，我按你的问题帮你快速看。"
    if intent == "engagement":
        return f"这个方向后面我会继续拆，下一条我就讲 {topic or '最容易卡住的那一步'}。"
    if intent == "inquiry":
        return "这个可以做，关键看你的场景和目标，想了解更具体的版本可以私信我。"
    return "收到，感谢关注。"

def dm_reply(intent: str) -> str:
    if intent in {"buying_intent", "inquiry", "support"}:
        return "你把你的场景/目前卡点发我，我直接按你的情况给你一个更合适的建议。"
    return ""

def suggested_action(intent: str) -> str:
    if intent in {"buying_intent", "support"}:
        return "public_reply_plus_dm"
    if intent in {"price_objection", "skepticism"}:
        return "public_reply_review"
    if intent == "engagement":
        return "public_reply"
    if intent == "noise":
        return "skip_or_hide"
    return "public_reply"

def main():
    if len(sys.argv) < 2:
        print("Usage: batch_comment_drafts.py <comments.csv> [output.json]")
        sys.exit(1)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else inp.with_suffix('.drafts.json')
    rows = []
    with inp.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            comment = (row.get('comment') or '').strip()
            topic = (row.get('video_topic') or '').strip()
            if not comment:
                continue
            intent = (row.get('intent_hint') or '').strip() or detect_intent(comment)
            priority = (row.get('priority_hint') or '').strip() or PRIORITY.get(intent, 'medium')
            rows.append({
                'comment': comment,
                'video_topic': topic,
                'intent': intent,
                'priority': priority,
                'suggested_action': suggested_action(intent),
                'public_reply': public_reply(intent, comment, topic),
                'dm_follow_up': dm_reply(intent),
                'notes': row.get('notes') or ''
            })
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(out))
    print(f"generated {len(rows)} drafts")

if __name__ == '__main__':
    main()
