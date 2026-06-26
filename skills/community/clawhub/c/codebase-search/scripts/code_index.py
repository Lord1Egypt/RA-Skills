"""CodebaseIndex — ChromaDB-backed persistent vector index over PRSM source code."""
from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    filepath: str
    symbol_name: str
    symbol_type: str
    start_line: int
    end_line: int
    docstring: str
    module_path: str
    score: float
    snippet: str

class CodebaseIndex:
    COLLECTION = "prsm_codebase_v1"

    def __init__(self, repo_root: str, persist_dir: str = None):
        self.repo_root = str(Path(repo_root).resolve())
        self.persist_dir = persist_dir or str(Path(repo_root) / ".codebase_index")
        self._client = None
        self._collection = None

    def _init_client(self):
        if self._client is None:
            import chromadb
            self._client = chromadb.PersistentClient(path=self.persist_dir)
            self._collection = self._client.get_or_create_collection(
                name=self.COLLECTION,
                metadata={"hnsw:space": "cosine"},
            )

    def is_built(self) -> bool:
        try:
            self._init_client()
            return self._collection.count() > 0
        except Exception:
            return False

    async def build(self, force_rebuild: bool = False) -> int:
        from prsm.compute.nwtn.corpus.code_chunker import CodeChunker
        def _build():
            self._init_client()
            if force_rebuild:
                self._client.delete_collection(self.COLLECTION)
                self._collection = self._client.get_or_create_collection(
                    name=self.COLLECTION, metadata={"hnsw:space": "cosine"}
                )
            chunker = CodeChunker(self.repo_root)
            chunks = chunker.chunk_repo()
            if not chunks:
                return 0
            # Get existing IDs for dedup
            existing = set()
            if self._collection.count() > 0:
                existing = set(self._collection.get()["ids"])
            new_chunks = [c for c in chunks if c.chunk_id not in existing]
            if not new_chunks:
                return 0
            # Batch upsert
            batch_size = 100
            for i in range(0, len(new_chunks), batch_size):
                batch = new_chunks[i:i+batch_size]
                self._collection.upsert(
                    ids=[c.chunk_id for c in batch],
                    documents=[f"{c.symbol_name}: {c.docstring or c.source[:300]}" for c in batch],
                    metadatas=[{
                        "filepath": c.filepath,
                        "symbol_name": c.symbol_name,
                        "symbol_type": c.symbol_type,
                        "start_line": c.start_line,
                        "end_line": c.end_line,
                        "docstring": c.docstring[:500],
                        "module_path": c.module_path,
                        "snippet": c.source[:300],
                    } for c in batch],
                )
            return len(new_chunks)
        return await asyncio.to_thread(_build)

    async def search(self, query: str, top_k: int = 5, symbol_type: str = None) -> List[SearchResult]:
        def _search():
            self._init_client()
            where = {"symbol_type": symbol_type} if symbol_type else None
            kwargs = {"query_texts": [query], "n_results": min(top_k, self._collection.count() or 1)}
            if where:
                kwargs["where"] = where
            results = self._collection.query(**kwargs)
            out = []
            for i, meta in enumerate(results["metadatas"][0]):
                distance = results["distances"][0][i]
                score = 1.0 - distance
                out.append(SearchResult(
                    filepath=meta["filepath"],
                    symbol_name=meta["symbol_name"],
                    symbol_type=meta["symbol_type"],
                    start_line=meta["start_line"],
                    end_line=meta["end_line"],
                    docstring=meta.get("docstring", ""),
                    module_path=meta["module_path"],
                    score=score,
                    snippet=meta.get("snippet", ""),
                ))
            return out
        return await asyncio.to_thread(_search)
