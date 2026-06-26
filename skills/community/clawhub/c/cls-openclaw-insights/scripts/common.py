#!/usr/bin/env python3
"""
公共模块 - 提供共享的工具函数

包含：
- 凭证管理（从 TCCLI 凭证文件读取临时密钥）
- 腾讯云 CLS 客户端创建
- 地域验证
"""

import os
import sys
import re
import json
import time
from typing import Tuple, Set, Dict, Any, Optional

# TCCLI 凭证文件路径
TCCLI_CREDENTIAL_PATH = os.path.expanduser("~/.tccli/default.credential")

# 支持的腾讯云地域白名单
VALID_REGIONS: Set[str] = {
    "ap-beijing",
    "ap-guangzhou",
    "ap-shanghai",
    "ap-chengdu",
    "ap-nanjing",
    "ap-chongqing",
    "ap-hongkong",
    "na-siliconvalley",
    "na-ashburn",
    "ap-singapore",
    "ap-bangkok",
    "eu-frankfurt",
    "ap-tokyo",
    "ap-seoul",
    "ap-jakarta",
    "sa-saopaulo",
    "ap-shenzhen-fsi",
    "ap-shanghai-fsi",
    "ap-beijing-fsi",
    "ap-shanghai-adc",
}


def load_tccli_credential() -> Dict[str, Any]:
    """
    从 TCCLI 凭证文件读取凭证信息
    
    Returns:
        凭证字典，包含 secretId, secretKey, token 等字段
        
    Raises:
        SystemExit: 如果凭证文件不存在、格式错误或密钥已过期
    """
    if not os.path.exists(TCCLI_CREDENTIAL_PATH):
        print("Error: TCCLI 凭证不存在")
        print("\n请先安装 TCCLI 并完成授权登录:")
        print("  1. pip install tccli")
        print("  2. tccli auth login")
        sys.exit(1)
    
    try:
        with open(TCCLI_CREDENTIAL_PATH, "r", encoding="utf-8") as f:
            cred_data = json.load(f)
    except json.JSONDecodeError:
        print("Error: TCCLI 凭证格式错误")
        print("\n请重新执行授权登录: tccli auth login")
        sys.exit(1)
    except PermissionError:
        print("Error: 无权限读取 TCCLI 凭证")
        sys.exit(1)
    
    # 验证必需字段
    secret_id = cred_data.get("secretId", "").strip()
    secret_key = cred_data.get("secretKey", "").strip()
    token = cred_data.get("token", "").strip()
    
    if not secret_id or not secret_key:
        print("Error: TCCLI 凭证中缺少 secretId 或 secretKey")
        print("\n请重新执行授权登录: tccli auth login")
        sys.exit(1)
    
    # 检查临时密钥是否过期
    expires_at = cred_data.get("expiresAt")
    if expires_at and isinstance(expires_at, (int, float)):
        if time.time() > expires_at:
            print("Error: TCCLI 临时密钥已过期。")
            print("\n请重新执行授权登录: tccli auth login")
            sys.exit(1)
    
    return cred_data


def get_credentials_tuple() -> Tuple[str, str, str]:
    """
    从 TCCLI 凭证文件获取凭证（返回元组形式）
    
    Returns:
        (secret_id, secret_key, token) 元组
        
    Raises:
        SystemExit: 如果凭证文件不存在或格式错误
    """
    cred_data = load_tccli_credential()
    return (
        cred_data["secretId"],
        cred_data["secretKey"],
        cred_data.get("token", ""),
    )


def get_credentials_object():
    """
    从 TCCLI 凭证文件获取凭证（返回 Credential 对象形式）
    
    Returns:
        tencentcloud.common.credential.Credential 对象（包含临时密钥 token）
        
    Raises:
        SystemExit: 如果凭证文件不存在或 SDK 未安装
    """
    try:
        from tencentcloud.common import credential
    except ImportError:
        print("Error: tencentcloud-sdk-python is not installed.")
        print("Please install it with: pip install tencentcloud-sdk-python")
        sys.exit(1)
    
    secret_id, secret_key, token = get_credentials_tuple()
    return credential.Credential(secret_id, secret_key, token)


def create_cls_client(region: str):
    """
    创建 CLS API 客户端
    
    Args:
        region: 腾讯云地域
        
    Returns:
        CommonClient 对象
        
    Raises:
        SystemExit: 如果 SDK 未安装
        ValueError: 如果地域无效
    """
    try:
        from tencentcloud.common.common_client import CommonClient
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
    except ImportError:
        print("Error: tencentcloud-sdk-python is not installed.")
        print("Please install it with: pip install tencentcloud-sdk-python")
        sys.exit(1)
    
    # 验证地域
    validate_region(region)
    
    cred = get_credentials_object()
    
    http_profile = HttpProfile()
    http_profile.endpoint = "cls.tencentcloudapi.com"
    
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    
    return CommonClient("cls", "2020-10-16", cred, region, profile=client_profile)


def validate_region(region: str) -> None:
    """
    验证地域是否有效
    
    Args:
        region: 腾讯云地域
        
    Raises:
        ValueError: 如果地域无效
    """
    if region not in VALID_REGIONS:
        raise ValueError(
            f"Invalid region: '{region}'. "
            f"Valid regions are: {', '.join(sorted(VALID_REGIONS))}"
        )


def validate_topic_id(topic_id: str) -> None:
    """
    验证主题 ID 格式，防止路径遍历等注入攻击
    
    合法的 topic_id 只包含字母、数字、连字符和下划线。
    
    Args:
        topic_id: 主题 ID
        
    Raises:
        ValueError: 如果格式无效
    """
    if not topic_id:
        raise ValueError("Topic ID cannot be empty")
    
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', topic_id):
        raise ValueError(
            f"Invalid topic ID format: '{topic_id}'. "
            "Topic ID must contain only alphanumeric characters, hyphens, underscores, and dots."
        )


def validate_label_name(label_name: str) -> None:
    """
    验证 Prometheus 标签名格式，防止路径遍历等注入攻击
    
    合法的标签名只包含字母、数字和下划线（Prometheus 规范）。
    
    Args:
        label_name: 标签名
        
    Raises:
        ValueError: 如果格式无效
    """
    if not label_name:
        raise ValueError("Label name cannot be empty")
    
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', label_name):
        raise ValueError(
            f"Invalid label name format: '{label_name}'. "
            "Label names must match [a-zA-Z_][a-zA-Z0-9_]* (Prometheus naming convention)."
        )


def sanitize_error_message(error: Exception) -> str:
    """
    清理错误消息，移除可能包含的敏感信息（如凭证）
    
    Args:
        error: 异常对象
        
    Returns:
        清理后的错误消息
    """
    error_str = str(error)
    
    # 移除可能的 Basic Auth 凭证（格式：username:password@）
    error_str = re.sub(r'://[^:]+:[^@]+@', '://<credentials>@', error_str)
    
    # 移除 Authorization header 值（Basic、Bearer 等）
    error_str = re.sub(r'(Authorization[\'"]?\s*:\s*[\'"]?)(Basic|Bearer)?\s*[A-Za-z0-9+/=_.\-]+', r'\1<redacted>', error_str, flags=re.IGNORECASE)
    
    # 移除 SecretId 和 SecretKey 模式（腾讯云 AKID 前缀的密钥）
    error_str = re.sub(r'(AKID|SecretId|SecretKey)[A-Za-z0-9]{10,}', r'\1<redacted>', error_str, flags=re.IGNORECASE)
    
    # 移除可能的临时 token（长 Base64 字符串，通常 > 100 字符）
    error_str = re.sub(r'[A-Za-z0-9+/=_\-]{100,}', '<redacted_token>', error_str)
    
    return error_str
