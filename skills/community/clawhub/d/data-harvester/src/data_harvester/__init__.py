"""
OpenClaw Wealth Guide - 智能数据采集专家
数据采集器核心模块
"""

__version__ = "0.1.0"
__author__ = "dxg <852621787@qq.com>"
__description__ = "智能数据采集专家 - OpenClaw生态赚钱利器"

from .core import DataHarvester
from .config import Config
from .exceptions import DataHarvesterError

__all__ = [
    "DataHarvester",
    "Config", 
    "DataHarvesterError",
    "__version__",
    "__author__",
    "__description__",
]