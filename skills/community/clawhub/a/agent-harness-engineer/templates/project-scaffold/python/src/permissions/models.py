#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: permissions.models
# 说明: 权限模型定义
# 修改建议: 如需扩展，添加新的权限规则
# ============================================

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class PermissionMode(Enum):
    """权限模式"""
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


class PermissionLevel(Enum):
    """权限级别"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"


@dataclass
class PermissionRule:
    """权限规则"""
    pattern: str
    action: str  # allow | deny | ask
    level: PermissionLevel = PermissionLevel.READ


class PermissionManager:
    """权限管理器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.mode = PermissionMode(config.get("mode", "ask")) if config else PermissionMode.ASK
        self.rules: List[PermissionRule] = []
        
        if config and "rules" in config:
            for rule in config["rules"]:
                self.rules.append(PermissionRule(
                    pattern=rule["pattern"],
                    action=rule["action"],
                    level=PermissionLevel(rule.get("level", "read"))
                ))
    
    def check_permission(self, tool_name: str, tool_input: Dict[str, Any]) -> bool:
        """
        检查权限
        
        Args:
            tool_name: 工具名称
            tool_input: 工具输入
            
        Returns:
            True if allowed, False if denied
            
        Raises:
            PermissionError: if requires user approval
        """
        import fnmatch
        
        for rule in self.rules:
            if fnmatch.fnmatch(tool_name, rule.pattern):
                if rule.action == "deny":
                    return False
                elif rule.action == "ask":
                    raise PermissionError(f"Permission required for: {tool_name}")
        
        return True
    
    def add_rule(self, pattern: str, action: str, level: str = "read"):
        """添加权限规则"""
        self.rules.append(PermissionRule(
            pattern=pattern,
            action=action,
            level=PermissionLevel(level)
        ))
