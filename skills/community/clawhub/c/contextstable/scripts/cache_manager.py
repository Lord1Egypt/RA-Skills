import hashlib
import json
import pickle
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime, timedelta
from collections import OrderedDict
import threading


class EmbeddingCache:
    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: int = 3600,
        persist_path: str = None
    ):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.persist_path = Path(persist_path) if persist_path else None
        self._cache: OrderedDict = OrderedDict()
        self._timestamps: Dict[str, datetime] = {}
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

        if self.persist_path and self.persist_path.exists():
            self._load_from_disk()

    def _get_hash(self, text: str) -> str:
        normalized = ' '.join(text.split())
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()

    def get(self, text: str) -> Optional[List[float]]:
        with self._lock:
            text_hash = self._get_hash(text)

            if text_hash in self._cache:
                timestamp = self._timestamps.get(text_hash)
                if timestamp and datetime.now() - timestamp > timedelta(seconds=self.ttl_seconds):
                    del self._cache[text_hash]
                    del self._timestamps[text_hash]
                    self._misses += 1
                    return None

                self._cache.move_to_end(text_hash)
                self._hits += 1
                return self._cache[text_hash]

            self._misses += 1
            return None

    def set(self, text: str, embedding: List[float]):
        with self._lock:
            text_hash = self._get_hash(text)

            if len(self._cache) >= self.max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                if oldest_key in self._timestamps:
                    del self._timestamps[oldest_key]

            self._cache[text_hash] = embedding
            self._timestamps[text_hash] = datetime.now()
            self._cache.move_to_end(text_hash)

    def get_or_compute(self, text: str, compute_func) -> List[float]:
        cached = self.get(text)
        if cached is not None:
            return cached

        embedding = compute_func(text)
        self.set(text, embedding)
        return embedding

    def batch_get_or_compute(
        self,
        texts: List[str],
        compute_func
    ) -> List[List[float]]:
        results = []
        uncached_texts = []
        uncached_indices = []

        for i, text in enumerate(texts):
            cached = self.get(text)
            if cached is not None:
                results.append(cached)
            else:
                results.append(None)
                uncached_texts.append(text)
                uncached_indices.append(i)

        if uncached_texts:
            new_embeddings = compute_func(uncached_texts)
            for text, embedding in zip(uncached_texts, new_embeddings):
                self.set(text, embedding)

            for idx, embedding in zip(uncached_indices, new_embeddings):
                results[idx] = embedding

        return results

    def clear(self):
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
            self._hits = 0
            self._misses = 0

    def cleanup_expired(self):
        with self._lock:
            now = datetime.now()
            expired_keys = [
                key for key, timestamp in self._timestamps.items()
                if now - timestamp > timedelta(seconds=self.ttl_seconds)
            ]
            for key in expired_keys:
                if key in self._cache:
                    del self._cache[key]
                del self._timestamps[key]

    def save_to_disk(self):
        if not self.persist_path:
            return

        with self._lock:
            data = {
                'cache': dict(self._cache),
                'timestamps': {k: v.isoformat() for k, v in self._timestamps.items()}
            }

            self.persist_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.persist_path, 'wb') as f:
                pickle.dump(data, f)

    def _load_from_disk(self):
        if not self.persist_path or not self.persist_path.exists():
            return

        try:
            with open(self.persist_path, 'rb') as f:
                data = pickle.load(f)

            with self._lock:
                self._cache = OrderedDict(data.get('cache', {}))
                self._timestamps = {
                    k: datetime.fromisoformat(v)
                    for k, v in data.get('timestamps', {}).items()
                }
        except Exception:
            pass

    def get_statistics(self) -> Dict[str, Any]:
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0

        return {
            'cache_size': len(self._cache),
            'max_size': self.max_size,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': f"{hit_rate:.1%}",
            'ttl_seconds': self.ttl_seconds
        }


class PromptCache:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.Lock()

    def _get_key(self, user_prompt: str, context_hash: str) -> str:
        combined = f"{user_prompt}|{context_hash}"
        return hashlib.md5(combined.encode('utf-8')).hexdigest()

    def get_enhanced_prompt(self, user_prompt: str, context: str) -> Optional[str]:
        context_hash = hashlib.md5(context.encode('utf-8')).hexdigest()
        key = self._get_key(user_prompt, context_hash)

        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                return self._cache[key]
        return None

    def set_enhanced_prompt(self, user_prompt: str, context: str, enhanced_prompt: str):
        context_hash = hashlib.md5(context.encode('utf-8')).hexdigest()
        key = self._get_key(user_prompt, context_hash)

        with self._lock:
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)

            self._cache[key] = enhanced_prompt

    def clear(self):
        with self._lock:
            self._cache.clear()


class ContextSummaryCache:
    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self._summaries: OrderedDict = OrderedDict()
        self._lock = threading.Lock()

    def get_summary(self, content_hash: str) -> Optional[str]:
        with self._lock:
            if content_hash in self._summaries:
                self._summaries.move_to_end(content_hash)
                return self._summaries[content_hash]
        return None

    def set_summary(self, content_hash: str, summary: str):
        with self._lock:
            if len(self._summaries) >= self.max_size:
                self._summaries.popitem(last=False)

            self._summaries[content_hash] = summary

    def get_or_create_summary(
        self,
        content: str,
        summarize_func
    ) -> str:
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()

        cached = self.get_summary(content_hash)
        if cached is not None:
            return cached

        summary = summarize_func(content)
        self.set_summary(content_hash, summary)
        return summary


class CacheManager:
    def __init__(
        self,
        embedding_cache_size: int = 1000,
        prompt_cache_size: int = 100,
        summary_cache_size: int = 50,
        ttl_seconds: int = 3600,
        persist_dir: str = None
    ):
        persist_path = None
        if persist_dir:
            persist_path = Path(persist_dir) / 'embedding_cache.pkl'

        self.embedding_cache = EmbeddingCache(
            max_size=embedding_cache_size,
            ttl_seconds=ttl_seconds,
            persist_path=str(persist_path) if persist_path else None
        )
        self.prompt_cache = PromptCache(max_size=prompt_cache_size)
        self.summary_cache = ContextSummaryCache(max_size=summary_cache_size)

    def get_all_statistics(self) -> Dict[str, Any]:
        return {
            'embedding_cache': self.embedding_cache.get_statistics(),
            'prompt_cache': {
                'size': len(self.prompt_cache._cache),
                'max_size': self.prompt_cache.max_size
            },
            'summary_cache': {
                'size': len(self.summary_cache._summaries),
                'max_size': self.summary_cache.max_size
            }
        }

    def clear_all(self):
        self.embedding_cache.clear()
        self.prompt_cache.clear()
        self.summary_cache._summaries.clear()

    def save_all(self):
        self.embedding_cache.save_to_disk()

    def cleanup(self):
        self.embedding_cache.cleanup_expired()
