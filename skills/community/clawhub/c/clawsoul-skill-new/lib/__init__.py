"""
ClawSoul - 赋予 AI 灵魂的观测者
"""

from .memory_manager import get_memory_manager, MemoryManager
from .prompt_builder import get_prompt_builder, PromptBuilder
from .frustration_detector import get_frustration_detector, FrustrationDetector
from .analyzer import get_analyzer, Analyzer
from .interaction_learner import (
    get_interaction_learner,
    InteractionLearner,
    analyze_user_message,
    detect_preferences,
    update_soul,
    process_user_message,
)
from .ai_personality import local_analyze_ai_personality

__version__ = "1.0.0"
__all__ = [
    "get_memory_manager",
    "MemoryManager",
    "get_prompt_builder",
    "PromptBuilder",
    "get_frustration_detector",
    "FrustrationDetector",
    "get_analyzer",
    "Analyzer",
    "get_interaction_learner",
    "InteractionLearner",
    "analyze_user_message",
    "detect_preferences",
    "update_soul",
    "process_user_message",
    "local_analyze_ai_personality",
]
