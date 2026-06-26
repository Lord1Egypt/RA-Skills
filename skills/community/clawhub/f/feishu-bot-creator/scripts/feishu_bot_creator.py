#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feishu Bot Creator - 飞书机器人创建器
自动化创建和配置飞书机器人
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

# 飞书 API 基础 URL
FEISHU_API_BASE = os.environ.get("FEISHU_API_BASE", "https://open.feishu.cn")

class FeishuBotCreator:
    """飞书机器人创建器"""
    
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or os.environ.get("FEISHU_APP_ID")
        self.app_secret = app_secret or os.environ.get("FEISHU_APP_SECRET")
        self.access_token = None
        
        if not self.app_id or not self.app_secret:
            print("❌ 错误：需要设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量")
            print("   或者在创建时提供 --app-id 和 --app-secret 参数")
            sys.exit(1)
    
    def get_access_token(self):
        """获取访问令牌"""
        url = f"{FEISHU_API_BASE}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get("code") != 0:
            print(f"❌ 获取访问令牌失败：{data.get('msg')}")
            sys.exit(1)
        
        self.access_token = data.get("tenant_access_token")
        print("✅ 获取访问令牌成功")
        return self.access_token
    
    def create_app(self, name, description="", icon=""):
        """创建应用"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{FEISHU_API_BASE}/open-apis/application/v4/app/create"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "name": name,
            "description": description,
            "icon": icon,
            "homepage": "",
            "category": "效率办公"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if data.get("code") != 0:
            print(f"❌ 创建应用失败：{data.get('msg')}")
            return None
        
        app_info = data.get("data", {})
        print(f"✅ 创建应用成功：{name}")
        print(f"   App ID: {app_info.get('app_id')}")
        print(f"   App Secret: {app_info.get('app_secret')}")
        
        return app_info
    
    def update_app_permissions(self, app_id, permissions):
        """更新应用权限"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{FEISHU_API_BASE}/open-apis/application/v4/app/permission/batch"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "app_id": app_id,
            "permission_point_codes": permissions
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if data.get("code") != 0:
            print(f"⚠️  设置权限警告：{data.get('msg')}")
        else:
            print(f"✅ 设置权限成功：{', '.join(permissions)}")
    
    def create_bot(self, app_id, name, webhook_url=""):
        """创建机器人"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{FEISHU_API_BASE}/open-apis/bot/v4/create"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "app_id": app_id,
            "name": name,
            "webhook": webhook_url if webhook_url else None
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if data.get("code") != 0:
            print(f"❌ 创建机器人失败：{data.get('msg')}")
            return None
        
        bot_info = data.get("data", {})
        print(f"✅ 创建机器人成功：{name}")
        
        if bot_info.get("webhook"):
            print(f"   Webhook: {bot_info.get('webhook')}")
        
        return bot_info
    
    def save_config(self, config, output_path):
        """保存配置文件"""
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 配置文件已保存：{output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="飞书机器人创建器 - 自动化创建和配置飞书机器人",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 feishu_bot_creator.py --name "我的机器人"
  python3 feishu_bot_creator.py --name "AI 助手" --webhook-url "http://localhost:8080/webhook"
  python3 feishu_bot_creator.py --name "通知机器人" --permissions "im:message,im:chat"
        """
    )
    
    parser.add_argument("--name", required=True, help="机器人名称")
    parser.add_argument("--description", default="", help="机器人描述")
    parser.add_argument("--webhook-url", default="", help="Webhook URL")
    parser.add_argument("--permissions", default="im:message", help="权限列表，逗号分隔")
    parser.add_argument("--icon", default="", help="机器人图标 URL")
    parser.add_argument("--app-id", help="飞书应用 ID（可选，默认使用环境变量）")
    parser.add_argument("--app-secret", help="飞书应用密钥（可选，默认使用环境变量）")
    parser.add_argument("--output", help="输出配置文件路径")
    
    args = parser.parse_args()
    
    # 创建创建器实例
    creator = FeishuBotCreator(app_id=args.app_id, app_secret=args.app_secret)
    
    # 解析权限列表
    permissions = [p.strip() for p in args.permissions.split(",") if p.strip()]
    
    print(f"🤖 开始创建飞书机器人：{args.name}")
    print("-" * 50)
    
    # 创建应用
    app_info = creator.create_app(
        name=args.name,
        description=args.description,
        icon=args.icon
    )
    
    if not app_info:
        print("❌ 创建应用失败，已终止")
        sys.exit(1)
    
    # 设置权限
    if permissions:
        creator.update_app_permissions(app_info.get("app_id"), permissions)
    
    # 创建机器人
    bot_info = creator.create_bot(
        app_id=app_info.get("app_id"),
        name=args.name,
        webhook_url=args.webhook_url
    )
    
    # 准备配置
    config = {
        "name": args.name,
        "description": args.description,
        "app_id": app_info.get("app_id"),
        "app_secret": app_info.get("app_secret"),
        "bot_id": bot_info.get("bot_id") if bot_info else None,
        "webhook_url": bot_info.get("webhook") if bot_info else args.webhook_url,
        "permissions": permissions
    }
    
    # 保存配置
    output_path = args.output or f"~/.feishu/bots/{args.name}.json"
    output_path = os.path.expanduser(output_path)
    creator.save_config(config, output_path)
    
    print("-" * 50)
    print("✅ 飞书机器人创建完成！")
    print(f"\n配置信息已保存到：{output_path}")
    print("\n下一步:")
    print("1. 在飞书开放平台将机器人添加到群聊")
    print("2. 配置 webhook 接收消息（如需要）")
    print("3. 测试机器人功能")


if __name__ == "__main__":
    main()
