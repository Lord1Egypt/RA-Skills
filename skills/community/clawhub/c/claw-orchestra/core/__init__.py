"""ClawOrchestra Core - 四元组抽象与编排器"""

from .four_tuple import AgentTuple
from .orchestrator import Orchestrator, orchestrate
from .action_space import Delegate, Finish
from .openclaw_adapter import OpenClawAdapter, SpawnResult, spawn_agent

__all__ = [
    "AgentTuple",
    "Orchestrator", 
    "orchestrate",
    "Delegate",
    "Finish",
    "OpenClawAdapter",
    "SpawnResult",
    "spawn_agent",
]