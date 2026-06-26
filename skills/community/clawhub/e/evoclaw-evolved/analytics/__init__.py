# Evoclaw Analytics Module
# 分析元数据安全

from .metadata_safety import (
    AnalyticsMetadataVerified,
    strip_code_and_paths,
    verify_safe_for_analytics,
    sanitize_for_analytics,
    _CODE_PATTERNS,
    _FILE_PATH_PATTERNS,
)

__all__ = [
    "AnalyticsMetadataVerified",
    "strip_code_and_paths",
    "verify_safe_for_analytics",
    "sanitize_for_analytics",
]
