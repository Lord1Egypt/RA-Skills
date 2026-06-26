# Evoclaw Features Module
# 功能开关系统

from .feature_engine import (
    FeatureEngine,
    FeatureFlag,
    FlagType,
    FeatureCache,
    CacheEntry,
    get_engine,
    feature,
    get_feature_config,
    set_feature,
    get_heartbeat_interval,
    get_dream_trigger_sessions,
    get_memory_max_lines,
)

__all__ = [
    "FeatureEngine",
    "FeatureFlag",
    "FlagType",
    "FeatureCache",
    "CacheEntry",
    "get_engine",
    "feature",
    "get_feature_config",
    "set_feature",
    "get_heartbeat_interval",
    "get_dream_trigger_sessions",
    "get_memory_max_lines",
]
