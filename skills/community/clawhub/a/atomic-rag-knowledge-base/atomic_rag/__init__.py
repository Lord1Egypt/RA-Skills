"""
Atomic RAG Knowledge Base Builder
原子化RAG知识库构建器

让AI真正学会一本书，而非只是看过。
"""

from .builder import AtomicRAGBuilder
from .rag import MultiRecallRAG
from .processors import (
    MathProcessor,
    PhysicsProcessor,
    ChemistryProcessor,
    MedicineProcessor
)

__version__ = "1.0.0"
__author__ = "学来学去AI团队"

__all__ = [
    "AtomicRAGBuilder",
    "MultiRecallRAG",
    "MathProcessor",
    "PhysicsProcessor",
    "ChemistryProcessor",
    "MedicineProcessor"
]
