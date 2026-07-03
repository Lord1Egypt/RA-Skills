#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: llm.factory
# 说明: LLM客户端工厂函数
# 修改建议: 如需添加新供应商，在providers字典中添加
# ============================================

from typing import Dict, Any

from .client import LLMClient
from .providers.anthropic import AnthropicClient
from .providers.openai import OpenAIClient
from .providers.local import LocalClient


def create_llm_client(config: Dict[str, Any]) -> LLMClient:
    """
    根据配置创建对应的LLM客户端
    
    Args:
        config: 配置字典，必须包含 provider 字段
        
    Returns:
        LLMClient实例
        
    Raises:
        ValueError: 如果供应商未知
    """
    provider = config.get("provider", "anthropic").lower()
    
    providers = {
        "anthropic": AnthropicClient,
        "openai": OpenAIClient,
        "azure": OpenAIClient,  # Azure使用OpenAI兼容API
        "local": LocalClient,
    }
    
    if provider not in providers:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Supported: {', '.join(providers.keys())}"
        )
    
    client = providers[provider](config)
    
    if not client.validate_config():
        raise ValueError(f"Invalid configuration for provider: {provider}")
    
    return client
