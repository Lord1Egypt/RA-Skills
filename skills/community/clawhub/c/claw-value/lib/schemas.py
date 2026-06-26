"""
ClawValue 数据模型模块

定义结构化的数据模型，包含：
- 日志条目模型
- 技能模型
- 配置模型
- 评估结果模型

使用 dataclass 提供类型安全和自动方法。
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum

# 使用绝对导入或条件导入
try:
    from .constants import LogLevel, LogType, SkillCategory
except ImportError:
    from constants import LogLevel, LogType, SkillCategory


# =============================================================================
# 枚举定义
# =============================================================================

class LogSeverity(Enum):
    """日志严重程度枚举"""
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4
    
    @classmethod
    def from_string(cls, level_str: str) -> 'LogSeverity':
        """从字符串创建枚举值"""
        mapping = {
            'DEBUG': cls.DEBUG,
            'INFO': cls.INFO,
            'WARN': cls.WARN,
            'WARNING': cls.WARN,
            'ERROR': cls.ERROR,
            'FATAL': cls.FATAL,
            'TRACE': cls.DEBUG
        }
        return mapping.get(level_str.upper(), cls.INFO)


class UsageDepth(Enum):
    """使用深度枚举"""
    SHALLOW = 'shallow'
    MODERATE = 'moderate'
    DEEP = 'deep'
    
    @property
    def label(self) -> str:
        """获取中文标签"""
        labels = {
            'shallow': '浅度使用',
            'moderate': '中度使用',
            'deep': '深度使用'
        }
        return labels.get(self.value, '未知')


# =============================================================================
# 日志模型
# =============================================================================

@dataclass
class LogEntry:
    """
    日志条目模型
    
    结构化表示单条日志记录，包含解析后的所有关键信息。
    
    Attributes:
        message: 日志消息内容
        level: 日志级别 (DEBUG/INFO/WARN/ERROR/FATAL)
        timestamp: 时间戳字符串
        subsystem: 子系统标识 (如 tools, gateway, agent)
        log_type: 日志类型分类
        raw_data: 原始 JSON 数据
    """
    message: str
    level: str = LogLevel.INFO
    timestamp: str = ''
    subsystem: str = 'unknown'
    log_type: str = LogType.OTHER
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def severity(self) -> LogSeverity:
        """获取日志严重程度枚举"""
        return LogSeverity.from_string(self.level)
    
    @property
    def is_error(self) -> bool:
        """是否为错误日志"""
        return self.severity.value >= LogSeverity.ERROR.value
    
    @property
    def is_tool_related(self) -> bool:
        """是否与工具/技能相关"""
        return self.log_type == LogType.TOOL
    
    @classmethod
    def from_openclaw_json(cls, data: Dict[str, Any]) -> 'LogEntry':
        """
        从 OpenClaw 日志 JSON 创建实例
        
        Args:
            data: OpenClaw 日志 JSON 对象
            
        Returns:
            LogEntry 实例
        """
        # 提取消息
        message = data.get('0', '') or data.get('message', '')
        
        # 提取元数据
        meta = data.get('_meta', {})
        level = meta.get('logLevelName', LogLevel.INFO)
        
        # 提取子系统
        subsystem = cls._extract_subsystem(message)
        
        # 分类日志类型
        log_type = cls._classify_message(message)
        
        return cls(
            message=message,
            level=level,
            timestamp=data.get('time', ''),
            subsystem=subsystem,
            log_type=log_type,
            raw_data=data
        )
    
    @staticmethod
    def _extract_subsystem(message: str) -> str:
        """从消息中提取子系统标识"""
        if message.startswith('['):
            end = message.find(']')
            if end > 0:
                return message[1:end]
        return 'unknown'
    
    @staticmethod
    def _classify_message(message: str) -> str:
        """分类日志消息类型"""
        msg_lower = message.lower()
        
        if 'error' in msg_lower or 'failed' in msg_lower:
            return LogType.ERROR
        elif 'session' in msg_lower:
            return LogType.SESSION
        elif 'tool' in msg_lower or 'skill' in msg_lower:
            return LogType.TOOL
        elif 'model' in msg_lower or 'token' in msg_lower:
            return LogType.MODEL
        elif 'webhook' in msg_lower or 'message' in msg_lower:
            return LogType.MESSAGE
        elif 'connected' in msg_lower or 'disconnected' in msg_lower:
            return LogType.CONNECTION
        else:
            return LogType.OTHER
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'message': self.message,
            'level': self.level,
            'timestamp': self.timestamp,
            'subsystem': self.subsystem,
            'log_type': self.log_type
        }


@dataclass
class LogStats:
    """
    日志统计模型
    
    汇总日志分析结果。
    """
    total_entries: int = 0
    info_count: int = 0
    warn_count: int = 0
    error_count: int = 0
    tool_calls: int = 0
    model_calls: int = 0
    connections: int = 0
    errors: int = 0
    
    def add_entry(self, entry: LogEntry) -> None:
        """添加日志条目到统计"""
        self.total_entries += 1
        
        # 按级别统计
        if entry.level == LogLevel.ERROR:
            self.error_count += 1
        elif entry.level == LogLevel.WARN:
            self.warn_count += 1
        else:
            self.info_count += 1
        
        # 按类型统计
        if entry.log_type == LogType.ERROR:
            self.errors += 1
        elif entry.log_type == LogType.TOOL:
            self.tool_calls += 1
        elif entry.log_type == LogType.MODEL:
            self.model_calls += 1
        elif entry.log_type == LogType.CONNECTION:
            self.connections += 1
    
    def to_dict(self) -> Dict[str, int]:
        """转换为字典格式"""
        return {
            'total_entries': self.total_entries,
            'info_count': self.info_count,
            'warn_count': self.warn_count,
            'error_count': self.error_count,
            'tool_calls': self.tool_calls,
            'model_calls': self.model_calls,
            'connections': self.connections,
            'errors': self.errors
        }


# =============================================================================
# 技能模型
# =============================================================================

@dataclass
class Skill:
    """
    技能模型
    
    表示一个 OpenClaw 技能的元数据。
    
    Attributes:
        name: 技能名称
        description: 技能描述
        version: 版本号
        author: 作者
        is_custom: 是否为自定义技能
        is_high_risk: 是否为高风险技能
        category: 技能类别
        source: 技能来源（workspace/builtin/extra）
        filepath: 文件路径
    """
    name: str
    description: str = ''
    version: str = '1.0.0'
    author: str = ''
    is_custom: bool = True
    is_high_risk: bool = False
    category: str = SkillCategory.其他
    source: str = 'workspace'  # workspace/builtin/extra
    filepath: str = ''
    
    @classmethod
    def from_skill_md(cls, filepath: str, source: str = 'workspace') -> Optional['Skill']:
        """
        从 SKILL.md 文件解析技能信息
        
        Args:
            filepath: SKILL.md 文件路径
            source: 技能来源（workspace/builtin/extra）
            
        Returns:
            Skill 实例，解析失败返回 None
        """
        import os
        import re
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 YAML frontmatter
            metadata = cls._parse_frontmatter(content)
            
            # 获取名称和描述
            name = metadata.get('name', os.path.basename(os.path.dirname(filepath)))
            description = metadata.get('description', '')
            
            # 综合名称和描述判断类别
            category = cls._guess_category(f"{name} {description}")
            
            # 检测高风险技能
            is_high_risk = 'voice-call' in name or '1password' in name
            
            return cls(
                name=name,
                description=description,
                version=metadata.get('version', '1.0.0'),
                author=metadata.get('author', ''),
                is_custom=(source == 'workspace'),
                is_high_risk=is_high_risk,
                category=category,
                source=source,
                filepath=filepath
            )
        except FileNotFoundError:
            return None
    
    @staticmethod
    def _parse_frontmatter(content: str) -> Dict[str, str]:
        """
        解析 YAML frontmatter
        
        支持标准 YAML 格式，包括多行字符串
        """
        metadata = {}
        
        if not content.startswith('---'):
            return metadata
            
        parts = content.split('---', 2)
        if len(parts) < 3:
            return metadata
            
        yaml_content = parts[1].strip()
        lines = yaml_content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # 处理多行字符串标记
                if value in ('>', '|'):
                    # 收集缩进的多行内容
                    multiline_value = []
                    i += 1
                    while i < len(lines):
                        next_line = lines[i]
                        # 如果是新的键值对（以非空格开头），停止
                        if next_line and not next_line[0].isspace() and ':' in next_line:
                            break
                        if next_line.strip():
                            multiline_value.append(next_line.strip())
                        i += 1
                    metadata[key] = ' '.join(multiline_value)
                    continue
                elif value:
                    # 单行值
                    metadata[key] = value.strip('"').strip("'")
            
            i += 1
        
        return metadata
    
    @staticmethod
    def _guess_category(description: str) -> str:
        """
        根据描述猜测技能类别
        
        使用中文分类名称，支持更丰富的关键词匹配
        
        Args:
            description: 技能描述文本
            
        Returns:
            分类名称（中文）
        """
        desc_lower = description.lower()
        
        # 按优先级匹配分类
        for category, keywords in SkillCategory.KEYWORDS.items():
            if any(kw in desc_lower for kw in keywords):
                return category
        
        return SkillCategory.其他
    
    def get_category_from_name_and_desc(self, name: str, description: str) -> str:
        """
        根据名称和描述综合判断技能类别
        
        Args:
            name: 技能名称
            description: 技能描述
            
        Returns:
            分类名称（中文）
        """
        combined = f"{name} {description}".lower()
        
        for category, keywords in SkillCategory.KEYWORDS.items():
            if any(kw in combined for kw in keywords):
                return category
        
        return SkillCategory.其他
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'author': self.author,
            'is_custom': self.is_custom,
            'is_high_risk': self.is_high_risk,
            'category': self.category
        }


# =============================================================================
# 配置模型
# =============================================================================

@dataclass
class OpenClawConfig:
    """
    OpenClaw 配置模型
    
    从 openclaw.json 提取的关键配置信息。
    
    Attributes:
        primary_model: 主模型名称
        heartbeat_interval: 心跳间隔（秒）
        sandbox_enabled: 是否启用沙箱
        tools_profile: 工具配置名称
        agent_count: Agent 数量
        channels: 渠道列表
    """
    primary_model: str = 'unknown'
    heartbeat_interval: int = 0
    sandbox_enabled: bool = False
    tools_profile: str = 'default'
    agent_count: int = 1
    channels: List[str] = field(default_factory=list)
    
    @property
    def has_heartbeat(self) -> bool:
        """是否启用心跳检测"""
        return self.heartbeat_interval > 0
    
    @classmethod
    def from_json_file(cls, filepath: str) -> Optional['OpenClawConfig']:
        """
       从 JSON 文件解析配置
        
        Args:
            filepath: openclaw.json 文件路径
            
        Returns:
            OpenClawConfig 实例，解析失败返回 None
        """
        import json
        import re
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 移除注释（支持 JSON5）
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
            config = json.loads(content)
            return cls._extract_from_config(config)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    @classmethod
    def _extract_from_config(cls, config: Dict[str, Any]) -> 'OpenClawConfig':
        """从配置字典提取关键信息"""
        agents_config = config.get('agents', {})
        defaults = agents_config.get('defaults', {})
        
        return cls(
            primary_model=defaults.get('model', {}).get('primary', 'unknown'),
            heartbeat_interval=defaults.get('heartbeat', {}).get('every', 0),
            sandbox_enabled=config.get('sandbox', {}).get('enabled', False),
            tools_profile=config.get('tools', {}).get('profile', 'default'),
            agent_count=len(agents_config.get('instances', [])) or 1,
            channels=list(config.get('channels', {}).keys())
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'primary_model': self.primary_model,
            'heartbeat_interval': self.heartbeat_interval,
            'sandbox_enabled': self.sandbox_enabled,
            'tools_profile': self.tools_profile,
            'agent_count': self.agent_count,
            'channels': self.channels,
            'has_heartbeat': self.has_heartbeat
        }


# =============================================================================
# 评估结果模型
# =============================================================================

@dataclass
class EvaluationResult:
    """
    评估结果模型
    
    完整的 Claw 值评估结果。
    
    Attributes:
        depth_level: 使用深度等级 (1-5)
        usage_depth: 使用深度枚举
        value_estimate: 价值估算
        lobster_skill: 龙虾等级标题
        lobster_rank: 龙虾等级名称
        lobster_message: 趣味化消息
        skill_score: 技能得分
        automation_score: 自动化得分
        integration_score: 集成得分
        total_score: 总分
        achievements: 成就列表
        metrics: 详细指标
    """
    depth_level: int = 1
    usage_depth: str = UsageDepth.SHALLOW.value
    value_estimate: str = '0元'
    lobster_skill: str = ''
    lobster_rank: str = ''
    lobster_message: str = ''
    skill_score: float = 0.0
    automation_score: float = 0.0
    integration_score: float = 0.0
    total_score: float = 0.0
    achievements: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    evaluated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'evaluated_at': self.evaluated_at,
            'depth_level': self.depth_level,
            'usage_depth': self.usage_depth,
            'value_estimate': self.value_estimate,
            'lobster_skill': self.lobster_skill,
            'lobster_rank': self.lobster_rank,
            'lobster_message': self.lobster_message,
            'skill_score': self.skill_score,
            'automation_score': self.automation_score,
            'integration_score': self.integration_score,
            'total_score': self.total_score,
            'achievements': self.achievements,
            'metrics': self.metrics
        }


# =============================================================================
# 采集数据模型
# =============================================================================

@dataclass
class CollectionData:
    """
    数据采集结果模型
    
    整合所有采集的数据源。
    """
    skills: List[Skill] = field(default_factory=list)
    config: Optional[OpenClawConfig] = None
    log_stats: LogStats = field(default_factory=LogStats)
    usage_days: int = 1
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def total_skills(self) -> int:
        """技能总数"""
        return len(self.skills)
    
    @property
    def custom_skills(self) -> int:
        """自定义技能数量"""
        return len([s for s in self.skills if s.is_custom])
    
    @property
    def categories(self) -> Dict[str, int]:
        """技能分类统计"""
        result = {}
        for skill in self.skills:
            result[skill.category] = result.get(skill.category, 0) + 1
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'collected_at': self.collected_at,
            'total_skills': self.total_skills,
            'custom_skills': self.custom_skills,
            'usage_days': self.usage_days,
            'skills': [s.to_dict() for s in self.skills],
            'config': self.config.to_dict() if self.config else None,
            'log_stats': self.log_stats.to_dict(),
            'categories': self.categories
        }