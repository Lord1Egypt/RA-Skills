"""Abstract base class for all memory layers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseMemory(ABC):
    """Abstract base for all 5 memory layers."""

    @abstractmethod
    async def initialize(self) -> None:
        """Set up connections, create tables/collections if needed."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully close connections."""

    @abstractmethod
    async def store(self, data: Any, **kwargs) -> str:
        """Store a memory item. Returns the item ID."""

    @abstractmethod
    async def retrieve(self, memory_id: str, **kwargs) -> Optional[Any]:
        """Retrieve a single memory by ID."""

    @abstractmethod
    async def search(self, query: Any, **kwargs) -> list[Any]:
        """Search memories matching the query."""

    @abstractmethod
    async def delete(self, memory_id: str) -> bool:
        """Delete a memory. Returns True if found and deleted."""

    @abstractmethod
    async def count(self, **kwargs) -> int:
        """Count stored items matching optional filters."""
