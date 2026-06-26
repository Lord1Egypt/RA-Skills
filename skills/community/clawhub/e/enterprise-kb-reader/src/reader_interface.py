#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只读查询器接口 - 提供统一的查询接口
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config_loader import load_config
from .chroma_client import ChromaVectorDB
from .embedder import Embedder
from .retriever import SimpleRetriever

class ReaderInterface:
    """只读查询器接口"""
    
    def __init__(self):
        """初始化查询器"""
        self.config = load_config()
        self._init_components()
    
    def _init_components(self):
        """初始化组件"""
        try:
            # 初始化向量数据库
            self.db = ChromaVectorDB(
                collection_name=self.config.collection_name
            )
            
            # 初始化嵌入器
            self.embedder = Embedder(
                model=self.config.embedding_model,
                api_key=self.config.embedding_api_key,
                provider=self.config.embedding_provider,
                base_url=self.config.embedding_base_url
            )
            
            # 初始化检索器
            self.retriever = SimpleRetriever(
                db=self.db,
                embedder=self.embedder,
                top_k=self.config.retrieval_top_k,
                threshold=self.config.vector_threshold
            )
            
        except Exception as e:
            raise Exception(f"组件初始化失败: {e}")
    
    def query(self, query_text: str) -> str:
        """查询知识库"""
        try:
            results = self.retriever.search(query_text)
            
            if not results:
                return "❌ 未找到相关内容，请尝试其他关键词"
            
            # 格式化结果
            response = f"✅ 找到 {len(results)} 个相关结果:\n\n"
            
            for i, result in enumerate(results, 1):
                response += f"[结果{i}] 相似度: {result['score']:.3f}\n"
                response += f"文档: {result['metadata'].get('document_name', '未知')}\n"
                
                # 智能内容显示
                content = result['text'].strip()
                if len(content) <= 300:
                    response += f"内容: {content}\n"
                else:
                    response += f"内容: {content[:150]}...{content[-150:]}\n"
                
                response += "\n"
            
            return response.strip()
            
        except Exception as e:
            return f"❌ 查询失败: {e}"
    
    def search_detailed(self, query_text: str) -> str:
        """详细搜索"""
        try:
            results = self.retriever.search(query_text, top_k=self.config.max_results)
            
            if not results:
                return "❌ 未找到相关内容"
            
            response = f"🔍 搜索结果 (共 {len(results)} 条):\n"
            response += "=" * 50 + "\n\n"
            
            for i, result in enumerate(results, 1):
                doc_name = result['metadata'].get('document_name', '未知')
                response += f"[{i}] {doc_name}\n"
                response += f"相似度: {result['score']:.3f}\n"
                
                # 显示完整内容
                response += f"内容:\n{result['text']}\n"
                response += "-" * 40 + "\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ 搜索失败: {e}"
    
    def list_documents(self) -> str:
        """列出文档"""
        try:
            documents = self.db.list_documents()
            
            if not documents:
                return "📭 知识库为空"
            
            response = f"📚 知识库文档列表 (共 {len(documents)} 个):\n\n"
            
            for i, doc in enumerate(documents, 1):
                response += f"{i}. 📄 {doc['name']}\n"
                response += f"   📦 块数: {doc['count']}\n\n"
            
            return response.strip()
            
        except Exception as e:
            return f"❌ 获取文档列表失败: {e}"
    
    def get_stats(self) -> str:
        """获取统计信息"""
        try:
            stats = self.db.get_stats()
            
            response = "📊 知识库统计信息:\n\n"
            response += f"📄 文档数量: {stats.get('document_count', 0)}\n"
            response += f"📦 文档块数: {stats.get('chunk_count', 0)}\n"
            
            return response
            
        except Exception as e:
            return f"❌ 获取统计信息失败: {e}"