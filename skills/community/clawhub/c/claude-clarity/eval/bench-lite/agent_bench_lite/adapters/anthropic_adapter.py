"""
Anthropic Claude adapter.

Wraps the ``anthropic`` Python SDK to provide :class:`BaseAdapter`-compatible
access to Claude models.  Requires ``pip install agent-bench-lite[anthropic]``.
"""

from __future__ import annotations

from typing import Any

from agent_bench_lite.adapters.base import BaseAdapter, ToolHandler


class AnthropicAdapter(BaseAdapter):
    """Adapter for the Anthropic Messages API (Claude).

    Args:
        model: Model identifier (e.g. ``"claude-sonnet-4-20250514"``).
        api_key: Anthropic API key.  Falls back to ``ANTHROPIC_API_KEY`` env var.
        max_tokens: Maximum tokens per response.
        temperature: Sampling temperature (0 = deterministic).

    Example::

        adapter = AnthropicAdapter(model="claude-sonnet-4-20250514")
        response = await adapter.send_message([
            {"role": "user", "content": "Hello!"}
        ])
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        api_key: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> None:
        try:
            import anthropic
        except ImportError as exc:
            raise ImportError(
                "The 'anthropic' package is required.  "
                "Install it with: pip install agent-bench-lite[anthropic]"
            ) from exc

        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def send_message(
        self,
        messages: list[dict[str, str]],
        *,
        system: str | None = None,
    ) -> str:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system

        response = await self._client.messages.create(**kwargs)

        # Extract text from the response content blocks.
        parts: list[str] = []
        for block in response.content:
            if hasattr(block, "text"):
                parts.append(block.text)
        return "\n".join(parts)

    async def send_message_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]],
        tool_handler: ToolHandler,
        *,
        system: str | None = None,
        max_tool_rounds: int = 5,
    ) -> str:
        # Convert generic tool defs to Anthropic format.
        anthropic_tools = self._convert_tools(tools)

        # Build a mutable conversation.
        conversation: list[dict[str, Any]] = [dict(m) for m in messages]

        for _round in range(max_tool_rounds):
            kwargs: dict[str, Any] = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": conversation,
                "tools": anthropic_tools,
            }
            if system:
                kwargs["system"] = system

            response = await self._client.messages.create(**kwargs)

            # Collect text and tool-use blocks.
            text_parts: list[str] = []
            tool_uses: list[dict[str, Any]] = []
            for block in response.content:
                if hasattr(block, "text"):
                    text_parts.append(block.text)
                elif block.type == "tool_use":
                    tool_uses.append(
                        {"id": block.id, "name": block.name, "input": block.input}
                    )

            if not tool_uses:
                return "\n".join(text_parts)

            # Append assistant turn with all content blocks.
            assistant_content: list[dict[str, Any]] = []
            for block in response.content:
                if hasattr(block, "text"):
                    assistant_content.append({"type": "text", "text": block.text})
                elif block.type == "tool_use":
                    assistant_content.append(
                        {
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input,
                        }
                    )
            conversation.append({"role": "assistant", "content": assistant_content})

            # Execute each tool call and build tool_result blocks.
            tool_results: list[dict[str, Any]] = []
            for tu in tool_uses:
                result_str = await tool_handler(tu["name"], tu["input"])
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tu["id"],
                        "content": result_str,
                    }
                )
            conversation.append({"role": "user", "content": tool_results})

        # Final attempt without tools.
        final = await self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=conversation,
        )
        return "\n".join(
            block.text for block in final.content if hasattr(block, "text")
        )

    # ── Helper ───────────────────────────────────────────────────────

    @staticmethod
    def _convert_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Convert generic tool schemas to Anthropic's expected format."""
        converted = []
        for tool in tools:
            converted.append(
                {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "input_schema": tool.get("parameters", {"type": "object", "properties": {}}),
                }
            )
        return converted
