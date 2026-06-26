"""
core/bm25.py — BM25 Full-Text Searcher v1.2.41
使用 rank_bm25 库实现 BM25 关键词检索。
"""

from __future__ import annotations

from typing import Optional


class BM25Searcher:
    """
    BM25 搜索引擎，基于 rank_bm25 库。

    用法:
        searcher = BM25Searcher(corpus=["doc1", "doc2", ...])
        results = searcher.search("query", top_k=10)
        # returns [(doc_index, score), ...]
    """

    def __init__(self, corpus: Optional[list[str]] = None):
        """
        Initialize BM25 index with optional corpus.

        Args:
            corpus: initial document list
        """
        self._corpus: list[str] = []
        self._index = None
        self._tokenized_corpus: list[list[str]] = []

        if corpus:
            self.add_documents(corpus)

    def add_documents(self, documents: list[str]) -> None:
        """
        Add documents to the BM25 index.

        Args:
            documents: list of document texts
        """
        from rank_bm25 import BM25Okapi

        # Append new documents
        new_tokenized = [self._tokenize(doc) for doc in documents]
        self._corpus.extend(documents)
        self._tokenized_corpus.extend(new_tokenized)

        # Rebuild index
        if self._tokenized_corpus:
            self._index = BM25Okapi(self._tokenized_corpus)

    def _tokenize(self, text: str) -> list[str]:
        """
        Simple whitespace + lowercase tokenization.
        Subclasses can override for language-specific tokenization.
        """
        return text.lower().split()

    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        """
        Search for top_k documents most relevant to query.

        Args:
            query: search query text
            top_k: number of top results to return

        Returns:
            list of (doc_index, score) tuples, sorted by score descending.
            Returns empty list if index is empty.
        """
        if not self._index or not self._corpus:
            return []

        tokenized_query = self._tokenize(query)
        scores = self._index.get_scores(tokenized_query)

        # Get top-k indices sorted by score
        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        return [(i, float(scores[i])) for i in top_indices if scores[i] > 0]

    def get_document(self, index: int) -> Optional[str]:
        """Get document text by index."""
        if 0 <= index < len(self._corpus):
            return self._corpus[index]
        return None

    def __len__(self) -> int:
        """Return number of indexed documents."""
        return len(self._corpus)

    def clear(self) -> None:
        """Clear all indexed documents."""
        self._corpus.clear()
        self._tokenized_corpus.clear()
        self._index = None
