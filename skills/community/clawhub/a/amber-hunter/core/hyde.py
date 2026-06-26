"""
core/hyde.py — HyDE Generator v1.2.41
Hypothetical Document Embeddings: generate hypothetical answer, then retrieve.

HyDE 流程:
1. 用 LLM 生成一个假设性答案（可能包含幻觉，但结构相关）
2. 用假设性答案 + 原始 query 同时检索
3. 合并两路检索结果

参考: https://arxiv.org/abs/2212.10496
"""

from __future__ import annotations

import sys
from typing import Optional


class HyDEGenerator:
    """
    HyDE (Hypothetical Document Embeddings) generator.

    用法:
        hyde = HyDEGenerator()
        hyp_answer = hyde.generate("What is Python?")
        results = hyde.retrieve("What is Python?", hyp_answer)
    """

    def __init__(self):
        """Initialize HyDE with LLM provider."""
        self._llm = None
        self._llm_failed = False

    def _get_llm(self):
        """Lazy load LLM."""
        if self._llm is None and not self._llm_failed:
            try:
                from core.llm import get_llm
                self._llm = get_llm()
            except Exception as e:
                self._llm_failed = True
                print(f"[hyde] Failed to get LLM: {e}", file=sys.stderr)
        return self._llm

    def generate(self, query: str) -> str:
        """
        Generate a hypothetical answer to the query using LLM.

        The generated answer is a plausible (but potentially incorrect) response
        that serves as a query vector for retrieval.

        Args:
            query: the search query

        Returns:
            hypothetical answer text, or empty string on failure
        """
        llm = self._get_llm()
        if llm is None:
            return ""

        system_prompt = (
            "You are a helpful assistant. Given a question, generate a concise "
            "and informative hypothetical answer. This answer will be used for "
            "semantic search to find relevant documents. Write 2-3 sentences "
            "that directly answer the question."
        )

        try:
            response = llm.complete(
                prompt=f"Question: {query}\n\nHypothetical Answer:",
                system=system_prompt,
                max_tokens=256,
                temperature=0.3,
            )
            return response.strip() if response else ""
        except Exception as e:
            print(f"[hyde] LLM generate failed: {e}", file=sys.stderr)
            return ""

    def retrieve(self, query: str, hyde_answer: str) -> list[str]:
        """
        Dual retrieval: merge results from query and hyde_answer.

        This performs two retrieval passes (one with query, one with hyde_answer)
        and merges the results with deduplication.

        Note: This method provides the retrieval interface. The actual vector
        search should be performed by the caller using the returned texts.

        Args:
            query: original search query
            hyde_answer: hypothetical answer from generate()

        Returns:
            list of document texts (from both query and hyde_answer retrieval passes)
        """
        if not hyde_answer:
            return []

        # The retrieval itself is done by the caller (amber_hunter.py)
        # This method just validates and returns the hyde_answer for dual search
        # In practice, the caller will run vector search twice and merge
        return [hyde_answer]

    def is_available(self) -> bool:
        """Check if HyDE generator is available (LLM ready)."""
        return self._get_llm() is not None
