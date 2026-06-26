#!/usr/bin/env python3
"""
Agent Selector Skill - 人格身份切换

导出接口：
- AgentSelector: Agent 选择器（安全增强版）
- auto_select_agent: 自动选择 Agent
- select_roundtable_agents: 为 RoundTable 选择 Agent
- switch_agent: 切换人格身份
"""

from .agent_selector import (
    AgentSelector,
    auto_select_agent,
    select_roundtable_agents,
    switch_agent,
    AgentCategory,
    AgentProfile,
)

__all__ = [
    "AgentSelector",
    "auto_select_agent",
    "select_roundtable_agents",
    "switch_agent",
    "AgentCategory",
    "AgentProfile",
]

__version__ = "2.0.0"
__author__ = "Krislu"
__license__ = "MIT"
