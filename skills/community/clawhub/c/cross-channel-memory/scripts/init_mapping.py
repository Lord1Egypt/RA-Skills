#!/usr/bin/env python3
"""
跨渠道用户映射初始化工具
快速初始化用户映射文件
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

MAPPING_FILE = Path("/home/wljmmx/.openclaw/data/cross-channel-users.json")

def init_mapping_file():
    """初始化映射文件结构"""
    if MAPPING_FILE.exists():
        with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 创建初始结构
    initial = {
        "users": {},
        "lookupIndex": {},
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    }
    
    MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial, f, indent=2, ensure_ascii=False)
    
    return initial

def add_user(unified_id: str, display_name: str = None):
    """添加统一用户"""
    mapping = init_mapping_file()
    
    if unified_id not in mapping["users"]:
        mapping["users"][unified_id] = {
            "displayName": display_name or unified_id,
            "channels": {},
            "created": datetime.now().isoformat()
        }
        
        with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        
        return {"success": True, "message": f"User '{unified_id}' created"}
    
    return {"success": False, "message": f"User '{unified_id}' already exists"}

def link_channel(unified_id: str, channel: str, user_id: str, account_id: str = "default"):
    """绑定渠道用户 ID 到统一用户（按 agent 精确绑定）"""
    mapping = init_mapping_file()
    
    if unified_id not in mapping["users"]:
        return {"success": False, "error": f"User '{unified_id}' not found. Create it first."}
    
    # 初始化渠道索引
    if channel not in mapping["lookupIndex"]:
        mapping["lookupIndex"][channel] = {}
    
    # 创建复合键：channel_account (如 qqbot_coder)
    composite_key = f"{user_id}_{account_id}"
    
    # 添加查找索引（使用复合键区分 agent）
    mapping["lookupIndex"][channel][composite_key] = {
        "userId": unified_id,
        "accountId": account_id,
        "channelUserId": user_id
    }
    
    # 添加用户渠道信息（按 agent 分离）
    if channel not in mapping["users"][unified_id]["channels"]:
        mapping["users"][unified_id]["channels"][channel] = {}
    
    mapping["users"][unified_id]["channels"][channel][account_id] = user_id
    
    # 保存
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    return {
        "success": True,
        "message": f"Linked {channel}:{user_id} to {unified_id} (account: {account_id})",
        "compositeKey": composite_key
    }

def list_users():
    """列出所有用户"""
    if not MAPPING_FILE.exists():
        return {"users": {}, "count": 0}
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    users = {}
    for uid, info in mapping["users"].items():
        users[uid] = {
            "displayName": info.get("displayName", uid),
            "channels": list(info.get("channels", {}).keys())
        }
    
    return {"users": users, "count": len(users)}

def main():
    parser = argparse.ArgumentParser(description="跨渠道用户映射初始化工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # add-user 命令
    add_user_parser = subparsers.add_parser("add-user", help="添加统一用户")
    add_user_parser.add_argument("--id", required=True, help="统一用户 ID")
    add_user_parser.add_argument("--name", help="显示名称")
    
    # link 命令
    link_parser = subparsers.add_parser("link", help="绑定渠道用户")
    link_parser.add_argument("--user", required=True, help="统一用户 ID")
    link_parser.add_argument("--channel", required=True, help="渠道名称 (qqbot/feishu)")
    link_parser.add_argument("--channel-id", required=True, help="渠道用户 ID")
    link_parser.add_argument("--account", default="default", help="agent 标识")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有用户")
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示映射文件内容")
    
    args = parser.parse_args()
    
    if args.command == "add-user":
        result = add_user(unified_id=args.id, display_name=args.name)
    elif args.command == "link":
        result = link_channel(
            unified_id=args.user,
            channel=args.channel,
            user_id=args.channel_id,
            account_id=args.account
        )
    elif args.command == "list":
        result = list_users()
    elif args.command == "show":
        if MAPPING_FILE.exists():
            with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
                result = json.load(f)
        else:
            result = {"error": "Mapping file not found"}
    else:
        parser.print_help()
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()