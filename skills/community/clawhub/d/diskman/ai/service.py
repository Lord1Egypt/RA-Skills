"""AI Service for enhanced analysis."""

import os
from dataclasses import dataclass
from typing import Any

from ..models import DirectoryInfo
from .providers import AIProvider, OpenAIProvider


@dataclass
class AIConfig:
    """Configuration for OpenAI-compatible AI providers.

    Supports any API that implements the OpenAI chat completions interface:
    - OpenAI (default)
    - Azure OpenAI
    - DeepSeek
    - Moonshot (Kimi)
    - Zhipu (智谱)
    - Qwen (通义千问)
    - Local models (Ollama, vLLM, etc.)
    - Any other OpenAI-compatible endpoint
    """

    api_key: str | None = None
    base_url: str = "https://api.openai.com"
    model: str = "gpt-4o-mini"


class AIService:
    """
    AI Service for enhanced directory analysis.

    Provides AI-powered analysis when rule-based analysis
    is insufficient.
    """

    def __init__(self, config: AIConfig | None = None):
        """
        Initialize AI service.

        Args:
            config: AI configuration (default: from environment)
        """
        if config is None:
            config = AIConfig(
                api_key=os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("AI_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com",
                model=os.getenv("AI_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o-mini",
            )

        self._config = config
        self._provider: AIProvider | None = None
        self._init_provider()

    def _init_provider(self):
        """Initialize OpenAI-compatible provider."""
        if self._config.api_key:
            self._provider = OpenAIProvider(
                api_key=self._config.api_key,
                model=self._config.model,
                base_url=self._config.base_url,
            )

    @property
    def available(self) -> bool:
        """Check if AI provider is available."""
        return self._provider is not None

    def get_provider(self) -> AIProvider:
        """Get the configured provider."""
        if not self._provider:
            raise ValueError("No AI provider configured. Set AI_API_KEY or OPENAI_API_KEY environment variable.")
        return self._provider

    async def analyze(
        self,
        directories: list[DirectoryInfo],
        user_context: str | None = None,
        target_drive: str | None = None,
    ) -> dict[str, Any]:
        """
        Analyze directories using AI.

        Args:
            directories: Directories to analyze
            user_context: User context (e.g., "Python developer")
            target_drive: Target drive for migration

        Returns:
            Analysis results
        """
        ai_provider = self.get_provider()

        # Prepare data for AI
        dir_data = [
            {
                "path": d.path,
                "size_mb": d.size_mb,
                "link_type": d.link_type.value,
                "file_types": d.file_types,
            }
            for d in directories[:50]  # Limit for API
        ]

        result = await ai_provider.analyze(
            directories=dir_data,
            user_context=user_context,
            target_drive=target_drive,
        )

        return result

    async def get_provider_info(self) -> dict[str, Any]:
        """Get provider information."""
        if not self._provider:
            return {"available": False, "reason": "No API key configured"}

        available = await self._provider.is_available()
        return {
            "available": available,
            "model": self._provider.model,
            "base_url": self._config.base_url,
        }
