"""
Article Taster - 文章品鉴师
帮助用户提前品尝文章可读性，过滤低质量内容
"""

__version__ = "1.0.0"
__author__ = "Article Taster Team"

from .article_classifier import ArticleClassifier
from .tech_analyzer import TechAnalyzer
from .creative_analyzer import CreativeAnalyzer
from .novel_analyzer import NovelAnalyzer
from .ai_detector import AIDetector
from .scorer import QualityScorer
from .report_generator import ReportGenerator

__all__ = [
    "ArticleClassifier",
    "TechAnalyzer",
    "CreativeAnalyzer",
    "NovelAnalyzer",
    "AIDetector",
    "QualityScorer",
    "ReportGenerator",
]
