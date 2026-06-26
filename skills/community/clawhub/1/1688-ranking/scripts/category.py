#!/usr/bin/env python3
"""
1688 类目查询脚本
使用正确的 HMAC-SHA1 签名算法
"""

import os
import sys
import json
import argparse
import requests

# 添加 scripts 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.auth import get_access_token, sign_request_hmac_sha1

# API 基础URL
BASE_URL = "https://gw.open.1688.com/openapi"

def get_app_credentials():
    """获取应用凭证"""
    app_key = os.getenv('ALI1688_APP_KEY')
    app_secret = os.getenv('ALI1688_APP_SECRET')
    refresh_token = os.getenv('ALI1688_REFRESH_TOKEN')
    access_token = os.getenv('ALI1688_ACCESS_TOKEN')
    
    if not app_key or not app_secret:
        raise Exception("Missing ALI1688_APP_KEY or ALI1688_APP_SECRET")
    
    return app_key, app_secret, refresh_token, access_token

def get_categories(cate_id=0, language='en'):
    """获取类目信息"""
    app_key, app_secret, refresh_token, access_token = get_app_credentials()
    
    # 获取有效的 access_token
    token = get_access_token(app_key, app_secret, refresh_token, access_token)
    
    # 构造请求参数
    params = {
        'categoryId': str(cate_id),
        'language': language,
        'access_token': token
    }
    
    # URL path for signature
    url_path = f"param2/1/com.alibaba.fenxiao.crossborder/category.translation.getById/{app_key}"
    
    # 生成 HMAC-SHA1 签名
    sign = sign_request_hmac_sha1(url_path, params, app_secret)
    params['_aop_signature'] = sign
    
    # 构造完整URL
    url = f"{BASE_URL}/{url_path}"
    
    try:
        response = requests.post(url, data=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"API request failed: {e}")

def main():
    parser = argparse.ArgumentParser(description='1688 Category Query')
    parser.add_argument('cate_id', type=int, nargs='?', default=0, 
                       help='Category ID (default: 0 for all top-level categories)')
    parser.add_argument('--language', default='en',
                       help='Language code (default: en)')
    
    args = parser.parse_args()
    
    try:
        result = get_categories(args.cate_id, args.language)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()