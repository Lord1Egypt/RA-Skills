"""因子模块 - 基础因子 + 增强IC分析"""
from __future__ import annotations

from .base import (
    Factor,
    FactorResult,
    FactorValue,
    FactorCombiner,
    register_factor,
    get_all_factors,
    get_factors_by_category,
    get_factor,
)

from .enhanced_ic import (
    EnhancedFactorAnalyzer,
    MultiFactorICAnalyzer,
    FactorPerformanceTracker,
    FactorICResult,
    FactorDecayResult,
)

__all__ = [
    "Factor",
    "FactorResult",
    "FactorValue",
    "FactorCombiner",
    "register_factor",
    "get_all_factors",
    "get_factors_by_category",
    "get_factor",
    "EnhancedFactorAnalyzer",
    "MultiFactorICAnalyzer",
    "FactorPerformanceTracker",
    "FactorICResult",
    "FactorDecayResult",
]
