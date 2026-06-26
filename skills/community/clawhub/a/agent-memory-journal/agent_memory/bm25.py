from __future__ import annotations

import math
from collections import Counter

import json
import hashlib
from pathlib import Path

from .normalize import normalize_claim

NORMALIZER_VERSION = 2


class BM25Index:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.k1 = k1
        self.b = b
        self.doc_tokens = [normalize_claim(doc)[1] for doc in docs]
        self.doc_freqs = [Counter(tokens) for tokens in self.doc_tokens]
        self.doc_lens = [len(tokens) for tokens in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / len(self.doc_lens) if self.doc_lens else 0.0
        self.idf = self._build_idf()

    @classmethod
    def from_cache(cls, cache_path: Path, docs: list[str], k1: float = 1.5, b: float = 0.75):
        # Hash docs to see if cache is valid
        docs_hash = hashlib.sha256("\n".join(docs).encode("utf-8")).hexdigest()
        if cache_path.exists():
            try:
                data = json.loads(cache_path.read_text(encoding="utf-8"))
                if data.get("hash") == docs_hash and data.get("normalizer_version") == NORMALIZER_VERSION:
                    instance = cls.__new__(cls)
                    instance.docs = docs
                    instance.k1 = k1
                    instance.b = b
                    instance.doc_tokens = data["doc_tokens"]
                    instance.doc_freqs = [Counter(d) for d in data["doc_freqs"]]
                    instance.doc_lens = data["doc_lens"]
                    instance.avgdl = data["avgdl"]
                    instance.idf = data["idf"]
                    return instance
            except Exception:
                pass
        
        instance = cls(docs, k1, b)
        # Save to cache
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps({
                "hash": docs_hash,
                "normalizer_version": NORMALIZER_VERSION,
                "doc_tokens": instance.doc_tokens,
                "doc_freqs": [dict(f) for f in instance.doc_freqs],
                "doc_lens": instance.doc_lens,
                "avgdl": instance.avgdl,
                "idf": instance.idf
            }), encoding="utf-8")
        except Exception:
            pass
        return instance

    def _build_idf(self) -> dict[str, float]:
        df = Counter()
        for tokens in self.doc_tokens:
            for token in set(tokens):
                df[token] += 1
        total = len(self.doc_tokens)
        return {
            token: math.log(1 + (total - freq + 0.5) / (freq + 0.5))
            for token, freq in df.items()
        }

    def score(self, query: str) -> list[float]:
        q_tokens = normalize_claim(query)[1]
        scores: list[float] = []
        for freqs, doc_len in zip(self.doc_freqs, self.doc_lens):
            total = 0.0
            for token in q_tokens:
                if token not in freqs:
                    continue
                tf = freqs[token]
                idf = self.idf.get(token, 0.0)
                denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl if self.avgdl else 0.0))
                total += idf * ((tf * (self.k1 + 1)) / denom)
            scores.append(total)
        return scores
