#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent2: RAG检索Agent
案例检索 + 风险控制（并行执行）
Author: Timo (miscdd@163.com)
License: MIT
"""

import logging
from typing import Dict, List
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RAGResult:
    """RAG检索结果"""
    cases: List[Dict]
    risks: List[str]
    risk_level: str
    confidence: float
    retrieval_time_ms: float


class Agent2RAG:
    """RAG检索Agent - 并行执行案例检索和风险控制"""
    
    def __init__(self):
        # 导入现有模块
        try:
            from case_retriever import CaseRetriever
            from risk_control import RiskController, RiskLevel
            self.case_retriever = CaseRetriever()
            self.risk_controller = RiskController()
            self.RiskLevel = RiskLevel
            self.available = True
        except ImportError as e:
            logger.warning(f"RAG模块导入失败: {e}")
            self.available = False
    
    def retrieve(self, query) -> RAGResult:
        """执行RAG检索（并行）
        
        Args:
            query: ParsedQuery对象
            
        Returns:
            RAGResult: 检索结果
        """
        import time
        start_time = time.time()
        
        if not self.available:
            return self._fallback_result(query)
        
        logger.info(f"🔍 开始RAG检索: 材料={query.material}")
        
        # 并行执行
        with ThreadPoolExecutor(max_workers=2) as executor:
            # 提交任务
            case_future = executor.submit(
                self._search_cases,
                query.material,
                query.dimensions,
                query.surface
            )
            
            risk_future = executor.submit(
                self._assess_risks,
                query
            )
            
            # 获取结果
            cases = case_future.result()
            risk_assessment = risk_future.result()
        
        # 计算置信度
        confidence = self._calculate_confidence(cases, risk_assessment)
        
        # 计算耗时
        retrieval_time = (time.time() - start_time) * 1000
        
        result = RAGResult(
            cases=cases,
            risks=risk_assessment.get('risks', []),
            risk_level=risk_assessment.get('level', 'LOW'),
            confidence=confidence,
            retrieval_time_ms=retrieval_time
        )
        
        logger.info(f"✅ RAG检索完成: {len(cases)}个案例, 置信度={confidence:.2f}, 耗时={retrieval_time:.0f}ms")
        return result
    
    def _search_cases(self, material: str, dimensions: List[float], surface: str) -> List[Dict]:
        """搜索相似案例"""
        try:
            results = self.case_retriever.search(
                material=material,
                dimensions=dimensions,
                surface=surface,
                top_k=5
            )
            
            # 转换为字典列表
            return [
                {
                    "case_id": r.case_id,
                    "material": r.material,
                    "price": r.price,
                    "similarity": r.similarity,
                    "metadata": r.metadata
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"案例检索失败: {e}")
            return []
    
    def _assess_risks(self, query) -> Dict:
        """评估风险"""
        try:
            assessment = self.risk_controller.assess({
                "unit_price": 50.0,  # 估算价格
                "material": query.material,
                "surface": query.surface
            })
            
            return {
                "risks": assessment.risks,
                "level": assessment.level.value,
                "score": assessment.score
            }
        except Exception as e:
            logger.error(f"风险评估失败: {e}")
            return {"risks": [], "level": "LOW", "score": 100}
    
    def _calculate_confidence(self, cases: List[Dict], risk_assessment: Dict) -> float:
        """计算置信度"""
        if not cases:
            return 0.5
        
        # 案例相似度
        avg_similarity = sum(c.get('similarity', 0.5) for c in cases) / len(cases)
        
        # 风险分数
        risk_score = risk_assessment.get('score', 100) / 100
        
        # 综合置信度
        confidence = avg_similarity * 0.7 + risk_score * 0.3
        
        return min(confidence, 1.0)
    
    def _fallback_result(self, query) -> RAGResult:
        """降级结果（模块不可用时）"""
        return RAGResult(
            cases=[{
                "case_id": "FALLBACK",
                "material": query.material,
                "price": 50.0,
                "similarity": 0.6,
                "metadata": {}
            }],
            risks=[],
            risk_level="LOW",
            confidence=0.6,
            retrieval_time_ms=10
        )


if __name__ == "__main__":
    # 测试
    from agent1_parser import ParsedQuery
    
    agent = Agent2RAG()
    
    test_query = ParsedQuery(
        material="AL6061",
        dimensions=[100, 50, 10],
        surface="anodize",
        quantity=10,
        deadline=None,
        special_requirements=[],
        raw_input="测试查询"
    )
    
    result = agent.retrieve(test_query)
    
    print(f"\n📊 RAG检索结果:")
    print(f"  案例数: {len(result.cases)}")
    print(f"  置信度: {result.confidence:.2f}")
    print(f"  风险等级: {result.risk_level}")
    print(f"  耗时: {result.retrieval_time_ms:.0f}ms")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")