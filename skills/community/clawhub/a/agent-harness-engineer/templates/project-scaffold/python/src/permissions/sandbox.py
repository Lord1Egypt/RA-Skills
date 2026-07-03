#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: permissions.sandbox
# 说明: 沙箱管理实现
# 修改建议: 如需扩展，继承SandboxManager类
# ============================================

import os
from typing import List, Dict, Any
from pathlib import Path

from ..utils.logging import get_logger

logger = get_logger(__name__)


class SandboxManager:
    """沙箱管理器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.enabled = config.get("enabled", True) if config else True
        self.allowed_directories = config.get("allowed_directories", ["workspace/"]) if config else ["workspace/"]
        self.denied_patterns = config.get("denied_patterns", []) if config else []
    
    def validate_path(self, path: str) -> bool:
        """
        验证路径是否在允许范围内
        
        Args:
            path: 要验证的路径
            
        Returns:
            True if allowed, False if denied
        """
        if not self.enabled:
            return True
        
        # 检查是否在允许的目录内
        path_obj = Path(path).resolve()
        allowed = False
        for allowed_dir in self.allowed_directories:
            allowed_path = Path(allowed_dir).resolve()
            if str(path_obj).startswith(str(allowed_path)):
                allowed = True
                break
        
        if not allowed:
            logger.warning(f"Path outside allowed directories: {path}")
            return False
        
        # 检查是否匹配拒绝模式
        for pattern in self.denied_patterns:
            if pattern in str(path_obj):
                logger.warning(f"Path matches denied pattern: {pattern}")
                return False
        
        return True
    
    def validate_command(self, command: str) -> bool:
        """
        验证命令是否安全
        
        Args:
            command: 要验证的命令
            
        Returns:
            True if allowed, False if denied
        """
        if not self.enabled:
            return True
        
        # 检查危险命令
        dangerous_patterns = ["rm -rf", "sudo", "dd if=", "> /dev", "mkfs"]
        for pattern in dangerous_patterns:
            if pattern in command:
                logger.warning(f"Dangerous command detected: {command}")
                return False
        
        return True
