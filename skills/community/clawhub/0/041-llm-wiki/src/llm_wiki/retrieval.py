"""
Embedding 检索引擎

负责索引构建、缓存管理和混合搜索。
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .core import WikiManager, WikiPage
from .embeddings import EmbeddingProvider


class EmbeddingIndex:
    """基于 embedding 的 wiki 页面索引"""

    def __init__(self, wiki: WikiManager, provider: EmbeddingProvider):
        self.wiki = wiki
        self.provider = provider
        self.cache_path = wiki.wiki_dir / ".cache" / "embeddings.json"
        self.cache: Dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        if self.cache_path.exists():
            try:
                self.cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
            except Exception:
                self.cache = {}
        else:
            self.cache = {}

    def _save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


    def build(self, force: bool = False) -> Tuple[int, int]:
        """
        构建或增量更新 embedding 索引。

        返回: (indexed_count, skipped_count)
        """
        pages = self.wiki.list_pages()
        provider_name = self.provider.name
        model = getattr(self.provider, "model", "")

        # 检查缓存是否需要重建
        if force or self.cache.get("provider") != provider_name or self.cache.get("model") != model:
            self.cache = {
                "version": 1,
                "provider": provider_name,
                "model": model,
                "dimension": self.provider.dimension,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "pages": {},
            }
            force = True

        if "pages" not in self.cache:
            self.cache["pages"] = {}

        to_embed: List[Tuple[str, WikiPage]] = []
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
            now = datetime.now().isoformat()
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

        self.cache["updated_at"] = datetime.now().isoformat()
        self._save_cache()
        return indexed, skipped

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        keyword_weight: float = 0.3,
        vector_weight: float = 0.5,
        link_weight: float = 0.2,
        enable_link_traversal: bool = True,
    ) -> List[Tuple[str, float]]:
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
        scores: Dict[str, float] = {}

        # 1. Keyword Match
        for title, page in pages.items():
            kw_score = 0.0
            if query_lower in title.lower():
                kw_score += 1.0
            for tag in page.tags:
                if query_lower in tag.lower():
                    kw_score += 0.5
                    break
            if query_lower in page.content.lower():
                kw_score += 0.2
            scores[title] = kw_score * keyword_weight

        # 2. Vector Search
        query_vec = np.array(self.provider.embed_query(query), dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            query_norm = 1.0

        for title, record in self.cache["pages"].items():
            if title not in pages:
                continue
            vec = np.array(record["embedding"], dtype=np.float32)
            vec_norm = np.linalg.norm(vec)
            if vec_norm == 0:
                vec_norm = 1.0
            similarity = float(np.dot(query_vec, vec) / (query_norm * vec_norm))
            # 将 [-1, 1] 映射到 [0, 1]
            similarity = (similarity + 1.0) / 2.0
            scores[title] = scores.get(title, 0.0) + similarity * vector_weight

        # 3. Link Traversal
        if enable_link_traversal and link_weight > 0:
            # 取当前 keyword + vector 的 top_k 作为种子
            seed_titles = [
                t for t, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
            ]
            link_boosts: Dict[str, float] = {}
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
