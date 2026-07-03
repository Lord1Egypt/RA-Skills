"""
工具注册表模块 (抽象接口)
规模: Professional
预期行数: ~80行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. ToolDefinition dataclass - name, description, parameters (JSON Schema), handler, category
2. ToolCategory enum - READ_ONLY, WRITE, NETWORK, SYSTEM
3. ToolRegistry 类:
   - register(tool: ToolDefinition) - 注册工具
   - get(name: str) -> ToolDefinition - 按名称获取
   - list_by_category(category: ToolCategory) -> List - 按类别列出
   - get_schemas() -> List[Dict] - 获取所有工具的 OpenAI function calling 格式
   - get_read_only() / get_write() - 获取只读/写入工具分组

⚠ 工具分区执行依赖于 get_read_only() 和 get_write() 方法
⚠ 工具参数使用 JSON Schema 格式定义
⚠ 工具执行器由调用方提供, 注册表只管理元数据
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Callable, Optional
from enum import Enum, auto


class ToolCategory(Enum):
    """工具类别"""
    # TODO: READ_ONLY, WRITE, NETWORK, SYSTEM


@dataclass
class ToolDefinition:
    """工具定义"""
    # TODO: name, description, parameters (JSON Schema), handler, category


class ToolRegistry:
    """工具注册表"""

    # TODO: 实现 register(), get(), list_by_category(), get_schemas(), get_read_only(), get_write()
    pass