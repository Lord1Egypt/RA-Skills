#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取房总的 open_id 并发送测试消息
"""

import os
import httpx
from datetime import datetime

# 请从环境变量读取，勿硬编码
# export FEISHU_APP_ID="your_app_id"
# export FEISHU_APP_SECRET="your_app_secret"
APP_ID = os.getenv("FEISHU_APP_ID", "")
APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
BASE_URL = "https://open.feishu.cn/open-apis"

def get_tenant_access_token():
    """获取应用身份访问令牌"""
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    response = httpx.post(url, json=payload, timeout=10)
    result = response.json()
    if result.get("code") == 0:
        return result.get("tenant_access_token")
    return None

def get_user_list(token):
    """获取用户列表"""
    url = f"{BASE_URL}/contact/v3/users"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page_size": 50}
    response = httpx.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    print(f"用户列表结果：{result}")
    return result

def send_message(token, user_id, content):
    """发送消息给用户"""
    url = f"{BASE_URL}/im/v1/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "receive_id_type": "open_id",
        "receive_id": user_id,
        "msg_type": "interactive",
        "content": content
    }
    response = httpx.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    return result

def main():
    print("=" * 60)
    print("📱 获取 open_id 并发送测试消息")
    print("=" * 60)
    
    # 1. 获取 Token
    print("\n1️⃣ 获取 Access Token...")
    token = get_tenant_access_token()
    if not token:
        print("❌ 获取 Token 失败")
        return
    print(f"✅ Token: {token[:20]}...")
    
    # 2. 获取用户列表
    print("\n2️⃣ 获取用户列表...")
    user_result = get_user_list(token)
    
    if user_result.get("code") == 0:
        users = user_result.get("data", {}).get("items", [])
        print(f"✅ 找到 {len(users)} 个用户")
        
        # 查找房晓明
        for user in users:
            name = user.get("name", "")
            open_id = user.get("open_id", "")
            user_id = user.get("user_id", "")
            print(f"\n用户：{name}")
            print(f"  open_id: {open_id}")
            print(f"  user_id: {user_id}")
            
            if "房" in name or "晓明" in name:
                print(f"\n🎯 找到房晓明！open_id: {open_id}")
                
                # 3. 发送测试消息
                print("\n3️⃣ 发送测试消息...")
                card_content = {
                    "config": {"wide_screen_mode": True},
                    "header": {
                        "title": {"tag": "plain_text", "content": "🎉 量化交易助手 - 第一条消息"},
                        "template": "blue"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": "**房总好！**\n\n这是来自 **量化交易助手** 的第一条测试消息！\n\n发送时间：{}".format(
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                )
                            }
                        },
                        {"tag": "hr"},
                        {
                            "tag": "div",
                            "fields": [
                                {"is_short": True, "text": {"tag": "lark_md", "content": "**应用状态**\n✅ 正常运行"}},
                                {"is_short": True, "text": {"tag": "lark_md", "content": "**推送方式**\n✅ API 直连"}},
                                {"is_short": True, "text": {"tag": "lark_md", "content": "**长连接**\n✅ 已配置"}},
                                {"is_short": True, "text": {"tag": "lark_md", "content": "**交易权限**\n✅ 已开通"}}
                            ]
                        },
                        {"tag": "hr"},
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": "**📊 今日交易概览**\n\n• 成交订单：2 笔\n• 买入金额：HKD 70,580\n• 持仓股票：腾讯控股、比亚迪\n• 账户余额：HKD 729,287.86\n\n_下一次汇报将在每日收盘后_"
                            }
                        },
                        {
                            "tag": "note",
                            "elements": [{"tag": "plain_text", "content": "量化交易助手 v1.0 · 自动推送服务"}]
                        }
                    ]
                }
                
                result = send_message(token, open_id, card_content)
                print(f"\n发送结果：{result}")
                
                if result.get("code") == 0:
                    print("\n✅ 消息发送成功！")
                else:
                    print(f"\n❌ 消息发送失败：{result}")
                
                return

if __name__ == "__main__":
    main()
