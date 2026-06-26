"""
AutoDream Core Adapters

平台适配器导出。
"""

from .base import BaseAdapter
from .openclaw import OpenClawAdapter

__all__ = [
    "BaseAdapter",
    "OpenClawAdapter",
]
