#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单检索器 - 只读查询器专用
"""

from typing import List, Dict, Any
from .chroma_client import ChromaVectorDB
from .embedder import Embedder

Optional = type(None)


class SimpleRetriever:
    """简单检索器"""
    
    def __init__(self, db: ChromaVectorDB, embedder: Embedder, 
                 top_k: int = 5, threshold: float = 0.3):
        """
        初始化检索器
        
        Args:
            db: 向量数据库
            embedder: 嵌入器
            top_k: 返回结果数量
            threshold: 相似度阈值
        """
        self.db = db
        self.embedder = embedder
        self.top_k = top_k
        self.threshold = threshold
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        搜索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量（可选）
            
        Returns:
            搜索结果列表
        """
        if top_k is None:
            top_k = self.top_k
        
        try:
            # 生成查询向量
            query_embedding = self.embedder.embed_text(query)
            
            # 向量搜索
            results = self.db.search(query_embedding, top_k=top_k)
            
            # 过滤低相似度结果
            filtered_results = []
            for result in results:
                if result['score'] >= self.threshold:
                    filtered_results.append(result)
            
            return filtered_results
            
        except Exception as e:
            print(f"搜索失败: {e}")
            return []