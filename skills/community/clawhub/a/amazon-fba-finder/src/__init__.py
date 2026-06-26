"""
Amazon FBA Finder - 高利润产品发现引擎
"""

from .main import AmazonFBAFinder
from .product_finder import ProductFinder, ProductOpportunity
from .competition_analyzer import CompetitionAnalyzer, MarketAnalysis, CompetitionLevel
from .supplier_recommender import SupplierRecommender, SupplierRecommendation
from .profit_calculator import ProfitCalculator, ProductDimensions, ProfitAnalysis

__version__ = "1.0.0"
__author__ = "小龙"
__all__ = [
    "AmazonFBAFinder",
    "ProductFinder",
    "ProductOpportunity",
    "CompetitionAnalyzer",
    "MarketAnalysis",
    "CompetitionLevel",
    "SupplierRecommender",
    "SupplierRecommendation",
    "ProfitCalculator",
    "ProductDimensions",
    "ProfitAnalysis"
]
