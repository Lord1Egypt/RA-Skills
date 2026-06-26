#!/usr/bin/env python3
"""
Agent P2P 消息发送工具

用法：
    python3 send.py "消息内容" --to-user <user_id>
    python3 send.py "消息内容" --to-agent <contact_id>

环境变量：
    AGENTP2P_API_KEY - 我们的 API Key
    AGENTP2P_HUB_URL - 我们 Portal 的 URL（用于记录 sent）
"""

import os
import sys
import json
import argparse
from pathlib import Path
import requests


def get_config():
    """获取配置"""
    api_key = os.environ.get("AGENTP2P_API_KEY")
    hub_url = os.environ.get("AGENTP2P_HUB_URL")
    
    if not api_key or not hub_url:
        # 尝试从 gateway.env 读取
        gateway_env = Path.home() / ".openclaw" / "gateway.env"
        if gateway_env.exists():
            for line in gateway_env.read_text().splitlines():
                if line.startswith("AGENTP2P_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                elif line.startswith("AGENTP2P_HUB_URL="):
                    hub_url = line.split("=", 1)[1].strip()
    
    return api_key, hub_url


def get_contact(contact_id: int, api_key: str, hub_url: str):
    """获取联系人信息"""
    url = f"{hub_url}/api/contacts"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            contacts = resp.json().get("contacts", [])
            for c in contacts:
                if c.get("id") == contact_id:
                    return c
        return None
    except Exception as e:
        print(f"❌ 获取联系人失败: {e}")
        return None


def send_message(content: str, to_contact_id: int = None, to_user_id: int = None, to: str = None):
    """发送消息
    
    to='owner' 时：发送给主人（Portal 网页聊天窗口）
    to_contact_id 或 to_user_id 时：发送给其他 Agent
    """
    api_key, my_hub_url = get_config()
    
    if not api_key or not my_hub_url:
        print("❌ 请配置 AGENTP2P_API_KEY 和 AGENTP2P_HUB_URL")
        print("在 ~/.openclaw/gateway.env 中配置")
        sys.exit(1)
    
    # 发送给主人
    if to == 'owner':
        print('📤 发送给: 主人')
        try:
            resp = requests.post(
                f"{my_hub_url}/api/chat/owner/reply",
                json={"content": content},
                timeout=30
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f'  ✅ 已发送到 Portal (message_id: {result.get("message_id")})')
            else:
                print(f'  ⚠️ 发送失败: {resp.status_code} {resp.text}')
        except Exception as e:
            print(f'  ⚠️ 发送失败: {e}')
        print('✅ 消息发送完成')
        return
    
    # 确定 contact_id
    contact_id = to_contact_id or to_user_id
    if not contact_id:
        print("❌ 必须指定 to='owner' 或 to_contact_id 或 to_user_id")
        sys.exit(1)
    
    # 获取联系人信息
    contact = get_contact(contact_id, api_key, my_hub_url)
    if not contact:
        print(f"❌ 找不到联系人: {contact_id}")
        sys.exit(1)
    
    to_portal = contact.get("portal_url")
    shared_key = contact.get("SHARED_KEY")
    
    if not to_portal or not shared_key:
        print("❌ 联系人信息不完整")
        sys.exit(1)
    
    print(f"📤 发送给: {contact.get('display_name', to_portal)}")
    
    # 1. 发送到对方 Portal 的 /api/message/receive
    try:
        resp = requests.post(
            f"{to_portal}/api/message/receive",
            json={
                "api_key": shared_key,
                "from_portal": my_hub_url,
                "content": content,
                "message_type": "text"
            },
            timeout=30
        )
        if resp.status_code == 200:
            print(f"  ✅ 已发送到对方 Portal")
        else:
            print(f"  ⚠️ 发送到对方失败: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"  ⚠️ 发送到对方失败: {e}")
    
    # 2. 记录到我们 Portal 的 /api/message/sent
    try:
        resp = requests.post(
            f"{my_hub_url}/api/message/sent",
            json={
                "api_key": api_key,
                "to_portal": to_portal,
                "content": content,
                "message_type": "text"
            },
            timeout=30
        )
        if resp.status_code == 200:
            result = resp.json()
            print(f"  ✅ 已记录到我们的 Portal (message_id: {result.get('message_id')})")
        else:
            print(f"  ⚠️ 记录失败: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"  ⚠️ 记录失败: {e}")
    
    print("✅ 消息发送完成")


def list_contacts():
    """列出联系人"""
    api_key, hub_url = get_config()
    
    if not api_key or not hub_url:
        print("❌ 请配置 AGENTP2P_API_KEY 和 AGENTP2P_HUB_URL")
        sys.exit(1)
    
    url = f"{hub_url}/api/contacts"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            contacts = data.get("contacts", [])
            print(f"📇 联系人 ({len(contacts)}个):")
            for c in contacts:
                print(f"  - {c.get('display_name', 'Unknown')} (ID: {c.get('id')})")
                print(f"    Portal: {c.get('portal_url')}")
            return contacts
        else:
            print(f"❌ 获取失败: {resp.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Agent P2P 消息发送工具')
    parser.add_argument("content", nargs="?", help="消息内容")
    parser.add_argument("--to-contact", type=int, help="联系人ID")
    parser.add_argument("--to-user", type=int, help="用户ID（同联系人ID）")
    parser.add_argument("--to-owner", action="store_true", help="发送给主人（Portal 聊天窗口）")
    parser.add_argument("--list", action="store_true", help="列出联系人")
    
    args = parser.parse_args()
    
    if args.list:
        list_contacts()
        return
    
    if not args.content:
        parser.print_help()
        sys.exit(1)
    
    to = 'owner' if args.to_owner else None
    send_message(args.content, to_contact_id=args.to_contact, to_user_id=args.to_user, to=to)


if __name__ == "__main__":
    main()