"""
core/embedding.py — Embedding Provider Abstraction v1.2.41
支持 MiniLM / Voyage / OpenAI / Ollama / BGE-M3
v1.2.41: 升级 BAAI/bge-m3 (1024-dim, 多语言支持)
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union
import json
import os
import re

import numpy as np


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass
class EmbedConfig:
    """User configuration for embedding provider."""
    provider: str = "minilm"  # minilm | voyage | openai | ollama | bge
    model: str = "all-MiniLM-L6-v2"
    api_key: str = ""
    base_url: str = ""
    dimension: int = 384
    timeout: float = 30.0

    @classmethod
    def from_dict(cls, d: dict) -> "EmbedConfig":
        return cls(
            provider=d.get("provider", "minilm"),
            model=d.get("model", "all-MiniLM-L6-v2"),
            api_key=d.get("api_key", ""),
            base_url=d.get("base_url", ""),
            dimension=int(d.get("dimension", 384)),
            timeout=float(d.get("timeout", 30.0)),
        )

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "model": self.model,
            "api_key": self.api_key,
            "base_url": self.base_url,
            "dimension": self.dimension,
            "timeout": self.timeout,
        }


# ---------------------------------------------------------------------------
# Base Provider
# ---------------------------------------------------------------------------

class EmbedProvider(ABC):
    """Abstract base for all embedding providers."""

    def __init__(self, config: EmbedConfig):
        self.config = config

    @abstractmethod
    def encode(self, texts: Union[str, list[str]]) -> np.ndarray:
        """
        Encode text(s) into embedding vector(s).
        Returns shape (dim,) for single string, (n, dim) for list.
        """

    def provider_name(self) -> str:
        return self.config.provider


# ---------------------------------------------------------------------------
# MiniLM (local, sentence-transformers)
# ---------------------------------------------------------------------------

class MiniLMProvider(EmbedProvider):
    """Local MiniLM via sentence-transformers."""

    _model = None

    def encode(self, texts: Union[str, list[str]]) -> np.ndarray:
        if MiniLMProvider._model is None:
            from sentence_transformers import SentenceTransformer
            MiniLMProvider._model = SentenceTransformer(
                self.config.model or "all-MiniLM-L6-v2",
                local_files_only=True,  # 避免网络超时，从本地缓存加载
            )
        return MiniLMProvider._model.encode(texts)


# ---------------------------------------------------------------------------
# Voyage AI
# ---------------------------------------------------------------------------

class VoyageProvider(EmbedProvider):
    """Voyage AI API."""

    DEFAULT_URL = "https://api.voyageai.com/v1/embeddings"

    def encode(self, texts: Union[str, list[str]]) -> np.ndarray:
        import httpx

        input_list = [texts] if isinstance(texts, str) else texts
        payload = {
            "input": input_list,
            "model": self.config.model or "voyage-2",
        }
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        base = self.config.base_url or self.DEFAULT_URL
        r = httpx.post(base, json=payload, headers=headers, timeout=self.config.timeout)
        r.raise_for_status()
        data = r.json()["data"]
        vecs = [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]
        result = np.array(vecs)
        return result[0] if isinstance(texts, str) else result


# ---------------------------------------------------------------------------
# OpenAI (ada-002 / text-embedding-3)
# ---------------------------------------------------------------------------

class OpenAIEmbedProvider(EmbedProvider):
    """OpenAI Embeddings API."""

    DEFAULT_URL = "https://api.openai.com/v1/embeddings"

    def encode(self, texts: Union[str, list[str]]) -> np.ndarray:
        import httpx

        input_list = [texts] if isinstance(texts, str) else texts
        payload = {
            "input": input_list,
            "model": self.config.model or "text-embedding-ada-002",
        }
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        base = self.config.base_url or self.DEFAULT_URL
        r = httpx.post(f"{base}/embeddings", json=payload, headers=headers, timeout=self.config.timeout)
        r.raise_for_status()
        data = r.json()["data"]
        vecs = [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]
        result = np.array(vecs)
        return result[0] if isinstance(texts, str) else result


# ---------------------------------------------------------------------------
# Ollama (local)
# ---------------------------------------------------------------------------

class OllamaEmbedProvider(EmbedProvider):
    """Ollama embeddings API (nomic-embed-text etc.)."""

    DEFAULT_URL = "http://localhost:11434"

    def encode(self, texts: Union[str, list[str]]) -> np.ndarray:
        import httpx, json

        input_list = [texts] if isinstance(texts, str) else texts
        payload = {
            "model": self.config.model or "nomic-embed-text",
            "input": input_list,
        }
        base = self.config.base_url or self.DEFAULT_URL
        r = httpx.post(f"{base}/api/embeddings", json=payload, timeout=self.config.timeout)
        r.raise_for_status()
        return np.array(r.json()["embedding"])


# ---------------------------------------------------------------------------
# BGE-M3 Provider (v1.2.41 — 多语言, 1024-dim)
# ---------------------------------------------------------------------------

class BGEProvider(EmbedProvider):
    """BAAI/bge-m3 本地模型 via sentence-transformers.
    
    支持多语言（中英日韩等），维度 1024，比 MiniLM 的 384 维更强大。
    模型会自动从 huggingface 下载。
    """

    _model = None

    def encode(self, texts: Union[str, list[str]]) -> np.ndarray:
        if BGEProvider._model is None:
            from sentence_transformers import SentenceTransformer
            model_name = self.config.model or "BAAI/bge-m3"
            BGEProvider._model = SentenceTransformer(model_name)
        return BGEProvider._model.encode(texts)

    def encode_chunks(self, text: str, chunk_size: int = 256, chunk_overlap: int = 32) -> list[list[float]]:
        """
        Chunk long text by sentence boundaries and encode each chunk.

        算法：
        1. 用句子边界（。！？.!?\n）分割文本
        2. 按 chunk_size 组装相邻句子
        3. 相邻块重叠 chunk_overlap 字符

        Args:
            text: 待分块文本
            chunk_size: 每块目标字符数（默认 256）
            chunk_overlap: 块间重叠字符数（默认 32）

        Returns:
            list of embeddings, one per chunk
        """
        if not text or len(text.strip()) < 20:
            return []

        # 句子分割正则
        sentence_delimiters = re.compile(r'[。！？.!?\n]+')
        sentences = [s.strip() for s in sentence_delimiters.split(text) if s.strip()]

        if not sentences:
            return []

        # 滑动窗口构建 chunks
        chunks: list[str] = []
        start = 0
        while start < len(sentences):
            end = start + 1
            current_size = len(sentences[start])
            # 尽量填充到 chunk_size
            while end < len(sentences) and current_size + len(sentences[end]) + 1 < chunk_size:
                current_size += len(sentences[end]) + 1
                end += 1
            chunk_text = ' '.join(sentences[start:end])
            chunks.append(chunk_text)
            # 滑动：下次从重叠位置开始
            if end <= start:
                break
            start = end - 1
            # 重新确定下一轮起点，确保有进展
            overlap_chars = 0
            next_start = start
            while next_start < len(sentences) and overlap_chars < chunk_overlap:
                overlap_chars += len(sentences[next_start]) + 1
                next_start += 1
            start = max(start + 1, next_start - 1)
            if start >= len(sentences):
                break

        if not chunks:
            return []

        # 批量编码
        embeddings = self.encode(chunks)
        return [emb.tolist() for emb in embeddings]


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_PROVIDERS = {
    "minilm": MiniLMProvider,
    "voyage": VoyageProvider,
    "openai": OpenAIEmbedProvider,
    "ollama": OllamaEmbedProvider,
    "bge": BGEProvider,
}


def get_embed(config: EmbedConfig = None) -> EmbedProvider:
    """Factory: create EmbedProvider from config. Defaults to MiniLM."""
    if config is None:
        config = _load_embed_config()
    key = config.provider.lower()
    if key in ("ollama",):
        key = "ollama"
    provider_class = _PROVIDERS.get(key, MiniLMProvider)
    return provider_class(config)


def _load_embed_config() -> EmbedConfig:
    """Load embedding config from ~/.amber-hunter/config.json."""
    cfg_path = os.path.expanduser("~/.amber-hunter/config.json")
    if os.path.exists(cfg_path):
        try:
            data = json.loads(open(cfg_path).read())
            if "embedding" in data:
                return EmbedConfig.from_dict(data["embedding"])
        except Exception:
            pass
    return EmbedConfig()


def save_embed_config(config: EmbedConfig) -> None:
    """Save embedding config to ~/.amber-hunter/config.json."""
    import json
    cfg_path = os.path.expanduser("~/.amber-hunter/config.json")
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
    data = {}
    if os.path.exists(cfg_path):
        try:
            data = json.loads(open(cfg_path).read())
        except Exception:
            pass
    data["embedding"] = config.to_dict()
    open(cfg_path, "w").write(json.dumps(data, indent=2))


# ---------------------------------------------------------------------------
# Module-level provider singleton (lazy, cached)
# ---------------------------------------------------------------------------

_embed_provider_singleton: EmbedProvider | None = None


def get_cached_embed() -> EmbedProvider:
    """Get the cached global embedding provider instance."""
    global _embed_provider_singleton
    if _embed_provider_singleton is None:
        _embed_provider_singleton = get_embed()
    return _embed_provider_singleton


def reset_embed_provider() -> None:
    """Reset the cached provider (useful after config change)."""
    global _embed_provider_singleton
    _embed_provider_singleton = None


# ── Snippet Extraction v1.2.32 ─────────────────────────────────────────────

def find_snippets(
    content: str,
    query: str,
    window_chars: int = 200,
    step_chars: int = 100,
    top_k: int = 3,
    min_score: float = 0.3,
) -> list[dict]:
    """
    用 embedding 余弦相似度找出 content 中与 query 最相关的文本片段。

    算法：滑动窗口 + 向量相似度
    - window_chars: 窗口大小（默认 200 字符）
    - step_chars: 滑动步长（默认 100 字符）
    - top_k: 返回最多 top_k 个片段
    - min_score: 低于此分数的片段被过滤

    返回: [{"text": "...", "sim_score": 0.xx, "offset": N}, ...]
    按 sim_score 降序。
    """
    try:
        import numpy as _np
        provider = get_cached_embed()
        if not content or len(content.strip()) < 20:
            return []

        q_vec = provider.encode(query[:512])
        q_norm = _np.linalg.norm(q_vec) + 1e-8

        # 构建滑动窗口
        windows = []
        offset = 0
        while offset < len(content):
            end = min(offset + window_chars, len(content))
            # 尝试在句子边界结束
            if end < len(content):
                for punct in ('。', '！', '？', '.', '!', '?', '\n'):
                    last_punct = content.rfind(punct, offset, end)
                    if last_punct > offset + 50:
                        end = last_punct + 1
                        break
            window_text = content[offset:end].strip()
            if len(window_text) > 40:  # 太短的窗口跳过
                windows.append((offset, window_text))
            offset += step_chars

        if not windows:
            return []

        texts = [w[1] for w in windows]
        # 批量编码（限制每段最多 512 字符）
        texts_capped = [t[:512] for t in texts]
        w_vecs = provider.encode(texts_capped)

        # 计算每个窗口与 query 的余弦相似度
        scores = []
        for i, (offset, w_text) in enumerate(windows):
            v = w_vecs[i]
            norm = _np.linalg.norm(v) + 1e-8
            sim = float(_np.dot(q_vec, v) / (norm * q_norm))
            scores.append((sim, offset, w_text))

        scores.sort(key=lambda x: x[0], reverse=True)

        result = []
        seen_ranges = []
        for sim, offset, w_text in scores:
            if sim < min_score:
                break
            # 去重：跳过与已有结果高度重叠的窗口（offset 重叠 > 50%）
            overlaps = False
            for _, seen_end in seen_ranges:
                overlap = min(offset + window_chars, seen_end) - max(offset, seen_end - window_chars)
                if overlap > window_chars * 0.5:
                    overlaps = True
                    break
            if overlaps:
                continue
            result.append({
                "text": w_text,
                "sim_score": round(sim, 3),
                "offset": offset,
            })
            seen_ranges.append((offset, offset + len(w_text)))
            if len(result) >= top_k:
                break

        return result
    except Exception as e:
        import sys
        print(f"[embedding] find_snippets failed: {e}", file=sys.stderr)
        return []
