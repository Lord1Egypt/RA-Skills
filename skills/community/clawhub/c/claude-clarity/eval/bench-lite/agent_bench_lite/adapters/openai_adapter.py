"""
OpenAI adapter.

Wraps the ``openai`` Python SDK to provide :class:`BaseAdapter`-compatible
access to GPT models.  Requires ``pip install agent-bench-lite[openai]``.
"""

from __future__ import annotations

import json
from typing import Any

from agent_bench_lite.adapters.base import BaseAdapter, ToolHandler


class OpenAIAdapter(BaseAdapter):
    """Adapter for the OpenAI Chat Completions API.

    Args:
        model: Model identifier (e.g. ``"gpt-4o"``).
        api_key: OpenAI API key.  Falls back to ``OPENAI_API_KEY`` env var.
        max_tokens: Maximum tokens per response.
        temperature: Sampling temperature (0 = deterministic).

    Example::

        adapter = OpenAIAdapter(model="gpt-4o")
        response = await adapter.send_message([
            {"role": "user", "content": "Hello!"}
        ])
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> None:
        try:
            import openai
        except ImportError as exc:
            raise ImportError(
                "The 'openai' package is required.  "
                "Install it with: pip install agent-bench-lite[openai]"
            ) from exc

        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = openai.AsyncOpenAI(api_key=api_key)

    async def send_message(
        self,
        messages: list[dict[str, str]],
        *,
        system: str | None = None,
    ) -> str:
        msgs: list[dict[str, str]] = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.extend(messages)

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=msgs,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content or ""

    async def send_message_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]],
        tool_handler: ToolHandler,
        *,
        system: str | None = None,
        max_tool_rounds: int = 5,
    ) -> str:
        openai_tools = self._convert_tools(tools)

        conversation: list[dict[str, Any]] = []
        if system:
            conversation.append({"role": "system", "content": system})
        conversation.extend(dict(m) for m in messages)

        for _round in range(max_tool_rounds):
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=conversation,
                tools=openai_tools,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            choice = response.choices[0]
            message = choice.message

            # If there are no tool calls, we're done.
            if not message.tool_calls:
                return message.content or ""

            # Append the assistant message with tool calls.
            conversation.append(message.model_dump())

            # Execute each tool call.
            for tool_call in message.tool_calls:
                func = tool_call.function
                try:
                    params = json.loads(func.arguments) if func.arguments else {}
                except json.JSONDecodeError:
                    params = {}

                result_str = await tool_handler(func.name, params)
                conversation.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_str,
                    }
                )

        # Final round without tools.
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=conversation,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content or ""

    # ── Helper ───────────────────────────────────────────────────────

    @staticmethod
    def _convert_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Convert generic tool schemas to OpenAI function-calling format."""
        converted = []
        for tool in tools:
            converted.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {"type": "object", "properties": {}}),
                    },
                }
            )
        return converted
