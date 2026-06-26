"""
AutoDream Core - 通用记忆整理引擎

平台无关的核心实现，支持多种 Agent 平台适配器。

用法:
    from autodream_core import AutoDreamEngine, OpenClawAdapter
    
    adapter = OpenClawAdapter(workspace="/path/to/workspace")
    engine = AutoDreamEngine(adapter)
    result = engine.run()
"""

from .engine import AutoDreamEngine
from .stages.orientation import OrientationStage
from .stages.gather import GatherStage
from .stages.consolidate import ConsolidateStage
from .stages.prune import PruneStage
from .utils.frontmatter import parse_frontmatter
from .utils.text import normalize, canonical, stable_id
from .utils.dates import parse_relative_dates
from .utils.state import DreamState, StateManager
from .analytics import AnalyticsLogger

__version__ = "1.0.0"
__all__ = [
    "AutoDreamEngine",
    "OrientationStage",
    "GatherStage",
    "ConsolidateStage",
    "PruneStage",
    "parse_frontmatter",
    "normalize",
    "canonical",
    "stable_id",
    "parse_relative_dates",
    "DreamState",
    "StateManager",
    "AnalyticsLogger",
]
