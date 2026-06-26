"""
Dream Self-improving Extensions
扩展梦境技能，实现：
- 技能用进废退系统
- 工作复盘与明日计划
- 技能缺口检测与自主学习
- 技能全自动开发
- 完整每日汇报生成
"""

from .skill_evolution import SkillScorer, DecayEngine, SkillRegistry
from .work_review import WorkAnalyzer, TomorrowPlanner
from .skill_explorer import GapDetector, SkillLearner
from .skill_developer import SkillGenerator, SkillQualityAssessor
from .reporter import DailyReporter, SkillReportGenerator

__all__ = [
    'SkillScorer',
    'DecayEngine',
    'SkillRegistry',
    'WorkAnalyzer',
    'TomorrowPlanner',
    'GapDetector',
    'SkillLearner',
    'SkillGenerator',
    'SkillQualityAssessor',
    'DailyReporter',
    'SkillReportGenerator',
]
