"""
Configuration module for Code Quality Guardian
配置模块
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import yaml


class Config:
    """配置类"""
    
    # 默认配置
    DEFAULTS = {
        "language": "python",
        "tools": ["flake8", "pylint", "bandit", "radon"],
        "thresholds": {
            "max_complexity": 10,
            "max_line_length": 100,
            "min_quality_score": 8.0,
        },
        "ignore_patterns": [
            "*/tests/*",
            "*/test_*",
            "*/venv/*",
            "*/virtualenv/*",
            "*/__pycache__/*",
            "*/.git/*",
            "*/node_modules/*",
            "*/migrations/*",
        ],
        "fail_on": "high",  # critical, high, medium, low, never
    }
    
    # 支持的语言
    SUPPORTED_LANGUAGES = ["python", "javascript", "typescript", "go"]
    
    # 语言对应的工具
    LANGUAGE_TOOLS = {
        "python": ["flake8", "pylint", "bandit", "radon", "mypy"],
        "javascript": ["eslint", "jshint"],
        "typescript": ["eslint", "tslint"],
        "go": ["go vet", "golint", "staticcheck"],
    }
    
    def __init__(
        self,
        language: str = "python",
        tools: Optional[List[str]] = None,
        thresholds: Optional[Dict[str, Any]] = None,
        ignore_patterns: Optional[List[str]] = None,
        fail_on: str = "high",
        tool_configs: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化配置
        
        Args:
            language: 目标语言
            tools: 要使用的工具列表
            thresholds: 阈值配置
            ignore_patterns: 忽略的文件模式
            fail_on: 遇到何种级别的问题时失败
            tool_configs: 各工具的详细配置
        """
        self.language = language.lower()
        if self.language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"不支持的语言: {language}")
        
        self.tools = tools or self.LANGUAGE_TOOLS.get(self.language, [])
        self.thresholds = {**self.DEFAULTS["thresholds"], **(thresholds or {})}
        self.ignore_patterns = ignore_patterns or self.DEFAULTS["ignore_patterns"]
        self.fail_on = fail_on
        self.tool_configs = tool_configs or {}
    
    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "Config":
        """
        从文件加载配置
        
        Args:
            path: 配置文件路径
            
        Returns:
            Config 实例
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix in [".yml", ".yaml"]:
                data = yaml.safe_load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {path.suffix}")
        
        return cls(
            language=data.get("language", "python"),
            tools=data.get("tools"),
            thresholds=data.get("thresholds"),
            ignore_patterns=data.get("ignore"),
            fail_on=data.get("fail_on", "high"),
            tool_configs={k: v for k, v in data.items() if k not in [
                "language", "tools", "thresholds", "ignore", "fail_on"
            ]},
        )
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        从环境变量加载配置
        
        Returns:
            Config 实例
        """
        config_path = os.getenv("QUALITY_GUARDIAN_CONFIG")
        if config_path and Path(config_path).exists():
            return cls.from_file(config_path)
        
        return cls(
            language=os.getenv("QUALITY_GUARDIAN_LANGUAGE", "python"),
            fail_on=os.getenv("QUALITY_GUARDIAN_FAIL_ON", "high"),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "language": self.language,
            "tools": self.tools,
            "thresholds": self.thresholds,
            "ignore_patterns": self.ignore_patterns,
            "fail_on": self.fail_on,
            "tool_configs": self.tool_configs,
        }
    
    def get_tool_config(self, tool: str) -> Dict[str, Any]:
        """获取特定工具的配置"""
        return self.tool_configs.get(tool, {})
