"""策略模块 - 集成传统策略、机器学习策略、优化器、集成引擎"""
from __future__ import annotations

from .strategies import (
    Strategy,
    RawSignal,
    get_all_strategies,
    get_strategy,
    MABreakoutStrategy,
    MACDCrossStrategy,
    BollingerSqueezeStrategy,
    RSIOversoldStrategy,
    KDJCrossStrategy,
    VolumeShrinkStrategy,
    VolumePriceDivergenceStrategy,
    OBVTrendStrategy,
    DoubleMAStrategy,
    SupportBounceStrategy,
)

from .optimizer import (
    StrategyOptimizer,
    WalkForwardOptimizer,
    EnsembleOptimizer,
    ParamSpace,
    OptimizationResult,
)

from .ml_strategies import (
    BaseMLStrategy,
    XGBoostStrategy,
    LightGBMStrategy,
    RandomForestStrategy,
    MLPStrategy,
    EnsembleMLStrategy,
    AdaptiveMLStrategy,
    FeatureEngineer,
    MLSignal,
)

from .ensemble import (
    EnsembleStrategyEngine,
    AdaptiveStrategySelector,
    StrategyCombinationOptimizer,
    MarketRegimeDetector,
    StrategyWeightOptimizer,
    MarketRegime,
    EnsembleSignal,
    StrategySignal,
)

__all__ = [
    "Strategy",
    "RawSignal",
    "get_all_strategies",
    "get_strategy",
    "StrategyOptimizer",
    "WalkForwardOptimizer",
    "EnsembleOptimizer",
    "BaseMLStrategy",
    "XGBoostStrategy",
    "LightGBMStrategy",
    "RandomForestStrategy",
    "MLPStrategy",
    "EnsembleMLStrategy",
    "AdaptiveMLStrategy",
    "EnsembleStrategyEngine",
    "AdaptiveStrategySelector",
    "StrategyCombinationOptimizer",
    "MarketRegimeDetector",
    "MarketRegime",
    "EnsembleSignal",
]
