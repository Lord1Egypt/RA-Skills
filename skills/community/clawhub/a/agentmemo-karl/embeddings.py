"""Embedding generation, HNSW indexing, and search for agentMemo v3.0.0."""
from __future__ import annotations
import logging
import threading
from collections import OrderedDict
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

_model = None
_lock = threading.Lock()


class EmbeddingCache:
    """Thread-safe LRU cache for embeddings."""

    def __init__(self, maxsize: int = 8192):
        self.maxsize = maxsize
        self._cache: OrderedDict[str, bytes] = OrderedDict()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get(self, text: str) -> Optional[bytes]:
        with self._lock:
            if text in self._cache:
                self._cache.move_to_end(text)
                self.hits += 1
                return self._cache[text]
            self.misses += 1
            return None

    def put(self, text: str, embedding: bytes):
        with self._lock:
            if text in self._cache:
                self._cache.move_to_end(text)
                self._cache[text] = embedding
            else:
                self._cache[text] = embedding
                if len(self._cache) > self.maxsize:
                    self._cache.popitem(last=False)

    @property
    def size(self) -> int:
        return len(self._cache)


embedding_cache = EmbeddingCache()


class HNSWIndex:
    """HNSW approximate nearest neighbor index using hnswlib."""

    def __init__(self, dim: int = 384, max_elements: int = 100000, ef_construction: int = 200, M: int = 16):
        self.dim = dim
        self.max_elements = max_elements
        self._index = None
        self._id_map: dict[int, str] = {}  # internal_id -> memory_id
        self._reverse_map: dict[str, int] = {}  # memory_id -> internal_id
        self._next_id = 0
        self._lock = threading.Lock()
        self.ef_construction = ef_construction
        self.M = M

    def _ensure_index(self):
        if self._index is None:
            import hnswlib
            self._index = hnswlib.Index(space='cosine', dim=self.dim)
            self._index.init_index(max_elements=self.max_elements, ef_construction=self.ef_construction, M=self.M)
            self._index.set_ef(50)

    def add(self, memory_id: str, embedding: bytes):
        vec = np.frombuffer(embedding, dtype=np.float32)
        if len(vec) != self.dim:
            return
        with self._lock:
            self._ensure_index()
            if memory_id in self._reverse_map:
                return
            internal_id = self._next_id
            self._next_id += 1
            # Resize if needed
            if internal_id >= self.max_elements:
                self._index.resize_index(self.max_elements * 2)
                self.max_elements *= 2
            self._index.add_items(vec.reshape(1, -1), np.array([internal_id]))
            self._id_map[internal_id] = memory_id
            self._reverse_map[memory_id] = internal_id

    def remove(self, memory_id: str):
        with self._lock:
            if memory_id in self._reverse_map:
                internal_id = self._reverse_map.pop(memory_id)
                if self._index is not None:
                    try:
                        self._index.mark_deleted(internal_id)
                    except Exception:
                        pass
                self._id_map.pop(internal_id, None)

    def search(self, query_embedding: bytes, k: int = 10) -> list[tuple[str, float]]:
        vec = np.frombuffer(query_embedding, dtype=np.float32)
        if len(vec) != self.dim:
            return []
        with self._lock:
            if self._index is None or len(self._id_map) == 0:
                return []
            actual_k = min(k, len(self._id_map))
            if actual_k == 0:
                return []
            try:
                labels, distances = self._index.knn_query(vec.reshape(1, -1), k=actual_k)
            except Exception:
                return []
            results = []
            for label, dist in zip(labels[0], distances[0]):
                mid = self._id_map.get(int(label))
                if mid:
                    # hnswlib cosine distance = 1 - cosine_similarity
                    score = 1.0 - float(dist)
                    results.append((mid, score))
            return results

    @property
    def size(self) -> int:
        return len(self._reverse_map)


hnsw_index = HNSWIndex()


def get_model():
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer
                logger.info("Loading embedding model all-MiniLM-L6-v2...")
                _model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Embedding model loaded.")
    return _model


def embed_text(text: str) -> bytes:
    cached = embedding_cache.get(text)
    if cached is not None:
        return cached
    model = get_model()
    vec = model.encode(text, normalize_embeddings=True)
    result = np.array(vec, dtype=np.float32).tobytes()
    embedding_cache.put(text, result)
    return result


def embed_batch(texts: list[str]) -> list[bytes]:
    results: list[Optional[bytes]] = [None] * len(texts)
    to_encode: list[tuple[int, str]] = []

    for i, text in enumerate(texts):
        cached = embedding_cache.get(text)
        if cached is not None:
            results[i] = cached
        else:
            to_encode.append((i, text))

    if to_encode:
        model = get_model()
        batch_texts = [t for _, t in to_encode]
        vecs = model.encode(batch_texts, normalize_embeddings=True, batch_size=min(64, len(batch_texts)))
        for (idx, text), vec in zip(to_encode, vecs):
            emb_bytes = np.array(vec, dtype=np.float32).tobytes()
            embedding_cache.put(text, emb_bytes)
            results[idx] = emb_bytes

    return results  # type: ignore


def embedding_from_bytes(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def search_memories_semantic(query: str, memories: list[dict], limit: int = 10,
                             min_score: float = 0.3, budget_tokens: Optional[int] = None,
                             use_hnsw: bool = True) -> tuple[list[dict], int]:
    query_emb = embed_text(query)

    if use_hnsw and hnsw_index.size > 0:
        # Use HNSW for approximate search, fetch more candidates than needed
        hnsw_results = hnsw_index.search(query_emb, k=min(limit * 3, hnsw_index.size))
        mem_by_id = {m["id"]: m for m in memories}
        scored = []
        for mid, score in hnsw_results:
            if score >= min_score and mid in mem_by_id:
                mem = mem_by_id[mid]
                scored.append({
                    "id": mem["id"], "text": mem["text"], "namespace": mem["namespace"],
                    "score": round(score, 4), "effective_importance": mem["effective_importance"],
                    "metadata": mem["metadata"], "tags": mem.get("tags", []),
                    "created_at": mem["created_at"],
                })
    else:
        # Brute-force fallback
        query_vec = embedding_from_bytes(query_emb)
        scored = []
        for mem in memories:
            if not mem.get("embedding"):
                continue
            mem_emb = embedding_from_bytes(mem["embedding"])
            score = cosine_similarity(query_vec, mem_emb)
            if score >= min_score:
                scored.append({
                    "id": mem["id"], "text": mem["text"], "namespace": mem["namespace"],
                    "score": round(score, 4), "effective_importance": mem["effective_importance"],
                    "metadata": mem["metadata"], "tags": mem.get("tags", []),
                    "created_at": mem["created_at"],
                })

    scored.sort(key=lambda x: x["score"] * (0.7 + 0.3 * x["effective_importance"]), reverse=True)
    scored = scored[:limit]

    total_tokens = 0
    if budget_tokens:
        filtered = []
        for item in scored:
            tokens = len(item["text"]) // 4 + 1
            if total_tokens + tokens <= budget_tokens:
                total_tokens += tokens
                filtered.append(item)
        return filtered, total_tokens
    else:
        total_tokens = sum(len(item["text"]) // 4 + 1 for item in scored)
        return scored, total_tokens


def search_memories_keyword(query: str, memories: list[dict], limit: int = 10,
                            budget_tokens: Optional[int] = None) -> tuple[list[dict], int]:
    query_lower = query.lower()
    query_terms = query_lower.split()
    scored = []

    for mem in memories:
        text_lower = mem["text"].lower()
        # Simple TF-based scoring
        term_hits = sum(1 for term in query_terms if term in text_lower)
        if term_hits == 0:
            continue
        score = term_hits / len(query_terms)
        scored.append({
            "id": mem["id"], "text": mem["text"], "namespace": mem["namespace"],
            "score": round(score, 4), "effective_importance": mem["effective_importance"],
            "metadata": mem["metadata"], "tags": mem.get("tags", []),
            "created_at": mem["created_at"],
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    scored = scored[:limit]

    total_tokens = 0
    if budget_tokens:
        filtered = []
        for item in scored:
            tokens = len(item["text"]) // 4 + 1
            if total_tokens + tokens <= budget_tokens:
                total_tokens += tokens
                filtered.append(item)
        return filtered, total_tokens
    else:
        total_tokens = sum(len(item["text"]) // 4 + 1 for item in scored)
        return scored, total_tokens


def search_memories_hybrid(query: str, memories: list[dict], limit: int = 10,
                           min_score: float = 0.3, budget_tokens: Optional[int] = None) -> tuple[list[dict], int]:
    """Reciprocal rank fusion of semantic and keyword results."""
    semantic_results, _ = search_memories_semantic(query, memories, limit=limit * 2, min_score=min_score)
    keyword_results, _ = search_memories_keyword(query, memories, limit=limit * 2)

    k = 60  # RRF constant
    rrf_scores: dict[str, float] = {}
    result_map: dict[str, dict] = {}

    for rank, item in enumerate(semantic_results):
        rrf_scores[item["id"]] = rrf_scores.get(item["id"], 0) + 1.0 / (k + rank + 1)
        result_map[item["id"]] = item

    for rank, item in enumerate(keyword_results):
        rrf_scores[item["id"]] = rrf_scores.get(item["id"], 0) + 1.0 / (k + rank + 1)
        if item["id"] not in result_map:
            result_map[item["id"]] = item

    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:limit]
    scored = []
    for mid in sorted_ids:
        item = result_map[mid]
        item["score"] = round(rrf_scores[mid], 4)
        scored.append(item)

    total_tokens = 0
    if budget_tokens:
        filtered = []
        for item in scored:
            tokens = len(item["text"]) // 4 + 1
            if total_tokens + tokens <= budget_tokens:
                total_tokens += tokens
                filtered.append(item)
        return filtered, total_tokens
    else:
        total_tokens = sum(len(item["text"]) // 4 + 1 for item in scored)
        return scored, total_tokens


def search_memories(query: str, memories: list[dict], limit: int = 10,
                    min_score: float = 0.3, budget_tokens: Optional[int] = None,
                    mode: str = "semantic") -> tuple[list[dict], int]:
    if mode == "keyword":
        return search_memories_keyword(query, memories, limit=limit, budget_tokens=budget_tokens)
    elif mode == "hybrid":
        return search_memories_hybrid(query, memories, limit=limit, min_score=min_score, budget_tokens=budget_tokens)
    else:
        return search_memories_semantic(query, memories, limit=limit, min_score=min_score, budget_tokens=budget_tokens)
