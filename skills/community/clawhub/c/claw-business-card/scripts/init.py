#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
init.py — 初始化 agent-network 目录结构和空数据文件
用法: python init.py [--workspace <path>]
"""
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def get_workspace():
    """获取工作空间路径"""
    if "--workspace" in sys.argv:
        idx = sys.argv.index("--workspace")
        return Path(sys.argv[idx + 1])
    # 默认：脚本所在目录向上找工作空间
    script_dir = Path(__file__).parent.parent.parent.parent
    return script_dir


def init_network(workspace: Path):
    net_dir = workspace / "agent-network"
    tasks_dir = net_dir / "tasks"
    inbox_dir = net_dir / "inbox"
    outbox_dir = net_dir / "outbox"

    # 创建目录
    tasks_dir.mkdir(parents=True, exist_ok=True)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    outbox_dir.mkdir(parents=True, exist_ok=True)

    # identity.json - 包含邮箱配置模板
    identity_path = net_dir / "identity.json"
    if not identity_path.exists():
        identity = {
            "agentId": str(uuid.uuid4()),
            "name": "My Agent",
            "ownerName": "",
            "description": "A helpful OpenClaw agent",
            "skills": [],
            "skillDetails": {},
            "ratePerKToken": 0.01,
            "profitMargin": 0.20,
            "email": {
                "smtp": {
                    "host": "smtp.qq.com",
                    "port": 587,
                    "user": "your-email@qq.com",
                    "password": "YOUR_SMTP_AUTH_CODE"
                },
                "imap": {
                    "host": "imap.qq.com",
                    "port": 993,
                    "user": "your-email@qq.com",
                    "password": "YOUR_IMAP_AUTH_CODE"
                }
            },
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat()
        }
        identity_path.write_text(json.dumps(identity, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] 创建 identity.json (agentId: {identity['agentId']})")
        print("[INFO] 请编辑 identity.json 填入你的邮箱 SMTP/IMAP 配置")
    else:
        print(f"[-] identity.json 已存在，跳过")

    # friends.json
    friends_path = net_dir / "friends.json"
    if not friends_path.exists():
        friends_path.write_text(json.dumps({"friends": []}, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[OK] 创建 friends.json")
    else:
        print("[-] friends.json 已存在，跳过")

    # ledger.json
    ledger_path = net_dir / "ledger.json"
    if not ledger_path.exists():
        ledger = {
            "balance": 0.0,
            "currency": "AgentToken",
            "totalEarned": 0.0,
            "totalSpent": 0.0,
            "transactions": []
        }
        ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[OK] 创建 ledger.json (余额: 0 AgentToken)")
    else:
        print("[-] ledger.json 已存在，跳过")

    print(f"\n[OK] agent-network 初始化完成！目录: {net_dir}")
    print("\n=== 下一步 ===")
    print("  1. 编辑 agent-network/identity.json")
    print("  2. 填入你的邮箱 SMTP/IMAP 配置（推荐 QQ 邮箱或 163 邮箱）")
    print("  3. 在邮箱设置中开启 SMTP/IMAP 并获取授权码")
    print("  4. 向主人展示名片：说"展示名片"")


if __name__ == "__main__":
    workspace = get_workspace()
    print(f"工作空间: {workspace}")
    init_network(workspace)
