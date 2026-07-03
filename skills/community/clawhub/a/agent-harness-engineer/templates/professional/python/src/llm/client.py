"""
LLM 客户端抽象接口
规模: Professional
预期行数: ~50行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. Message dataclass - role, content, tool_calls, tool_call_id
2. ToolCall dataclass - id, name, arguments
3. LLMResponse dataclass - content, tool_calls, usage, finish_reason
4. LLMClient 抽象类 - 定义统一的 LLM 调用接口:
   - chat(messages: List[Message], tools: List[Dict]) -> LLMResponse
   - 支持文本响应和工具调用响应

⚠ 此处仅定义抽象接口, 不实现任何具体供应商
⚠ 所有 LLM 供应商实现都必须遵循此接口
⚠ 使用 @abstractmethod 装饰器
⚠ 不导入任何第三方 SDK (openai, anthropic 等)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Message:
    """标准化消息格式"""
    role: str
    content: Optional[str] = None
    # TODO: tool_calls, tool_call_id


@dataclass
class ToolCall:
    """标准化工具调用格式"""
    # TODO: id, name, arguments


@dataclass
class LLMResponse:
    """标准化 LLM 响应格式"""
    # TODO: content, tool_calls, usage, finish_reason


class LLMClient(ABC):
    """LLM 客户端抽象接口"""

    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """
        发送消息并获取响应

        Args:
            messages: 消息历史列表
            tools: 可用的工具定义列表 (OpenAI function calling 格式)

        Returns:
            LLMResponse: 包含文本响应或工具调用的标准化响应
        """
        # TODO: AI 根据用户选择的供应商实现此接口
        pass