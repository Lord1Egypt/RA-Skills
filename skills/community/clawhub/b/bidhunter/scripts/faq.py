#!/usr/bin/env python3
"""
faq.py - Search the BidHunter FAQ (BidHunter v1.5, A8).

Parses docs/FAQ.md (## Q: ... blocks with keyword tags) and returns entries
whose keywords/title/body match the given terms. With no terms, lists all Qs.

Usage:
  python3 faq.py                       # list all questions
  python3 faq.py 推送 失败              # search by keywords
  python3 faq.py 评分                   # search
"""
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FAQ_PATH = os.path.join(SCRIPT_DIR, "docs", "FAQ.md")


def load_entries():
    if not os.path.exists(FAQ_PATH):
        return []
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    # split by '## Q:'
    blocks = re.split(r"\n## Q:", text)
    entries = []
    for i, b in enumerate(blocks):
        if i == 0:
            # maybe first block has '## Q:' inside
            if "Q:" not in b:
                continue
            b = b[b.find("Q:"):]
        else:
            b = "Q:" + b
        m = re.match(r"Q:\s*(.+?)\n关键词:\s*(.+?)\n(.*)", b, re.S)
        if not m:
            continue
        q = m.group(1).strip()
        kw = m.group(2).strip()
        ans = m.group(3).strip()
        entries.append({"q": q, "kw": kw, "ans": ans})
    return entries


def main():
    terms = [t for t in sys.argv[1:] if t]
    entries = load_entries()
    if not entries:
        print("FAQ 文件缺失。", file=sys.stderr)
        sys.exit(1)

    if not terms:
        print("📚 BidHunter 常见问题（输入关键词检索，如: faq.py 推送 失败）\n")
        for e in entries:
            print(f"· {e['q']}")
        return

    qset = " ".join(terms)
    hits = []
    for e in entries:
        hay = (e["q"] + " " + e["kw"] + " " + e["ans"]).lower()
        if any(t.lower() in hay for t in terms):
            hits.append(e)
    if not hits:
        print(f"未找到与「{qset}」相关的 FAQ。试试: faq.py 配置 / faq.py 推送 / faq.py 评分")
        return
    print(f"🔍 找到 {len(hits)} 条相关 FAQ：\n")
    for e in hits:
        print(f"❓ {e['q']}")
        print(f"{e['ans']}\n")


if __name__ == "__main__":
    main()
