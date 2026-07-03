#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: tools.registry
# 说明: 工具注册表，管理所有可用工具
# 修改建议: 如需添加新工具，调用register方法
# ============================================

import json
from typing import Dict, List, Any, Callable
from dataclasses import dataclass

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ToolDefinition:
    """工具定义"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable
    is_concurrency_safe: bool = False


class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
    
    def register(self, name: str, description: str, input_schema: Dict[str, Any], 
                 handler: Callable, is_concurrency_safe: bool = False):
        """
        注册工具
        
        Args:
            name: 工具名称
            description: 工具描述
            input_schema: 输入参数Schema
            handler: 处理函数
            is_concurrency_safe: 是否支持并发执行
        """
        self._tools[name] = ToolDefinition(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler,
            is_concurrency_safe=is_concurrency_safe
        )
        logger.info(f"Registered tool: {name}")
    
    def get_definitions(self) -> List[Dict[str, Any]]:
        """获取所有工具定义（用于LLM）"""
        return [
            {
                "type": "custom",
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self._tools.values()
        ]
    
    def execute(self, name: str, input_data: Dict[str, Any]) -> Any:
        """
        执行工具
        
        Args:
            name: 工具名称
            input_data: 输入参数
            
        Returns:
            工具执行结果
            
        Raises:
            ValueError: 如果工具不存在
        """
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        
        tool = self._tools[name]
        logger.info(f"Executing tool: {name}")
        
        try:
            result = tool.handler(input_data)
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {name} - {e}")
            raise
    
    def list_tools(self) -> List[str]:
        """列出所有工具名称"""
        return list(self._tools.keys())
    
    def get_tool_info(self, name: str) -> Dict[str, Any]:
        """获取工具信息"""
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        
        tool = self._tools[name]
        return {
            "name": tool.name,
            "description": tool.description,
            "is_concurrency_safe": tool.is_concurrency_safe
        }
