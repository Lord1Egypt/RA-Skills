"""
CivilLabClaw-AI 技能包
AI+ 土木交叉方向 - 机器学习、深度学习、数字孪生、智能监测

版本：v1.0 (设计阶段)
创建日期：2026-03-20
"""

__version__ = "1.0.0"
__author__ = "SuperMike"
__email__ = "civilabclaw@example.com"

from .core.router import TaskRouter
from .ml_struct.predictor import StructuralPredictor
from .dl_damage.detector import DamageDetector
from .digital_twin.twinner import DigitalTwin
from .smart_monitor.analyzer import MonitorAnalyzer

__all__ = [
    "TaskRouter",
    "StructuralPredictor",
    "DamageDetector",
    "DigitalTwin",
    "MonitorAnalyzer",
]
