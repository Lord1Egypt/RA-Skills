#!/usr/bin/env python3
"""Render couple-content JSON into publish-ready markdown copy.

Usage:
    python3 render_content.py content.json out.md

Pure standard library — no dependencies. Validates the JSON structure,
warns on over-long fields, and renders a video-voice-over script + card copy.
"""

import json
import sys
import os

# Field length limits (hard rules from the prompt template)
LIMITS = {
    "title": 12,
    "question": 40,
    "answer": 30,
    "tip": 50,
    "hook": 30,
    "cta": 30,
    "price": 14,
    "evidence": 80,
    "why": 60,
    "how": 40,
}


def die(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(path):
    if not os.path.isfile(path):
        die(f"file not found: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        die(f"invalid JSON in {path}: {e}")


def check_limits(obj, key):
    """Warn (not fail) when a field exceeds its limit."""
    text = obj.get(key, "")
    limit = LIMITS.get(key)
    if limit and len(text) > limit:
        print(f"[WARN] '{key}' {len(text)}字 > {limit}字上限: {text[:20]}…")


def validate(data):
    mode = data.get("mode") or data.get("stage")
    if mode not in ("questions", "gifts", "gift_reveal"):
        die("mode/stage must be 'questions', 'gifts', or 'gift_reveal'")

    if mode == "gift_reveal":
        preferences = data.get("preference_summary", [])
        items = data.get("gift_options", [])
        if not isinstance(preferences, list):
            die("preference_summary must be an array")
        if not isinstance(items, list) or not items:
            die("gift_options must be a non-empty array")
        for i, pref in enumerate(preferences, 1):
            for field in ("dimension", "what_they_said", "inference", "confidence"):
                if not pref.get(field):
                    die(f"preference_summary[{i}] missing field: {field}")
        for i, item in enumerate(items, 1):
            for field in ("title", "price", "evidence", "why", "how"):
                if not item.get(field):
                    die(f"gift_options[{i}] missing field: {field}")
                check_limits(item, field)
        return mode, items

    for field in ("topic", "hook", "cta"):
        if not data.get(field):
            die(f"missing required field: {field}")
        check_limits(data, field)

    items = data.get("content_json", [])
    if not isinstance(items, list) or not items:
        die("content_json must be a non-empty array")

    if mode == "questions":
        req = ("title", "question", "answer", "tip")
    else:
        req = ("title", "price", "why", "how")

    for i, item in enumerate(items, 1):
        for field in req:
            if not item.get(field):
                die(f"content_json[{i}] missing field: {field}")
            check_limits(item, field)

    return mode, items


def render(data, mode, items):
    if mode == "gift_reveal":
        out = ["# 根据互动回答生成的礼物揭晓\n", "## 偏好推断\n"]
        confidence_names = {"high": "高", "medium": "中", "low": "低"}
        for pref in data.get("preference_summary", []):
            confidence = confidence_names.get(pref["confidence"], pref["confidence"])
            out.append(f"**{pref['dimension']}**(置信度:{confidence})")
            out.append(f"- TA说过:{pref['what_they_said']}")
            out.append(f"- 合理推测:{pref['inference']}\n")

        out.append("## 礼物方案\n")
        for i, item in enumerate(items, 1):
            out.append(f"**{i}. {item['title']}** · {item['price']}")
            out.append(f"- 回答依据:{item['evidence']}")
            out.append(f"- 为什么适合:{item['why']}")
            out.append(f"- 怎么送:{item['how']}\n")

        uncertainties = data.get("uncertainties", [])
        if uncertainties:
            out.append("## 还不确定\n")
            out.extend(f"- {text}" for text in uncertainties)
            out.append("")
        out.append("> 推荐基于互动回答的合理推测,购买前请结合预算和对方近期需求确认。")
        return "\n".join(out).rstrip() + "\n"

    out = []
    out.append(f"# {data['topic']}\n")

    # A readable transcript for the interaction.
    out.append("## 互动记录\n")
    out.append(f"**开场钩子**:{data['hook']}\n")
    for i, item in enumerate(items, 1):
        if mode == "questions":
            out.append(f"**第{i}题 · {item['title']}**")
            out.append(f"问:{item['question']}")
            out.append(f"参考答案:{item['answer']}")
            out.append(f"点评:{item['tip']}")
        else:
            out.append(f"**第{i}件 · {item['title']}({item['price']})**")
            out.append(f"为什么:{item['why']}")
            out.append(f"怎么送:{item['how']}")
        out.append("")
    out.append(f"**结尾 CTA**:{data['cta']}\n")

    # A compact version for saving or sharing with the other participant.
    out.append("## 题目卡片\n")
    if mode == "questions":
        for i, item in enumerate(items, 1):
            out.append(f"**Q{i} {item['title']}** — {item['question']}")
            out.append(f"💡 {item['answer']} {item['tip']}\n")
    else:
        for i, item in enumerate(items, 1):
            out.append(f"**{i}. {item['title']}** · {item['price']}")
            out.append(f"{item['why']}")
            out.append(f"💡 送礼场景:{item['how']}\n")

    return "\n".join(out).rstrip() + "\n"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    data = load_json(sys.argv[1])
    mode, items = validate(data)
    text = render(data, mode, items)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(text)
    print(f"OK: {mode} × {len(items)} items → {sys.argv[2]}")
    print(f"互动内容 {len(text)} 字符,可直接在对话中使用或保存。")


if __name__ == "__main__":
    main()
