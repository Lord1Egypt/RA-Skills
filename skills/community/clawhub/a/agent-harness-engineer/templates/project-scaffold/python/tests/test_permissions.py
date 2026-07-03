#!/usr/bin/env python3
"""
测试权限系统
"""

import pytest

from src.permissions.models import PermissionManager, PermissionMode
from src.permissions.sandbox import SandboxManager


class TestPermissionManager:
    """测试权限管理器"""
    
    def test_allow_mode(self):
        """测试允许模式"""
        manager = PermissionManager({
            "mode": "allow",
            "rules": []
        })
        assert manager.mode == PermissionMode.ALLOW
    
    def test_deny_rule(self):
        """测试拒绝规则"""
        manager = PermissionManager({
            "mode": "ask",
            "rules": [
                {"pattern": "Bash(rm -rf *)", "action": "deny"}
            ]
        })
        
        # 应该被拒绝
        result = manager.check_permission("Bash(rm -rf /)", {})
        assert result == False
    
    def test_ask_rule(self):
        """测试询问规则"""
        manager = PermissionManager({
            "mode": "ask",
            "rules": [
                {"pattern": "Bash(sudo *)", "action": "ask"}
        }
        )
        
        # 应该抛出异常
        with pytest.raises(PermissionError):
            manager.check_permission("Bash(sudo ls)", {})


class TestSandboxManager:
    """测试沙箱管理器"""
    
    def test_validate_path(self):
        """测试路径验证"""
        manager = SandboxManager({
            "enabled": True,
            "allowed_directories": ["workspace/"],
            "denied_patterns": [".env"]
        })
        
        # 允许的路径
        assert manager.validate_path("workspace/test.txt") == True
        
        # 拒绝的路径
        assert manager.validate_path("workspace/.env") == False
    
    def test_validate_command(self):
        """测试命令验证"""
        manager = SandboxManager({
            "enabled": True,
            "allowed_directories": [],
            "denied_patterns": []
        })
        
        # 安全的命令
        assert manager.validate_command("ls -la") == True
        
        # 危险的命令
        assert manager.validate_command("rm -rf /") == False
