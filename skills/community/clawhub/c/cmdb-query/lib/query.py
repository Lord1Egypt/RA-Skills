#!/usr/bin/env python3
"""
CMDB Query Tool
查询 CMDB 资产数据
"""

import requests
import json
import argparse
from typing import Optional, Dict, Any

# 配置
BASE_URL = "https://10.255.227.233/cmdb/v1/api"
USERNAME = "openclaw_read"
PASSWORD = "JzXCxTaDxE"

# Token 缓存（简单实现，实际应使用更安全的存储）
TOKEN_CACHE: Optional[str] = None
TOKEN_EXPIRY: Optional[float] = None


def get_token() -> str:
    """获取或刷新 Token"""
    global TOKEN_CACHE, TOKEN_EXPIRY
    
    # 检查缓存是否有效（提前 5 分钟刷新）
    if TOKEN_CACHE and TOKEN_EXPIRY and TOKEN_EXPIRY > (time.time() + 300):
        return TOKEN_CACHE
    
    # 登录获取 Token
    url = f"{BASE_URL}/oauth/token"
    data = {"username": USERNAME, "password": PASSWORD}
    
    # 注意：这个 API 需要跳过证书验证
    response = requests.post(
        url,
        json=data,
        verify=False,  # 跳过证书验证
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"登录失败：{response.status_code} {response.text}")
    
    result = response.json()
    if result.get("code") != 20000:
        raise Exception(f"登录失败：{result.get('message')}")
    
    TOKEN_CACHE = result["data"]["token"]
    # Token 有效期 8 小时
    TOKEN_EXPIRY = time.time() + 8 * 3600 - 300  # 提前 5 分钟失效
    
    return TOKEN_CACHE


def query_resources(
    label: str,
    query_filter: Optional[Dict[str, Any]] = None,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    查询资源实例
    
    Args:
        label: 资源类型标识符（如 host, application, RDS_database）
        query_filter: 查询条件，例如 {"$or": [{"name": {"$regex": "test"}}]}
        page: 页码
        page_size: 每页数量
    
    Returns:
        查询结果
    """
    url = f"{BASE_URL}/cloudresources/resource/instance/{label}"
    
    headers = {
        "Authorization": f"Token {get_token()}",
        "Content-Type": "application/json"
    }
    
    body = {
        "query_filter": query_filter or {},
        "format_user_field": "true"
    }
    
    # 分页参数在 URL 上
    params = {"page": page, "page_size": page_size}
    
    # 注意：跳过证书验证
    response = requests.post(
        url,
        json=body,
        params=params,
        headers=headers,
        verify=False,  # 跳过证书验证
        timeout=60
    )
    
    if response.status_code != 200:
        raise Exception(f"查询失败 {label}: {response.status_code} {response.text}")
    
    result = response.json()
    if result.get("code") != 20000:
        raise Exception(f"查询失败 {label}: {result.get('message')}")
    
    return result


def list_all_models() -> list:
    """列出所有资源模型"""
    url = f"{BASE_URL}/cloudresources/resourcefield"
    
    headers = {
        "Authorization": f"Token {get_token()}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        url,
        json={},
        headers=headers,
        verify=False,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"获取模型定义失败：{response.status_code}")
    
    result = response.json()
    if result.get("code") != 20000:
        raise Exception(f"获取模型定义失败：{result.get('message')}")
    
    return result["data"]["items"]


def print_results(result: Dict[str, Any], fields: Optional[list] = None):
    """打印查询结果"""
    items = result.get("data", {}).get("items", [])
    total = result.get("data", {}).get("total", 0)
    
    print(f"\n共 {total} 条记录，当前第 {result.get('data', {}).get('page', 1)} 页\n")
    
    if not items:
        print("无结果")
        return
    
    # 如果没有指定字段，使用第一个结果的字段
    if not fields and items:
        fields = list(items[0].keys())
    
    # 打印表格
    for item in items:
        row = [f"{item.get(f, '')}" for f in fields]
        print(" | ".join(row))


if __name__ == "__main__":
    import time
    
    parser = argparse.ArgumentParser(description="CMDB 查询工具")
    parser.add_argument("label", help="资源类型，如 host, application")
    parser.add_argument("--name", "-n", help="按名称过滤")
    parser.add_argument("--env", "-e", help="按环境过滤")
    parser.add_argument("--page", "-p", type=int, default=1, help="页码")
    parser.add_argument("--page-size", "-s", type=int, default=10, help="每页数量")
    parser.add_argument("--all", "-a", action="store_true", help="列出所有模型定义")
    
    args = parser.parse_args()
    
    if args.all:
        # 列出所有模型
        models = list_all_models()
        print("资源模型列表：")
        for m in models:
            print(f"  {m['label']}: {m['name']}")
    else:
        # 构建查询条件
        query_filter = {}
        if args.name:
            query_filter["name"] = args.name
        if args.env:
            query_filter["environment"] = args.env
        
        try:
            result = query_resources(
                label=args.label,
                query_filter=query_filter if query_filter else None,
                page=args.page,
                page_size=args.page_size
            )
            print_results(result)
        except Exception as e:
            print(f"错误：{e}")
