#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: llm.providers.openai
# 说明: OpenAI GPT客户端实现
# 修改建议: 如需扩展，继承OpenAIClient并覆盖方法
# ============================================

import json as json_mod
from typing import Dict, Any, Optional, List

from ..client import LLMClient, Message, ToolCall, LLMResponse

# 可选依赖
try:
    import openai
except ImportError:
    openai = None


class OpenAIClient(LLMClient):
    """OpenAI GPT客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if openai is None:
            raise ImportError("openai package not installed. Run: pip install openai")
        self.client = openai.AsyncOpenAI(
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
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=openai_messages,
            tools=tools or [],
            **kwargs
        )
        
        message = response.choices[0].message
        content = message.content or ""
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=json_mod.loads(tc.function.arguments)
                ))
        
        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            },
            model=response.model
        )
    
    def validate_config(self) -> bool:
        """验证配置"""
        return bool(self.config.get("api_key"))
