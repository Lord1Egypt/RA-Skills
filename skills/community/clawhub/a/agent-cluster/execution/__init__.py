"""
Execution Engine Abstraction Layer

执行引擎抽象层 - 支持 Claude MA / Local / DeepSeek / GPT-6 四引擎热切换

Architecture:
    EngineRouter → selects best engine based on task characteristics
                    ├── ClaudeMAEngine     (Claude Managed Agents, 通用任务)
                    ├── LocalEngine        (自建引擎, 垂直知识/自进化)
                    ├── DeepSeekEngine     (国产模型, 合规场景)
                    └── GPT6Engine        (GPT-6, 超长上下文/多模态)

Change Log:
    - 2026-04-14: 初始版本，v2.0 执行层解耦
    - 2026-04-14: v3.0 新增 GPT-6 引擎
"""

from .engine_base import (
    AuthProfile,
    AuthKeyState,
    AuthProfileError,
    NoAvailableKeyError,
    KeyCooldownError,
    KeyHealthStatus,
    ExecutionEngine,
    ExecutionResult,
    StreamChunk,
)
from .engine_router import EngineRouter, RoutingRule, RoutingContext, RoutingStrategy
from .claude_ma_engine import ClaudeMAEngine
from .local_engine import LocalEngine
from .deepseek_engine import DeepSeekEngine
from .gpt6_engine import GPT6Engine

__all__ = [
    # AuthProfile
    "AuthProfile",
    "AuthKeyState",
    "AuthProfileError",
    "NoAvailableKeyError",
    "KeyCooldownError",
    "KeyHealthStatus",
    # Base
    "ExecutionEngine",
    "ExecutionResult",
    "StreamChunk",
    # Router
    "EngineRouter",
    "RoutingRule",
    "RoutingContext",
    "RoutingStrategy",
    # Engines
    "ClaudeMAEngine",
    "LocalEngine",
    "DeepSeekEngine",
    "GPT6Engine",
]
