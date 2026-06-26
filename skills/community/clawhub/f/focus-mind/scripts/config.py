#!/usr/bin/env python3
"""
FocusMind 配置管理
支持从文件加载配置
"""

import json
import os
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict


DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


@dataclass
class FocusMindSettings:
    """FocusMind 设置"""
    threshold_tokens: int = 10000
    summary_style: str = "structured"
    auto_cleanup: bool = False
    preserve_recent: int = 5
    compress_ratio: float = 0.3


@dataclass
class AutoTriggerSettings:
    """自动触发设置"""
    enabled: bool = False
    threshold_tokens: int = 10000
    check_interval_seconds: int = 1800
    min_score_to_trigger: int = 70
    auto_summarize: bool = True
    notify_only: bool = False


@dataclass
class CacheSettings:
    """缓存设置"""
    enabled: bool = True
    default_ttl: int = 300
    max_size: int = 100


@dataclass
class NotificationSettings:
    """通知设置"""
    enabled: bool = False
    notification_type: str = "console"  # console, webhook, file
    webhook_url: str = ""


@dataclass
class OutputSettings:
    """输出设置"""
    default_format: str = "markdown"  # markdown, json
    show_stats: bool = True
    show_recommendations: bool = True


@dataclass
class Config:
    """完整配置"""
    version: str = "1.0.0"
    focus_mind: FocusMindSettings = field(default_factory=FocusMindSettings)
    auto_trigger: AutoTriggerSettings = field(default_factory=AutoTriggerSettings)
    cache: CacheSettings = field(default_factory=CacheSettings)
    notification: NotificationSettings = field(default_factory=NotificationSettings)
    output: OutputSettings = field(default_factory=OutputSettings)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Config":
        """从字典创建"""
        return cls(
            version=data.get("focus-mind", {}).get("version", "1.0.0"),
            focus_mind=FocusMindSettings(**data.get("focus-mind", {}).get("config", {})),
            auto_trigger=AutoTriggerSettings(**data.get("focus-mind", {}).get("auto_trigger", {})),
            cache=CacheSettings(**data.get("focus-mind", {}).get("cache", {})),
            notification=NotificationSettings(**data.get("focus-mind", {}).get("notification", {})),
            output=OutputSettings(**data.get("focus-mind", {}).get("output", {}))
        )
    
    @classmethod
    def from_file(cls, filepath: str = DEFAULT_CONFIG_PATH) -> "Config":
        """从文件加载"""
        if not os.path.exists(filepath):
            return cls()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except Exception as e:
            print(f"⚠️ 配置加载失败: {e}, 使用默认配置")
            return cls()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "focus-mind": {
                "version": self.version,
                "config": asdict(self.focus_mind),
                "auto_trigger": asdict(self.auto_trigger),
                "cache": asdict(self.cache),
                "notification": asdict(self.notification),
                "output": asdict(self.output)
            }
        }
    
    def save(self, filepath: str = DEFAULT_CONFIG_PATH):
        """保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


def load_config(filepath: Optional[str] = None) -> Config:
    """加载配置"""
    return Config.from_file(filepath or DEFAULT_CONFIG_PATH)


# 便捷函数
def get_settings() -> FocusMindSettings:
    """获取 FocusMind 设置"""
    return load_config().focus_mind


def get_auto_trigger_settings() -> AutoTriggerSettings:
    """获取自动触发设置"""
    return load_config().auto_trigger


# 导出
__all__ = [
    "Config",
    "FocusMindSettings",
    "AutoTriggerSettings",
    "CacheSettings",
    "NotificationSettings",
    "OutputSettings",
    "load_config",
    "get_settings",
    "get_auto_trigger_settings"
]
