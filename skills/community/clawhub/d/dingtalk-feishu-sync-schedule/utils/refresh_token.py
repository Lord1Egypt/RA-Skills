#!/usr/bin/env python3
"""
飞书token自动刷新工具
从 ~/.feishu/config.json 读取应用凭证和token，自动刷新 access token
"""

import os
import sys

# 添加父目录到路径，导入配置加载器
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config_loader import get_feishu_config, load_config

FEISHU_CONFIG_PATH = os.path.expanduser("~/.feishu/config.json")

def refresh_access_token():
    """刷新飞书 access token"""
    import requests
    import json

    config = load_config()
    feishu = get_feishu_config(config)

    app_id = feishu.get('app_id')
    app_secret = feishu.get('app_secret')

    if not app_id or not app_secret:
        print("❌ 飞书配置不完整，缺少 app_id 或 app_secret")
        return False

    if not os.path.exists(FEISHU_CONFIG_PATH):
        print(f"❌ 配置文件不存在: {FEISHU_CONFIG_PATH}")
        return False

    with open(FEISHU_CONFIG_PATH, 'r', encoding='utf-8') as f:
        token_data = json.load(f)

    refresh_token = token_data.get('refresh_token')
    if not refresh_token:
        print("❌ 找不到 refresh_token")
        return False

    url = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"
    resp = requests.post(url, json={
        "grant_type": "refresh_token",
        "app_id": app_id,
        "app_secret": app_secret,
        "refresh_token": refresh_token
    })

    data = resp.json()
    if data.get('code') != 0:
        print(f"❌ 刷新失败: {data.get('msg')}")
        return False

    new_data = data.get('data', {})
    # 只更新 token 相关字段，保留其他配置
    for k in ['access_token', 'refresh_token', 'expires_in', 'refresh_expires_in']:
        if k in new_data:
            token_data[k] = new_data[k]
    with open(FEISHU_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(token_data, f, indent=2, ensure_ascii=False)

    print(f"✅ token刷新成功")
    print(f"   新 access_token: {new_data.get('access_token', '')[:10]}...")
    print(f"   过期时间: {new_data.get('expires_in')}秒")
    return True

if __name__ == '__main__':
    success = refresh_access_token()
    exit(0 if success else 1)
