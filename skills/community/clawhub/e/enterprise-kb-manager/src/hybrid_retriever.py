#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合检索引擎 (Hybrid Retrieval Engine)

结合向量检索、关键词检索和重排序的高级检索系统，参考Dify的混合检索模式。

核心特性:
1. 向量检索 (Vector Search) - 语义相似度匹配
2. 关键词检索 (Keyword Search) - 精确词汇匹配  
3. 混合融合 (Hybrid Fusion) - 结合两种检索结果
4. 重排序 (Reranking) - 基于语义相关性重新排序
5. 自适应权重 - 根据查询类型动态调整权重

作者: OpenClaw Team
版本: 1.0.0
参考: Dify Hybrid Search, Azure Cognitive Search
"""

import re
import math
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import Counter, defaultdict
import jieba
import jieba.analyse

from .chroma_client import ChromaVectorDB, SearchResult
from .embedder import Embedder

# 设置日志
logger = logging.getLogger(__name__)

# 初始化jieba
jieba.setLogLevel(logging.WARNING)


@dataclass
class HybridSearchResult:
    """混合搜索结果"""
    chunk_id: str
    text: str
    document_name: str
    document_id: str
    chunk_index: int
    
    # 分数详情
    vector_score: float = 0.0      # 向量相似度分数
    keyword_score: float = 0.0     # 关键词匹配分数
    hybrid_score: float = 0.0      # 混合分数
    rerank_score: float = 0.0      # 重排序分数
    final_score: float = 0.0       # 最终分数
    
    # 匹配详情
    matched_keywords: List[str] = None
    keyword_positions: List[int] = None
    
    def __post_init__(self):
        if self.matched_keywords is None:
            self.matched_keywords = []
        if self.keyword_positions is None:
            self.keyword_positions = []


@dataclass
class SearchConfig:
    """搜索配置"""
    # 基础参数
    top_k: int = 10
    vector_weight: float = 0.7      # 向量检索权重
    keyword_weight: float = 0.3     # 关键词检索权重
    
    # 阈值设置 - 提高阈值确保只返回真正匹配的数据
    vector_threshold: float = 0.5   # 向量相似度阈值 (提高到0.5)
    keyword_threshold: float = 0.5  # 关键词匹配阈值 (提高到0.5)
    final_threshold: float = 0.4    # 最终结果阈值 (提高到0.4)
    
    # 检索参数
    vector_top_k: int = 20          # 向量检索候选数
    keyword_top_k: int = 20         # 关键词检索候选数
    
    # 重排序参数
    enable_rerank: bool = True      # 是否启用重排序
    rerank_top_k: int = 10          # 重排序候选数
    
    # 自适应权重
    enable_adaptive_weights: bool = True  # 是否启用自适应权重
    
    # 严格匹配模式
    strict_mode: bool = True        # 严格模式：只返回高度匹配的结果
    min_keyword_matches: int = 1    # 关键词查询至少匹配的词数


class KeywordSearcher:
    """关键词搜索器 - 基于BM25算法"""
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        初始化BM25搜索器
        
        Args:
            k1: 词频饱和参数
            b: 长度归一化参数
        """
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.avgdl = 0
        
    def build_index(self, documents: List[Dict[str, Any]]):
        """
        构建关键词索引
        
        Args:
            documents: 文档列表，每个文档包含id, text, metadata
        """
        logger.info(f"构建关键词索引，文档数量: {len(documents)}")
        
        self.documents = documents
        self.doc_freqs = []
        
        # 分词并统计词频
        for doc in documents:
            text = doc['text']
            words = list(jieba.cut_for_search(text))
            word_freq = Counter(words)
            self.doc_freqs.append(word_freq)
            self.doc_len.append(len(words))
        
        # 计算平均文档长度
        self.avgdl = sum(self.doc_len) / len(self.doc_len) if self.doc_len else 0
        
        # 计算IDF
        self._calculate_idf()
        
        logger.info(f"关键词索引构建完成，词汇数量: {len(self.idf)}")
    
    def _calculate_idf(self):
        """计算逆文档频率(IDF)"""
        df = defaultdict(int)
        
        # 统计每个词在多少个文档中出现
        for doc_freq in self.doc_freqs:
            for word in doc_freq.keys():
                df[word] += 1
        
        # 计算IDF
        num_docs = len(self.documents)
        for word, freq in df.items():
            self.idf[word] = math.log((num_docs - freq + 0.5) / (freq + 0.5) + 1.0)
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float, List[str]]]:
        """
        BM25搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            List[Tuple[doc_index, score, matched_words]]
        """
        if not self.documents:
            return []
        
        # 查询分词
        query_words = list(jieba.cut_for_search(query))
        query_word_freq = Counter(query_words)
        
        # 计算每个文档的BM25分数
        scores = []
        for i, doc_freq in enumerate(self.doc_freqs):
            score = 0.0
            matched_words = []
            
            for word in query_word_freq:
                if word in doc_freq:
                    # 计算BM25分数
                    tf = doc_freq[word]
                    idf = self.idf.get(word, 0)
                    
                    # BM25公式
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avgdl)
                    score += idf * numerator / denominator
                    
                    matched_words.append(word)
            
            if score > 0:
                scores.append((i, score, matched_words))
        
        # 按分数排序
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class SimpleReranker:
    """简单重排序器 - 基于语义相关性"""
    
    def __init__(self, embedder: Embedder):
        """
        初始化重排序器
        
        Args:
            embedder: 嵌入生成器
        """
        self.embedder = embedder
    
    def rerank(self, query: str, results: List[HybridSearchResult], 
               top_k: int = 10) -> List[HybridSearchResult]:
        """
        重排序搜索结果
        
        Args:
            query: 原始查询
            results: 搜索结果列表
            top_k: 返回结果数量
            
        Returns:
            重排序后的结果列表
        """
        if not results:
            return []
        
        logger.debug(f"重排序 {len(results)} 个结果")
        
        try:
            # 生成查询嵌入
            query_embedding = self.embedder.embed_query(query)
            
            # 生成文档嵌入并计算相似度
            texts = [result.text for result in results]
            doc_embeddings = self.embedder.embed_texts(texts)
            
            # 计算余弦相似度
            for i, result in enumerate(results):
                if i < len(doc_embeddings):
                    similarity = self._cosine_similarity(query_embedding, doc_embeddings[i])
                    result.rerank_score = similarity
                    
                    # 更新最终分数 (混合分数 + 重排序分数)
                    result.final_score = 0.7 * result.hybrid_score + 0.3 * result.rerank_score
            
            # 按最终分数排序
            results.sort(key=lambda x: x.final_score, reverse=True)
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"重排序失败: {e}")
            # 如果重排序失败，返回原始结果
            for result in results:
                result.final_score = result.hybrid_score
            return results[:top_k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class HybridRetriever:
    """混合检索器 - 结合向量检索和关键词检索"""
    
    def __init__(self, db: ChromaVectorDB, embedder: Embedder, 
                 config: SearchConfig = None):
        """
        初始化混合检索器
        
        Args:
            db: 向量数据库
            embedder: 嵌入生成器
            config: 搜索配置
        """
        self.db = db
        self.embedder = embedder
        self.config = config or SearchConfig()
        
        # 初始化组件
        self.keyword_searcher = KeywordSearcher()
        self.reranker = SimpleReranker(embedder) if config.enable_rerank else None
        
        # 构建关键词索引
        self._build_keyword_index()
        
        logger.info("混合检索器初始化完成")
    
    def _build_keyword_index(self):
        """构建关键词索引"""
        try:
            # 从向量数据库获取所有文档
            all_docs = self.db.get_all_documents()
            
            if not all_docs:
                logger.warning("数据库中没有文档，跳过关键词索引构建")
                return
            
            # 获取所有文档块
            documents = []
            for doc in all_docs:
                doc_id = doc['document_id']
                # 这里需要实现获取文档所有块的方法
                chunks = self._get_document_chunks(doc_id)
                documents.extend(chunks)
            
            # 构建关键词索引
            self.keyword_searcher.build_index(documents)
            
        except Exception as e:
            logger.error(f"构建关键词索引失败: {e}")
    
    def _get_document_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """获取文档的所有块"""
        try:
            # 使用ChromaDB查询特定文档的所有块
            results = self.db.collection.get(
                where={"document_id": document_id},
                include=["documents", "metadatas"]
            )
            
            chunks = []
            if results["ids"]:
                for i, chunk_id in enumerate(results["ids"]):
                    chunks.append({
                        "id": chunk_id,
                        "text": results["documents"][i],
                        "metadata": results["metadatas"][i]
                    })
            
            return chunks
            
        except Exception as e:
            logger.error(f"获取文档块失败: {e}")
            return []
    
    def _detect_query_type(self, query: str) -> Dict[str, float]:
        """
        检测查询类型并返回自适应权重
        
        Args:
            query: 查询文本
            
        Returns:
            包含vector_weight和keyword_weight的字典
        """
        # 简单的查询类型检测逻辑
        query_len = len(query)
        
        # 检测是否包含专有名词、数字、日期等
        has_numbers = bool(re.search(r'\d+', query))
        has_quotes = '"' in query or "'" in query
        has_specific_terms = any(term in query for term in ['什么时候', '多少', '哪里', '谁', '什么是', '如何'])
        
        # 计算关键词密度
        words = list(jieba.cut(query))
        unique_words = set(words)
        keyword_density = len(unique_words) / len(words) if words else 0
        
        # 检测是否为精确查询（包含专有名词）
        has_proper_nouns = any(word in query for word in ['蓝源', '基本法', '激情创业', '团队合作'])
        
        # 自适应权重计算
        if has_numbers or has_quotes or has_specific_terms or has_proper_nouns:
            # 精确查询，大幅增加关键词权重
            vector_weight = 0.3
            keyword_weight = 0.7
        elif query_len < 6:
            # 短查询（可能是关键词），增加关键词权重
            vector_weight = 0.4
            keyword_weight = 0.6
        elif keyword_density > 0.8:
            # 高关键词密度，增加关键词权重
            vector_weight = 0.4
            keyword_weight = 0.6
        else:
            # 语义查询，保持向量权重优势
            vector_weight = 0.7
            keyword_weight = 0.3
        
        logger.debug(f"查询类型检测: 向量权重={vector_weight}, 关键词权重={keyword_weight}")
        return {"vector_weight": vector_weight, "keyword_weight": keyword_weight}
    
    def search(self, query: str, top_k: int = None, config: SearchConfig = None) -> List[HybridSearchResult]:
        """
        混合搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            config: 搜索配置（覆盖默认配置）
            
        Returns:
            混合搜索结果列表
        """
        # 使用传入的配置或默认配置
        search_config = config or self.config
        if top_k is not None:
            search_config.top_k = top_k
        
        logger.info(f"开始混合搜索: {query}")
        
        # 自适应权重调整
        if search_config.enable_adaptive_weights:
            adaptive_weights = self._detect_query_type(query)
            vector_weight = adaptive_weights["vector_weight"]
            keyword_weight = adaptive_weights["keyword_weight"]
        else:
            vector_weight = search_config.vector_weight
            keyword_weight = search_config.keyword_weight
        
        # 1. 向量检索
        vector_results = self._vector_search(query, search_config.vector_top_k)
        logger.debug(f"向量检索返回 {len(vector_results)} 个结果")
        
        # 2. 关键词检索
        keyword_results = self._keyword_search(query, search_config.keyword_top_k)
        logger.debug(f"关键词检索返回 {len(keyword_results)} 个结果")
        
        # 3. 融合结果
        hybrid_results = self._merge_results(
            vector_results, keyword_results, 
            vector_weight, keyword_weight, search_config
        )
        logger.debug(f"融合后得到 {len(hybrid_results)} 个结果")
        
        # 4. 重排序（可选）
        if self.reranker and search_config.enable_rerank:
            final_results = self.reranker.rerank(
                query, hybrid_results, search_config.rerank_top_k
            )
            logger.debug(f"重排序后得到 {len(final_results)} 个结果")
        else:
            # 按混合分数排序
            hybrid_results.sort(key=lambda x: x.hybrid_score, reverse=True)
            final_results = hybrid_results[:search_config.top_k]
            for result in final_results:
                result.final_score = result.hybrid_score
        
        # 5. 应用严格过滤
        if search_config.strict_mode:
            filtered_results = self._apply_strict_filtering(
                final_results, query, search_config
            )
        else:
            # 应用最终阈值过滤
            filtered_results = [
                result for result in final_results 
                if result.final_score >= search_config.final_threshold
            ]
        
        logger.info(f"混合搜索完成，返回 {len(filtered_results)} 个结果")
        return filtered_results
    
    def _apply_strict_filtering(self, results: List[HybridSearchResult], 
                               query: str, config: SearchConfig) -> List[HybridSearchResult]:
        """
        应用严格过滤，确保只返回真正匹配的结果
        
        Args:
            results: 搜索结果列表
            query: 原始查询
            config: 搜索配置
            
        Returns:
            严格过滤后的结果
        """
        filtered_results = []
        query_words = set(jieba.cut(query.lower()))
        
        for result in results:
            # 检查是否满足最终分数阈值
            if result.final_score < config.final_threshold:
                continue
            
            # 检查向量相似度
            if result.vector_score < config.vector_threshold:
                continue
            
            # 如果有关键词匹配，检查关键词匹配质量
            if result.matched_keywords:
                # 计算匹配词占查询词的比例
                matched_query_words = set(result.matched_keywords) & query_words
                match_ratio = len(matched_query_words) / len(query_words) if query_words else 0
                
                # 至少匹配一定比例的查询词
                if match_ratio < 0.3 and len(matched_query_words) < config.min_keyword_matches:
                    continue
            
            # 检查文本相关性（避免返回完全不相关的内容）
            text_lower = result.text.lower()
            has_query_context = any(word in text_lower for word in query_words if len(word) > 1)
            
            if not has_query_context and result.vector_score < 0.7:
                continue
            
            filtered_results.append(result)
        
        return filtered_results
    
    def _vector_search(self, query: str, top_k: int) -> List[Tuple[SearchResult, float]]:
        """向量检索"""
        try:
            query_vector = self.embedder.embed_query(query)
            search_results = self.db.search(query_vector, top_k=top_k)
            
            # 过滤低相似度结果
            filtered_results = [
                (result, result.score) for result in search_results
                if result.score >= self.config.vector_threshold
            ]
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"向量检索失败: {e}")
            return []
    
    def _keyword_search(self, query: str, top_k: int) -> List[Tuple[int, float, List[str]]]:
        """关键词检索"""
        try:
            results = self.keyword_searcher.search(query, top_k)
            
            # 过滤低分数结果
            filtered_results = [
                (doc_idx, score, matched_words) for doc_idx, score, matched_words in results
                if score >= self.config.keyword_threshold
            ]
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"关键词检索失败: {e}")
            return []
    
    def _merge_results(self, vector_results: List[Tuple[SearchResult, float]], 
                      keyword_results: List[Tuple[int, float, List[str]]],
                      vector_weight: float, keyword_weight: float,
                      config: SearchConfig) -> List[HybridSearchResult]:
        """融合向量检索和关键词检索结果"""
        
        # 创建结果字典，以chunk_id为键
        merged_results = {}
        
        # 处理向量检索结果
        for search_result, vector_score in vector_results:
            chunk_id = search_result.id
            
            hybrid_result = HybridSearchResult(
                chunk_id=chunk_id,
                text=search_result.text,
                document_name=search_result.metadata.get("document_name", ""),
                document_id=search_result.metadata.get("document_id", ""),
                chunk_index=search_result.metadata.get("chunk_index", 0),
                vector_score=vector_score,
                keyword_score=0.0,
                matched_keywords=[],
                keyword_positions=[]
            )
            
            merged_results[chunk_id] = hybrid_result
        
        # 处理关键词检索结果
        for doc_idx, keyword_score, matched_words in keyword_results:
            if doc_idx < len(self.keyword_searcher.documents):
                doc = self.keyword_searcher.documents[doc_idx]
                chunk_id = doc['id']
                
                if chunk_id in merged_results:
                    # 更新已存在的结果
                    merged_results[chunk_id].keyword_score = keyword_score
                    merged_results[chunk_id].matched_keywords = matched_words
                else:
                    # 创建新的结果
                    metadata = doc.get('metadata', {})
                    hybrid_result = HybridSearchResult(
                        chunk_id=chunk_id,
                        text=doc['text'],
                        document_name=metadata.get("document_name", ""),
                        document_id=metadata.get("document_id", ""),
                        chunk_index=metadata.get("chunk_index", 0),
                        vector_score=0.0,
                        keyword_score=keyword_score,
                        matched_keywords=matched_words,
                        keyword_positions=[]
                    )
                    
                    merged_results[chunk_id] = hybrid_result
        
        # 计算混合分数
        for result in merged_results.values():
            # 归一化分数到[0,1]范围
            normalized_vector_score = min(1.0, max(0.0, result.vector_score))
            normalized_keyword_score = min(1.0, max(0.0, result.keyword_score / 10.0))  # BM25分数通常较大
            
            # 计算加权混合分数
            result.hybrid_score = (
                vector_weight * normalized_vector_score + 
                keyword_weight * normalized_keyword_score
            )
        
        # 转换为列表并按混合分数排序
        results_list = list(merged_results.values())
        results_list.sort(key=lambda x: x.hybrid_score, reverse=True)
        
        return results_list[:config.top_k * 2]  # 返回更多候选用于重排序


# 便捷函数
def create_hybrid_retriever(db: ChromaVectorDB, embedder: Embedder, 
                           **config_kwargs) -> HybridRetriever:
    """
    创建混合检索器的便捷函数
    
    Args:
        db: 向量数据库
        embedder: 嵌入生成器
        **config_kwargs: 搜索配置参数
        
    Returns:
        配置好的混合检索器
    """
    config = SearchConfig(**config_kwargs)
    return HybridRetriever(db, embedder, config)


if __name__ == "__main__":
    # 测试混合检索器
    print("混合检索器模块加载完成")
    print("主要特性:")
    print("- 向量检索 (语义相似度)")
    print("- 关键词检索 (BM25算法)")
    print("- 混合融合 (自适应权重)")
    print("- 重排序 (语义相关性)")
    print("- 自适应权重调整")