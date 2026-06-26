#!/usr/bin/env python3
"""
FocusMind 集成模块
提供统一的 Python API 供其他 Agent 调用
"""

import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field

# 添加当前目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 导入核心功能
from scripts.check_context import (
    analyze_context_health,
    format_health_report,
    HealthChecker
)
from scripts.summarize import (
    generate_summary,
    format_summary_markdown
)
from scripts.extract_goals import (
    extract_goals,
    format_goals_markdown
)
from scripts.auto_trigger import (
    AutoTrigger,
    TriggerConfig,
    on_heartbeat
)


@dataclass
class FocusMindConfig:
    """FocusMind 配置"""
    threshold_tokens: int = 10000
    summary_style: str = "structured"
    auto_cleanup: bool = False
    preserve_recent: int = 5
    compress_ratio: float = 0.3


class FocusMind:
    """
    FocusMind 核心类
    
    用法:
        fm = FocusMind()
        result = fm.analyze(context)
        if result.need_cleanup:
            summary = fm.summarize(context)
            goals = fm.extract_goals(context)
    """
    
    def __init__(self, config: Optional[FocusMindConfig] = None):
        self.config = config or FocusMindConfig()
    
    def analyze(self, context: Any) -> Dict[str, Any]:
        """分析上下文健康度"""
        return analyze_context_health(context, threshold=self.config.threshold_tokens)
    
    def need_cleanup(self, context: Any) -> bool:
        """判断是否需要清理"""
        health = self.analyze(context)
        return health["level"] in ["yellow", "red"]
    
    def summarize(self, context: Any) -> Dict[str, Any]:
        """生成上下文摘要"""
        return generate_summary(context, style=self.config.summary_style)
    
    def extract_goals(self, context: Any) -> Dict[str, Any]:
        """提取核心目标"""
        return extract_goals(context)
    
    def full_analysis(self, context: Any) -> Dict[str, Any]:
        """完整分析: 健康度 + 摘要 + 目标"""
        health = self.analyze(context)
        summary = self.summarize(context)
        goals = self.extract_goals(context)
        
        return {
            "health": health,
            "summary": summary,
            "goals": goals,
            "need_cleanup": self.need_cleanup(context),
            "recommendations": health.get("recommendations", [])
        }
    
    def format_report(self, context: Any, output_format: str = "markdown") -> str:
        """格式化报告"""
        if output_format == "json":
            result = self.full_analysis(context)
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        health = self.analyze(context)
        summary = self.summarize(context)
        goals = self.extract_goals(context)
        
        return f"""
{'='*50}
🧠 FocusMind 完整分析报告
{'='*50}

{format_health_report(health)}

{'-'*50}

{format_summary_markdown(summary)}

{'-'*50}

{format_goals_markdown(goals)}
"""


# 便捷函数
def need_cleanup(context: Any, threshold: int = 10000) -> bool:
    """快速判断是否需要清理"""
    health = analyze_context_health(context, threshold=threshold)
    return health["level"] in ["yellow", "red"]


# 导出
__all__ = [
    "FocusMind",
    "FocusMindConfig",
    "HealthChecker",
    "AutoTrigger",
    "TriggerConfig",
    "analyze_context_health",
    "generate_summary",
    "extract_goals",
    "need_cleanup",
    "on_heartbeat",
    "format_health_report",
    "format_summary_markdown",
    "format_goals_markdown",
]
