#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTE-Rerank-v2 重排序器
使用阿里巴巴达摩院的 gte-rerank-v2 模型进行重排序
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    import dashscope
    from dashscope import TextReRank
    from http import HTTPStatus
except ImportError:
    print("请安装 dashscope: pip install dashscope")
    raise

logger = logging.getLogger(__name__)

@dataclass
class RerankResult:
    """重排序结果"""
    index: int          # 原始索引
    relevance_score: float  # 相关性分数
    text: str          # 文本内容

class GTEReranker:
    """GTE-Rerank-v2 重排序器"""
    
    def __init__(self, api_key: str):
        """
        初始化 GTE 重排序器
        
        Args:
            api_key: DashScope API密钥
        """
        self.api_key = api_key
        self.model = "gte-rerank-v2"  # DashScope 中的 GTE 重排序模型名称
        
        # 设置 API 密钥
        dashscope.api_key = api_key
        
        logger.info(f"初始化 GTE-Rerank 重排序器")
    
    def rerank(self, query: str, documents: List[str], top_k: Optional[int] = None) -> List[RerankResult]:
        """
        使用 GTE-Rerank 对文档进行重排序
        
        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回前K个结果，None表示返回所有
            
        Returns:
            重排序结果列表，按相关性分数降序排列
        """
        if not documents:
            return []
        
        if top_k is None:
            top_k = len(documents)
        
        logger.debug(f"使用 GTE-Rerank 重排序 {len(documents)} 个文档")
        
        try:
            # 使用 DashScope TextReRank API
            response = TextReRank.call(
                model=self.model,
                query=query,
                documents=documents,
                top_n=min(top_k, len(documents)),
                return_documents=True
            )
            
            if response.status_code != HTTPStatus.OK:
                logger.error(f"GTE重排序请求失败: {response.status_code} - {response.message}")
                return []
            
            # 解析响应
            if not hasattr(response, 'output') or not response.output:
                logger.error(f"GTE重排序响应格式错误: {response}")
                return []
            
            # 转换结果
            rerank_results = []
            for item in response.output.results:
                rerank_results.append(RerankResult(
                    index=item.index,
                    relevance_score=item.relevance_score,
                    text=documents[item.index]  # 直接使用原始文档
                ))
            
            logger.debug(f"GTE重排序完成，返回 {len(rerank_results)} 个结果")
            return rerank_results
            
        except Exception as e:
            logger.error(f"GTE重排序失败: {e}")
            return []
    
    def batch_rerank(self, queries: List[str], documents_list: List[List[str]], 
                     top_k: Optional[int] = None) -> List[List[RerankResult]]:
        """
        批量重排序
        
        Args:
            queries: 查询列表
            documents_list: 文档列表的列表
            top_k: 每个查询返回的结果数
            
        Returns:
            每个查询的重排序结果列表
        """
        results = []
        for query, documents in zip(queries, documents_list):
            result = self.rerank(query, documents, top_k)
            results.append(result)
        return results

def test_gte_reranker():
    """测试 GTE 重排序器"""
    print("=" * 60)
    print("🔍 测试 GTE-Rerank 重排序器")
    print("=" * 60)
    
    # 设置API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量")
        print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
        return
    
    # 创建重排序器
    reranker = GTEReranker(api_key)
    
    # 测试数据
    query = "蓝源的核心价值观"
    documents = [
        "蓝源科技致力于为客户提供优质的服务和产品。",
        "激情创业是蓝源的核心价值观之一，要求员工保持创新精神。",
        "团队合作在蓝源文化中占据重要地位。",
        "蓝源基本法规定了公司的基本制度和价值观体系。",
        "客户导向是蓝源始终坚持的经营理念。"
    ]
    
    print(f"查询: {query}")
    print(f"文档数量: {len(documents)}")
    print("\n原始文档:")
    for i, doc in enumerate(documents):
        print(f"  [{i}] {doc}")
    
    # 执行重排序
    print("\n🔄 执行重排序...")
    results = reranker.rerank(query, documents, top_k=3)
    
    print(f"\n✅ 重排序结果 (Top {len(results)}):")
    for i, result in enumerate(results):
        print(f"  [{i+1}] 分数: {result.relevance_score:.4f}")
        print(f"      原始索引: {result.index}")
        print(f"      内容: {result.text}")
        print()

if __name__ == "__main__":
    test_gte_reranker()