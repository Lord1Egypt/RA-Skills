#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: permissions.hooks
# 说明: Hook系统实现
# 修改建议: 如需扩展，添加新的Hook类型
# ============================================

import os
import sys
from typing import Dict, Any, Callable, List
from pathlib import Path

from ..utils.logging import get_logger

logger = get_logger(__name__)


class HookSystem:
    """Hook系统"""
    
    def __init__(self, hooks_dir: str = "config/hooks"):
        self.hooks_dir = Path(hooks_dir)
        self.pre_hooks: List[Callable] = []
        self.post_hooks: List[Callable] = []
        self._load_hooks()
    
    def _load_hooks(self):
        """加载Hook脚本"""
        if not self.hooks_dir.exists():
            return
        
        for hook_file in self.hooks_dir.glob("*.py"):
            try:
                # 动态导入Hook模块
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    hook_file.stem, hook_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 注册Hook
                if hasattr(module, "pre_tool_use"):
                    self.pre_hooks.append(module.pre_tool_use)
                if hasattr(module, "post_tool_use"):
                    self.post_hooks.append(module.post_tool_use)
                
                logger.info(f"Loaded hook: {hook_file.name}")
            except Exception as e:
                logger.error(f"Failed to load hook {hook_file}: {e}")
    
    def execute_pre_hooks(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """执行前置Hook"""
        for hook in self.pre_hooks:
            try:
                tool_input = hook(tool_name, tool_input)
            except Exception as e:
                logger.error(f"Pre-hook failed: {e}")
        return tool_input
    
    def execute_post_hooks(self, tool_name: str, tool_input: Dict[str, Any], tool_output: str) -> str:
        """执行后置Hook"""
        for hook in self.post_hooks:
            try:
                tool_output = hook(tool_name, tool_input, tool_output)
            except Exception as e:
                logger.error(f"Post-hook failed: {e}")
        return tool_output
