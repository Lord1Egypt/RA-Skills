"""
适配器模块
提供各种数据源适配器的工厂和实现
"""

from .base import (
    SourceAdapter,
    WebAdapter,
    ApiAdapter,
    FileAdapter,
    DatabaseAdapter,
    AdapterError,
    FetchError
)

__all__ = [
    "SourceAdapter",
    "WebAdapter", 
    "ApiAdapter",
    "FileAdapter",
    "DatabaseAdapter",
    "AdapterError",
    "FetchError",
]