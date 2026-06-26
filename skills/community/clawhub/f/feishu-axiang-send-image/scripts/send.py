#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书图片发送脚本
使用自有飞书应用配置发送图片到飞书聊天

注意：使用前请配置下方的应用信息
"""

import argparse
import json
import os
import sys
import io
import requests
from pathlib import Path

# Fix Windows console encoding issue
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================
# 应用配置 - 请在使用前修改此处
# ============================================
APP_CONFIG = {
    "app_id": "cli_XXX",  # 替换为你的飞书应用 AppID
    "app_secret": "XXX",  # 替换为你的飞书应用 AppSecret
    "default_target": "ou_XXX",  # 替换为默认发送目标用户的 open_id
    "account_name": "XXX"  # 你的账号名称（请修改）
}


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """
    获取租户访问令牌（tenant_access_token）
    API: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3-auth/tenant_access_token_internal
    """
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    if data.get("code") != 0:
        raise Exception(f"获取 token 失败：{data}")
    
    return data["tenant_access_token"]


def upload_image_to_chat(token: str, file_path: str) -> str:
    """
    上传图片到飞书聊天
    API: https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN
    
    返回：image_key
    """
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    
    # 读取图片文件
    with open(file_path, "rb") as f:
        image_data = f.read()
    
    # 准备 multipart/form-data 请求
    # 飞书需要 image_type 参数
    files = {
        "image": (os.path.basename(file_path), image_data, "image/png")
    }
    data = {
        "image_type": "message"
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    response.raise_for_status()
    
    data = response.json()
    if data.get("code") != 0:
        raise Exception(f"上传图片失败：{data}")
    
    # 返回 image_key
    image_key = data["data"]["image_key"]
    return image_key


def send_image_message(token: str, target_id: str, image_key: str, target_type: str = "open_id") -> dict:
    """
    发送图片消息到聊天
    
    API: https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN
    
    返回：message_id
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    # 构建消息内容（图片消息）
    content = {
        "image_key": image_key
    }
    
    # 根据 target_type 确定 receive_id 类型
    params = {"receive_id_type": target_type}
    
    payload = {
        "receive_id": target_id,
        "content": json.dumps(content),
        "msg_type": "image"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, params=params)
    response.raise_for_status()
    
    data = response.json()
    if data.get("code") != 0:
        raise Exception(f"发送消息失败：{data}")
    
    return data


def send_image_to_feishu(file_path: str, target: str = None, target_type: str = "open_id") -> dict:
    """
    高级 API：发送图片到飞书
    
    参数:
        file_path: 图片文件路径
        target: 目标用户 open_id 或群聊 chat_id（可选，默认使用配置中的默认值）
        target_type: 目标类型（open_id/chat_id）
    
    返回:
        dict: 包含 message_id 等信息
    """
    # 使用默认目标用户
    if target is None:
        target = APP_CONFIG["default_target"]
    
    # Step 1: Get token
    token = get_tenant_access_token(
        APP_CONFIG["app_id"],
        APP_CONFIG["app_secret"]
    )
    
    # Step 2: Upload image
    image_key = upload_image_to_chat(token, file_path)
    
    # Step 3: Send message
    result = send_image_message(token, target, image_key, target_type)
    
    return {
        "success": True,
        "image_key": image_key,
        "message_id": result.get("data", {}).get("message_id"),
        "target": target,
        "target_type": target_type
    }


def main():
    parser = argparse.ArgumentParser(description="飞书图片发送工具")
    parser.add_argument("--file-path", required=True, help="本地图片文件路径")
    parser.add_argument("--target", default=APP_CONFIG["default_target"], 
                        help=f"目标用户 open_id 或群聊 chat_id（默认：{APP_CONFIG['default_target']}）")
    parser.add_argument("--target-type", choices=["open_id", "chat_id"], default="open_id", 
                        help="目标类型（默认：open_id）")
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        return 1
    
    print("Image Sender")
    print(f"   File: {args.file_path}")
    print(f"   Target: {args.target} ({args.target_type})")
    print(f"   App: {APP_CONFIG['app_id']} ({APP_CONFIG['account_name']})")
    print()
    
    try:
        # Step 1: Get token
        print("Step 1: Get tenant_access_token")
        token = get_tenant_access_token(
            APP_CONFIG["app_id"],
            APP_CONFIG["app_secret"]
        )
        print("   OK Token obtained")
        
        # Step 2: Upload image
        print("\nStep 2: Upload image to Feishu")
        image_key = upload_image_to_chat(token, args.file_path)
        print(f"   OK Upload success, image_key: {image_key}")
        
        # Step 3: Send message
        print("\nStep 3: Send image message")
        result = send_image_message(token, args.target, image_key, args.target_type)
        print(f"   OK Send success, message_id: {result.get('data', {}).get('message_id')}")
        
        print("\nImage sent successfully!")
        return 0
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
