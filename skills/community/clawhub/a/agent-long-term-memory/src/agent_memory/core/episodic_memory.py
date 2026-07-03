# -*- coding: utf-8 -*-
"""Episodic memory -- vector-based long-term semantic memory.

Corresponds to the "长期情景记忆" layer: conversation chunks are
embedded and stored in a vector DB for fuzzy semantic retrieval.
This is "模糊召回" (fuzzy recall) for non-factual content.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from .models import Episode

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
except ImportError:
    chromadb = None  # type: ignore[assignment]


class EpisodicMemory:
    """Vector-store backed episodic memory using ChromaDB.

    Each episode is a semantic chunk of conversation. Retrieval is
    done by embedding the query and finding nearest neighbors.
    """

    def __init__(
        self,
        collection_name: str = "agent_episodes",
        persist_dir: str = "./data/chroma",
        embedding_fn: Optional[callable] = None,
    ) -> None:
        if chromadb is None:
            raise ImportError(
                "chromadb is required for EpisodicMemory. "
                "Install with: pip install chromadb"
            )

        self._embed_fn = embedding_fn
        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name
        )

    def add(self, episode: Episode, embedding: Optional[list[float]] = None) -> None:
        """Store an episode with its embedding.

        embedding must be provided directly. Generate it externally
        in async context if needed.
        """
        if embedding is None:
            raise ValueError("embedding must be provided for add()")

        metadata = {
            "summary": episode.summary or "",
            "created_at": episode.created_at.isoformat(),
        }

        self._collection.add(
            ids=[episode.id],
            embeddings=[embedding],
            documents=[episode.content],
            metadatas=[metadata],
        )

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        query_embedding: Optional[list[float]] = None,
    ) -> list[Episode]:
        """Semantic search: find episodes relevant to query_text.

        query_embedding must be provided directly.
        """
        if query_embedding is None:
            raise ValueError("query_embedding must be provided for query()")

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

        episodes: list[Episode] = []
        if results and results["ids"] and results["ids"][0]:
            for i, ep_id in enumerate(results["ids"][0]):
                doc = results["documents"][0][i] if results.get("documents") else ""
                meta = (
                    results["metadatas"][0][i]
                    if results.get("metadatas")
                    else {}
                )
                episodes.append(
                    Episode(
                        id=ep_id,
                        content=doc,
                        summary=meta.get("summary", ""),
                        created_at=datetime.fromisoformat(
                            meta.get("created_at", datetime.now().isoformat())
                        ),
                    )
                )
        return episodes

    def delete(self, episode_id: str) -> None:
        self._collection.delete(ids=[episode_id])

    def count(self) -> int:
        return self._collection.count()
