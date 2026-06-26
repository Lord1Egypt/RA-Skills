#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workflow编排引擎
串联Agent1 → Agent2 → Agent3 完整流程
Author: Timo (miscdd@163.com)
License: MIT
"""

import yaml
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkflowEngine:
    """Workflow编排引擎"""
    
    def __init__(self, workflow_path: str = None):
        """初始化Workflow引擎
        
        Args:
            workflow_path: workflow.yaml路径
        """
        if workflow_path is None:
            workflow_path = Path(__file__).parent / "workflow.yaml"
        
        self.workflow = self._load_workflow(workflow_path)
        self.agents = self._init_agents()
        self.execution_history = []
    
    def _load_workflow(self, path: str) -> Dict:
        """加载Workflow定义"""
        with open(path, 'r', encoding='utf-8') as f:
            workflow = yaml.safe_load(f)
        
        logger.info(f"✅ Workflow加载成功: v{workflow.get('version', 'unknown')}")
        return workflow
    
    def _init_agents(self) -> Dict:
        """初始化所有Agent"""
        from agent1_parser import Agent1Parser
        from agent2_rag import Agent2RAG
        from agent3_meta import Agent3MetaCognitive
        
        agents = {
            'agent1_parser': Agent1Parser(),
            'agent2_rag': Agent2RAG(),
            'agent3_meta': Agent3MetaCognitive(),
        }
        
        logger.info(f"✅ 已初始化 {len(agents)} 个Agent")
        return agents
    
    def execute(self, user_input: str, fallback_mode: bool = False) -> Dict[str, Any]:
        """执行完整Workflow
        
        Args:
            user_input: 用户输入文本
            fallback_mode: 是否启用兜底模式
            
        Returns:
            完整执行结果
        """
        start_time = datetime.now()
        execution_id = start_time.strftime("%Y%m%d_%H%M%S")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 开始执行Workflow: {execution_id}")
        logger.info(f"📝 用户输入: {user_input}")
        logger.info(f"{'='*60}")
        
        result = {
            "execution_id": execution_id,
            "workflow_version": self.workflow.get('version', '2.0.1'),
            "user_input": user_input,
            "success": False,
            "steps": {},
            "mode": "full_workflow"
        }
        
        try:
            # Step 1: 输入解析
            logger.info("\n🔄 Step 1: 输入解析 (Agent1)")
            parsed_query = self.agents['agent1_parser'].parse(user_input)
            result["steps"]["agent1"] = {
                "status": "success",
                "output": {
                    "material": parsed_query.material,
                    "dimensions": parsed_query.dimensions,
                    "surface": parsed_query.surface,
                    "quantity": parsed_query.quantity
                }
            }
            
            # 兜底模式判断
            if fallback_mode or self._should_fallback(parsed_query):
                logger.info("⚠️ 启动Rule-Only兜底模式")
                return self._execute_fallback(parsed_query, result)
            
            # Step 2: RAG检索
            logger.info("\n🔄 Step 2: RAG检索 (Agent2)")
            rag_result = self.agents['agent2_rag'].retrieve(parsed_query)
            result["steps"]["agent2"] = {
                "status": "success",
                "output": {
                    "cases_count": len(rag_result.cases),
                    "confidence": rag_result.confidence,
                    "risk_level": rag_result.risk_level,
                    "retrieval_time_ms": rag_result.retrieval_time_ms
                }
            }
            
            # Step 3: 元认知审核（UniSkill可选）
            logger.info("\n🔄 Step 3: 元认知审核 (Agent3)")
            meta_result = self.agents['agent3_meta'].review(rag_result, parsed_query)
            result["steps"]["agent3"] = {
                "status": "success",
                "output": {
                    "unit_price": meta_result.final_quote['unit_price'],
                    "lead_time": meta_result.final_quote['lead_time'],
                    "approval_status": meta_result.approval_status,
                    "processing_time_ms": meta_result.processing_time_ms
                }
            }
            
            # 汇总结果
            result["success"] = True
            result["final_quote"] = meta_result.final_quote
            result["debate_log"] = meta_result.debate_log
            result["competitor_analysis"] = meta_result.competitor_analysis
            
        except Exception as e:
            logger.error(f"❌ Workflow执行失败: {e}")
            logger.info("⚠️ 自动降级到Rule-Only兜底模式")
            
            # 自动降级
            if "parsed_query" in locals():
                return self._execute_fallback(parsed_query, result)
            
            result["error"] = str(e)
            result["success"] = False
            result["mode"] = "error_fallback"
        
        # 计算总耗时
        end_time = datetime.now()
        result["duration_seconds"] = (end_time - start_time).total_seconds()
        
        # 记录执行历史
        self.execution_history.append(result)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Workflow执行完成: {result['duration_seconds']:.2f}秒")
        logger.info(f"{'='*60}")
        
        return result
    
    def _should_fallback(self, query) -> bool:
        """判断是否需要降级到兜底模式
        
        工业稳定铁律：
        - 新材料（无历史数据）
        - 特殊要求过多
        - 系统不稳定时
        """
        # 检查配置
        try:
            import json
            config_path = Path(__file__).parent / "config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # 生产模式强制兜底
                    if config.get("stability", {}).get("mode") == "production":
                        return True
        except:
            pass
        
        return False
    
    def _execute_fallback(self, query, result: Dict) -> Dict:
        """执行Rule-Only兜底模式"""
        from rule_only import RuleOnlyEngine
        
        engine = RuleOnlyEngine()
        quote = engine.calculate(
            query.material,
            query.dimensions,
            query.surface,
            query.quantity
        )
        
        result["success"] = True
        result["mode"] = "rule_only_fallback"
        result["final_quote"] = {
            "unit_price": quote.unit_price,
            "total_price": quote.total_price,
            "lead_time": quote.lead_time,
            "material": query.material,
            "surface": query.surface,
            "quantity": query.quantity,
            "transparency": "纯规则计算，100%稳定",
            "mode": quote.mode
        }
        result["debate_log"] = ["⚠️ Rule-Only兜底模式启动", "✅ 纯规则计算完成"]
        
        return result
    
    def generate_report(self, result: Dict) -> str:
        """生成报价报告
        
        Args:
            result: Workflow执行结果
            
        Returns:
            Markdown格式的报告
        """
        if not result.get("success"):
            return f"❌ Workflow执行失败: {result.get('error', '未知错误')}"
        
        quote = result.get("final_quote", {})
        steps = result.get("steps", {})
        
        report = f"""# 🦫 CNC智能报价报告

> Workflow版本: {result.get('workflow_version', '2.0.0')}  
> 执行ID: {result.get('execution_id', 'N/A')}  
> 处理时间: {result.get('duration_seconds', 0):.2f}秒

---

## 📊 报价明细

| 项目 | 值 |
|------|-----|
| **材料** | {quote.get('material', 'N/A')} |
| **单价** | ¥{quote.get('unit_price', 0):.2f} |
| **总价** | ¥{quote.get('total_price', 0):.2f} |
| **数量** | {quote.get('quantity', 1)}件 |
| **交期** | {quote.get('lead_time', 5)}天 |
| **表面处理** | {quote.get('surface', '无')} |

---

## 📋 成本分解

| 项目 | 说明 |
|------|------|
| 基础价格 | ¥{quote.get('price_breakdown', {}).get('base_price', 0):.2f} |
| 数量折扣 | {quote.get('price_breakdown', {}).get('quantity_discount', '无')} |
| 表面处理 | {quote.get('price_breakdown', {}).get('surface_cost', '无')} |

---

## ⚠️ 风险预警

"""
        # 从Agent2获取风险
        agent2_output = steps.get("agent2", {}).get("output", {})
        risk_level = agent2_output.get("risk_level", "LOW")
        confidence = agent2_output.get("confidence", 0)
        
        report += f"""**风险等级**: {risk_level}  
**置信度**: {confidence:.0%}

"""
        
        # 竞品对比
        report += """---

## 📊 行业对比

| 平台类型 | 平均报价时间 | 透明度 | 我们的优势 |
|------|----------|--------|-----------|
| A类平台 | 24h | 黑盒 | 效率提升144倍 |
| B类平台 | 48h | 黑盒 | 效率提升288倍 |
| C类平台 | 12h | 半透明 | 效率提升72倍 |
| **我们的系统** | **10min** | **白盒** | - |

---

## 🧠 元认知辩论记录

"""
        for log in result.get("debate_log", []):
            report += f"- {log}\n"
        
        report += f"""
---

## ✅ 审批状态

**{result.get("final_quote", {}).get("approval_status", "pending").upper()}**

---

> 🦫 海狸 (Beaver) | 靠得住、能干事、在状态  
> Author: Timo (miscdd@163.com)
"""
        
        return report


def main():
    """主函数 - 测试运行"""
    print("\n" + "="*60)
    print("🦫 CNC智能报价Workflow - 测试运行")
    print("="*60)
    
    # 创建引擎
    engine = WorkflowEngine()
    
    # 测试用例
    test_cases = [
        "铝合金6061，100x50x10mm，表面阳极氧化，10件",
        "不锈钢304，200x100x5mm，镀铬，加急，50件",
        "45号钢，80x40x8mm，淬火处理，下周要货",
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n\n{'='*60}")
        print(f"测试用例 {i}: {test_input}")
        print("="*60)
        
        # 执行Workflow
        result = engine.execute(test_input)
        
        # 生成报告
        report = engine.generate_report(result)
        print(report)
    
    print("\n\n" + "="*60)
    print("✅ 测试完成")
    print("="*60)


if __name__ == "__main__":
    main()