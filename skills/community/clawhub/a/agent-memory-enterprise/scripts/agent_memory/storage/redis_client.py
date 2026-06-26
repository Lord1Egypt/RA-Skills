"""Async Redis connection manager."""

from __future__ import annotations

import redis.asyncio as aioredis

from agent_memory.config import RedisConfig
from agent_memory.exceptions import StorageConnectionError


class RedisClient:
    """Async Redis connection pool manager."""

    def __init__(self, config: RedisConfig):
        self._config = config
        self._pool: aioredis.Redis | None = None

    async def initialize(self) -> None:
        try:
            self._pool = aioredis.from_url(
                self._config.url,
                max_connections=self._config.max_connections,
                decode_responses=self._config.decode_responses,
            )
            await self._pool.ping()
        except Exception as e:
            raise StorageConnectionError(f"Failed to connect to Redis: {e}") from e

    async def shutdown(self) -> None:
        if self._pool:
            await self._pool.aclose()
            self._pool = None

    @property
    def client(self) -> aioredis.Redis:
        if self._pool is None:
            raise StorageConnectionError("Redis client not initialized")
        return self._pool
