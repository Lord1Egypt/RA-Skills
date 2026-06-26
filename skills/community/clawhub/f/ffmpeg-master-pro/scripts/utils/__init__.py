"""
FFmpeg Master - 工具模块
包含预设管理器、批量报告生成器和文件工具
"""

from .batch_reporter import BatchReportGenerator, ProcessResult, BatchStatistics
from .preset_manager import PresetManager

__all__ = [
    "BatchReportGenerator",
    "ProcessResult",
    "BatchStatistics",
    "PresetManager",
]
