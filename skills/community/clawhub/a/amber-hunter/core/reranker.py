"""
core/reranker.py — Cross-Encoder Reranker v1.2.41
使用 BAAI/bge-reranker-v2-m3 本地模型进行语义重排序。
自动降级：模型加载失败时返回原文顺序。
"""

from __future__ import annotations

from typing import Optional
import sys


class Reranker:
    """
    Cross-Encoder Reranker using BAAI/bge-reranker-v2-m3.

    用法:
        reranker = Reranker()
        results = reranker.rerank("query", ["doc1", "doc2", ...], top_k=5)
        # returns [(doc_index, score), ...]
    """

    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        """
        Initialize reranker with model.

        Args:
            model_name: HuggingFace model name for cross-encoder reranker.
                       Defaults to BAAI/bge-reranker-v2-m3
        """
        self._model_name = model_name
        self._model = None
        self._failed = False

    def _ensure_model(self):
        """Lazy load the cross-encoder model."""
        if self._model is not None or self._failed:
            return

        try:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(
                self._model_name,
                max_length=512,
                trust_remote_code=True,
            )
        except Exception as e:
            self._failed = True
            print(f"[reranker] Failed to load {self._model_name}: {e}", file=sys.stderr)
            self._model = None

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int = 10,
    ) -> list[tuple[int, float]]:
        """
        Rerank documents by relevance to query using cross-encoder.

        Args:
            query: the search query
            documents: list of document texts to rerank
            top_k: number of top results to return

        Returns:
            list of (doc_index, score) tuples, sorted by score descending.
            Falls back to original order if model loading fails.
        """
        if not documents:
            return []

        self._ensure_model()

        # Fallback: return original order with uniform scores
        if self._model is None:
            n = min(top_k, len(documents))
            return [(i, 1.0 / (i + 1)) for i in range(n)]

        try:
            # Prepare sentence pairs for cross-encoder
            sentence_pairs = [[query, doc] for doc in documents]

            # Get relevance scores
            scores = self._model.predict(sentence_pairs)

            # Sort by score descending and return top-k
            indexed_scores = list(enumerate(scores))
            indexed_scores.sort(key=lambda x: x[1], reverse=True)

            return [(idx, float(score)) for idx, score in indexed_scores[:top_k]]

        except Exception as e:
            print(f"[reranker] Reranking failed: {e}", file=sys.stderr)
            # Fallback: original order
            n = min(top_k, len(documents))
            return [(i, 1.0 / (i + 1)) for i in range(n)]

    def is_available(self) -> bool:
        """Check if the reranker model is loaded and available."""
        self._ensure_model()
        return self._model is not None
