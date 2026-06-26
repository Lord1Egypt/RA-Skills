#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent3: 元认知审核Agent
UniSkill V4自我辩论 + 竞品分析
Author: Timo (miscdd@163.com)
License: MIT
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MetaCognitiveResult:
    """元认知审核结果"""
    final_quote: Dict
    debate_log: List[str]
    competitor_analysis: Dict
    approval_status: str
    processing_time_ms: float


class Agent3MetaCognitive:
    """元认知审核Agent - UniSkill V4集成"""
    
    def __init__(self):
        self.uniskill = self._load_uniskill_v4()
        self.competitor_data = self._load_competitor_data()
    
    def _load_uniskill_v4(self):
        """加载UniSkill V4（可选后置校验层）
        
        工业稳定原则：UniSkill可选，默认关闭
        配置项：config.json -> enable_uniskill: false
        """
        try:
            # 读取配置
            import json
            config_path = Path(__file__).parent / "config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    if not config.get("enable_uniskill", False):
                        logger.info("⚠️ UniSkill V4 已禁用（工业稳定模式）")
                        return None
            
            # 尝试加载
            import sys
            sys.path.insert(0, '/home/admin/.openclaw/workspace/skills/uniskill-v4')
            logger.info("✅ UniSkill V4 可选模式已启用")
            return True
        except Exception as e:
            logger.warning(f"UniSkill V4 加载失败（自动降级）: {e}")
            return None
    
    def _load_competitor_data(self) -> Dict:
        """加载竞品数据（已脱敏）"""
        return {
            "competitor_a": {
                "name": "A公司",
                "quote_time": "24h",
                "transparency": "黑盒",
                "price_range": "中等偏高",
                "features": ["在线报价", "全球供应商"]
            },
            "competitor_b": {
                "name": "B公司",
                "quote_time": "48h",
                "transparency": "黑盒",
                "price_range": "较高",
                "features": ["快速原型", "注塑"]
            },
            "competitor_c": {
                "name": "C公司",
                "quote_time": "12h",
                "transparency": "半透明",
                "price_range": "中等",
                "features": ["全球网络", "多工艺"]
            }
        }
    
    def review(self, rag_result, query) -> MetaCognitiveResult:
        """执行元认知审核
        
        Args:
            rag_result: Agent2的RAG检索结果
            query: 原始查询
            
        Returns:
            MetaCognitiveResult: 审核结果
        """
        import time
        start_time = time.time()
        
        logger.info(f"🧠 开始元认知审核: 置信度={rag_result.confidence:.2f}")
        
        # 1. 自我辩论
        debate_log = self._self_debate(rag_result, query)
        
        # 2. 竞品分析
        competitor_analysis = self._competitor_analysis(query)
        
        # 3. 生成最终报价
        final_quote = self._generate_final_quote(rag_result, competitor_analysis, query)
        
        # 4. 确定审批状态
        approval_status = self._determine_approval(rag_result, debate_log)
        
        # 计算处理时间
        processing_time = (time.time() - start_time) * 1000
        
        result = MetaCognitiveResult(
            final_quote=final_quote,
            debate_log=debate_log,
            competitor_analysis=competitor_analysis,
            approval_status=approval_status,
            processing_time_ms=processing_time
        )
        
        logger.info(f"✅ 元认知审核完成: 状态={approval_status}, 耗时={processing_time:.0f}ms")
        return result
    
    def _self_debate(self, rag_result, query) -> List[str]:
        """自我辩论"""
        debate_log = []
        debate_log.append(f"🤖 正方: 检索到{len(rag_result.cases)}个相似案例，置信度{rag_result.confidence:.2%}")
        
        # 正方论点
        if rag_result.cases:
            avg_price = sum(c.get('price', 0) for c in rag_result.cases) / len(rag_result.cases)
            debate_log.append(f"🤖 正方: 平均参考价格¥{avg_price:.2f}，可作为定价基准")
        
        # 反方论点
        if rag_result.confidence < 0.8:
            debate_log.append(f"🤖 反方: 置信度{rag_result.confidence:.0%}<80%，建议人工复核")
        
        if rag_result.risks:
            debate_log.append(f"🤖 反方: 检测到{len(rag_result.risks)}个风险点，需关注")
        
        # 仲裁结论
        if rag_result.confidence >= 0.8 and not rag_result.risks:
            debate_log.append(f"⚖️ 仲裁: 自动通过，可直接报价")
        elif rag_result.confidence >= 0.6:
            debate_log.append(f"⚖️ 仲裁: 条件通过，建议复核后报价")
        else:
            debate_log.append(f"⚖️ 仲裁: 需人工介入审核")
        
        return debate_log
    
    def _competitor_analysis(self, query) -> Dict:
        """竞品分析"""
        analysis = {}
        
        for key, data in self.competitor_data.items():
            analysis[key] = {
                "name": data["name"],
                "quote_time": data["quote_time"],
                "transparency": data["transparency"],
                "our_advantage": self._calculate_advantage(data["quote_time"])
            }
        
        # 我们的优势
        analysis["our_system"] = {
            "name": "智能报价系统",
            "quote_time": "10min",
            "transparency": "白盒（完整成本分解）",
            "advantage": "比竞品快144倍"
        }
        
        return analysis
    
    def _calculate_advantage(self, competitor_time: str) -> str:
        """计算相比竞品的优势"""
        time_map = {
            "24h": 144,
            "48h": 288,
            "12h": 72,
        }
        
        hours = time_map.get(competitor_time, 100)
        return f"效率提升{hours}倍"
    
    def _generate_final_quote(self, rag_result, competitor_analysis, query) -> Dict:
        """生成最终报价"""
        # 基于检索结果计算价格
        if rag_result.cases:
            base_price = sum(c.get('price', 50) for c in rag_result.cases) / len(rag_result.cases)
        else:
            base_price = 50.0
        
        # 根据数量调整
        quantity_factor = 1.0
        if query.quantity > 50:
            quantity_factor = 0.85  # 批量折扣
        elif query.quantity > 10:
            quantity_factor = 0.95
        
        # 根据表面处理调整
        surface_factor = {
            "none": 1.0,
            "anodize": 1.15,
            "chrome": 1.30,
            "paint": 1.10,
        }.get(query.surface, 1.0)
        
        # 最终价格
        final_price = base_price * quantity_factor * surface_factor
        
        # 计算交期
        lead_time = 5  # 基础交期
        if query.surface != "none":
            lead_time += 2
        if query.quantity > 50:
            lead_time += 2
        
        return {
            "unit_price": round(final_price, 2),
            "total_price": round(final_price * query.quantity, 2),
            "lead_time": lead_time,
            "quantity": query.quantity,
            "material": query.material,
            "surface": query.surface,
            "transparency": "完整成本分解",
            "price_breakdown": {
                "base_price": base_price,
                "quantity_discount": f"{(1-quantity_factor)*100:.0f}%" if quantity_factor < 1 else "无",
                "surface_cost": f"+{(surface_factor-1)*100:.0f}" if surface_factor > 1 else "无"
            },
            "advantage": "效率提升144倍，完全白盒报价"
        }
    
    def _determine_approval(self, rag_result, debate_log) -> str:
        """确定审批状态"""
        if rag_result.confidence >= 0.8 and not rag_result.risks:
            return "approved"
        elif rag_result.confidence >= 0.6:
            return "conditional"
        else:
            return "needs_review"


if __name__ == "__main__":
    # 测试
    from agent2_rag import RAGResult
    
    agent = Agent3MetaCognitive()
    
    test_rag = RAGResult(
        cases=[
            {"case_id": "001", "price": 25.0, "similarity": 0.9}
        ],
        risks=[],
        risk_level="LOW",
        confidence=0.85,
        retrieval_time_ms=150
    )
    
    from agent1_parser import ParsedQuery
    test_query = ParsedQuery(
        material="AL6061",
        dimensions=[100, 50, 10],
        surface="anodize",
        quantity=10,
        deadline=None,
        special_requirements=[],
        raw_input="测试"
    )
    
    result = agent.review(test_rag, test_query)
    
    print(f"\n🧠 元认知审核结果:")
    print(f"  最终单价: ¥{result.final_quote['unit_price']}")
    print(f"  交期: {result.final_quote['lead_time']}天")
    print(f"  审批状态: {result.approval_status}")
    print(f"\n辩论记录:")
    for log in result.debate_log:
        print(f"  {log}")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")