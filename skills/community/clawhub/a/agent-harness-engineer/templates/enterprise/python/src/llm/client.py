"""
LLM 客户端抽象接口 - 企业版
规模: Enterprise
预期行数: ~80行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. Message, ToolCall, LLMResponse dataclass (同 Professional)
2. LLMClient 抽象类 - 扩展接口:
   - chat() - 基础调用
   - chat_stream() - 流式调用 (async generator)
   - count_tokens() - Token 计数
   - health_check() - 供应商健康检查
3. LLMUsage dataclass - prompt_tokens, completion_tokens, cost
4. LLMError 自定义异常类

⚠ 流式接口是 Enterprise 的关键要求
⚠ 包括成本追踪 (Usage 中的 cost 字段)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, AsyncIterator


@dataclass
class Message:
    """标准化消息格式"""
    # TODO: role, content, tool_calls, tool_call_id


@dataclass
class ToolCall:
    """标准化工具调用格式"""
    # TODO: id, name, arguments


@dataclass
class LLMUsage:
    """Token 使用量和成本"""
    # TODO: prompt_tokens, completion_tokens, total_tokens, cost


@dataclass
class LLMResponse:
    """标准化 LLM 响应格式"""
    # TODO: content, tool_calls, usage, finish_reason, model, latency_ms


class LLMError(Exception):
    """LLM 调用错误"""
    # TODO: error_type, message, retryable, status_code


class LLMClient(ABC):
    """LLM 客户端抽象接口 - 企业版"""

    @abstractmethod
    async def chat(
        self, messages: List[Message], tools: Optional[List[Dict]] = None
    ) -> LLMResponse:
        """发送消息并获取响应"""
        pass

    @abstractmethod
    async def chat_stream(
        self, messages: List[Message], tools: Optional[List[Dict]] = None
    ) -> AsyncIterator[str]:
        """流式发送消息并逐块返回响应"""
        pass

    @abstractmethod
    async def count_tokens(self, messages: List[Message]) -> int:
        """计算消息的 Token 数量"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """检查 LLM 服务是否可用"""
        pass