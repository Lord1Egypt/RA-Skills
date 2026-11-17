import hashlib
import json
import numpy as np
from pathlib import Path


class VectorRecognizer:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or "sentence-transformers/all-MiniLM-L6-v2"
        self._model = None
        self._fallback = False
        self._cache: dict[str, list[float]] = {}

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                self._fallback = True
        return self._model

    def _hash_embedding(self, text: str, dim: int = 384) -> list[float]:
        # 本地确定性哈希回退，保证离线/无模型时仍可运行
        raw = text.encode("utf-8")
        vec = []
        while len(vec) < dim:
            raw = hashlib.sha256(raw).digest()
            vec.extend(list(raw))
        vec = np.array(vec[:dim], dtype=np.float32)
        norm = np.linalg.norm(vec)
        return (vec / (norm + 1e-10)).tolist()

    def encode(self, text: str) -> list[float]:
        model = self._load_model()
        if self._fallback or model is None:
            return self._hash_embedding(text)
        vec = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
        return vec.tolist()

    def cosine_similarity(self, a: list[float], b: list[float]) -> float:
        na = np.array(a)
        nb = np.array(b)
        return float(np.dot(na, nb) / (np.linalg.norm(na) * np.linalg.norm(nb) + 1e-10))

    def match_modules(self, requirement_text: str, module_vectors: dict[str, list[float]]) -> dict:
        req_vec = self.encode(requirement_text)
        scores = {
            mid: self.cosine_similarity(req_vec, vec)
            for mid, vec in module_vectors.items()
        }
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        return {
            "requirement_vector": req_vec,
            "scores": sorted_scores,
            "high_confidence": [k for k, v in sorted_scores.items() if v >= 0.75],
            "low_confidence": [k for k, v in sorted_scores.items() if 0.45 <= v < 0.75],
        }
