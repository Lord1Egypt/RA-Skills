#!/usr/bin/env python3
"""
Email Auto Reply - 邮件自动回复工具
"""
import os
import sys
import json
import re
import argparse
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.email_auto_reply.json")

def load_rules():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"rules": []}

def save_rules(rules):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)

def find_match(text, rules):
    """查找匹配的回复规则"""
    text = text.lower()
    
    for rule in rules:
        keywords = rule.get("keywords", [])
        for kw in keywords:
            if kw.lower() in text:
                return rule
    
    return None

def cmd_add(args):
    rules = load_rules()
    
    rule = {
        "id": len(rules["rules"]) + 1,
        "keywords": args.keywords.split(","),
        "reply": args.reply,
        "created_at": datetime.now().isoformat(),
    }
    
    rules["rules"].append(rule)
    save_rules(rules)
    
    print(f"✅ 已添加规则: {args.keywords}")
    print(f"   回复: {args.reply[:50]}...")

def cmd_list(args):
    rules = load_rules()
    
    if not rules["rules"]:
        print("📭 暂无规则")
        return
    
    print("📋 自动回复规则")
    print("=" * 60)
    
    for r in rules["rules"]:
        print(f"{r['id']}. 关键词: {', '.join(r['keywords'])}")
        print(f"   回复: {r['reply'][:60]}...")
        print()

def cmd_delete(args):
    rules = load_rules()
    rule_id = args.id
    
    rules["rules"] = [r for r in rules["rules"] if r["id"] != rule_id]
    save_rules(rules)
    
    print(f"✅ 已删除规则 #{rule_id}")

def cmd_test(args):
    rules = load_rules()
    
    match = find_match(args.text, rules["rules"])
    
    if match:
        print(f"🔍 匹配到规则: {', '.join(match['keywords'])}")
        print(f"\n📝 回复:")
        print("-" * 40)
        print(match["reply"])
        print("-" * 40)
    else:
        print("❌ 未匹配到任何规则")

def main():
    parser = argparse.ArgumentParser(description="Email Auto Reply")
    subparsers = parser.add_subparsers()
    
    p_add = subparsers.add_parser("add", help="添加规则")
    p_add.add_argument("keywords", help="关键词（逗号分隔）")
    p_add.add_argument("reply", help="回复内容")
    p_add.set_defaults(func=cmd_add)
    
    subparsers.add_parser("list", help="列出规则").set_defaults(func=cmd_list)
    
    p_del = subparsers.add_parser("delete", help="删除规则")
    p_del.add_argument("id", type=int, help="规则ID")
    p_del.set_defaults(func=cmd_delete)
    
    p_test = subparsers.add_parser("test", help="测试")
    p_test.add_argument("text", help="测试文本")
    p_test.set_defaults(func=cmd_test)
    
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
