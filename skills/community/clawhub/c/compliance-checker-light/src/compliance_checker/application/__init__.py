"""
Application 层

提供依赖注入容器和 CLI 命令模块。
"""

from .bootstrap import (
    CheckerConfig,
    Container,
    create_container,
)

__all__ = [
    "CheckerConfig",
    "Container",
    "create_container",
]
