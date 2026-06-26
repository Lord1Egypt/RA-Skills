#!/usr/bin/env python3
"""
gaokao-tutor: 错题本管理脚本
用法:
  python3 mistakes.py add --subject 数学 --topic 概率 --ability 应用 --reason "忘记乘法公式" --summary "两事件概率题"
  python3 mistakes.py list [--subject 数学]
  python3 mistakes.py due          # 今日到期复习
  python3 mistakes.py stats        # 薄弱点统计
  python3 mistakes.py done <id>    # 标记已掌握
"""

import json
import os
import sys
import argparse
from datetime import date, timedelta

MISTAKES_FILE = os.path.expanduser("~/.openclaw/workspace/memory/gaokao-mistakes.json")

REVIEW_INTERVALS = [1, 3, 7, 15, 30]  # 艾宾浩斯间隔（天）


def load_mistakes():
    if not os.path.exists(MISTAKES_FILE):
        return {"mistakes": []}
    with open(MISTAKES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_mistakes(data):
    os.makedirs(os.path.dirname(MISTAKES_FILE), exist_ok=True)
    with open(MISTAKES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_mistake(subject, topic, ability, reason, summary):
    data = load_mistakes()
    mistakes = data["mistakes"]

    # 生成 ID
    existing_ids = [m["id"] for m in mistakes]
    new_id = f"m{len(mistakes)+1:03d}"
    while new_id in existing_ids:
        new_id = f"m{int(new_id[1:])+1:03d}"

    today = date.today().isoformat()
    next_review = (date.today() + timedelta(days=REVIEW_INTERVALS[0])).isoformat()

    mistake = {
        "id": new_id,
        "date": today,
        "subject": subject,
        "topic": topic,
        "ability": ability,          # 记忆/理解/应用/分析
        "question_summary": summary,
        "error_reason": reason,
        "review_count": 0,
        "next_review": next_review,
        "mastered": False
    }
    mistakes.append(mistake)
    save_mistakes(data)
    print(f"✅ 已记录错题 [{new_id}]：{subject}·{topic}")
    print(f"   下次复习时间：{next_review}")
    return mistake


def list_mistakes(subject=None):
    data = load_mistakes()
    mistakes = [m for m in data["mistakes"] if not m.get("mastered")]
    if subject:
        mistakes = [m for m in mistakes if m["subject"] == subject]

    if not mistakes:
        print("📚 错题本是空的！继续加油～")
        return

    # 按科目分组
    by_subject = {}
    for m in mistakes:
        subj = m["subject"]
        by_subject.setdefault(subj, []).append(m)

    print(f"📚 错题本（共{len(mistakes)}道）\n")
    for subj, items in by_subject.items():
        print(f"【{subj}】{len(items)}道")
        for m in items:
            print(f"  [{m['id']}] {m['topic']} — {m['question_summary'][:30]}...")
            print(f"         错误原因：{m['error_reason']} | 下次复习：{m['next_review']}")
    print()


def get_due_today():
    data = load_mistakes()
    today = date.today().isoformat()
    due = [
        m for m in data["mistakes"]
        if not m.get("mastered") and m["next_review"] <= today
    ]
    return due, data


def show_due():
    due, _ = get_due_today()
    if not due:
        print("🎉 今天没有到期的错题，太棒了！")
        return

    print(f"📖 今日复习（{len(due)}道）\n")
    for i, m in enumerate(due, 1):
        print(f"{i}. [{m['id']}] {m['subject']}·{m['topic']}")
        print(f"   题目：{m['question_summary']}")
        print(f"   当时错的原因：{m['error_reason']}")
        print()
    print("复习完成后发送「完成复习 [id]」标记进度")


def mark_reviewed(mistake_id):
    due, data = get_due_today()
    mistakes = data["mistakes"]

    for m in mistakes:
        if m["id"] == mistake_id:
            if m.get("mastered"):
                print(f"[{mistake_id}] 已经标记为掌握了～")
                return

            review_count = m["review_count"] + 1
            m["review_count"] = review_count

            if review_count >= len(REVIEW_INTERVALS):
                m["mastered"] = True
                m["next_review"] = None
                print(f"🏆 [{mistake_id}] 已完成全部复习，标记为掌握！")
            else:
                days = REVIEW_INTERVALS[review_count]
                next_date = (date.today() + timedelta(days=days)).isoformat()
                m["next_review"] = next_date
                print(f"✅ [{mistake_id}] 复习完成！下次复习：{next_date}（第{review_count+1}次）")

            save_mistakes(data)
            return

    print(f"❌ 未找到错题 [{mistake_id}]")


def show_stats():
    data = load_mistakes()
    mistakes = [m for m in data["mistakes"] if not m.get("mastered")]

    if not mistakes:
        print("📊 错题本是空的，继续加油！")
        return

    # 按知识点统计
    topic_count = {}
    for m in mistakes:
        key = f"{m['subject']}·{m['topic']}"
        topic_count[key] = topic_count.get(key, 0) + 1

    # 按能力层次统计
    ability_count = {}
    for m in mistakes:
        ability = m.get("ability", "未分类")
        ability_count[ability] = ability_count.get(ability, 0) + 1

    total = len(mistakes)
    print(f"📊 错题统计（共{total}道未掌握）\n")

    print("【最薄弱知识点 Top 5】")
    sorted_topics = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)
    for i, (topic, count) in enumerate(sorted_topics[:5], 1):
        bar = "█" * count
        print(f"{i}. {topic} — {count}道  {bar}")

    print("\n【能力层次分析】")
    for ability, count in ability_count.items():
        pct = count / total * 100
        advice = {
            "记忆": "加强背诵和复现",
            "理解": "重读教材推导过程",
            "应用": "多做同类练习题",
            "分析": "练习解题框架"
        }.get(ability, "有针对性地复习")
        print(f"  {ability}类：{count}道（{pct:.0f}%）→ {advice}")

    # 今日到期
    today = date.today().isoformat()
    due_count = sum(1 for m in mistakes if m["next_review"] <= today)
    if due_count > 0:
        print(f"\n⚠️ 今日有 {due_count} 道题到期复习，发送「今日复习」开始")


def main():
    parser = argparse.ArgumentParser(description="高考错题本管理")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="添加错题")
    add_parser.add_argument("--subject", required=True)
    add_parser.add_argument("--topic", required=True)
    add_parser.add_argument("--ability", default="应用",
                            choices=["记忆", "理解", "应用", "分析"])
    add_parser.add_argument("--reason", default="方法不对")
    add_parser.add_argument("--summary", default="题目摘要")

    # list
    list_parser = subparsers.add_parser("list", help="查看错题本")
    list_parser.add_argument("--subject", default=None)

    # due
    subparsers.add_parser("due", help="今日到期复习")

    # stats
    subparsers.add_parser("stats", help="薄弱点统计")

    # done
    done_parser = subparsers.add_parser("done", help="标记已复习")
    done_parser.add_argument("id", help="错题ID")

    args = parser.parse_args()

    if args.command == "add":
        add_mistake(args.subject, args.topic, args.ability, args.reason, args.summary)
    elif args.command == "list":
        list_mistakes(args.subject)
    elif args.command == "due":
        show_due()
    elif args.command == "stats":
        show_stats()
    elif args.command == "done":
        mark_reviewed(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
