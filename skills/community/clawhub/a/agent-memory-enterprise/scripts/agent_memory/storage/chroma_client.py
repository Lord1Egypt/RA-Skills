"""ChromaDB client wrapper for knowledge vector storage."""

from __future__ import annotations

import asyncio
from typing import Any

import chromadb

from agent_memory.config import ChromaConfig
from agent_memory.exceptions import StorageConnectionError


class ChromaClient:
    """ChromaDB persistent client wrapper with async support."""

    def __init__(self, config: ChromaConfig):
        self._config = config
        self._client: chromadb.ClientAPI | None = None
        self._collection: chromadb.Collection | None = None

    async def initialize(self) -> None:
        try:
            self._client = await asyncio.to_thread(
                chromadb.PersistentClient, path=self._config.persist_directory
            )
            self._collection = await asyncio.to_thread(
                self._client.get_or_create_collection,
                name=self._config.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        except Exception as e:
            raise StorageConnectionError(f"Failed to initialize ChromaDB: {e}") from e

    async def shutdown(self) -> None:
        self._client = None
        self._collection = None

    @property
    def collection(self) -> chromadb.Collection:
        if self._collection is None:
            raise StorageConnectionError("ChromaDB collection not initialized")
        return self._collection

    async def add(
        self,
        ids: list[str],
        documents: list[str],
        metadatas: list[dict[str, Any]] | None = None,
    ) -> None:
        await asyncio.to_thread(
            self.collection.add,
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

    async def query(
        self,
        query_texts: list[str],
        n_results: int = 5,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self.collection.query,
            query_texts=query_texts,
            n_results=n_results,
            where=where,
        )

    async def delete(self, ids: list[str] | None = None, where: dict[str, Any] | None = None) -> None:
        await asyncio.to_thread(
            self.collection.delete,
            ids=ids,
            where=where,
        )

    async def count(self) -> int:
        return await asyncio.to_thread(self.collection.count)
