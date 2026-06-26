#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级检索系统 (Advanced Retrieval System)

参考Dify的检索策略，实现多种智能检索模式：
1. 父子检索 (Parent-Child Retrieval) - 子块匹配，父块返回
2. 混合检索 (Hybrid Retrieval) - 向量+关键词
3. 语义检索 (Semantic Retrieval) - 纯向量相似度
4. 全文检索 (Full-Text Retrieval) - 纯关键词匹配
5. 重排序检索 (Rerank Retrieval) - 多阶段检索

核心特性:
- 多种检索策略
- 智能结果融合
- 上下文增强
- 相关性重排序
- 自适应权重调整

作者: OpenClaw Team
版本: 1.0.0
参考: Dify Retrieval Strategy
"""

import logging
import math
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

from .gte_reranker import GTEReranker

from .chroma_client import ChromaVectorDB, SearchResult
from .embedder import Embedder
from .advanced_chunker import AdvancedChunk
from .hybrid_retriever import KeywordSearcher, HybridSearchResult

# 设置日志
logger = logging.getLogger(__name__)


class RetrievalMode(Enum):
    """检索模式"""
    VECTOR = "vector"                    # 纯向量检索
    KEYWORD = "keyword"                  # 纯关键词检索
    HYBRID = "hybrid"                    # 混合检索
    PARENT_CHILD = "parent_child"        # 父子检索
    RERANK = "rerank"                    # 重排序检索


class ContextStrategy(Enum):
    """上下文策略"""
    NONE = "none"                        # 无上下文
    PARENT_ONLY = "parent_only"          # 仅父块
    SIBLINGS = "siblings"                # 兄弟块
    FULL_CONTEXT = "full_context"        # 完整上下文


@dataclass
class RetrievalConfig:
    """检索配置"""
    # 基础参数
    mode: RetrievalMode = RetrievalMode.PARENT_CHILD
    top_k: int = 5
    
    # 阈值设置
    vector_threshold: float = 0.5
    keyword_threshold: float = 0.3
    final_threshold: float = 0.4
    
    # 权重设置
    vector_weight: float = 0.7
    keyword_weight: float = 0.3
    
    # 父子检索参数
    child_search_top_k: int = 20         # 子块搜索数量
    parent_return_top_k: int = 5         # 父块返回数量
    context_strategy: ContextStrategy = ContextStrategy.PARENT_ONLY
    
    # 重排序参数
    enable_rerank: bool = True
    rerank_model: str = "gte-rerank-v2"  # gte-rerank-v2, cross_encoder, llm_rerank
    rerank_top_k: int = 10
    
    # 多样性参数
    enable_diversity: bool = True        # 启用结果多样性
    diversity_threshold: float = 0.8     # 多样性阈值
    max_same_document: int = 3           # 同一文档最大结果数
    
    # 上下文增强
    enable_context_expansion: bool = True # 启用上下文扩展
    context_window_size: int = 2         # 上下文窗口大小


@dataclass
class AdvancedRetrievalResult:
    """高级检索结果"""
    chunk_id: str
    text: str
    document_name: str
    document_id: str
    chunk_index: int
    
    # 分数信息
    vector_score: float = 0.0
    keyword_score: float = 0.0
    hybrid_score: float = 0.0
    rerank_score: float = 0.0
    final_score: float = 0.0
    
    # 层次信息
    chunk_type: str = "general"          # general, parent, child
    parent_id: Optional[str] = None
    child_ids: List[str] = None
    
    # 匹配信息
    matched_keywords: List[str] = None
    keyword_positions: List[int] = None
    
    # 上下文信息
    context_chunks: List[str] = None     # 上下文块ID
    expanded_text: str = ""              # 扩展后的文本
    
    # 元数据
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.child_ids is None:
            self.child_ids = []
        if self.matched_keywords is None:
            self.matched_keywords = []
        if self.keyword_positions is None:
            self.keyword_positions = []
        if self.context_chunks is None:
            self.context_chunks = []
        if self.metadata is None:
            self.metadata = {}


class AdvancedRetriever:
    """高级检索系统"""
    
    def __init__(self, db: ChromaVectorDB, embedder: Embedder, 
                 config: RetrievalConfig = None):
        """
        初始化高级检索系统
        
        Args:
            db: 向量数据库
            embedder: 嵌入生成器
            config: 检索配置
        """
        self.db = db
        self.embedder = embedder
        self.config = config or RetrievalConfig()
        
        # 初始化关键词搜索器
        self.keyword_searcher = KeywordSearcher()
        self._build_keyword_index()
        
        # 初始化重排序器
        self.gte_reranker = None
        if self.config.enable_rerank and self.config.rerank_model == "gte-rerank-v2":
            try:
                import os
                api_key = os.getenv("DASHSCOPE_API_KEY")
                if api_key:
                    self.gte_reranker = GTEReranker(api_key)
                    logger.info("GTE-Rerank-v2 重排序器初始化成功")
                else:
                    logger.warning("未找到 DASHSCOPE_API_KEY，将使用简单重排序")
            except Exception as e:
                logger.error(f"GTE-Rerank-v2 初始化失败: {e}，将使用简单重排序")
        
        # 初始化块关系映射
        self.chunk_relationships = {}
        self._build_chunk_relationships()
        
        logger.info(f"高级检索系统初始化完成，模式: {self.config.mode.value}")
        if self.gte_reranker:
            logger.info("✅ 使用 GTE-Rerank-v2 重排序器")
        else:
            logger.info("✅ 使用简单重排序器")
    
    def _build_keyword_index(self):
        """构建关键词索引"""
        try:
            # 获取所有文档块
            all_docs = self.db.get_all_documents()
            documents = []
            
            for doc in all_docs:
                doc_id = doc['document_id']
                chunks = self._get_document_chunks(doc_id)
                documents.extend(chunks)
            
            self.keyword_searcher.build_index(documents)
            logger.info(f"关键词索引构建完成，文档数: {len(documents)}")
            
        except Exception as e:
            logger.error(f"构建关键词索引失败: {e}")
    
    def _get_document_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """获取文档的所有块"""
        try:
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
    
    def _build_chunk_relationships(self):
        """构建块关系映射"""
        try:
            # 获取所有块的关系信息
            all_docs = self.db.get_all_documents()
            
            for doc in all_docs:
                doc_id = doc['document_id']
                chunks = self._get_document_chunks(doc_id)
                
                for chunk in chunks:
                    chunk_id = chunk['id']
                    metadata = chunk.get('metadata', {})
                    
                    # 解析块类型和关系
                    chunk_type = metadata.get('chunk_type', 'general')
                    parent_id = metadata.get('parent_id')
                    
                    self.chunk_relationships[chunk_id] = {
                        'type': chunk_type,
                        'parent_id': parent_id,
                        'document_id': doc_id,
                        'metadata': metadata
                    }
            
            logger.info(f"块关系映射构建完成，块数: {len(self.chunk_relationships)}")
            
        except Exception as e:
            logger.error(f"构建块关系映射失败: {e}")
    
    def search(self, query: str, top_k: int = None, 
               config: RetrievalConfig = None) -> List[AdvancedRetrievalResult]:
        """
        高级搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            config: 检索配置
            
        Returns:
            高级检索结果列表
        """
        search_config = config or self.config
        if top_k is not None:
            search_config.top_k = top_k
        
        logger.info(f"开始高级搜索: {query}, 模式: {search_config.mode.value}")
        
        # 根据模式选择检索策略
        if search_config.mode == RetrievalMode.VECTOR:
            results = self._vector_search(query, search_config)
        elif search_config.mode == RetrievalMode.KEYWORD:
            results = self._keyword_search(query, search_config)
        elif search_config.mode == RetrievalMode.HYBRID:
            results = self._hybrid_search(query, search_config)
        elif search_config.mode == RetrievalMode.PARENT_CHILD:
            results = self._parent_child_search(query, search_config)
        elif search_config.mode == RetrievalMode.RERANK:
            results = self._rerank_search(query, search_config)
        else:
            results = self._parent_child_search(query, search_config)
        
        # 后处理
        results = self._post_process_results(results, query, search_config)
        
        logger.info(f"高级搜索完成，返回 {len(results)} 个结果")
        return results
    
    def _parent_child_search(self, query: str, config: RetrievalConfig) -> List[AdvancedRetrievalResult]:
        """
        父子检索 - Dify的核心策略
        
        策略：
        1. 使用子块进行精确匹配
        2. 返回父块提供更多上下文
        3. 保持检索精度和上下文完整性的平衡
        """
        logger.debug("执行父子检索策略")
        
        # 1. 子块检索 - 获取更多候选
        child_results = self._search_child_chunks(query, config.child_search_top_k)
        
        if not child_results:
            logger.warning("子块检索无结果")
            return []
        
        # 2. 父块聚合 - 按父块分组子块结果
        parent_groups = self._group_by_parent(child_results)
        
        # 3. 父块排序 - 基于子块的最佳匹配分数
        ranked_parents = self._rank_parent_chunks(parent_groups, config)
        
        # 4. 构建最终结果
        final_results = []
        for parent_info in ranked_parents[:config.parent_return_top_k]:
            parent_result = self._build_parent_result(parent_info, config)
            if parent_result:
                final_results.append(parent_result)
        
        return final_results
    
    def _search_child_chunks(self, query: str, top_k: int) -> List[Tuple[SearchResult, float, List[str]]]:
        """搜索子块"""
        results = []
        
        # 向量搜索子块
        try:
            query_vector = self.embedder.embed_query(query)
            vector_results = self.db.search(query_vector, top_k=top_k * 2)
            
            # 过滤出子块
            for result in vector_results:
                chunk_id = result.id
                if chunk_id in self.chunk_relationships:
                    chunk_info = self.chunk_relationships[chunk_id]
                    if chunk_info['type'] == 'child':
                        results.append((result, result.score, []))
            
        except Exception as e:
            logger.error(f"子块向量搜索失败: {e}")
        
        # 关键词搜索子块
        try:
            keyword_results = self.keyword_searcher.search(query, top_k)
            
            for doc_idx, score, matched_words in keyword_results:
                if doc_idx < len(self.keyword_searcher.documents):
                    doc = self.keyword_searcher.documents[doc_idx]
                    chunk_id = doc['id']
                    
                    if chunk_id in self.chunk_relationships:
                        chunk_info = self.chunk_relationships[chunk_id]
                        if chunk_info['type'] == 'child':
                            # 创建SearchResult对象
                            search_result = SearchResult(
                                id=chunk_id,
                                text=doc['text'],
                                metadata=doc.get('metadata', {}),
                                distance=1.0 - (score / 10.0),  # 转换为距离
                                score=score / 10.0  # 归一化分数
                            )
                            results.append((search_result, score / 10.0, matched_words))
            
        except Exception as e:
            logger.error(f"子块关键词搜索失败: {e}")
        
        # 按分数排序并去重
        unique_results = {}
        for result, score, keywords in results:
            chunk_id = result.id
            if chunk_id not in unique_results or score > unique_results[chunk_id][1]:
                unique_results[chunk_id] = (result, score, keywords)
        
        sorted_results = sorted(unique_results.values(), key=lambda x: x[1], reverse=True)
        return sorted_results[:top_k]
    
    def _group_by_parent(self, child_results: List[Tuple[SearchResult, float, List[str]]]) -> Dict[str, List[Tuple[SearchResult, float, List[str]]]]:
        """按父块分组子块结果"""
        parent_groups = defaultdict(list)
        
        for result, score, keywords in child_results:
            chunk_id = result.id
            if chunk_id in self.chunk_relationships:
                parent_id = self.chunk_relationships[chunk_id]['parent_id']
                if parent_id:
                    parent_groups[parent_id].append((result, score, keywords))
        
        return dict(parent_groups)
    
    def _rank_parent_chunks(self, parent_groups: Dict[str, List], config: RetrievalConfig) -> List[Dict[str, Any]]:
        """排序父块"""
        ranked_parents = []
        
        for parent_id, child_results in parent_groups.items():
            # 计算父块分数：使用最佳子块分数和平均分数的组合
            scores = [score for _, score, _ in child_results]
            best_score = max(scores)
            avg_score = sum(scores) / len(scores)
            combined_score = 0.7 * best_score + 0.3 * avg_score
            
            # 收集匹配的关键词
            all_keywords = []
            for _, _, keywords in child_results:
                all_keywords.extend(keywords)
            unique_keywords = list(set(all_keywords))
            
            ranked_parents.append({
                'parent_id': parent_id,
                'score': combined_score,
                'child_count': len(child_results),
                'child_results': child_results,
                'matched_keywords': unique_keywords
            })
        
        # 按分数排序
        ranked_parents.sort(key=lambda x: x['score'], reverse=True)
        return ranked_parents
    
    def _build_parent_result(self, parent_info: Dict[str, Any], config: RetrievalConfig) -> Optional[AdvancedRetrievalResult]:
        """构建父块结果"""
        try:
            parent_id = parent_info['parent_id']
            
            # 获取父块内容
            parent_data = self.db.collection.get(
                ids=[parent_id],
                include=["documents", "metadatas"]
            )
            
            if not parent_data["ids"]:
                return None
            
            parent_text = parent_data["documents"][0]
            parent_metadata = parent_data["metadatas"][0]
            
            # 创建结果对象
            result = AdvancedRetrievalResult(
                chunk_id=parent_id,
                text=parent_text,
                document_name=parent_metadata.get("document_name", ""),
                document_id=parent_metadata.get("document_id", ""),
                chunk_index=parent_metadata.get("chunk_index", 0),
                chunk_type="parent",
                final_score=parent_info['score'],
                matched_keywords=parent_info['matched_keywords'],
                child_ids=[r[0].id for r in parent_info['child_results']],
                metadata=parent_metadata
            )
            
            # 上下文扩展
            if config.enable_context_expansion:
                result.expanded_text = self._expand_context(result, config)
            
            return result
            
        except Exception as e:
            logger.error(f"构建父块结果失败: {e}")
            return None
    
    def _expand_context(self, result: AdvancedRetrievalResult, config: RetrievalConfig) -> str:
        """扩展上下文"""
        try:
            if config.context_strategy == ContextStrategy.NONE:
                return result.text
            
            expanded_parts = [result.text]
            
            if config.context_strategy == ContextStrategy.PARENT_ONLY:
                # 已经是父块，无需扩展
                return result.text
            
            elif config.context_strategy == ContextStrategy.SIBLINGS:
                # 添加兄弟块
                siblings = self._get_sibling_chunks(result.chunk_id, config.context_window_size)
                for sibling_text in siblings:
                    expanded_parts.append(sibling_text)
            
            elif config.context_strategy == ContextStrategy.FULL_CONTEXT:
                # 添加完整文档上下文
                full_context = self._get_full_document_context(result.document_id)
                expanded_parts.append(full_context)
            
            return "\n\n".join(expanded_parts)
            
        except Exception as e:
            logger.error(f"上下文扩展失败: {e}")
            return result.text
    
    def _get_sibling_chunks(self, chunk_id: str, window_size: int) -> List[str]:
        """获取兄弟块"""
        # 简化实现：获取同一文档的相邻块
        try:
            if chunk_id not in self.chunk_relationships:
                return []
            
            document_id = self.chunk_relationships[chunk_id]['document_id']
            chunks = self._get_document_chunks(document_id)
            
            # 找到当前块的位置
            current_index = -1
            for i, chunk in enumerate(chunks):
                if chunk['id'] == chunk_id:
                    current_index = i
                    break
            
            if current_index == -1:
                return []
            
            # 获取窗口内的兄弟块
            siblings = []
            start = max(0, current_index - window_size)
            end = min(len(chunks), current_index + window_size + 1)
            
            for i in range(start, end):
                if i != current_index:
                    siblings.append(chunks[i]['text'])
            
            return siblings
            
        except Exception as e:
            logger.error(f"获取兄弟块失败: {e}")
            return []
    
    def _get_full_document_context(self, document_id: str) -> str:
        """获取完整文档上下文"""
        try:
            chunks = self._get_document_chunks(document_id)
            texts = [chunk['text'] for chunk in chunks]
            return "\n\n".join(texts)
        except Exception as e:
            logger.error(f"获取完整文档上下文失败: {e}")
            return ""
    
    def _vector_search(self, query: str, config: RetrievalConfig) -> List[AdvancedRetrievalResult]:
        """纯向量检索"""
        try:
            query_vector = self.embedder.embed_query(query)
            search_results = self.db.search(query_vector, top_k=config.top_k * 2)
            
            results = []
            for sr in search_results:
                if sr.score >= config.vector_threshold:
                    result = AdvancedRetrievalResult(
                        chunk_id=sr.id,
                        text=sr.text,
                        document_name=sr.metadata.get("document_name", ""),
                        document_id=sr.metadata.get("document_id", ""),
                        chunk_index=sr.metadata.get("chunk_index", 0),
                        vector_score=sr.score,
                        final_score=sr.score,
                        metadata=sr.metadata
                    )
                    results.append(result)
            
            return results[:config.top_k]
            
        except Exception as e:
            logger.error(f"向量检索失败: {e}")
            return []
    
    def _keyword_search(self, query: str, config: RetrievalConfig) -> List[AdvancedRetrievalResult]:
        """纯关键词检索"""
        try:
            keyword_results = self.keyword_searcher.search(query, config.top_k * 2)
            
            results = []
            for doc_idx, score, matched_words in keyword_results:
                if doc_idx < len(self.keyword_searcher.documents) and score >= config.keyword_threshold:
                    doc = self.keyword_searcher.documents[doc_idx]
                    metadata = doc.get('metadata', {})
                    
                    result = AdvancedRetrievalResult(
                        chunk_id=doc['id'],
                        text=doc['text'],
                        document_name=metadata.get("document_name", ""),
                        document_id=metadata.get("document_id", ""),
                        chunk_index=metadata.get("chunk_index", 0),
                        keyword_score=score,
                        final_score=score / 10.0,  # 归一化
                        matched_keywords=matched_words,
                        metadata=metadata
                    )
                    results.append(result)
            
            return results[:config.top_k]
            
        except Exception as e:
            logger.error(f"关键词检索失败: {e}")
            return []
    
    def _hybrid_search(self, query: str, config: RetrievalConfig) -> List[AdvancedRetrievalResult]:
        """混合检索"""
        # 获取向量和关键词结果
        vector_results = self._vector_search(query, config)
        keyword_results = self._keyword_search(query, config)
        
        # 合并结果
        merged_results = {}
        
        # 处理向量结果
        for result in vector_results:
            merged_results[result.chunk_id] = result
        
        # 处理关键词结果
        for result in keyword_results:
            if result.chunk_id in merged_results:
                # 更新已存在的结果
                existing = merged_results[result.chunk_id]
                existing.keyword_score = result.keyword_score
                existing.matched_keywords = result.matched_keywords
                existing.hybrid_score = (
                    config.vector_weight * existing.vector_score +
                    config.keyword_weight * result.keyword_score / 10.0
                )
                existing.final_score = existing.hybrid_score
            else:
                # 添加新结果
                result.hybrid_score = config.keyword_weight * result.keyword_score / 10.0
                result.final_score = result.hybrid_score
                merged_results[result.chunk_id] = result
        
        # 排序并返回
        sorted_results = sorted(merged_results.values(), key=lambda x: x.final_score, reverse=True)
        return sorted_results[:config.top_k]
    
    def _rerank_search(self, query: str, config: RetrievalConfig) -> List[AdvancedRetrievalResult]:
        """重排序检索"""
        # 先进行混合检索获取候选
        candidates = self._hybrid_search(query, RetrievalConfig(top_k=config.rerank_top_k))
        
        if not candidates:
            return []
        
        # 重排序（简化实现）
        reranked_results = self._simple_rerank(query, candidates)
        
        return reranked_results[:config.top_k]
    
    def _simple_rerank(self, query: str, candidates: List[AdvancedRetrievalResult]) -> List[AdvancedRetrievalResult]:
        """智能重排序实现 - 专用 GTE-Rerank-v2"""
        if not candidates:
            return candidates
        
        # 如果启用了 GTE 重排序器，使用 GTE 重排序
        if self.gte_reranker:
            return self._gte_rerank(query, candidates)
        else:
            logger.warning("GTE重排序器未初始化，返回原始排序")
            return candidates
    
    def _gte_rerank(self, query: str, candidates: List[AdvancedRetrievalResult]) -> List[AdvancedRetrievalResult]:
        """使用 GTE-Rerank-v2 进行重排序"""
        try:
            # 提取文档文本
            documents = [result.text for result in candidates]
            
            # 使用 GTE 重排序
            gte_results = self.gte_reranker.rerank(
                query=query,
                documents=documents,
                top_k=len(candidates)
            )
            
            # 如果 GTE 重排序失败，返回原始候选
            if not gte_results:
                logger.warning("GTE重排序返回空结果，使用原始排序")
                return candidates
            
            # 更新候选结果的分数
            reranked_candidates = []
            for gte_result in gte_results:
                original_result = candidates[gte_result.index]
                # 更新重排序分数
                original_result.rerank_score = gte_result.relevance_score
                # 融合原始分数和重排序分数
                original_result.final_score = (
                    0.5 * original_result.hybrid_score + 
                    0.5 * gte_result.relevance_score
                )
                reranked_candidates.append(original_result)
            
            logger.debug(f"GTE重排序完成，处理了 {len(reranked_candidates)} 个结果")
            return reranked_candidates
            
        except Exception as e:
            logger.error(f"GTE重排序失败: {e}，使用原始排序")
            return candidates

    
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
    
    def _post_process_results(self, results: List[AdvancedRetrievalResult], 
                             query: str, config: RetrievalConfig) -> List[AdvancedRetrievalResult]:
        """后处理结果"""
        # 应用多样性过滤
        if config.enable_diversity:
            results = self._apply_diversity_filter(results, config)
        
        # 应用最终阈值
        filtered_results = [
            result for result in results
            if result.final_score >= config.final_threshold
        ]
        
        return filtered_results
    
    def _apply_diversity_filter(self, results: List[AdvancedRetrievalResult], 
                               config: RetrievalConfig) -> List[AdvancedRetrievalResult]:
        """应用多样性过滤"""
        if not results:
            return results
        
        # 按文档分组统计
        doc_counts = defaultdict(int)
        filtered_results = []
        
        for result in results:
            doc_id = result.document_id
            
            # 检查同一文档的结果数量限制
            if doc_counts[doc_id] < config.max_same_document:
                filtered_results.append(result)
                doc_counts[doc_id] += 1
        
        return filtered_results


# 便捷函数
def create_advanced_retriever(db: ChromaVectorDB, embedder: Embedder, 
                             mode: str = "parent_child", **kwargs) -> AdvancedRetriever:
    """
    创建高级检索器的便捷函数
    
    Args:
        db: 向量数据库
        embedder: 嵌入生成器
        mode: 检索模式
        **kwargs: 其他配置参数
        
    Returns:
        配置好的高级检索器
    """
    retrieval_mode = RetrievalMode(mode)
    config = RetrievalConfig(mode=retrieval_mode, **kwargs)
    return AdvancedRetriever(db, embedder, config)


if __name__ == "__main__":
    # 测试高级检索系统
    print("高级检索系统模块加载完成")
    print("支持的检索模式:")
    print("- vector: 纯向量检索")
    print("- keyword: 纯关键词检索")
    print("- hybrid: 混合检索")
    print("- parent_child: 父子检索 (推荐)")
    print("- rerank: 重排序检索")