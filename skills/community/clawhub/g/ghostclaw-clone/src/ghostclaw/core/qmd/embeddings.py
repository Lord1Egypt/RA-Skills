"""EmbeddingManager — handles chunking and embedding generation for reports."""

import hashlib
from pathlib import Path
from typing import List, Dict, Any

from ghostclaw.core.vector_store import VectorStore


class EmbeddingManager:
    """Manages report chunking and embedding generation."""

    def __init__(self, vector_store: VectorStore, embedding_backend: str):
        self.vector_store = vector_store
        self.embedding_backend = embedding_backend

    def _extract_chunks(self, report: Dict[str, Any], run_id: int) -> List[Dict[str, Any]]:
        """
        Break a report into semantic chunks for embedding.

        Chunks are created from issues, ghosts, red flags, and AI synthesis paragraphs.
        Each chunk includes metadata about its source.
        """
        chunks = []
        repo_path = report.get("repo_path", "")
        timestamp = report.get("metadata", {}).get("timestamp", "")
        stack = report.get("stack", "")
        vibe_score = report.get("vibe_score", 0)

        # Helper to create chunk
        def make_chunk(text: str, kind: str, extra: Dict = None):
            chunk_id = hashlib.sha256(f"{run_id}:{kind}:{text[:100]}".encode()).hexdigest()[:16]
            meta = {
                "run_id": run_id,
                "kind": kind,
                "repo_path": repo_path,
                "timestamp": timestamp,
                "stack": stack,
                "vibe_score": vibe_score,
            }
            if extra:
                meta.update(extra)
            return {"chunk_id": chunk_id, "text": text, "metadata": meta}

        # Issues
        for issue in report.get("issues", []):
            if isinstance(issue, dict):
                msg = issue.get("message", "")
                if msg:
                    chunks.append(make_chunk(msg, "issue", {"file": issue.get("file")}))
            else:
                chunks.append(make_chunk(str(issue), "issue"))

        # Architectural ghosts
        for ghost in report.get("architectural_ghosts", []):
            if isinstance(ghost, dict):
                msg = ghost.get("message", "")
                if msg:
                    chunks.append(make_chunk(msg, "ghost"))
            else:
                chunks.append(make_chunk(str(ghost), "ghost"))

        # Red flags
        for flag in report.get("red_flags", []):
            if isinstance(flag, dict):
                msg = flag.get("message", "")
                if msg:
                    chunks.append(make_chunk(msg, "red_flag"))
            else:
                chunks.append(make_chunk(str(flag), "red_flag"))

        # AI synthesis (split into paragraphs)
        synthesis = report.get("ai_synthesis") or ""
        if synthesis:
            for para in synthesis.split("\n\n"):
                para = para.strip()
                if para:
                    chunks.append(make_chunk(para, "synthesis"))

        return chunks

    def _embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[List[float]]:
        """
        Generate embeddings for a list of chunks.
        Returns a list of embedding vectors (one per chunk).
        """
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.vector_store.embed_batch(texts)
        return embeddings
