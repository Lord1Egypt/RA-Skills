#!/usr/bin/env python3
"""
RoundTable Skill - 多 Agent 深度讨论系统

导出接口：
- RoundTableEngine: 执行引擎
- RoundTableNotifier: 通知模块
- AgentSelector: Agent 选择器
- run_roundtable: 快捷入口
- auto_select_agent: 自动选择 Agent
"""

from .roundtable_engine import RoundTableEngine, RoundState, RoundConfig, AgentResult
from .roundtable_notifier import RoundTableNotifier
from .agent_selector import AgentSelector, auto_select_agent, select_roundtable_agents
from .model_selector import ModelSelector, select_model_for_role, list_available_models
from .prompts.prompt_builder import build_prompt, build_fallback_prompt


async def run_roundtable(topic: str, mode: str = "pre-ac", user_channel: str = "",
                        agent_source: str = "", agents: Optional[List[str]] = None,
                        enable_chat_room: bool = False) -> bool:
    """
    RoundTable 快捷入口

    Args:
        topic: 讨论主题
        mode: 模式（pre-ac: AC 前讨论，post-ac: AC 后审查）
        user_channel: 用户通知渠道
        agent_source: Agent 来源路径（可选）
        agents: 指定 Agent 列表（可选）
        enable_chat_room: 是否启用聊天室

    Returns:
        bool: 是否成功完成
    """
    engine = RoundTableEngine(
        topic, mode, agent_source, agents,
        enable_chat_room=enable_chat_room,
    )
    return await engine.run(user_channel)


__all__ = [
    "RoundTableEngine",
    "RoundTableNotifier",
    "AgentSelector",
    "ModelSelector",
    "RoundState",
    "RoundConfig",
    "AgentResult",
    "run_roundtable",
    "build_prompt",
    "build_fallback_prompt",
    "auto_select_agent",
    "select_roundtable_agents",
    "select_model_for_role",
    "list_available_models",
]

__version__ = "1.0.1"
