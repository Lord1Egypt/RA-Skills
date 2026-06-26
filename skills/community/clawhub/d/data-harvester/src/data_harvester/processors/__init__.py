"""
处理器模块
提供数据处理器的工厂和管道实现
"""

from .base import (
    DataProcessor,
    ProcessingResult,
    CleanProcessor,
    TransformProcessor
)
from .factory import ProcessorFactory
from .pipeline import ProcessorPipeline, PipelineResult

__all__ = [
    "DataProcessor",
    "ProcessingResult",
    "CleanProcessor", 
    "TransformProcessor",
    "ProcessorFactory",
    "ProcessorPipeline",
    "PipelineResult",
]