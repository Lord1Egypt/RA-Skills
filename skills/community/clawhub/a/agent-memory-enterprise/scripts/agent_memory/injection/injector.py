"""Memory injector - injects scored memories into model context within token budget."""

from __future__ import annotations

from typing import Any, Optional

import tiktoken

from agent_memory.config import InjectorConfig
from agent_memory.injection.formatters import (
    format_context_memory,
    format_experience,
    format_knowledge_result,
    format_task_memory,
    format_user_profile,
)
from agent_memory.models.base import MemoryType
from agent_memory.models.scoring import ImportanceScore
from agent_memory.scoring.importance_scorer import ImportanceScorer


class MemoryInjector:
    """Injects scored memories into model context within token budget."""

    def __init__(self, config: InjectorConfig, scorer: ImportanceScorer):
        self._config = config
        self._scorer = scorer
        try:
            self._encoder = tiktoken.get_encoding(config.tokenizer_model)
        except Exception:
            self._encoder = tiktoken.get_encoding("cl100k_base")

    async def inject(
        self,
        memories: list[tuple[Any, ImportanceScore]],
        base_prompt: str = "",
        system_prompt: Optional[str] = None,
    ) -> str:
        """Inject memories into a prompt within the token budget.

        Args:
            memories: List of (memory_item, importance_score) tuples.
            base_prompt: The base user prompt.
            system_prompt: Optional system prompt.

        Returns:
            Assembled prompt string with injected memories.
        """
        # Calculate available budget
        system_tokens = self.estimate_tokens(system_prompt) if system_prompt else 0
        base_tokens = self.estimate_tokens(base_prompt)
        budget = int(self._config.token_budget * self._config.budget_threshold)
        available = budget - system_tokens - base_tokens

        if available <= 0:
            return base_prompt

        # Sort by importance score descending
        sorted_memories = sorted(memories, key=lambda x: x[1].total, reverse=True)

        # Build memory sections
        sections: list[tuple[str, str]] = []
        used_tokens = 0

        for item, score in sorted_memories:
            formatted = self._format_item(item, score.memory_type)
            if not formatted:
                continue

            tokens = self.estimate_tokens(formatted)
            if used_tokens + tokens <= available:
                sections.append((score.memory_type.value, formatted))
                used_tokens += tokens
            else:
                # Try a shorter version (first line only)
                short = formatted.split("\n")[0]
                short_tokens = self.estimate_tokens(short)
                if used_tokens + short_tokens <= available:
                    sections.append((score.memory_type.value, short + "..."))
                    used_tokens += short_tokens

        # Assemble final prompt
        parts = []
        if system_prompt:
            parts.append(system_prompt)
        if sections:
            memory_text = "\n\n".join(text for _, text in sections)
            parts.append(f"[Memory Context]\n{memory_text}")
        if base_prompt:
            parts.append(base_prompt)

        return "\n\n---\n\n".join(parts)

    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text string."""
        if not text:
            return 0
        return len(self._encoder.encode(text))

    def _format_item(self, item: Any, memory_type: MemoryType) -> str:
        """Format a memory item based on its type."""
        formatters = {
            MemoryType.CONTEXT: format_context_memory,
            MemoryType.TASK: format_task_memory,
            MemoryType.USER: format_user_profile,
            MemoryType.KNOWLEDGE: format_knowledge_result,
            MemoryType.EXPERIENCE: format_experience,
        }
        formatter = formatters.get(memory_type)
        if formatter:
            return formatter(item)
        return str(item) if item else ""
