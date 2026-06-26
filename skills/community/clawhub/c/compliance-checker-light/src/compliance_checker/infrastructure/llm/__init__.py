"""
LLM 模块

Infrastructure 层的 LLM 客户端实现，遵循 Core 层的 LLMClientProtocol。
"""

from .client import LLMClient
from .config import LLMConfig
from .semantic_matcher import LLMSemanticMatcher
from .ocr_engine import (
    NoOCREngine,
    PaddleOCREngine,
    AliyunOCREngine,
    create_ocr_engine,
)

__all__ = [
    "LLMClient",
    "LLMConfig",
    "LLMSemanticMatcher",
    "NoOCREngine",
    "PaddleOCREngine",
    "AliyunOCREngine",
    "create_ocr_engine",
]
