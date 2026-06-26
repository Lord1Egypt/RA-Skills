#!/usr/bin/env python3
"""
钉钉多维表格 API 技能实现
提供表格管理、数据增删改查等功能
"""

import os
import json
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
import requests


# ======================= 配置 =======================

DINGTALK_API_BASE = "https://api.dingtalk.com"

# 从环境变量或配置文件读取凭证
def get_dingtalk_credentials():
    """获取钉钉凭证"""
    # 优先从环境变量读取
    client_id = os.environ.get("DINGTALK_CLIENT_ID")
    client_secret = os.environ.get("DINGTALK_CLIENT_SECRET")
    
    # 如果环境变量没有，尝试从配置文件读取
    if not client_id or not client_secret:
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                dingtalk_config = config.get("channels", {}).get("ddingtalk", {})
                accounts = dingtalk_config.get("accounts", {})
                default_account = accounts.get("default", {})
                client_id = default_account.get("clientId")
                client_secret = default_account.get("clientSecret")
        except Exception:
            pass
    
    if not client_id or not client_secret:
        raise ValueError("钉钉凭证未配置，请设置 DINGTALK_CLIENT_ID 和 DINGTALK_CLIENT_SECRET 环境变量")
    
    return client_id, client_secret


# ======================= Access Token 管理 =======================

_token_cache = {}

def get_access_token(client_id: str, client_secret: str) -> str:
    """获取钉钉 access_token"""
    cache_key = client_id
    current_time = time.time()
    
    # 检查缓存（提前 5 分钟过期）
    if cache_key in _token_cache:
        token_info = _token_cache[cache_key]
        if current_time < token_info["expire_time"] - 300:
            return token_info["token"]
    
    # 请求新 token
    url = f"{DINGTALK_API_BASE}/v1.0/oauth2/accessToken"
    headers = {"Content-Type": "application/json"}
    body = {
        "appKey": client_id,
        "appSecret": client_secret
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    result = response.json()
    
    if not result.get("accessToken"):
        raise ValueError(f"获取 access_token 失败：{result}")
    
    token = result["accessToken"]
    expire_in = result.get("expireIn", 7200)  # 默认 2 小时
    
    # 缓存 token
    _token_cache[cache_key] = {
        "token": token,
        "expire_time": current_time + expire_in
    }
    
    return token


def dingtalk_api_request(method: str, path: str, body: Optional[Dict] = None, 
                         access_token: Optional[str] = None,
                         params: Optional[Dict] = None) -> Dict:
    """
    钉钉 API 统一调用方法
    
    Args:
        method: HTTP 方法 (GET/POST/PUT/DELETE)
        path: API 路径
        body: 请求体
        access_token: 可选的 access_token
        params: URL 查询参数
    
    Returns:
        API 响应结果
    """
    url = f"{DINGTALK_API_BASE}{path}"
    headers = {"Content-Type": "application/json"}
    
    if access_token:
        headers["x-acs-dingtalk-access-token"] = access_token
    
    if method.upper() == "GET":
        response = requests.get(url, headers=headers, params=params or body or {}, timeout=30)
    else:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=body or {},
            params=params,
            timeout=30
        )
    
    response.raise_for_status()
    return response.json()


# ======================= 多维表格 API =======================

def bitable_list(space_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """
    获取多维表格列表
    
    Args:
        space_id: 可选的空间 ID
        limit: 返回数量限制
    
    Returns:
        表格列表
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    params = {"limit": limit}
    if space_id:
        params["space_id"] = space_id
    
    try:
        result = dingtalk_api_request("GET", "/v1.0/bitable/apps", params=params, access_token=access_token)
        return result.get("result", {}).get("list", [])
    except Exception as e:
        return [{"error": f"获取表格列表失败：{str(e)}"}]


def bitable_get_meta(app_token: str) -> Dict:
    """
    获取表格元数据
    
    Args:
        app_token: 表格应用 token（从 URL 获取，如 /base/XXX 或 /wiki/XXX 中的 XXX）
    
    Returns:
        表格元数据（包含表格列表、名称等）
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    try:
        result = dingtalk_api_request("GET", f"/v1.0/bitable/apps/{app_token}", access_token=access_token)
        return result.get("result", {})
    except Exception as e:
        return {"error": f"获取表格元数据失败：{str(e)}"}


def bitable_list_fields(app_token: str, table_id: str) -> List[Dict]:
    """
    获取表格字段列表
    
    Args:
        app_token: 表格应用 token
        table_id: 表格 ID
    
    Returns:
        字段列表
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    try:
        result = dingtalk_api_request(
            "GET", 
            f"/v1.0/bitable/apps/{app_token}/tables/{table_id}/fields",
            access_token=access_token
        )
        return result.get("result", {}).get("items", [])
    except Exception as e:
        return [{"error": f"获取字段列表失败：{str(e)}"}]


def bitable_list_records(app_token: str, table_id: str, 
                         filter: Optional[str] = None,
                         sort: Optional[str] = None,
                         page_size: int = 100,
                         page_token: Optional[str] = None) -> Dict:
    """
    查询记录
    
    Args:
        app_token: 表格应用 token
        table_id: 表格 ID
        filter: 筛选条件（JSON 字符串）
        sort: 排序字段（JSON 字符串）
        page_size: 每页数量，默认 100
        page_token: 分页 token
    
    Returns:
        记录列表和分页信息
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    params = {
        "pageSize": page_size
    }
    
    if page_token:
        params["pageToken"] = page_token
    
    body = {}
    if filter:
        try:
            body["filter"] = json.loads(filter)
        except json.JSONDecodeError:
            body["filter"] = filter
    
    if sort:
        try:
            body["sort"] = json.loads(sort)
        except json.JSONDecodeError:
            body["sort"] = sort
    
    try:
        result = dingtalk_api_request(
            "POST",
            f"/v1.0/bitable/apps/{app_token}/tables/{table_id}/records/search",
            body=body,
            params=params,
            access_token=access_token
        )
        return result.get("result", {})
    except Exception as e:
        return {"error": f"查询记录失败：{str(e)}"}


def bitable_get_record(app_token: str, table_id: str, record_id: str) -> Dict:
    """
    获取单条记录
    
    Args:
        app_token: 表格应用 token
        table_id: 表格 ID
        record_id: 记录 ID
    
    Returns:
        记录详情
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    try:
        result = dingtalk_api_request(
            "GET",
            f"/v1.0/bitable/apps/{app_token}/tables/{table_id}/records/{record_id}",
            access_token=access_token
        )
        return result.get("result", {})
    except Exception as e:
        return {"error": f"获取记录失败：{str(e)}"}


def bitable_create_record(app_token: str, table_id: str, fields: Dict) -> str:
    """
    新增记录
    
    Args:
        app_token: 表格应用 token
        table_id: 表格 ID
        fields: 字段值（字典）
    
    Returns:
        创建的记录 ID
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    body = {"fields": fields}
    
    try:
        result = dingtalk_api_request(
            "POST",
            f"/v1.0/bitable/apps/{app_token}/tables/{table_id}/records",
            body=body,
            access_token=access_token
        )
        return result.get("result", {}).get("recordId", "")
    except Exception as e:
        return f"创建失败：{str(e)}"


def bitable_update_record(app_token: str, table_id: str, record_id: str, fields: Dict) -> bool:
    """
    更新记录
    
    Args:
        app_token: 表格应用 token
        table_id: 表格 ID
        record_id: 记录 ID
        fields: 要更新的字段值
    
    Returns:
        更新结果
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    body = {"fields": fields}
    
    try:
        result = dingtalk_api_request(
            "PUT",
            f"/v1.0/bitable/apps/{app_token}/tables/{table_id}/records/{record_id}",
            body=body,
            access_token=access_token
        )
        return result.get("success", False)
    except Exception as e:
        return False


def bitable_delete_record(app_token: str, table_id: str, record_id: str) -> bool:
    """
    删除记录
    
    Args:
        app_token: 表格应用 token
        table_id: 表格 ID
        record_id: 记录 ID
    
    Returns:
        删除结果
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    try:
        result = dingtalk_api_request(
            "DELETE",
            f"/v1.0/bitable/apps/{app_token}/tables/{table_id}/records/{record_id}",
            access_token=access_token
        )
        return result.get("success", False)
    except Exception:
        return False


def bitable_create_field(app_token: str, table_id: str, 
                         field_name: str, field_type: str) -> str:
    """
    添加字段
    
    Args:
        app_token: 表格应用 token
        table_id: 表格 ID
        field_name: 字段名称
        field_type: 字段类型 (Text/Number/Date/SingleSelect/MultiSelect/Checkbox/User/Phone/URL)
    
    Returns:
        创建的字段 ID
    """
    client_id, client_secret = get_dingtalk_credentials()
    access_token = get_access_token(client_id, client_secret)
    
    # 字段类型映射
    type_map = {
        "Text": 1,
        "Number": 2,
        "SingleSelect": 3,
        "MultiSelect": 4,
        "Date": 5,
        "Checkbox": 7,
        "User": 11,
        "Phone": 13,
        "URL": 15,
    }
    
    body = {
        "name": field_name,
        "type": type_map.get(field_type, 1)
    }
    
    try:
        result = dingtalk_api_request(
            "POST",
            f"/v1.0/bitable/apps/{app_token}/tables/{table_id}/fields",
            body=body,
            access_token=access_token
        )
        return result.get("result", {}).get("fieldId", "")
    except Exception as e:
        return f"创建失败：{str(e)}"


# ======================= 工具函数 =======================

def format_field(field: Dict) -> str:
    """格式化字段显示"""
    name = field.get("name", "")
    type_ = field.get("type", "")
    field_id = field.get("fieldId", "")
    return f"{field_id}: {name} ({type_})"


def format_record(record: Dict, fields: Optional[List] = None) -> str:
    """格式化记录显示"""
    record_id = record.get("recordId", "")
    fields_data = record.get("fields", {})
    
    lines = [f"📄 记录 ID: {record_id}"]
    for key, value in fields_data.items():
        lines.append(f"   {key}: {value}")
    
    return "\n".join(lines)


# ======================= 主函数（供技能调用） =======================

def main():
    """测试函数"""
    print("钉钉多维表格 API 技能测试")
    
    try:
        # 测试获取表格列表
        tables = bitable_list(limit=5)
        print(f"\n多维表格 ({len(tables)}):")
        for table in tables:
            print(f"  - {table.get('name', '未知')} ({table.get('appId', '')})")
            
    except Exception as e:
        print(f"测试失败：{e}")


if __name__ == "__main__":
    main()
