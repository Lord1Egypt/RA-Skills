"""
ClawOrchestra - OpenClaw 原生多智能体编排器

基于 AOrchestra 思想，用四元组(I,C,T,M)动态创建子Agent。

使用方式：
    from claw_orchestra import Orchestrator, AgentTuple
    
    orchestrator = Orchestrator()
    result = orchestrator.run("帮我调研 LangChain 框架")
"""

__version__ = "0.1.0"
__author__ = "ClawOrchestra Team"

# 核心模块
from .core import (
    AgentTuple,
    Orchestrator,
    Delegate,
    Finish,
    OpenClawAdapter,
    orchestrate,
)

# 路由器
from .router import (
    ContextRouter,
    ModelRouter,
    ToolRouter,
    route_context,
    select_model,
    select_tools,
)

# 学习模块
from .learner import (
    ExperienceStore,
    CostTracker,
    record_experience,
    find_similar_experiences,
    track_cost,
    get_cost_tracker,
    get_experience_store,
)

__all__ = [
    # 核心
    "AgentTuple",
    "Orchestrator",
    "Delegate",
    "Finish",
    "OpenClawAdapter",
    "orchestrate",
    # 路由
    "ContextRouter",
    "ModelRouter",
    "ToolRouter",
    "route_context",
    "select_model",
    "select_tools",
    # 学习
    "ExperienceStore",
    "CostTracker",
    "record_experience",
    "find_similar_experiences",
    "track_cost",
    "get_cost_tracker",
    "get_experience_store",
]