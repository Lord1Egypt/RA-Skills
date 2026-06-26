"""Async SQLAlchemy engine + session manager."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from agent_memory.config import PostgreSQLConfig
from agent_memory.exceptions import StorageConnectionError


class PostgresClient:
    """Async PostgreSQL connection manager using SQLAlchemy 2.0."""

    def __init__(self, config: PostgreSQLConfig, base=None):
        self._config = config
        self._base = base
        self._engine = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    async def initialize(self) -> None:
        try:
            self._engine = create_async_engine(
                self._config.url,
                pool_size=self._config.pool_size,
                max_overflow=self._config.max_overflow,
                echo=self._config.echo,
            )
            self._session_factory = async_sessionmaker(
                self._engine, expire_on_commit=False
            )
            # Create tables if base metadata is provided
            if self._base is not None:
                async with self._engine.begin() as conn:
                    await conn.run_sync(self._base.metadata.create_all)
        except Exception as e:
            raise StorageConnectionError(f"Failed to connect to PostgreSQL: {e}") from e

    async def shutdown(self) -> None:
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            raise StorageConnectionError("PostgreSQL client not initialized")
        return self._session_factory

    def session(self) -> AsyncSession:
        return self.session_factory()
