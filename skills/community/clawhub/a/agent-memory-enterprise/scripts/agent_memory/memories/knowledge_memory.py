"""Knowledge Memory - RAG-based knowledge retrieval using ChromaDB."""

from __future__ import annotations

import re
from typing import Any, Optional

from agent_memory.config import KnowledgeMemoryConfig
from agent_memory.core.base_memory import BaseMemory
from agent_memory.models.knowledge import Document, DocumentChunk, SearchResult
from agent_memory.storage.chroma_client import ChromaClient


class KnowledgeMemory(BaseMemory):
    """RAG-based knowledge retrieval using ChromaDB."""

    def __init__(self, chroma_client: ChromaClient, config: KnowledgeMemoryConfig):
        self._chroma = chroma_client
        self._config = config

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    async def store(self, data: Document, **kwargs) -> str:
        return await self.index_document(data)

    async def retrieve(self, memory_id: str, **kwargs) -> Optional[DocumentChunk]:
        """Retrieve a single chunk by its ID."""
        try:
            results = await self._chroma.collection.get(ids=[memory_id])
            if results["ids"]:
                return DocumentChunk(
                    id=results["ids"][0],
                    document_id=results["metadatas"][0].get("document_id", ""),
                    chunk_index=results["metadatas"][0].get("chunk_index", 0),
                    content=results["documents"][0],
                    metadata=results["metadatas"][0] if results["metadatas"] else {},
                )
        except Exception:
            pass
        return None

    async def search(self, query: Any, **kwargs) -> list[SearchResult]:
        if isinstance(query, str):
            return await self.search_similar(query, **kwargs)
        return []

    async def delete(self, memory_id: str) -> bool:
        try:
            await self._chroma.delete(ids=[memory_id])
            return True
        except Exception:
            return False

    async def count(self, **kwargs) -> int:
        return await self._chroma.count()

    # --- Extended interface ---

    async def index_document(self, document: Document) -> str:
        """Index a document by splitting into chunks and storing in ChromaDB."""
        chunks = self._chunk_text(document.content, self._config.chunk_size, self._config.chunk_overlap)

        ids = []
        documents = []
        metadatas = []

        for i, chunk_content in enumerate(chunks):
            chunk_id = f"{document.id}_chunk_{i}"
            ids.append(chunk_id)
            documents.append(chunk_content)
            metadatas.append({
                "document_id": document.id,
                "chunk_index": i,
                "domain": document.domain,
                "source": document.source,
                "title": document.title,
                **document.metadata,
            })

        if ids:
            await self._chroma.add(ids=ids, documents=documents, metadatas=metadatas)

        return document.id

    async def index_text(
        self,
        title: str,
        content: str,
        domain: str,
        source: str = "",
        metadata: Optional[dict] = None,
    ) -> str:
        """Convenience method to index raw text as a document."""
        doc = Document(
            title=title,
            content=content,
            domain=domain,
            source=source,
            metadata=metadata or {},
        )
        return await self.index_document(doc)

    async def search_similar(
        self,
        query: str,
        top_k: Optional[int] = None,
        domain: Optional[str] = None,
        metadata_filter: Optional[dict] = None,
    ) -> list[SearchResult]:
        """Search for similar knowledge chunks."""
        k = top_k or self._config.top_k
        where = metadata_filter
        if domain and not where:
            where = {"domain": domain}
        elif domain and where:
            where = {"$and": [where, {"domain": domain}]}

        results = await self._chroma.query(
            query_texts=[query],
            n_results=k,
            where=where if where else None,
        )

        search_results = []
        if results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                score = 1.0 - results["distances"][0][i] if results["distances"] else 0.0
                if score < self._config.similarity_threshold:
                    continue
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                search_results.append(
                    SearchResult(
                        chunk_id=chunk_id,
                        content=results["documents"][0][i],
                        score=score,
                        document_id=meta.get("document_id", ""),
                        chunk_index=meta.get("chunk_index", 0),
                        metadata=meta,
                        document_title=meta.get("title"),
                    )
                )

        return search_results

    async def delete_document(self, document_id: str) -> bool:
        """Delete all chunks for a document."""
        try:
            await self._chroma.delete(where={"document_id": document_id})
            return True
        except Exception:
            return False

    async def get_document_chunks(self, document_id: str) -> list[DocumentChunk]:
        """Get all chunks for a document."""
        try:
            results = await self._chroma.collection.get(
                where={"document_id": document_id}
            )
            chunks = []
            if results["ids"]:
                for i, cid in enumerate(results["ids"]):
                    meta = results["metadatas"][i] if results["metadatas"] else {}
                    chunks.append(
                        DocumentChunk(
                            id=cid,
                            document_id=document_id,
                            chunk_index=meta.get("chunk_index", 0),
                            content=results["documents"][i],
                            metadata=meta,
                        )
                    )
            return chunks
        except Exception:
            return []

    # --- Private helpers ---

    def _chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
        """Split text into overlapping chunks based on word count."""
        words = text.split()
        if not words:
            return []

        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))
            if end >= len(words):
                break
            start = end - chunk_overlap

        return chunks
