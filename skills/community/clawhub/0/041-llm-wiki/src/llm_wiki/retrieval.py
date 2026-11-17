"""
Embedding 检索引擎

负责索引构建、缓存管理和混合搜索。
"""

import json
from datetime import UTC, datetime
from typing import Any

import numpy as np

from .bm25 import BM25, tokenize
from .core import WikiManager, WikiPage
from .embeddings import EmbeddingProvider


class EmbeddingIndex:
    """基于 embedding 的 wiki 页面索引"""

    def __init__(self, wiki: WikiManager, provider: EmbeddingProvider):
        self.wiki = wiki
        self.provider = provider
        self.cache_path = wiki.wiki_dir / ".cache" / "embeddings.json"
        self.cache: dict[str, Any] = {}
        self._vector_signature: tuple[tuple[str, str, str], ...] = ()
        self._vector_titles: tuple[str, ...] = ()
        self._normalized_matrix = np.empty((0, 0), dtype=np.float32)
        self._load_cache()

    def _load_cache(self) -> None:
        if self.cache_path.exists():
            try:
                self.cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError, TypeError, ValueError):
                self.cache = {}
        else:
            self.cache = {}

    def _invalidate_vector_cache(self) -> None:
        self._vector_signature = ()
        self._vector_titles = ()
        self._normalized_matrix = np.empty((0, 0), dtype=np.float32)

    def _ensure_vector_matrix(
        self, page_titles: set[str]
    ) -> tuple[tuple[str, ...], np.ndarray]:
        cached_items = [
            (title, record)
            for title, record in self.cache.get("pages", {}).items()
            if title in page_titles and "embedding" in record
        ]
        signature = tuple(
            (title, str(record.get("hash", "")), str(record.get("updated_at", "")))
            for title, record in cached_items
        )
        if signature != self._vector_signature:
            if not cached_items:
                self._invalidate_vector_cache()
                return self._vector_titles, self._normalized_matrix
            matrix = np.asarray(
                [record["embedding"] for _, record in cached_items],
                dtype=np.float32,
            )
            if matrix.ndim != 2:
                raise ValueError("Embedding cache must contain equal-length vectors")
            norms = np.linalg.norm(matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self._vector_signature = signature
            self._vector_titles = tuple(title for title, _ in cached_items)
            self._normalized_matrix = matrix / norms
        return self._vector_titles, self._normalized_matrix

    def _save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def build(self, force: bool = False) -> tuple[int, int]:
        """
        构建或增量更新 embedding 索引。

        返回: (indexed_count, skipped_count)
        """
        pages = self.wiki.list_pages()
        provider_name = self.provider.name
        model = getattr(self.provider, "model", "")

        # 检查缓存是否需要重建
        if (
            force
            or self.cache.get("provider") != provider_name
            or self.cache.get("model") != model
        ):
            self.cache = {
                "version": 1,
                "provider": provider_name,
                "model": model,
                "dimension": self.provider.dimension,
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": datetime.now(UTC).isoformat(),
                "pages": {},
            }
            force = True

        if "pages" not in self.cache:
            self.cache["pages"] = {}

        to_embed: list[tuple[str, WikiPage]] = []
        skipped = 0

        for page in pages:
            page_hash = page.content_hash
            cached = self.cache["pages"].get(page.title)
            if not force and cached and cached.get("hash") == page_hash:
                skipped += 1
            else:
                to_embed.append((page_hash, page))

        indexed = 0
        if to_embed:
            texts = [p.content for _, p in to_embed]
            embeddings = self.provider.embed(texts)
            now = datetime.now(UTC).isoformat()
            for (page_hash, page), vec in zip(to_embed, embeddings):
                self.cache["pages"][page.title] = {
                    "hash": page_hash,
                    "updated_at": now,
                    "embedding": vec,
                }
                indexed += 1

        # 清理已删除页面
        current_titles = {p.title for p in pages}
        stale_titles = [t for t in self.cache["pages"] if t not in current_titles]
        for t in stale_titles:
            del self.cache["pages"][t]

        self.cache["updated_at"] = datetime.now(UTC).isoformat()
        self._invalidate_vector_cache()
        self._save_cache()
        return indexed, skipped

    def search(
        self,
        query: str,
        top_k: int | None = None,
        keyword_weight: float = 0.3,
        vector_weight: float = 0.5,
        link_weight: float = 0.2,
        enable_link_traversal: bool = True,
    ) -> list[tuple[str, float]]:
        """
        混合搜索：Keyword + Vector + Link Traversal

        返回: [(page_title, score), ...] 按 score 降序排列
        """
        if top_k is None:
            top_k = 10

        if not self.cache or not self.cache.get("pages"):
            return []

        pages = {p.title: p for p in self.wiki.list_pages()}
        query_lower = query.lower()
        scores: dict[str, float] = {}

        # 1. Keyword Match:标题/标签子串为强信号,内容相关性用 BM25 词项匹配
        corpus = BM25(
            [
                tokenize(f"{p.title} {' '.join(p.tags)} {p.content}")
                for p in pages.values()
            ]
        )
        raw_scores = corpus.scores(tokenize(query))
        bm25_scores = {
            title: (raw / (raw + corpus.k1) if raw > 0 else 0.0)
            for title, raw in zip(pages.keys(), raw_scores)
        }
        for title, page in pages.items():
            kw_score = 0.0
            if query_lower in title.lower():
                kw_score += 1.0
            for tag in page.tags:
                if query_lower in tag.lower():
                    kw_score += 0.5
                    break
            kw_score += 0.3 * bm25_scores.get(title, 0.0)
            scores[title] = kw_score * keyword_weight

        # 2. Vector Search (cached normalized matrix + one BLAS matvec)
        if vector_weight > 0 and self.cache.get("pages"):
            query_vec = np.asarray(self.provider.embed_query(query), dtype=np.float32)
            query_norm = np.linalg.norm(query_vec)
            norm_query = (query_vec / query_norm) if query_norm > 0 else query_vec
            titles, norm_matrix = self._ensure_vector_matrix(set(pages))
            if titles:
                if norm_matrix.shape[1] != norm_query.shape[0]:
                    raise ValueError(
                        "Query embedding dimension does not match the cached page embeddings"
                    )
                sims = (norm_matrix @ norm_query + 1.0) / 2.0
                for title, sim in zip(titles, sims):
                    scores[title] = scores.get(title, 0.0) + float(sim) * vector_weight

        # 3. Link Traversal
        if enable_link_traversal and link_weight > 0:
            # 取当前 keyword + vector 的 top_k 作为种子
            seed_titles = [
                t
                for t, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[
                    :top_k
                ]
            ]
            link_boosts: dict[str, float] = {}
            visited: set = set()

            for seed in seed_titles:
                page = pages.get(seed)
                if not page:
                    continue
                for link in page.links:
                    if link in pages and link not in link_boosts:
                        link_boosts[link] = link_weight * 0.5
                        visited.add(link)

            for hop1 in list(visited):
                page = pages.get(hop1)
                if not page:
                    continue
                for link in page.links:
                    if link in pages and link not in link_boosts:
                        link_boosts[link] = link_weight * 0.25

            for title, boost in link_boosts.items():
                scores[title] = scores.get(title, 0.0) + boost

        # 排序并返回 top_k
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:top_k]
