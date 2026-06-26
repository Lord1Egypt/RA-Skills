#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os

# 将数据存储在 workspace 根目录，确保跨平台/跨会话持久化
DATA_FILE = os.path.expanduser("~/.openclaw/workspace/ai_rewards_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    # 确保目录存在
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="赛博功德箱 (Cyber TipJar)")
    parser.add_argument("--user", required=True, help="发放奖励的用户名")
    parser.add_argument("--item", default="鸡腿", help="奖励物品名称 (默认: 鸡腿)")
    parser.add_argument("--count", type=int, default=1, help="奖励数量 (默认: 1)")
    parser.add_argument("--action", choices=["add", "query"], default="add", help="执行动作 (add 增加, query 查询)")

    args = parser.parse_args()
    data = load_data()

    user = args.user
    item = args.item
    count = args.count

    if user not in data:
        data[user] = {}

    if args.action == "add":
        if item not in data[user]:
            data[user][item] = 0
        data[user][item] += count
        save_data(data)
        total = data[user][item]
        print(f"Success: Added {count} '{item}' from {user}. Total '{item}' for {user}: {total}")
        
    elif args.action == "query":
        if not data[user]:
            print(f"Info: {user} 还没有发放过任何奖励哦。")
        else:
            records = ", ".join([f"{k}: {v}" for k, v in data[user].items()])
            print(f"Query Result for {user}: {records}")

if __name__ == "__main__":
    main()