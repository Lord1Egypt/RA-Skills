"""Simple reference adapter for Roundtable.

A minimal adapter that uses plain Python callables (no external framework
required).  Useful as a reference implementation and for quick testing.

Usage::

    from roundtable.adapters.simple import SimpleAdapter

    def my_speak(context):
        return f"I think {context['topic']} is important because..."

    adapter = SimpleAdapter(
        name="Alice",
        role="engineer",
        avatar="👩‍💻",
        speak_fn=my_speak,
    )
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from roundtable.adapters.base import RoundtableAdapter


class SimpleAdapter(RoundtableAdapter):
    """Minimal adapter using plain callables.

    Args:
        name: Agent display name.
        role: Role identifier (e.g. "engineer", "product").
        avatar: Emoji or image URL for the agent.
        title: Optional role title (e.g. "技术总监").
        description: Optional role description.
        speak_fn: ``async fn(context) -> str`` or ``fn(context) -> str``.
            If sync, it's wrapped automatically.
        listen_fn: Optional ``async fn(speech) -> dict | None``.
    """

    def __init__(
        self,
        name: str = "Agent",
        role: str = "default",
        avatar: str = "🤖",
        *,
        title: str | None = None,
        description: str | None = None,
        speak_fn: Callable[[dict[str, Any]], str] | None = None,
        listen_fn: Callable[[dict[str, Any]], dict[str, Any] | None] | None = None,
    ) -> None:
        self._name = name
        self._role = role
        self._avatar = avatar
        self._title = title
        self._description = description
        self._speak_fn = speak_fn or self._default_speak
        self._listen_fn = listen_fn

    def get_persona(self) -> dict[str, Any]:
        persona: dict[str, Any] = {
            "name": self._name,
            "role": self._role,
            "avatar": self._avatar,
        }
        if self._title:
            persona["title"] = self._title
        if self._description:
            persona["description"] = self._description
        return persona

    async def speak(self, context: dict[str, Any]) -> str:
        result = self._speak_fn(context)
        # Handle both sync and async speak_fn
        if hasattr(result, "__await__"):
            return str(await result)
        return str(result)

    async def listen(self, speech: dict[str, Any]) -> dict[str, Any] | None:
        if self._listen_fn is None:
            return None
        result = self._listen_fn(speech)
        if hasattr(result, "__await__"):
            return await result  # type: ignore[misc, no-any-return]
        return result

    @staticmethod
    def _default_speak(context: dict[str, Any]) -> str:
        topic = context.get("topic", "the topic")
        round_num = context.get("round", 1)
        return f"[Round {round_num}] I'd like to share my thoughts on: {topic}"
