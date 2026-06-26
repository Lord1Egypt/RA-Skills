"""
文本向量化封装

提供统一的encode接口，单例模式，延迟加载。
"""

import sys
from pathlib import Path
from typing import List

# 确保技能根目录在path中
_SKILL_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)

from scripts.core.semantic_model import SemanticModel, EMBEDDING_DIM, serialize_vector


class Text2VecEmbedder:
    """文本向量化器（单例）"""

    _instance = None

    def __init__(self, lazy: bool = True):
        self._model = SemanticModel()
        self._loaded = False
        if not lazy:
            self._ensure_loaded()

    @classmethod
    def get_instance(cls) -> "Text2VecEmbedder":
        if cls._instance is None:
            cls._instance = cls(lazy=True)
        return cls._instance

    def _ensure_loaded(self):
        if not self._loaded:
            self._model.load()
            self._loaded = True

    @property
    def is_available(self) -> bool:
        self._ensure_loaded()
        return self._model.is_available

    @property
    def mode(self) -> str:
        self._ensure_loaded()
        return self._model.mode

    @property
    def dim(self) -> int:
        return EMBEDDING_DIM

    def encode(self, text: str) -> List[float]:
        self._ensure_loaded()
        return self._model.encode(text)

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        self._ensure_loaded()
        return self._model.encode_batch(texts)

    def encode_for_db(self, text: str) -> bytes:
        vec = self.encode(text)
        return serialize_vector(vec) if vec else b""
