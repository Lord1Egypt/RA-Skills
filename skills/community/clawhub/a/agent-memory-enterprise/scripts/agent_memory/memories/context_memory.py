"""Context Memory - sliding-window conversation context stored in Redis."""

from __future__ import annotations

import json
from typing import Any, Optional

from agent_memory.config import ContextMemoryConfig
from agent_memory.core.base_memory import BaseMemory
from agent_memory.models.context import ContextMessage, ConversationWindow, MessageRole
from agent_memory.storage.redis_client import RedisClient


class ContextMemory(BaseMemory):
    """Sliding-window conversation context stored in Redis."""

    def __init__(self, redis_client: RedisClient, config: ContextMemoryConfig):
        self._redis = redis_client
        self._config = config

    async def initialize(self) -> None:
        pass  # Redis client is already initialized externally

    async def shutdown(self) -> None:
        pass  # Redis client is managed externally

    async def store(self, data: ContextMessage, **kwargs) -> str:
        session_id = kwargs.get("session_id")
        if not session_id:
            raise ValueError("session_id is required")
        window = await self.add_message(session_id, data)
        return data.id

    async def retrieve(self, memory_id: str, **kwargs) -> Optional[ContextMessage]:
        session_id = kwargs.get("session_id")
        if not session_id:
            return None
        window = await self.get_window(session_id)
        for msg in window.messages:
            if msg.id == memory_id:
                return msg
        return None

    async def search(self, query: Any, **kwargs) -> list[ContextMessage]:
        session_id = kwargs.get("session_id")
        if not session_id:
            return []
        window = await self.get_window(session_id)
        if isinstance(query, dict):
            role = query.get("role")
            if role:
                return [m for m in window.messages if m.role.value == role]
        return window.messages

    async def delete(self, memory_id: str) -> bool:
        # Context messages are managed by the window, not individually deletable
        return False

    async def count(self, **kwargs) -> int:
        session_id = kwargs.get("session_id")
        if not session_id:
            return 0
        window = await self.get_window(session_id)
        return len(window.messages)

    # --- Extended interface ---

    async def add_message(
        self, session_id: str, message: ContextMessage
    ) -> ConversationWindow:
        """Add a message to the session window, auto-trim if needed."""
        r = self._redis.client
        msg_key = f"ctx:{session_id}:msg:{message.id}"
        msgs_key = f"ctx:{session_id}:messages"
        window_key = f"ctx:{session_id}:window"

        msg_data = json.dumps({
            "id": message.id,
            "role": message.role.value,
            "content": message.content,
            "token_count": message.token_count,
            "metadata": message.metadata,
            "created_at": message.created_at.isoformat(),
        })

        pipe = r.pipeline(transaction=True)
        pipe.set(msg_key, msg_data)
        pipe.rpush(msgs_key, message.id)
        pipe.hset(window_key, mapping={
            "session_id": session_id,
            "updated_at": message.created_at.isoformat(),
        })
        pipe.hincrby(window_key, "total_tokens", message.token_count)
        if self._config.ttl_seconds > 0:
            pipe.expire(msg_key, self._config.ttl_seconds)
            pipe.expire(msgs_key, self._config.ttl_seconds)
            pipe.expire(window_key, self._config.ttl_seconds)
        await pipe.execute()

        return await self._trim_to_fit(session_id)

    async def get_window(self, session_id: str) -> ConversationWindow:
        """Get the current conversation window for a session."""
        r = self._redis.client
        window_key = f"ctx:{session_id}:window"
        msgs_key = f"ctx:{session_id}:messages"

        exists = await r.exists(window_key)
        if not exists:
            return ConversationWindow(session_id=session_id)

        msg_ids = await r.lrange(msgs_key, 0, -1)
        messages = []
        total_tokens = 0

        for mid in msg_ids:
            raw = await r.get(f"ctx:{session_id}:msg:{mid}")
            if raw:
                data = json.loads(raw)
                messages.append(ContextMessage(
                    id=data["id"],
                    role=MessageRole(data["role"]),
                    content=data["content"],
                    token_count=data["token_count"],
                    metadata=data.get("metadata", {}),
                    created_at=data["created_at"],
                ))
                total_tokens += data["token_count"]

        return ConversationWindow(
            session_id=session_id,
            messages=messages,
            total_tokens=total_tokens,
        )

    async def _trim_to_fit(self, session_id: str) -> ConversationWindow:
        """Trim oldest messages to fit within configured limits."""
        r = self._redis.client
        msgs_key = f"ctx:{session_id}:messages"

        while True:
            window = await self.get_window(session_id)
            needs_trim = False

            if len(window.messages) > self._config.max_messages:
                needs_trim = True
            elif window.total_tokens > self._config.max_tokens:
                needs_trim = True

            if not needs_trim:
                break

            # Pop the oldest non-system message
            oldest_id = await r.lpop(msgs_key)
            if not oldest_id:
                break

            # If it's a system message, put it back and try next
            msg_raw = await r.get(f"ctx:{session_id}:msg:{oldest_id}")
            if msg_raw:
                data = json.loads(msg_raw)
                if data["role"] == "system" and len(window.messages) > 1:
                    await r.rpush(msgs_key, oldest_id)
                    # Pop the next one instead
                    next_id = await r.lpop(msgs_key)
                    if next_id:
                        await r.delete(f"ctx:{session_id}:msg:{next_id}")
                        next_raw = await r.get(f"ctx:{session_id}:msg:{next_id}")
                        if next_raw:
                            tok = json.loads(next_raw)["token_count"]
                            await r.hincrby(
                                f"ctx:{session_id}:window", "total_tokens", -tok
                            )
                else:
                    await r.delete(f"ctx:{session_id}:msg:{oldest_id}")
                    await r.hincrby(
                        f"ctx:{session_id}:window", "total_tokens", -data["token_count"]
                    )

        return await self.get_window(session_id)

    async def clear_session(self, session_id: str) -> None:
        """Clear all messages for a session."""
        r = self._redis.client
        msgs_key = f"ctx:{session_id}:messages"
        msg_ids = await r.lrange(msgs_key, 0, -1)
        pipe = r.pipeline(transaction=True)
        for mid in msg_ids:
            pipe.delete(f"ctx:{session_id}:msg:{mid}")
        pipe.delete(msgs_key)
        pipe.delete(f"ctx:{session_id}:window")
        await pipe.execute()
