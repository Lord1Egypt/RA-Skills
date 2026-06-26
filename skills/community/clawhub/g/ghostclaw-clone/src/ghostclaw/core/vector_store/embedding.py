"""
Embedding providers for Ghostclaw vector store.
"""

import os
import logging
import numpy as np
from typing import List, Union, Optional

logger = logging.getLogger("ghostclaw.vector_store.embedding")


class EmbeddingProvider:
    """Handles text embedding generation using various backends."""

    def __init__(self, backend: str = "fastembed", cache_dir: Optional[str] = None):
        self.backend = backend
        self.cache_dir = cache_dir or os.path.expanduser("~/.cache/fastembed")
        self._embedder = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the embedding model based on backend."""
        if self._initialized:
            return

        if self.backend == "sentence-transformers":
            try:
                import sentence_transformers
                self._embedder = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")
            except ImportError:
                raise ImportError("sentence_transformers required for 'sentence-transformers' backend.")
        elif self.backend == "fastembed":
            try:
                from fastembed import TextEmbedding
                self._embedder = TextEmbedding(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    cache_dir=self.cache_dir
                )
            except ImportError:
                raise ImportError("fastembed required for 'fastembed' backend.")
        elif self.backend == "openai":
            try:
                import openai
                self._embedder = openai.OpenAI()
            except ImportError:
                raise ImportError("openai required for 'openai' backend.")
        else:
            raise ValueError(f"Unsupported embedding_backend: {self.backend}")

        self._initialized = True

    async def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts."""
        self.initialize()
        
        if self.backend == "fastembed":
            return list(self._embedder.embed(texts))
        elif self.backend == "sentence-transformers":
            emb_array = self._embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True, batch_size=32)
            return [emb for emb in emb_array]
        elif self.backend == "openai":
            response = self._embedder.embeddings.create(input=texts, model="text-embedding-ada-002")
            embeddings = []
            for data in response.data:
                emb = np.array(data.embedding, dtype=np.float32)
                norm = np.linalg.norm(emb)
                if norm > 0:
                    emb = emb / norm
                embeddings.append(emb)
            return embeddings
        
        raise ValueError(f"Unsupported embedding_backend: {self.backend}")
