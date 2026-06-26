#!/usr/bin/env python3
"""
ClawOrchestra - OpenClaw 原生多智能体编排器

基于 AOrchestra 思想，用四元组(I,C,T,M)动态创建子Agent。

使用方式：
    from claw_orchestra import Orchestrator, AgentTuple
    
    orchestrator = Orchestrator()
    result = orchestrator.run("帮我调研 LangChain 框架")
"""

import sys
import os

# 添加项目路径
PROJECT_ROOT = "/workspace/projects/claw-orchestra"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 导入核心模块
from core import (
    AgentTuple,
    Orchestrator,
    Delegate,
    Finish,
    OpenClawAdapter,
    orchestrate,
)
from core.llm_decision import LLMDecisionMaker, decompose_task
from router import (
    ContextRouter,
    ModelRouter,
    ToolRouter,
    route_context,
    select_model,
    select_tools,
)


# 版本
__version__ = "0.1.0"
__author__ = "ClawOrchestra Team"


# 便捷函数
def quick_research(
    topic: str,
    num_agents: int = 2,
    spawn_fn=None,
):
    """
    快速调研任务
    
    Args:
        topic: 调研主题
        num_agents: 并行 Agent 数量
        spawn_fn: sessions_spawn 函数
    
    Example:
        >>> result = quick_research("LangChain 框架", spawn_fn=sessions_spawn)
    """
    from core import AgentTuple, OpenClawAdapter
    
    adapter = OpenClawAdapter(verbose=True)
    if spawn_fn:
        adapter.set_spawn_fn(spawn_fn)
    
    # 创建多个 Agent 并行执行
    agents = []
    for i in range(num_agents):
        phi = AgentTuple.researcher(
            instruction=f"搜索 {topic} 的第 {i+1} 个关键方面",
            context=[f"主任务: {topic}"],
        )
        agents.append(phi)
    
    # 并行执行
    results = adapter.spawn_parallel(agents)
    
    # 整合结果
    outputs = [r.output for r in results if r.success]
    return "\n\n---\n\n".join(outputs)


def quick_compare(
    items: list,
    spawn_fn=None,
):
    """
    快速对比任务
    
    Args:
        items: 要对比的项目列表
        spawn_fn: sessions_spawn 函数
    
    Example:
        >>> result = quick_compare(["LangChain", "CrewAI", "AutoGen"], spawn_fn=sessions_spawn)
    """
    from core import AgentTuple, OpenClawAdapter
    
    adapter = OpenClawAdapter(verbose=True)
    if spawn_fn:
        adapter.set_spawn_fn(spawn_fn)
    
    # 为每个项目创建一个 Agent
    agents = []
    for item in items:
        phi = AgentTuple.researcher(
            instruction=f"搜索 {item} 的核心特性和优缺点",
            context=[f"对比任务: 对比 {', '.join(items)}"],
        )
        agents.append(phi)
    
    # 并行执行
    results = adapter.spawn_parallel(agents)
    
    # 整合结果
    outputs = [r.output for r in results if r.success]
    return "\n\n---\n\n".join(outputs)


# 导出
__all__ = [
    # 核心类
    "AgentTuple",
    "Orchestrator",
    "Delegate",
    "Finish",
    "OpenClawAdapter",
    
    # 路由器
    "ContextRouter",
    "ModelRouter",
    "ToolRouter",
    
    # 决策器
    "LLMDecisionMaker",
    
    # 便捷函数
    "orchestrate",
    "decompose_task",
    "route_context",
    "select_model",
    "select_tools",
    "quick_research",
    "quick_compare",
]