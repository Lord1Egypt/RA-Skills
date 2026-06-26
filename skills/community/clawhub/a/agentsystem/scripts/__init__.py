"""
HerClaw Agent System - Self-improving AI agent framework

This package provides:
- MemoryManager: Three-layer persistent memory
- PatternRecorder: Task pattern recording and recall
- SkillCreator: Autonomous skill generation
- SelfEvolution: RL-based continuous improvement
- NudgeSystem: Proactive behavior triggers

All modules work together to enable autonomous learning and evolution.
"""

from .memory_manager import MemoryManager, Episode, Knowledge, UserModel
from .pattern_recorder import PatternRecorder, Pattern
from .skill_creator import (
    SkillCreator, 
    Skill, 
    Opportunity, 
    OpportunityDetector,
    SkillGenerator,
    SkillValidator,
    SkillRegistry
)
from .self_evolution import (
    SelfEvolution,
    PerformanceMonitor,
    RLPipeline,
    EvolutionDeployer,
    Trajectory,
    BehaviorModel
)
from .nudge_system import (
    NudgeSystem,
    NudgeScheduler,
    Nudge,
    NudgeType,
    NudgeStatus,
    TriggerType
)

__version__ = "2.0.0"
__all__ = [
    # Memory
    "MemoryManager",
    "Episode", 
    "Knowledge",
    "UserModel",
    
    # Pattern Recording
    "PatternRecorder",
    "Pattern",
    
    # Skill Creation
    "SkillCreator",
    "Skill",
    "Opportunity",
    "OpportunityDetector",
    "SkillGenerator",
    "SkillValidator",
    "SkillRegistry",
    
    # Self-Evolution
    "SelfEvolution",
    "PerformanceMonitor",
    "RLPipeline",
    "EvolutionDeployer",
    "Trajectory",
    "BehaviorModel",
    
    # Nudge System
    "NudgeSystem",
    "NudgeScheduler",
    "Nudge",
    "NudgeType",
    "NudgeStatus",
    "TriggerType"
]
