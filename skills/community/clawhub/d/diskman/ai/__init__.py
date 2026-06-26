"""AI module - optional AI-powered analysis."""

from .providers import AIProvider, OpenAIProvider
from .service import AIConfig, AIService

__all__ = [
    "AIService",
    "AIConfig",
    "AIProvider",
    "OpenAIProvider",
]
