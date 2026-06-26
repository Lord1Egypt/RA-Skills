"""
ClawValue 核心库

提供数据采集、评估和模型定义。

使用示例:
    from lib import DataCollector, EvaluationEngine
    from lib import LogEntry, Skill, OpenClawConfig
    from lib import LogField, LogLevel, SkillCategory
"""

# 常量
from .constants import (
    # 版本信息
    VERSION, APP_NAME, APP_TITLE, APP_DESCRIPTION,
    # 路径配置
    LOG_DIR, OPENCLAW_HOME, OPENCLAW_CONFIG_FILE,
    SKILLS_DIR, SKILL_FILE, DEFAULT_DB_PATH,
    # 日志字段常量
    LogField, LogLevel, LogType,
    # 评估阈值
    SkillThreshold, DepthLevel, ValueRange, LobsterLevel,
    # 成就
    Achievement,
    # 技能分类
    SkillCategory,
    # API 响应
    APIResponse,
    # 默认值
    Defaults
)

# 数据模型
from .schemas import (
    # 枚举
    LogSeverity, UsageDepth,
    # 数据类
    LogEntry, LogStats,
    Skill, OpenClawConfig,
    EvaluationResult, CollectionData
)

# 采集器
from .collector import (
    LogParser, SkillScanner, ConfigAnalyzer, DataCollector
)

# 评估引擎 (从旧模块导入)
from .evaluation import EvaluationEngine

# 版本
__version__ = VERSION
__all__ = [
    # 常量
    'VERSION', 'APP_NAME', 'APP_TITLE', 'APP_DESCRIPTION',
    'LOG_DIR', 'OPENCLAW_HOME', 'OPENCLAW_CONFIG_FILE',
    'SKILLS_DIR', 'SKILL_FILE', 'DEFAULT_DB_PATH',
    'LogField', 'LogLevel', 'LogType',
    'SkillThreshold', 'DepthLevel', 'ValueRange', 'LobsterLevel',
    'Achievement', 'SkillCategory', 'APIResponse', 'Defaults',
    # 数据模型
    'LogSeverity', 'UsageDepth',
    'LogEntry', 'LogStats',
    'Skill', 'OpenClawConfig',
    'EvaluationResult', 'CollectionData',
    # 采集器
    'LogParser', 'SkillScanner', 'ConfigAnalyzer', 'DataCollector',
    # 评估引擎
    'EvaluationEngine'
]