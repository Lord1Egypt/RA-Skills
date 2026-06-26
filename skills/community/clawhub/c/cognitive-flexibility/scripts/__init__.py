# Cognitive Flexibility Skills

"""
认知灵活性技能包

基于人类四种认知模式：
- OOA: 经验模式（记忆驱动）✅
- OODA: 推理模式（知识驱动）✅
- OOCA: 创造模式（联想驱动）✅
- OOHA: 发现模式（假说驱动）✅
"""

from .chain_reasoner import OODAReasoner
from .pattern_matcher import PatternMatcher
from .self_assessor import SelfAssessor
from .cognitive_controller import CognitiveController
from .creative_explorer import CreativeExplorer
from .hypothesis_generator import HypothesisGenerator
from .usage_monitor import UsageMonitor

__all__ = [
    "OODAReasoner",
    "PatternMatcher", 
    "SelfAssessor",
    "CognitiveController",
    "CreativeExplorer",
    "HypothesisGenerator",
    "UsageMonitor"
]
__version__ = "2.1.0"
