"""
dnd_engine.context — DM 上下文加载与管理

统一加载 D&D DM 所需的规则、人格、模板等上下文信息，
不依赖任何特定运行时环境。
"""

from .loader import load_context, ContextBundle, list_available_references

__all__ = [
    "load_context",
    "ContextBundle",
    "list_available_references",
]