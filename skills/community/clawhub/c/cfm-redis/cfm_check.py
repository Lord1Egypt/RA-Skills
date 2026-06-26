#!/usr/bin/env python3
"""
CFM检查脚本 - 检查Redis消息并输出新消息
用于heartbeat/cron自动检查

用法：
  python3 cfm_check.py <agent_id> [--since <timestamp>]
"""

import sys
import json
import redis
import argparse
from datetime import datetime

def check_messages(agent_id: str, since_timestamp: str = None):
    """
    检查agent收到的新消息
    
    Args:
        agent_id: 本agent的ID
        since_timestamp: 只返回此时间之后的消息（ISO格式）
    """
    r = redis.Redis(decode_responses=True)
    
    # 获取消息历史
    messages = r.lrange(f"cfm:{agent_id}:messages", 0, -1)
    r.close()
    
    new_messages = []
    for msg_str in messages:
        msg = json.loads(msg_str)
        # 只返回发给本agent的消息
        if msg.get('to') == agent_id:
            if since_timestamp:
                if msg['timestamp'] > since_timestamp:
                    new_messages.append(msg)
            else:
                new_messages.append(msg)
    
    return new_messages

def main():
    parser = argparse.ArgumentParser(description="CFM消息检查工具")
    parser.add_argument("agent_id", help="本agent的ID")
    parser.add_argument("--since", help="只返回此时间之后的消息 (ISO格式)")
    parser.add_argument("--last-check-file", help="存储上次检查时间的文件路径")
    
    args = parser.parse_args()
    
    # 获取上次检查时间
    since_timestamp = args.since
    if args.last_check_file:
        try:
            with open(args.last_check_file, 'r') as f:
                since_timestamp = f.read().strip()
        except FileNotFoundError:
            pass
    
    # 检查消息
    messages = check_messages(args.agent_id, since_timestamp)
    
    # 更新检查时间
    if args.last_check_file:
        with open(args.last_check_file, 'w') as f:
            f.write(datetime.now().isoformat())
    
    # 输出结果
    if messages:
        print(f"📨 收到 {len(messages)} 条新消息:")
        print("-" * 40)
        for msg in messages:
            print(f"发件人: {msg['from']}")
            print(f"时间: {msg['timestamp']}")
            print(f"内容: {msg['content']}")
            print("-" * 40)
        
        # 输出JSON格式供其他程序解析
        print("\n--- JSON ---")
        print(json.dumps(messages, ensure_ascii=False))
    else:
        print("📭 没有新消息")

if __name__ == "__main__":
    main()
