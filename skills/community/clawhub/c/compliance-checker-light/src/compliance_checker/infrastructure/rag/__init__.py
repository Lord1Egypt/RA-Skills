"""
infrastructure/rag 子包

提供零外部向量库依赖的内存 Micro-RAG 能力，
专为合规文档有效期提取场景优化。
"""

from .chunker import ValidityTextChunker
from .validity_retriever import InMemoryValidityRetriever

__all__ = [
    "ValidityTextChunker",
    "InMemoryValidityRetriever",
]
