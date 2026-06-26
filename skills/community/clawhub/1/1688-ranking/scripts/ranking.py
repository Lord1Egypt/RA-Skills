#!/usr/bin/env python3
"""
1688 榜单查询脚本
支持商品榜单和热搜词查询
使用正确的 HMAC-SHA1 签名算法
"""

import os
import sys
import json
import argparse
import requests
from urllib.parse import quote

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

def query_top_list(rank_id, list_type='complex', limit=10, lang='en'):
    """查询商品榜单"""
    app_key, app_secret, refresh_token, access_token = get_app_credentials()
    
    # 获取有效的 access_token
    token = get_access_token(app_key, app_secret, refresh_token, access_token)
    
    # 构造 rankQueryParams 对象
    rank_query_params = {
        'rankId': str(rank_id),
        'rankType': list_type,  # Changed from 'type' to 'rankType'
        'limit': limit,         # Keep as number, not string
        'language': lang
    }
    
    # 构造请求参数（扁平化）
    params = {
        'rankQueryParams': json.dumps(rank_query_params, separators=(',', ':')),
        'access_token': token
    }
    
    # URL path for signature
    url_path = f"param2/1/com.alibaba.fenxiao.crossborder/product.topList.query/{app_key}"
    
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

def query_top_keyword(source_id, country='en', keyword_type='cate'):
    """查询热搜词"""
    app_key, app_secret, refresh_token, access_token = get_app_credentials()
    
    # 获取有效的 access_token
    token = get_access_token(app_key, app_secret, refresh_token, access_token)
    
    # 构造 topSeKeywordParam 对象
    top_se_keyword_param = {
        'sourceId': str(source_id),
        'country': country,
        'hotKeywordType': keyword_type  # Changed from 'type' to 'hotKeywordType'
    }
    
    # 构造请求参数（扁平化）
    params = {
        'topSeKeywordParam': json.dumps(top_se_keyword_param, separators=(',', ':')),
        'access_token': token
    }
    
    # URL path for signature
    url_path = f"param2/1/com.alibaba.fenxiao.crossborder/product.search.topKeyword/{app_key}"
    
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
    parser = argparse.ArgumentParser(description='1688 Ranking Skill')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # 商品榜单子命令
    top_list_parser = subparsers.add_parser('top-list', help='Query product ranking list')
    top_list_parser.add_argument('rank_id', type=int, help='Ranking/Category ID')
    top_list_parser.add_argument('--type', choices=['complex', 'hot', 'goodPrice'], 
                                default='complex', help='Ranking type')
    top_list_parser.add_argument('--limit', type=int, default=10, 
                                help='Number of products (1-20)')
    top_list_parser.add_argument('--lang', default='en', 
                                help='Language code (default: en)')
    
    # 热搜词子命令
    top_keyword_parser = subparsers.add_parser('top-keyword', help='Query top keywords')
    top_keyword_parser.add_argument('source_id', type=int, help='Category ID')
    top_keyword_parser.add_argument('--country', default='en', 
                                   help='Country/language code (default: en)')
    top_keyword_parser.add_argument('--type', default='cate', 
                                   help='Keyword type (fixed as cate)')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'top-list':
            result = query_top_list(
                rank_id=args.rank_id,
                list_type=args.type,
                limit=min(max(args.limit, 1), 20),  # 限制在1-20之间
                lang=args.lang
            )
        elif args.command == 'top-keyword':
            result = query_top_keyword(
                source_id=args.source_id,
                country=args.country,
                keyword_type=args.type
            )
        
        # 输出JSON结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()