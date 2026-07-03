# -*- coding: utf-8 -*-
"""Short-term memory -- sliding window of recent conversation turns.

Corresponds to the "短期记忆" layer: keeps the last N rounds
verbatim for conversational coherence (指代消解, topic continuity).
"""

from __future__ import annotations

from collections import deque
from typing import Optional

from .models import Message, MessageRole


class ShortTermMemory:
    """Ring buffer that retains exactly the last `max_turns` messages."""

    def __init__(self, max_turns: int = 20) -> None:
        self._buffer: deque[Message] = deque(maxlen=max_turns)

    def add(self, message: Message) -> None:
        self._buffer.append(message)

    def add_turn(self, user_text: str, assistant_text: str) -> None:
        self.add(Message(role=MessageRole.USER, content=user_text))
        self.add(Message(role=MessageRole.ASSISTANT, content=assistant_text))

    def get_recent(self, n: Optional[int] = None) -> list[Message]:
        if n is None:
            return list(self._buffer)
        result: list[Message] = []
        for msg in self._buffer:
            result.append(msg)
            if len(result) >= n:
                break
        return result

    def clear(self) -> None:
        self._buffer.clear()

    def __len__(self) -> int:
        return len(self._buffer)
