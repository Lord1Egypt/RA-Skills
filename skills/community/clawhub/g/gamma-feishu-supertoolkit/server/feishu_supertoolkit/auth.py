"""认证模块

处理飞书 API 的鉴权和请求
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

import requests


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 0:
        raise Exception(f"获取 access_token 失败：{data}")
    return data["tenant_access_token"]


def feishu_request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    files: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """发送飞书 API 请求
    
    Args:
        method: HTTP 方法
        path: API 路径
        params: 查询参数
        json_body: JSON 请求体
        headers: 额外请求头
        files: 上传的文件
        
    Returns:
        API 响应数据
    """
    import os
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        raise Exception("未配置 FEISHU_APP_ID 或 FEISHU_APP_SECRET")
    
    # 获取 token
    token = get_tenant_access_token(app_id, app_secret)
    
    # 构建请求头
    req_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    
    if headers:
        req_headers.update(headers)
    
    # 发送请求
    url = f"https://open.feishu.cn{path}"
    
    if files:
        # 文件上传使用 multipart/form-data
        req_headers.pop("Content-Type", None)  # 让 requests 自动设置
        response = requests.request(
            method,
            url,
            headers=req_headers,
            params=params,
            files=files,
            timeout=60,
        )
    else:
        response = requests.request(
            method,
            url,
            headers=req_headers,
            params=params,
            json=json_body,
            timeout=30,
        )
    
    response.raise_for_status()
    data = response.json()
    
    # 检查错误码
    code = data.get("code")
    if code and code != 0:
        raise Exception(f"飞书 API 错误：code={code}, msg={data.get('msg', '')}")
    
    return data
