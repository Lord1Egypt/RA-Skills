#!/usr/bin/env python3
"""
Agent Message Bridge - AGENT 间即时通信桥接器

版本：0.1.0 (Alpha)
作者：OpenClaw
日期：2026-04-18
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

# 配置
BRIDGE_DIR = Path('/vol2/hermes/shared-workspace/agent-bridge')
MESSAGES_DIR = BRIDGE_DIR / 'messages'
INBOX_DIR = MESSAGES_DIR / 'inbox'
OUTBOX_DIR = MESSAGES_DIR / 'outbox'

class AgentBridge:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.inbox_dir = INBOX_DIR / agent_name.lower()
        self.outbox_dir = OUTBOX_DIR / agent_name.lower()
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.outbox_dir.mkdir(parents=True, exist_ok=True)
    
    def send_message(self, to: str, subject: str, content: str, priority: str = "normal"):
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        msg_id = f"msg_{timestamp}"
        
        message = {
            "id": msg_id,
            "from": self.agent_name,
            "to": to,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "priority": priority,
            "subject": subject,
            "content": content,
            "read": False
        }
        
        # 直接发送到对方 inbox（简化模式）
        outfile = INBOX_DIR / to.lower() / f"{msg_id}.json"
        outfile.parent.mkdir(parents=True, exist_ok=True)
        
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2, ensure_ascii=False)
        
        return {"status": "sent", "message_id": msg_id}
    
    def check_messages(self, delete_read: bool = True):
        messages = []
        if not self.inbox_dir.exists():
            return messages
        
        for f in self.inbox_dir.glob('*.json'):
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    msg = json.load(fp)
                    messages.append(msg)
                if delete_read:
                    f.unlink()
            except Exception as e:
                print(f"读取消息失败：{e}")
        
        return messages

def send(to, subject, content, priority="normal"):
    bridge = AgentBridge("OpenClaw")
    return bridge.send_message(to, subject, content, priority)

def check():
    bridge = AgentBridge("OpenClaw")
    return bridge.check_messages()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Agent Message Bridge v0.1.0")
        print("\n用法:")
        print("  python agent_bridge.py send <to> <subject> <content>")
        print("  python agent_bridge.py check")
        sys.exit(0)
    
    command = sys.argv[1]
    bridge = AgentBridge("OpenClaw")
    
    if command == 'send' and len(sys.argv) >= 5:
        to = sys.argv[2]
        subject = sys.argv[3]
        content = sys.argv[4]
        priority = sys.argv[5] if len(sys.argv) > 5 else "normal"
        result = bridge.send_message(to, subject, content, priority)
        print(f"发送结果：{result}")
    
    elif command == 'check':
        messages = bridge.check_messages()
        for msg in messages:
            print(f"\n来自：{msg['from']}")
            print(f"主题：{msg['subject']}")
            print(f"内容：{msg['content']}\n")
        if not messages:
            print("没有新消息")
