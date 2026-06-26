#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Publishing Configuration
从 credentials/wechat.json 读取凭据
"""

import json
import os

# 从凭据文件读取
CREDENTIALS_PATH = "/root/.openclaw/credentials/wechat.json"

def load_credentials():
    """从 credentials 目录加载凭据"""
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH, 'r') as f:
            return json.load(f)
    return {}

creds = load_credentials()

# Default cover image media_id
DEFAULT_COVER_MEDIA_ID = "WOr7ZIAYNpvYmON1V3ZQwcJJM5-5tgg8B2WMeN-oQF6R3PSE5lrtwOhwvcAOc_ZC"

# WeChat Official Account Credentials (从 credentials 读取)
APPID = creds.get("app_id", "")
APPSECRET = creds.get("app_secret", "")
