#!/usr/bin/env python3
"""
ClawValue 数据采集模块

负责从 OpenClaw 系统采集各类数据：
- 日志解析：解析 /tmp/openclaw/ 目录下的 JSONL 日志
- 技能扫描：扫描 ~/.openclaw/workspace/skills/ 目录
- 配置分析：解析 ~/.openclaw/openclaw.json 配置文件

设计原则：
- 使用常量定义字段名，避免硬编码字符串
- 结构化数据模型，提供类型安全
- 模块化设计，每个采集器独立可测试
- 详细注释，便于维护

参考文档: docs/OPENCLAW_REFERENCE.md
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any

# 使用条件导入支持包内和直接运行
try:
    from .constants import (
        LOG_DIR, OPENCLAW_HOME, OPENCLAW_CONFIG_FILE,
        SKILLS_DIR, SKILL_FILE,
        LogField, LogLevel, LogType,
        SkillCategory
    )
    from .schemas import (
        LogEntry, LogStats, Skill, OpenClawConfig,
        CollectionData
    )
except ImportError:
    from constants import (
        LOG_DIR, OPENCLAW_HOME, OPENCLAW_CONFIG_FILE,
        SKILLS_DIR, SKILL_FILE,
        LogField, LogLevel, LogType,
        SkillCategory
    )
    from schemas import (
        LogEntry, LogStats, Skill, OpenClawConfig,
        CollectionData
    )


# =============================================================================
# 日志解析器
# =============================================================================

class LogParser:
    """
    OpenClaw 日志解析器
    
    负责解析 /tmp/openclaw/ 目录下的 JSONL 日志文件。
    
    日志格式参考：
    - 文件位置: /tmp/openclaw/openclaw-YYYY-MM-DD.log
    - 格式: 每行一个 JSON 对象
    - 文档: https://docs.openclaw.ai/zh-CN/logging
    
    Example:
        >>> parser = LogParser()
        >>> logs = parser.get_all_logs()
        >>> stats = parser.extract_stats(logs)
        >>> print(f"Total logs: {stats.total_entries}")
    """
    
    def __init__(self, log_dir: str = None):
        """
        初始化日志解析器
        
        Args:
            log_dir: 日志目录路径，默认使用官方定义的 /tmp/openclaw
        """
        self.log_dir = log_dir or LOG_DIR
    
    def parse_jsonl_file(self, filepath: str) -> List[LogEntry]:
        """
        解析单个 JSONL 日志文件
        
        Args:
            filepath: 日志文件路径
            
        Returns:
            LogEntry 列表
        """
        entries = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        entry = LogEntry.from_openclaw_json(data)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        # 跳过无法解析的行
                        continue
        except FileNotFoundError:
            pass
        
        return entries
    
    def get_all_logs(self) -> List[LogEntry]:
        """
        获取所有日志条目
        
        扫描日志目录下所有匹配 openclaw-*.log 的文件并解析。
        
        Returns:
            所有日志条目的列表
        """
        all_entries = []
        
        if not os.path.exists(self.log_dir):
            return all_entries
        
        for filename in os.listdir(self.log_dir):
            # 只处理 OpenClaw 日志文件
            if filename.startswith('openclaw-') and filename.endswith('.log'):
                filepath = os.path.join(self.log_dir, filename)
                entries = self.parse_jsonl_file(filepath)
                all_entries.extend(entries)
        
        return all_entries
    
    def extract_stats(self, entries: List[LogEntry]) -> LogStats:
        """
        从日志条目中提取统计信息
        
        Args:
            entries: 日志条目列表
            
        Returns:
            LogStats 统计对象
        """
        stats = LogStats()
        
        for entry in entries:
            stats.add_entry(entry)
        
        return stats
    
    def get_entries_by_type(self, entries: List[LogEntry], log_type: str) -> List[LogEntry]:
        """
        按类型过滤日志条目
        
        Args:
            entries: 日志条目列表
            log_type: 日志类型 (LogType 常量)
            
        Returns:
            过滤后的日志条目列表
        """
        return [e for e in entries if e.log_type == log_type]
    
    def get_entries_by_level(self, entries: List[LogEntry], level: str) -> List[LogEntry]:
        """
        按级别过滤日志条目
        
        Args:
            entries: 日志条目列表
            level: 日志级别 (LogLevel 常量)
            
        Returns:
            过滤后的日志条目列表
        """
        return [e for e in entries if e.level == level]


# =============================================================================
# 技能扫描器
# =============================================================================

class SkillScanner:
    """
    OpenClaw 技能扫描器
    
    负责扫描所有 workspace 目录下的技能，支持多 agent 配置。
    
    技能来源分类：
    - Workspace Skills（自定义）- 来自各 agent workspace/skills 目录
    - Built-in Skills（内置）- 来自 OpenClaw bundled
    - Extra Skills（扩展）- 来自插件如 qqbot
    
    Example:
        >>> scanner = SkillScanner()
        >>> skills = scanner.scan_all()
        >>> for skill in skills:
        ...     print(f"{skill.name}: {skill.description}")
    """
    
    def __init__(self, workspace: str = None):
        """
        初始化技能扫描器
        
        Args:
            workspace: 默认工作区路径，默认为 ~/.openclaw/workspace
        """
        if workspace is None:
            workspace = str(Path.home() / '.openclaw' / 'workspace')
        self.default_workspace = workspace
        self.openclaw_home = str(Path.home() / '.openclaw')
        self.config_file = os.path.join(self.openclaw_home, 'openclaw.json')
    
    def get_agent_workspaces(self) -> List[Dict[str, str]]:
        """
        从 openclaw.json 获取所有 agent 的 workspace 配置
        
        Returns:
            agent 配置列表，每个元素包含 id 和 workspace
        """
        agents = []
        
        # 添加默认 workspace
        agents.append({
            'id': 'default',
            'workspace': self.default_workspace
        })
        
        try:
            import re
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 移除注释（支持 JSON5）
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
            config = json.loads(content)
            
            # 解析 agents.list
            agents_list = config.get('agents', {}).get('list', [])
            for agent in agents_list:
                agent_id = agent.get('id', '')
                agent_workspace = agent.get('workspace', '')
                if agent_workspace and agent_workspace != self.default_workspace:
                    agents.append({
                        'id': agent_id,
                        'workspace': agent_workspace
                    })
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        return agents
    
    def scan_workspace_skills(self, workspace: str, source: str = 'workspace') -> List[Skill]:
        """
        扫描指定 workspace 的技能
        
        Args:
            workspace: 工作区路径
            source: 技能来源
            
        Returns:
            Skill 对象列表
        """
        skills = []
        skills_dir = os.path.join(workspace, SKILLS_DIR)
        
        if not os.path.exists(skills_dir):
            return skills
        
        for skill_name in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, skill_name)
            
            # 只处理目录
            if not os.path.isdir(skill_path):
                continue
            
            # 查找 SKILL.md 文件
            skill_md = os.path.join(skill_path, SKILL_FILE)
            if os.path.exists(skill_md):
                skill = Skill.from_skill_md(skill_md, source=source)
                if skill:
                    skills.append(skill)
        
        return skills
    
    def scan_extra_skills(self) -> List[Skill]:
        """
        扫描扩展技能（来自插件）
        
        检查 OpenClaw extensions 目录
        
        Returns:
            扩展技能列表
        """
        extra_skills = []
        extensions_dir = os.path.join(self.openclaw_home, 'extensions')
        
        if not os.path.exists(extensions_dir):
            return extra_skills
        
        # 扫描各插件的 skills 目录
        for plugin_name in os.listdir(extensions_dir):
            plugin_path = os.path.join(extensions_dir, plugin_name)
            if not os.path.isdir(plugin_path):
                continue
            
            # 检查插件的 skills 目录
            plugin_skills_dir = os.path.join(plugin_path, 'skills')
            if os.path.exists(plugin_skills_dir):
                for skill_name in os.listdir(plugin_skills_dir):
                    skill_path = os.path.join(plugin_skills_dir, skill_name)
                    if os.path.isdir(skill_path):
                        skill_md = os.path.join(skill_path, SKILL_FILE)
                        if os.path.exists(skill_md):
                            skill = Skill.from_skill_md(skill_md, source='extra')
                            if skill:
                                extra_skills.append(skill)
        
        return extra_skills
    
    def scan_all(self) -> List[Skill]:
        """
        扫描所有技能
        
        合并所有来源：各 agent workspace + 扩展技能
        
        Returns:
            Skill 对象列表
        """
        all_skills = []
        seen_names = set()
        
        # 1. 扫描所有 agent 的 workspace
        agents = self.get_agent_workspaces()
        for agent in agents:
            workspace = agent['workspace']
            agent_skills = self.scan_workspace_skills(workspace, source='workspace')
            for skill in agent_skills:
                if skill.name not in seen_names:
                    seen_names.add(skill.name)
                    all_skills.append(skill)
        
        # 2. 扫描扩展技能
        extra_skills = self.scan_extra_skills()
        for skill in extra_skills:
            if skill.name not in seen_names:
                seen_names.add(skill.name)
                all_skills.append(skill)
        
        return all_skills
    
    def get_skills_by_source(self, skills: List[Skill], source: str) -> List[Skill]:
        """
        按来源过滤技能
        
        Args:
            skills: 技能列表
            source: 来源（workspace/builtin/extra）
            
        Returns:
            过滤后的技能列表
        """
        return [s for s in skills if s.source == source]
    
    def get_by_category(self, skills: List[Skill], category: str) -> List[Skill]:
        """
        按类别过滤技能
        
        Args:
            skills: 技能列表
            category: 类别
            
        Returns:
            过滤后的技能列表
        """
        return [s for s in skills if s.category == category]
    
    def get_custom_skills(self, skills: List[Skill]) -> List[Skill]:
        """
        获取所有自定义技能
        
        Args:
            skills: 技能列表
            
        Returns:
            自定义技能列表
        """
        return [s for s in skills if s.is_custom]


# =============================================================================
# 配置分析器
# =============================================================================

class ConfigAnalyzer:
    """
    OpenClaw 配置分析器
    
    负责解析 ~/.openclaw/openclaw.json 配置文件。
    
    配置结构参考：
    - 文件位置: ~/.openclaw/openclaw.json
    - 格式: JSON5 (支持注释)
    - 文档: https://docs.openclaw.ai/zh-CN/gateway/configuration
    
    Example:
        >>> analyzer = ConfigAnalyzer()
        >>> config = analyzer.parse()
        >>> if config:
        ...     print(f"Primary model: {config.primary_model}")
    """
    
    def __init__(self, openclaw_home: str = None):
        """
        初始化配置分析器
        
        Args:
            openclaw_home: OpenClaw 主目录，默认为 ~/.openclaw
        """
        if openclaw_home is None:
            openclaw_home = str(Path.home() / '.openclaw')
        self.openclaw_home = openclaw_home
        self.config_file = os.path.join(openclaw_home, OPENCLAW_CONFIG_FILE)
    
    def parse(self) -> Optional[OpenClawConfig]:
        """
        解析配置文件
        
        Returns:
            OpenClawConfig 对象，解析失败返回 None
        """
        return OpenClawConfig.from_json_file(self.config_file)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            模型信息字典
        """
        config = self.parse()
        if not config:
            return {}
        
        return {
            'primary_model': config.primary_model,
            'agent_count': config.agent_count
        }
    
    def get_channels(self) -> List[str]:
        """
        获取配置的渠道列表
        
        Returns:
            渠道名称列表
        """
        config = self.parse()
        if not config:
            return []
        
        return config.channels


# =============================================================================
# 数据采集器（整合模块）
# =============================================================================

class DataCollector:
    """
    数据采集器 - 整合所有数据源
    
    协调日志解析、技能扫描和配置分析，提供统一的数据采集接口。
    
    Example:
        >>> collector = DataCollector()
        >>> data = collector.collect()
        >>> print(f"Skills: {data.total_skills}")
        >>> print(f"Log entries: {data.log_stats.total_entries}")
    """
    
    def __init__(self, openclaw_home: str = None, workspace: str = None):
        """
        初始化数据采集器
        
        Args:
            openclaw_home: OpenClaw 主目录
            workspace: 工作区路径
        """
        self.log_parser = LogParser()
        self.skill_scanner = SkillScanner(workspace)
        self.config_analyzer = ConfigAnalyzer(openclaw_home)
    
    def collect(self) -> CollectionData:
        """
        执行完整的数据采集
        
        Returns:
            CollectionData 采集结果
        """
        # 1. 解析日志
        log_entries = self.log_parser.get_all_logs()
        log_stats = self.log_parser.extract_stats(log_entries)
        
        # 2. 扫描技能
        skills = self.skill_scanner.scan_all()
        
        # 3. 解析配置
        config = self.config_analyzer.parse()
        
        # 4. 计算使用天数（基于最早的日志日期）
        usage_days = self._estimate_usage_days(log_entries)
        
        return CollectionData(
            skills=skills,
            config=config,
            log_stats=log_stats,
            usage_days=usage_days
        )
    
    def _estimate_usage_days(self, entries: List[LogEntry]) -> int:
        """
        估算使用天数
        
        基于日志时间戳范围计算。
        
        Args:
            entries: 日志条目列表
            
        Returns:
            使用天数
        """
        if not entries:
            return 1
        
        # 收集所有日期
        dates = set()
        for entry in entries:
            if entry.timestamp:
                # 提取日期部分 (YYYY-MM-DD)
                try:
                    date_part = entry.timestamp[:10]
                    dates.add(date_part)
                except Exception:
                    pass
        
        return max(len(dates), 1)
    
    def collect_summary(self) -> Dict[str, Any]:
        """
        获取采集摘要（用于快速展示）
        
        Returns:
            摘要信息字典
        """
        data = self.collect()
        
        return {
            'total_skills': data.total_skills,
            'custom_skills': data.custom_skills,
            'log_entries': data.log_stats.total_entries,
            'tool_calls': data.log_stats.tool_calls,
            'errors': data.log_stats.error_count,
            'primary_model': data.config.primary_model if data.config else 'unknown',
            'channels': len(data.config.channels) if data.config else 0,
            'usage_days': data.usage_days
        }


# =============================================================================
# 命令行入口
# =============================================================================

if __name__ == '__main__':
    """命令行测试入口"""
    
    print("=" * 60)
    print("🦞 ClawValue 数据采集测试")
    print("=" * 60)
    
    collector = DataCollector()
    
    # 采集数据
    print("\n📊 正在采集数据...")
    data = collector.collect()
    
    # 输出结果
    print(f"\n✅ 采集完成!")
    print(f"\n📁 技能统计:")
    print(f"   - 总数: {data.total_skills}")
    print(f"   - 自定义: {data.custom_skills}")
    
    print(f"\n📝 日志统计:")
    print(f"   - 总条目: {data.log_stats.total_entries}")
    print(f"   - INFO: {data.log_stats.info_count}")
    print(f"   - WARN: {data.log_stats.warn_count}")
    print(f"   - ERROR: {data.log_stats.error_count}")
    print(f"   - 工具调用: {data.log_stats.tool_calls}")
    
    if data.config:
        print(f"\n⚙️ 配置信息:")
        print(f"   - 主模型: {data.config.primary_model}")
        print(f"   - Agent 数量: {data.config.agent_count}")
        print(f"   - 渠道: {', '.join(data.config.channels) or '无'}")
        print(f"   - 心跳检测: {'已开启' if data.config.has_heartbeat else '未开启'}")
    
    print(f"\n📅 使用天数: {data.usage_days}")
    
    # 输出技能列表
    if data.skills:
        print(f"\n📋 技能列表:")
        for skill in data.skills[:10]:
            print(f"   - [{skill.category}] {skill.name}: {skill.description[:40]}...")