#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: llm.providers.anthropic
# 说明: Anthropic Claude客户端实现
# 修改建议: 如需扩展，继承AnthropicClient并覆盖方法
# ============================================

import json as json_mod
from typing import Dict, Any, Optional, List

from ..client import LLMClient, Message, ToolCall, LLMResponse

# 可选依赖
try:
    import anthropic
except ImportError:
    anthropic = None


class AnthropicClient(LLMClient):
    """Anthropic Claude客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if anthropic is None:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        self.client = anthropic.AsyncAnthropic(
            api_key=config.get("api_key"),
            base_url=config.get("base_url")
        )
    
    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> LLMResponse:
        """发送聊天请求"""
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=anthropic_messages,
            tools=tools or [],
            **kwargs
        )
        
        content = ""
        tool_calls = []
        for block in response.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    id=block.id,
                    name=block.name,
                    arguments=block.input
                ))
        
        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens
            },
            model=response.model
        )
    
    def validate_config(self) -> bool:
        """验证配置"""
        return bool(self.config.get("api_key"))
