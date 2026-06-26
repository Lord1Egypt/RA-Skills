"""LLM communication layer with conversation history management.

Provides an async wrapper around OpenAI-compatible chat completion APIs
and a Conversation class for managing multi-turn dialogue histories.
"""

import json
from dataclasses import dataclass, field

import httpx
from loguru import logger


@dataclass
class Message:
    """A single message in a conversation."""

    role: str
    content: str


class Conversation:
    """Rolling conversation history with an optional system prompt."""

    def __init__(self, system_prompt: str = "", max_history: int = 50):
        self._system_prompt = system_prompt
        self._max_history = max_history
        self._messages: list[Message] = []

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value: str) -> None:
        self._system_prompt = value

    def add(self, role: str, content: str) -> None:
        """Append a message and trim history if it exceeds the limit."""
        self._messages.append(Message(role=role, content=content))
        if len(self._messages) > self._max_history:
            self._messages = self._messages[-self._max_history :]

    def to_api_format(self) -> list[dict]:
        """Serialize the conversation into the OpenAI messages format."""
        msgs: list[dict] = []
        if self._system_prompt:
            msgs.append({"role": "system", "content": self._system_prompt})
        msgs.extend(
            {"role": m.role, "content": m.content} for m in self._messages
        )
        return msgs

    def clear(self) -> None:
        self._messages.clear()


class LLMHandler:
    """Async wrapper for OpenAI-compatible chat completion APIs."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o",
    ):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        """Initialize the HTTP client."""
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(120.0, connect=10.0),
        )
        logger.info("LLMHandler started (model=%s)", self._model)

    async def stop(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
        logger.info("LLMHandler stopped")

    async def chat(
        self, conversation: Conversation, temperature: float = 0.7
    ) -> str:
        """Send the conversation to the LLM and return the assistant reply."""
        if not self._client:
            raise RuntimeError("LLMHandler not started; call start() first")

        payload = {
            "model": self._model,
            "messages": conversation.to_api_format(),
            "temperature": temperature,
        }

        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        conversation.add("assistant", reply)
        return reply

    async def chat_json(
        self, conversation: Conversation, temperature: float = 0.3
    ) -> dict:
        """Send the conversation and parse the reply as JSON.

        Uses the response_format API parameter to enforce valid JSON output.
        """
        if not self._client:
            raise RuntimeError("LLMHandler not started; call start() first")

        payload = {
            "model": self._model,
            "messages": conversation.to_api_format(),
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        conversation.add("assistant", reply)
        return json.loads(reply)
