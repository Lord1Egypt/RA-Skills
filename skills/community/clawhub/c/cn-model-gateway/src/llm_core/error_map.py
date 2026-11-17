"""Unified error mapping for llm-core shared kernel.

Maps provider-specific errors to MCP standard error codes.
v1.9.0: YAML 外置 + 中文处置建议。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict

# MCP standard error codes
ERROR_PARAM_INVALID = -32602
ERROR_MODEL_UNAVAILABLE = -32001
ERROR_RATE_LIMITED = -32002
ERROR_INTERNAL = -32603
ERROR_PROVIDER_NOT_FOUND = -32000

# Provider-specific error patterns → MCP error codes
ERROR_MAP: Dict[str, Dict[str, Dict[str, str]]] = {}


def _load_yaml_error_map() -> None:
    """从 references/error_map.yaml 加载错误映射。"""
    global ERROR_MAP
    yaml_path = Path(__file__).resolve().parent.parent.parent / "references" / "error_map.yaml"
    if not yaml_path.exists():
        _load_builtin_error_map()
        return
    try:
        # 添加 _core/ 到 sys.path 以导入 yaml_simple
        core_dir = str(Path(__file__).resolve().parent.parent.parent / "_core")
        if core_dir not in sys.path:
            sys.path.insert(0, core_dir)
        from yaml_simple import load_file
        data = load_file(str(yaml_path))
        if data:
            ERROR_MAP = data
        else:
            _load_builtin_error_map()
    except Exception:
        _load_builtin_error_map()


def _load_builtin_error_map() -> None:
    """内置 fallback 错误映射。"""
    global ERROR_MAP
    ERROR_MAP = {
        "deepseek": {
            "invalid_api_key": {"code": ERROR_PARAM_INVALID, "message": "DeepSeek API key 无效或已过期", "suggestion": "检查 config.json 中 deepseek.api_key 是否正确"},
            "insufficient_quota": {"code": ERROR_RATE_LIMITED, "message": "DeepSeek 额度不足", "suggestion": "检查余额页"},
            "rate_limit": {"code": ERROR_RATE_LIMITED, "message": "DeepSeek 请求过于频繁，请稍后重试", "suggestion": "等待 60 秒后重试"},
        },
        "tongyi": {
            "InvalidApiKey": {"code": ERROR_PARAM_INVALID, "message": "通义 API key 无效", "suggestion": "检查 config.json 中 tongyi.api_key 是否正确"},
            "Throttling.RateLimit": {"code": ERROR_RATE_LIMITED, "message": "通义 请求频率超限", "suggestion": "等待 60 秒后重试"},
        },
        "zhipu": {
            "data_inspection_failed": {"code": ERROR_PARAM_INVALID, "message": "智谱 内容审核未通过，请检查输入内容", "suggestion": "修改提示词重试"},
            "invalid_api_key": {"code": ERROR_PARAM_INVALID, "message": "智谱 API key 无效", "suggestion": "检查 config.json 中 zhipu.api_key 是否正确"},
        },
        "kimi": {
            "invalid_api_key": {"code": ERROR_PARAM_INVALID, "message": "Kimi API key 无效", "suggestion": "检查 config.json 中 kimi.api_key 是否正确"},
            "rate_limit_exceeded": {"code": ERROR_RATE_LIMITED, "message": "Kimi 请求频率超限", "suggestion": "等待 60 秒后重试"},
        },
        "hunyuan": {
            "AuthFailure.SecretIdNotFound": {"code": ERROR_PARAM_INVALID, "message": "混元 SecretId 无效", "suggestion": "检查 config.json 中 hunyuan.api_key 格式"},
            "AuthFailure.SignatureFailure": {"code": ERROR_PARAM_INVALID, "message": "混元 签名失败，请检查 SecretKey", "suggestion": "检查 config.json 中 hunyuan.api_key 格式"},
        },
        "doubao": {
            "AuthenticationError": {"code": ERROR_PARAM_INVALID, "message": "豆包 API key 无效或 endpoint_id 错误", "suggestion": "检查 config.json 中 doubao.api_key 和 endpoint_id"},
            "RateLimitError": {"code": ERROR_RATE_LIMITED, "message": "豆包 请求频率超限", "suggestion": "等待 60 秒后重试"},
        },
        "minimax": {
            "api_key_invalid": {"code": ERROR_PARAM_INVALID, "message": "MiniMax API key 无效", "suggestion": "检查 config.json 中 minimax.api_key 是否正确"},
            "insufficient_balance": {"code": ERROR_RATE_LIMITED, "message": "MiniMax 余额不足", "suggestion": "检查余额页"},
        },
        "lingyi": {
            "invalid_token": {"code": ERROR_PARAM_INVALID, "message": "零一万物 API key 无效", "suggestion": "检查 config.json 中 lingyi.api_key 是否正确"},
            "rate_limit_exceeded": {"code": ERROR_RATE_LIMITED, "message": "零一万物 请求频率超限", "suggestion": "等待 60 秒后重试"},
        },
        "baichuan": {
            "invalid_apikey": {"code": ERROR_PARAM_INVALID, "message": "百川智能 API key 无效", "suggestion": "检查 config.json 中 baichuan.api_key 是否正确"},
            "quota_exceeded": {"code": ERROR_RATE_LIMITED, "message": "百川智能 额度不足", "suggestion": "检查余额页"},
        },
        "stepfun": {
            "auth_failed": {"code": ERROR_PARAM_INVALID, "message": "阶跃星辰 API key 无效", "suggestion": "检查 config.json 中 stepfun.api_key 是否正确"},
            "rate_limit": {"code": ERROR_RATE_LIMITED, "message": "阶跃星辰 请求频率超限", "suggestion": "等待 60 秒后重试"},
        },
    }


# 模块加载时自动加载 YAML
_load_yaml_error_map()


def map_error(provider: str, error_msg: str) -> str:
    """Map provider-specific errors to unified MCP error codes."""
    provider_map = ERROR_MAP.get(provider, {})
    for pattern, info in provider_map.items():
        if pattern.lower() in error_msg.lower():
            suggestion = info.get("suggestion", "")
            base = f"[MCP {info['code']}] {info['message']}"
            if suggestion:
                return f"{base}。处置建议：{suggestion}"
            return base
    return f"[MCP {ERROR_INTERNAL}] {provider} 调用失败: {error_msg}"
