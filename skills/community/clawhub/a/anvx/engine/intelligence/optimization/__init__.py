"""Optimization modules for the recommendation engine."""
from engine.intelligence.optimization.base_module import OptimizationModule
from engine.intelligence.optimization.model_routing import ModelRoutingModule
from engine.intelligence.optimization.caching_estimator import CachingEstimatorModule
from engine.intelligence.optimization.batch_detector import BatchDetectorModule
from engine.intelligence.optimization.unit_economics import UnitEconomicsModule
from engine.intelligence.optimization.price_comparison import PriceComparisonModule
from engine.intelligence.optimization.spend_forecast import SpendForecastModule

ALL_MODULES: list[type[OptimizationModule]] = [
    ModelRoutingModule,
    CachingEstimatorModule,
    BatchDetectorModule,
    UnitEconomicsModule,
    PriceComparisonModule,
    SpendForecastModule,
]

__all__ = [
    "OptimizationModule",
    "ALL_MODULES",
    "ModelRoutingModule",
    "CachingEstimatorModule",
    "BatchDetectorModule",
    "UnitEconomicsModule",
    "PriceComparisonModule",
    "SpendForecastModule",
]
