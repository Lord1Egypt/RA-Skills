"""Base AI provider interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class AIAnalysisResult:
    """Result from AI analysis."""

    recommendations: list[dict[str, Any]]
    summary: str
    total_releasable_mb: float


class AIProvider(ABC):
    """Base class for AI providers."""

    name: str = "base"
    model: str = "unknown"

    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def analyze(
        self,
        directories: list[dict[str, Any]],
        user_context: str | None = None,
        target_drive: str | None = None,
    ) -> dict[str, Any]:
        """
        Analyze directories using AI.

        Args:
            directories: List of directory data
            user_context: Optional user context
            target_drive: Optional target drive for migration

        Returns:
            Analysis result as dict
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if provider is available."""
        pass

    def _build_prompt(
        self,
        directories: list[dict[str, Any]],
        user_context: str | None,
        target_drive: str | None,
    ) -> str:
        """Build analysis prompt."""
        lines = [
            "Analyze these directories and provide cleanup/migration recommendations.",
            "",
            "Directories:",
        ]

        for d in directories:
            lines.append(f"  - {d['path']} ({d['size_mb']:.1f} MB)")

        if user_context:
            lines.extend(["", f"User context: {user_context}"])

        if target_drive:
            lines.extend(["", f"Target drive for migration: {target_drive}"])

        lines.extend(
            [
                "",
                "For each directory, provide:",
                "  - action: 'clean', 'migrate', 'keep', or 'review'",
                "  - risk: 'safe', 'low', 'medium', 'high', or 'critical'",
                "  - reason: brief explanation",
                "",
                "Respond in JSON format:",
                "{",
                '  "recommendations": [',
                '    {"path": "...", "action": "...",',
                '     "risk": "...", "reason": "...",',
                '     "target_path": "..."}',
                "  ],",
                '  "summary": "Brief summary of recommendations",',
                '  "total_releasable_mb": 0',
                "}",
            ]
        )

        return "\n".join(lines)
