#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChromaDB客户端 - 只读查询器专用
支持共享配置的多agent部署
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import os
from .system_config import load_system_config


class CustomEmbeddingFunction(EmbeddingFunction):
    """自定义嵌入函数"""
    
    def __call__(self, input: Documents) -> Embeddings:
        # 这个不会被调用，因为我们直接提供嵌入向量
        return [[0.0] * 1024] * len(input)


class ChromaVectorDB:
    """ChromaDB客户端 - 只读访问"""
    
    def __init__(self, db_path: str = None, 
                 collection_name: str = "enterprise_kb"):
        """
        初始化ChromaDB客户端
        
        Args:
            db_path: ChromaDB数据库目录路径 (可选，使用共享配置)
            collection_name: 集合名称
        """
        # 使用系统配置
        if db_path is None:
            system_config = load_system_config()
            db_path = system_config.data_path
            print(f"✓ 使用系统数据路径: {db_path}")
        
        self.db_path = db_path
        self.collection_name = collection_name
        
        # 检查系统目录是否存在 - 只读系统不创建目录
        if not os.path.exists(db_path):
            raise FileNotFoundError(
                f"⚠️ 系统数据目录不存在: {db_path}\n"
                f"请先运行 kb-manager setup 创建知识库环境"
            )
        
        # 初始化客户端
        try:
            self.client = chromadb.PersistentClient(path=db_path)
        except Exception as e:
            raise ConnectionError(f"无法连接到数据库: {e}")
        
        # 获取集合 - 只读系统不创建集合
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=CustomEmbeddingFunction()
            )
        except Exception as e:
            raise FileNotFoundError(
                f"⚠️ 知识库集合 '{collection_name}' 不存在\n"
                f"请先运行 kb-manager setup 创建知识库环境\n"
                f"错误详情: {e}"
            )
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        向量搜索
        
        Args:
            query_embedding: 查询向量
            top_k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=['documents', 'metadatas', 'distances']
            )
            
            # 格式化结果
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    distance = results['distances'][0][i]
                    score = 1 - distance  # 转换为相似度分数
                    
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] or {},
                        'distance': distance,
                        'score': score
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """列出所有文档"""
        try:
            # 获取所有数据
            results = self.collection.get(include=['metadatas'])
            
            # 统计每个文档的块数
            doc_stats = {}
            for metadata in results['metadatas']:
                if metadata:
                    doc_name = metadata.get('document_name', '未知')
                    if doc_name not in doc_stats:
                        doc_stats[doc_name] = 0
                    doc_stats[doc_name] += 1
            
            # 格式化结果
            documents = []
            for doc_name, count in doc_stats.items():
                documents.append({
                    'name': doc_name,
                    'count': count
                })
            
            return documents
            
        except Exception as e:
            print(f"获取文档列表失败: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        try:
            # 获取所有数据
            results = self.collection.get(include=['metadatas'])
            
            total_chunks = len(results['ids'])
            
            # 统计文档数量
            doc_names = set()
            for metadata in results['metadatas']:
                if metadata:
                    doc_name = metadata.get('document_name')
                    if doc_name:
                        doc_names.add(doc_name)
            
            return {
                'document_count': len(doc_names),
                'chunk_count': total_chunks
            }
            
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            return {'document_count': 0, 'chunk_count': 0}
    
    def count(self) -> int:
        """获取总记录数"""
        try:
            return self.collection.count()
        except Exception:
            return 0