#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import ssl
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any

# 成均平台配置
BASE_URL = "https://api.vsbclub.com"
PRECHECK_URL = f"{BASE_URL}/pre-sys/precheck/text"
DEFAULT_TIMEOUT = 30

# Header 缓存
_cached_api_key = None

def get_api_key():
    """获取 API Key（从 X-API-KEY header 鉴权）"""
    global _cached_api_key
    api_key = os.environ.get("CHENGJUN_API_KEY")
    
    # 使用缓存
    if _cached_api_key:
        return _cached_api_key
    
    if api_key:
        _cached_api_key = api_key
        return api_key
    
    raise ValueError(
        "API Key 未配置。请设置环境变量：CHENGJUN_API_KEY"
    )

def http_request(url, method='GET', params=None, data=None, headers=None, timeout=DEFAULT_TIMEOUT):
    """发送 HTTP 请求（使用标准库）"""
    # 构建 URL，参数放在 query string
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    
    # 创建请求
    req = urllib.request.Request(url, method=method)
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    
    # 如果有 data，作为 form 数据发送
    if data:
        if isinstance(data, dict):
            req.data = urllib.parse.urlencode(data).encode('utf-8')
        else:
            req.data = data if isinstance(data, bytes) else data.encode('utf-8')
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP错误 {e.code}: {e.reason}")
    except Exception as e:
        raise Exception(f"请求失败：{str(e)}")

def check_content(text: str) -> Dict[str, Any]:
    """获取访问token"""
    global _token_cache, _token_expires
    
    # 检查缓存
    import time
    if _token_cache and time.time() < _token_expires:
        return _token_cache
    
    # 获取凭证
    creds = get_api_credentials()
    
    # 如果是直接token，直接返回
    if creds["type"] == "direct_token":
        return creds["token"]
    
    # 否则调用接口获取token
    params = {
        "tenantId": creds["tenant_id"],
        "clientId": creds["client_id"],
        "clientSecret": creds["client_secret"]
    }
    
    try:
        result = http_request(TOKEN_URL, method='GET', params=params)
        
        if result.get("code") == 200 and "data" in result:
            token = result["data"].get("token")
            expires_in = result["data"].get("expiresIn", 7200)
            
            # 缓存token（提前60秒过期）
            _token_cache = token
            _token_expires = time.time() + expires_in - 60
            
            return token
        else:
            raise Exception(f"获取token失败: {result.get('msg', '未知错误')}")
            
    except Exception as e:
        raise Exception(f"获取token请求失败: {str(e)}")

def check_content(text: str) -> Dict[str, Any]:
    """
    检测文本内容
    
    Args:
        text: 待检测的文本内容
    
    Returns:
        检测结果字典
    """
    # 参数验证
    if not text:
        return {
            "code": -1,
            "msg": "待检测文本不能为空",
            "precheck": None
        }
    
    if len(text) > 5000:
        return {
            "code": -1,
            "msg": "文本长度超过 5000 字符限制",
            "precheck": None
        }
    
    try:
        # 获取 API Key
        api_key = get_api_key()
        
        # 使用 X-API-KEY header 进行鉴权
        headers = {
            "X-API-KEY": api_key
        }
        
        result = http_request(
            PRECHECK_URL,
            method='POST',
            params={"text": text},
            headers=headers
        )
        
        # 标准化返回格式
        if result.get("code") == 200:
            return {
                "code": 200,
                "msg": "检测成功",
                "precheck": result.get("precheck", {})
            }
        else:
            return {
                "code": result.get("code", -1),
                "msg": result.get("msg", "检测失败"),
                "precheck": None
            }
            
    except ValueError as e:
        return {
            "code": 401,
            "msg": str(e),
            "precheck": None
        }
    except Exception as e:
        return {
            "code": -2,
            "msg": f"API 调用失败：{str(e)}",
            "precheck": None
        }

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    主入口函数（兼容 OpenClaw 调用）
    
    Args:
        params: 参数字典，包含 text 等参数
    
    Returns:
        检测结果字典
    """
    text = params.get("text", "")
    
    return check_content(text)

if __name__ == "__main__":
    # 命令行调用支持
    if len(sys.argv) < 2:
        print(json.dumps({
            "code": -1,
            "msg": "请提供文本内容",
            "precheck": None
        }, ensure_ascii=False))
        sys.exit(1)
    
    text = sys.argv[1]
    
    result = check_content(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
