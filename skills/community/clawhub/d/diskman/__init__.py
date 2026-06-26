"""
Diskman - AI-ready disk space analysis and management.

A modular tool for analyzing and managing disk space, designed for
both direct use and AI agent integration via MCP.
"""

from .ai import AIConfig, AIService
from .analysis import DirectoryAnalyzer
from .models import (
    AnalysisContext,
    AnalysisResult,
    CleanResult,
    DirectoryInfo,
    DirectoryType,
    LinkType,
    MigrationResult,
    RecommendedAction,
    RiskLevel,
    ScanResult,
)
from .operations import DirectoryCleaner, DirectoryMigrator, DirectoryScanner

__version__ = "0.3.0"

__all__ = [
    # Models
    "DirectoryInfo",
    "AnalysisResult",
    "ScanResult",
    "MigrationResult",
    "CleanResult",
    "LinkType",
    "RiskLevel",
    "DirectoryType",
    "RecommendedAction",
    "AnalysisContext",
    # Operations
    "DirectoryScanner",
    "DirectoryMigrator",
    "DirectoryCleaner",
    # Analysis
    "DirectoryAnalyzer",
    # AI
    "AIService",
    "AIConfig",
]
