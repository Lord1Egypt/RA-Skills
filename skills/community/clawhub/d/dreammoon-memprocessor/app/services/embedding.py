"""向量嵌入服务"""
from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:
    """向量嵌入服务 - 使用SentenceTransformers"""
    
    def __init__(self):
        self.model: Optional[SentenceTransformer] = None
        self.model_name = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
    
    def init(self):
        """初始化模型"""
        if self.model is None:
            print(f"[Embedding] Loading model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"[Embedding] Model loaded, dimension: {self.dimension}")
    
    def encode(self, text: str, normalize: bool = True) -> List[float]:
        """
        将文本编码为向量
        
        Args:
            text: 输入文本
            normalize: 是否归一化（归一化后可用内积计算余弦相似度）
        
        Returns:
            向量列表
        """
        if self.model is None:
            self.init()
        
        embedding = self.model.encode(text, normalize_embeddings=normalize)
        return embedding.tolist()
    
    def encode_batch(self, texts: List[str], normalize: bool = True) -> List[List[float]]:
        """
        批量编码
        
        Args:
            texts: 文本列表
            normalize: 是否归一化
        
        Returns:
            向量列表的列表
        """
        if self.model is None:
            self.init()
        
        embeddings = self.model.encode(texts, normalize_embeddings=normalize)
        return [e.tolist() for e in embeddings]
    
    def calculate_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算两个向量的余弦相似度
        
        注意：输入向量需要已经归一化
        """
        a = np.array(vec1)
        b = np.array(vec2)
        
        # 如果已经归一化，内积就是余弦相似度
        return float(np.dot(a, b))
    
    def get_dimension(self) -> int:
        """获取向量维度"""
        return self.dimension


# 单例
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """获取嵌入服务单例"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
