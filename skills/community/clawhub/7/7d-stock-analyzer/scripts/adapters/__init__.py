"""
数据适配器模块
"""

from .efinance_adapter import EfinanceAdapter
from .akshare_adapter import AkshareAdapter
from .qveris_adapter import QverisAdapter

__all__ = [
    'EfinanceAdapter',
    'AkshareAdapter',
    'QverisAdapter'
]
