"""
Code Quality Guardian
代码质量守护者 - 主模块

一个全面的代码质量分析工具，支持多种编程语言
"""

__version__ = "1.0.0"
__author__ = "ClawHub"

from .analyzer import QualityAnalyzer
from .config import Config
from .models import AnalysisResult, Issue, Severity, Category
from .reports import ConsoleReporter, JsonReporter, HtmlReporter

__all__ = [
    "QualityAnalyzer",
    "Config", 
    "AnalysisResult",
    "Issue",
    "Severity",
    "Category",
    "ConsoleReporter",
    "JsonReporter", 
    "HtmlReporter",
]
