"""
Cloud Storage Manager - Universal cloud storage management
云存储管理器 - 通用云存储管理

Features:
- Multi-cloud support (AWS S3, Aliyun OSS, Tencent COS, Azure Blob)
- Unified API across all providers
- Sync operations
- Cross-provider copy
"""

__version__ = "1.0.0"
__author__ = "OpenClaw"

from .storage import StorageManager, Provider
from .sync import SyncManager, CrossProviderCopy

__all__ = [
    "StorageManager",
    "Provider",
    "SyncManager",
    "CrossProviderCopy",
]
