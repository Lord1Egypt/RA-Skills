# -*- coding: utf-8 -*-
"""Data models for the three-tier agent memory architecture."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """A single turn in a conversation."""

    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_openai(self) -> dict[str, str]:
        return {"role": self.role.value, "content": self.content}


@dataclass
class Entity:
    """A structured fact about the user extracted from conversation.

    Example: Entity(key="fear", value="狗", evidence="小时候被狗追过")
    """

    key: str
    value: str
    evidence: str = ""
    confidence: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_card_text(self) -> str:
        return f"{self.key}: {self.value}"


@dataclass
class Episode:
    """A semantic chunk of conversation stored for fuzzy retrieval."""

    id: str
    content: str
    summary: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_context_text(self) -> str:
        label = f"[历史片段] {self.summary}" if self.summary else "[历史片段]"
        return f"{label}\n{self.content}"


@dataclass
class MemoryContext:
    """The assembled context that goes into the final prompt."""

    system_prompt: str
    entity_cards: list[Entity] = field(default_factory=list)
    retrieved_episodes: list[Episode] = field(default_factory=list)
    recent_messages: list[Message] = field(default_factory=list)

    def build_messages(self) -> list[dict[str, str]]:
        """Build the final OpenAI-format message list."""
        messages: list[dict[str, str]] = []

        # 1. System prompt + entity cards ("档案袋")
        system_text = self.system_prompt
        if self.entity_cards:
            cards = "\n".join(
                f"- {e.to_card_text()}" for e in self.entity_cards
            )
            system_text += (
                f"\n\n=== 用户档案（结构化记忆，请优先信任） ===\n{cards}"
            )

        # 2. Retrieved episodes for context
        if self.retrieved_episodes:
            episodes_text = "\n\n---\n".join(
                e.to_context_text() for e in self.retrieved_episodes
            )
            system_text += (
                f"\n\n=== 历史相关片段（语义检索，仅供参考） ===\n{episodes_text}"
            )

        messages.append({"role": "system", "content": system_text})

        # 3. Recent conversation (short-term memory)
        for msg in self.recent_messages:
            messages.append(msg.to_openai())

        return messages
