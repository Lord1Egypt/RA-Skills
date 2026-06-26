#!/usr/bin/env python3
"""cn-smart-email 邮件分类与回复助手"""
import json
import sys
import re

CATEGORIES = {
    "工作": ["会议", "项目", "报告", "审批", "任务", "截止", "需求", "进度"],
    "个人": ["家", "朋友", "周末", "聚会", "生日", "旅行"],
    "通知": ["提醒", "确认", "验证", "通知", "更新", "系统"],
    "广告": ["优惠", "折扣", "促销", "限时", "免费", "领取"],
}

REPLY_TEMPLATES = {
    "formal": "您好，\n\n感谢您的来信。关于{topic}，我将在{time}前回复您。\n\n此致",
    "casual": "嗨，\n\n收到！关于{topic}，我稍后回复你~",
    "brief": "收到，稍后回复。",
}

def classify(text):
    scores = {}
    for cat, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in text)
        scores[cat] = score
    if max(scores.values()) == 0:
        return "其他"
    return max(scores, key=scores.get)

def generate_reply(text, tone="formal"):
    template = REPLY_TEMPLATES.get(tone, REPLY_TEMPLATES["formal"])
    topic = text[:20] + "..." if len(text) > 20 else text
    return template.format(topic=topic, time="2个工作日内")

def main():
    if len(sys.argv) < 2:
        print("用法: smart_email.py --classify <文本> | --reply <文本> [--tone formal|casual|brief]")
        return
    
    action = sys.argv[1]
    text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    # Parse --tone
    tone = "formal"
    if "--tone" in sys.argv:
        idx = sys.argv.index("--tone")
        if idx + 1 < len(sys.argv):
            tone = sys.argv[idx + 1]
        text = text.replace("--tone", "").replace(tone, "").strip()
    
    if action == "--classify":
        cat = classify(text)
        print(json.dumps({"category": cat, "text": text[:50]}, ensure_ascii=False))
    elif action == "--reply":
        reply = generate_reply(text, tone)
        print(reply)
    else:
        print(f"未知操作: {action}")

if __name__ == "__main__":
    main()
