#!/usr/bin/env python3
"""
Claude Code Enhancement Skill - 权限系统模块
参考 Claude Code 的 useCanUseTool 设计
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import yaml


class PermissionMode(Enum):
    """权限模式"""
    DEFAULT = "default"   # 每次询问
    AUTO = "auto"         # 自动决策
    BYPASS = "bypass"     # 全部放行
    PLAN = "plan"         # 计划模式


@dataclass
class PermissionRule:
    """权限规则"""
    tool: str
    action: str  # allow | deny | ask
    input_pattern: Optional[str] = None
    directory: Optional[str] = None
    command_whitelist: List[str] = field(default_factory=list)


@dataclass
class PermissionResult:
    """权限检查结果"""
    allowed: bool
    reason: str
    requires_confirmation: bool = False


class PermissionSystem:
    """权限系统 - 参考 Claude Code 的 Tool Permission"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.mode = PermissionMode.DEFAULT
        self.rules: List[PermissionRule] = []
        self.trust_patterns = [
            r"GlobTool",
            r"GrepTool", 
            r"FileReadTool",
        ]
        self.danger_patterns = [
            r"BashTool",
            r"FileWriteTool",
            r"FileEditTool",
            r"NetworkTool",
        ]
        
        # 默认规则
        self._init_default_rules()
        
        # 加载自定义规则
        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
    
    def _init_default_rules(self):
        """初始化默认规则"""
        # 信任的工具 - 自动允许
        for tool in ["GlobTool", "GrepTool", "FileReadTool"]:
            self.rules.append(PermissionRule(
                tool=tool,
                action="allow"
            ))
        
        # 危险工具 - 始终询问
        for tool in ["BashTool", "FileWriteTool", "FileEditTool"]:
            self.rules.append(PermissionRule(
                tool=tool,
                action="ask"
            ))
    
    def _load_config(self, config_path: str):
        """加载配置文件"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # 加载规则
            for rule in config.get('rules', []):
                self.rules.append(PermissionRule(
                    tool=rule.get('tool', ''),
                    action=rule.get('action', 'ask'),
                    input_pattern=rule.get('input_pattern'),
                    directory=rule.get('directory'),
                    command_whitelist=rule.get('command_whitelist', [])
                ))
        except Exception as e:
            print(f"加载配置失败: {e}")
    
    def set_mode(self, mode: str):
        """设置权限模式"""
        try:
            self.mode = PermissionMode(mode)
        except ValueError:
            self.mode = PermissionMode.DEFAULT
    
    def check(self, tool_name: str, input_data: str = "", 
              directory: str = "") -> PermissionResult:
        """检查工具权限"""
        # 绕过模式
        if self.mode == PermissionMode.BYPASS:
            return PermissionResult(
                allowed=True,
                reason="bypass 模式",
                requires_confirmation=False
            )
        
        # 计划模式
        if self.mode == PermissionMode.PLAN:
            return PermissionResult(
                allowed=True,
                reason="plan 模式，仅计划不执行",
                requires_confirmation=False
            )
        
        # 查找匹配的规则
        for rule in self.rules:
            if self._match_tool(rule.tool, tool_name):
                if rule.action == "allow":
                    return PermissionResult(
                        allowed=True,
                        reason=f"规则允许: {rule.tool}",
                        requires_confirmation=False
                    )
                elif rule.action == "deny":
                    return PermissionResult(
                        allowed=False,
                        reason=f"规则拒绝: {rule.tool}",
                        requires_confirmation=False
                    )
                else:  # ask
                    return PermissionResult(
                        allowed=False,
                        reason="需要用户确认",
                        requires_confirmation=True
                    )
        
        # 默认规则：检查工具名称模式
        tool_class = tool_name.split("Tool")[0] if "Tool" in tool_name else tool_name
        
        # 信任的工具
        for pattern in self.trust_patterns:
            if re.search(pattern, tool_name, re.IGNORECASE):
                return PermissionResult(
                    allowed=True,
                    reason="信任的工具",
                    requires_confirmation=False
                )
        
        # 危险工具
        for pattern in self.danger_patterns:
            if re.search(pattern, tool_name, re.IGNORECASE):
                return PermissionResult(
                    allowed=False,
                    reason="危险工具，需要确认",
                    requires_confirmation=True
                )
        
        # 默认允许
        return PermissionResult(
            allowed=True,
            reason="默认允许",
            requires_confirmation=False
        )
    
    def _match_tool(self, pattern: str, tool_name: str) -> bool:
        """匹配工具名称"""
        if "*" in pattern:
            regex = pattern.replace("*", ".*")
            return bool(re.match(regex, tool_name))
        return pattern == tool_name
    
    def add_rule(self, tool: str, action: str):
        """添加规则"""
        self.rules.append(PermissionRule(tool=tool, action=action))
    
    def get_status(self) -> str:
        """获取权限状态"""
        lines = [
            f"🔐 权限模式: **{self.mode.value}**",
            "",
            "📋 当前规则:",
        ]
        
        allow_rules = [r for r in self.rules if r.action == "allow"]
        ask_rules = [r for r in self.rules if r.action == "ask"]
        deny_rules = [r for r in self.rules if r.action == "deny"]
        
        if allow_rules:
            lines.append(f"  ✅ 允许: {', '.join(r.tool for r in allow_rules)}")
        if ask_rules:
            lines.append(f"  ⚠️ 询问: {', '.join(r.tool for r in ask_rules)}")
        if deny_rules:
            lines.append(f"  ❌ 拒绝: {', '.join(r.tool for r in deny_rules)}")
        
        return "\n".join(lines)


# 全局权限系统实例
_permission_system: Optional[PermissionSystem] = None


def get_permission_system() -> PermissionSystem:
    """获取全局权限系统实例"""
    global _permission_system
    if _permission_system is None:
        _permission_system = PermissionSystem()
    return _permission_system


# CLI 接口
if __name__ == "__main__":
    ps = get_permission_system()
    
    import sys
    
    if len(sys.argv) < 2:
        print("用法: permission.py <命令> [参数]")
        print("命令: status | mode <模式> | check <工具名>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        print(ps.get_status())
    elif cmd == "mode" and len(sys.argv) > 2:
        ps.set_mode(sys.argv[2])
        print(f"✅ 权限模式已设置为: {sys.argv[2]}")
    elif cmd == "check" and len(sys.argv) > 2:
        result = ps.check(sys.argv[2])
        print(f"工具: {sys.argv[2]}")
        print(f"允许: {result.allowed}")
        print(f"原因: {result.reason}")
        print(f"需确认: {result.requires_confirmation}")