"""
Hybrid Retriever - 混合检索器
Author: Timo (miscdd@163.com)
License: MIT
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """检索结果"""
    content: str
    score: float
    source: str
    metadata: Dict


class HybridRetriever:
    """混合检索器 - 向量检索 + 规则匹配"""
    
    def __init__(self, mode: str = "hybrid"):
        """
        初始化检索器
        
        Args:
            mode: 检索模式 (vector_only, rule_only, hybrid)
        """
        self.mode = mode
        self.vector_available = self._check_vector_support()
        logger.info(f"✅ 混合检索器初始化完成，模式: {mode}")
    
    def _check_vector_support(self) -> bool:
        """检查向量检索支持"""
        try:
            import faiss
            return True
        except ImportError:
            logger.warning("FAISS未安装，向量检索不可用")
            return False
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """
        执行检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filters: 过滤条件
        
        Returns:
            检索结果列表
        """
        results = []
        
        if self.mode in ["vector_only", "hybrid"] and self.vector_available:
            vector_results = self._vector_search(query, top_k)
            results.extend(vector_results)
        
        if self.mode in ["rule_only", "hybrid"]:
            rule_results = self._rule_match(query, filters, top_k)
            results.extend(rule_results)
        
        # 去重并排序
        results = self._deduplicate(results)
        results = sorted(results, key=lambda x: x.score, reverse=True)[:top_k]
        
        return results
    
    def _vector_search(self, query: str, top_k: int) -> List[RetrievalResult]:
        """向量检索"""
        # 简化实现 - 实际需要FAISS索引
        return [
            RetrievalResult(
                content=f"向量匹配: {query}",
                score=0.85,
                source="vector",
                metadata={"method": "semantic"}
            )
        ]
    
    def _rule_match(self, query: str, filters: Optional[Dict], top_k: int) -> List[RetrievalResult]:
        """规则匹配"""
        results = []
        
        # 材料关键词匹配
        materials = {
            "铝合金": "AL6061",
            "不锈钢": "SUS304",
            "钢": "STEEL45",
            "铝": "AL6061",
        }
        
        for keyword, material in materials.items():
            if keyword in query:
                results.append(RetrievalResult(
                    content=f"材料匹配: {material}",
                    score=0.9,
                    source="rule",
                    metadata={"material": material, "keyword": keyword}
                ))
        
        return results[:top_k]
    
    def _deduplicate(self, results: List[RetrievalResult]) -> List[RetrievalResult]:
        """去重"""
        seen = set()
        unique = []
        for r in results:
            key = r.content
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique


if __name__ == "__main__":
    retriever = HybridRetriever(mode="hybrid")
    results = retriever.retrieve("铝合金6061，表面阳极氧化")
    
    print("\n🔍 检索结果:")
    for r in results:
        print(f"  [{r.source}] {r.content} (score: {r.score})")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")