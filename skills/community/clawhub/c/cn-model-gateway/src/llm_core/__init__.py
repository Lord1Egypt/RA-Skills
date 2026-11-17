"""LLM Core - Shared kernel for cn-model-gateway and cn-llm-router.

This module provides the unified core for both MCP and CLI forms.
Version-locked during build injection.
"""
__version__ = "1.6.0"
__kernel_version__ = "1.6.0"

from .types import (
    ChatMessage, ChatResponse, ContentChunk, ToolCall,
    EmbeddingResult, RerankResult, TranscriptionResult,
    VideoUnderstandingResult, now_ms,
)
from .error_map import (
    ERROR_PARAM_INVALID, ERROR_MODEL_UNAVAILABLE,
    ERROR_RATE_LIMITED, ERROR_INTERNAL, ERROR_PROVIDER_NOT_FOUND,
    ERROR_MAP, map_error,
)
from .router import ModelRouter, ENV_KEY_MAP, HEALTH_CHECK_CACHE_TTL

__all__ = [
    # Version
    "__version__", "__kernel_version__",
    # Types
    "ChatMessage", "ChatResponse", "ContentChunk", "ToolCall",
    "EmbeddingResult", "RerankResult", "TranscriptionResult",
    "VideoUnderstandingResult", "now_ms",
    # Error mapping
    "ERROR_PARAM_INVALID", "ERROR_MODEL_UNAVAILABLE",
    "ERROR_RATE_LIMITED", "ERROR_INTERNAL", "ERROR_PROVIDER_NOT_FOUND",
    "ERROR_MAP", "map_error",
    # Router
    "ModelRouter", "ENV_KEY_MAP", "HEALTH_CHECK_CACHE_TTL",
]
