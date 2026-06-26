"""
Intent Recognition Layer - Package Init

M-A3 意图识别层，支持智能任务拆解和动态调整。

模块组成:
    - recognizer : 意图识别器
    - decomposer : 任务拆解引擎
    - adjuster   : 动态调整器
"""

from intent.recognizer import IntentType, Intent, SubTask, IntentRecognizer
from intent.decomposer import TaskDecomposer
from intent.adjuster import DynamicAdjuster

__all__ = [
    "IntentType",
    "Intent",
    "SubTask",
    "IntentRecognizer",
    "TaskDecomposer",
    "DynamicAdjuster",
]
