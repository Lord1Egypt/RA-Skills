"""Context memory models."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import Field

from .base import MemoryBase


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ContextMessage(MemoryBase):
    role: MessageRole
    content: str
    token_count: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConversationWindow(MemoryBase):
    session_id: str
    messages: list[ContextMessage] = Field(default_factory=list)
    total_tokens: int = 0
