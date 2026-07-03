#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: llm.client
# 说明: LLM客户端抽象接口
# 修改建议: 如需添加新供应商，继承LLMClient并实现抽象方法
# ============================================

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Message:
    """标准化消息格式"""
    role: str
    content: str


@dataclass
class ToolCall:
    """标准化工具调用格式"""
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class LLMResponse:
    """标准化LLM响应格式"""
    content: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    usage: Dict[str, int] = field(default_factory=dict)
    model: str = ""


class LLMClient(ABC):
    """LLM客户端抽象基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get("model")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.7)
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> LLMResponse:
        """发送聊天请求"""
        pass
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        return True
