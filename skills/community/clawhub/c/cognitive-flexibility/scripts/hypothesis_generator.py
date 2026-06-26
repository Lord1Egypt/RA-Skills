"""
Hypothesis Generator - 发现模式（OOHA）

基于假说驱动的探索性研究。
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime


class HypothesisGenerator:
    """假说生成器 - OOHA 发现模式"""
    
    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold
        self.hypotheses = []
    
    async def discover(self, task: str, context: Dict = None, tools: Any = None) -> Dict:
        """
        执行探索性发现
        
        Args:
            task: 任务描述
            context: 上下文信息
            tools: 工具接口
        
        Returns:
            发现结果
        """
        print(f"[OOHA] 开始探索性发现：{task}")
        
        # 1. 问题定义
        problem = self._define_problem(task)
        
        # 2. 假说生成
        hypotheses = self._generate_hypotheses(problem)
        
        # 3. 实验设计
        experiments = self._design_experiments(hypotheses)
        
        # 4. 验证计划
        validation_plan = self._create_validation_plan(experiments)
        
        # 5. 发现总结
        discovery = self._summarize_discovery(validation_plan, task)
        
        result = {
            "mode": "OOHA",
            "problem": problem,
            "hypotheses": hypotheses,
            "experiments": experiments,
            "validation_plan": validation_plan,
            "discovery": discovery,
            "confidence": self._assess_confidence(discovery),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"[OOHA] 完成，置信度：{result['confidence']:.2f}")
        
        return result
    
    def _define_problem(self, task: str) -> Dict:
        """问题定义"""
        # 提取核心问题
        question_words = ["为什么", "如何", "什么", "哪里", "何时", "谁"]
        
        core_question = task
        for word in question_words:
            if word in task:
                core_question = task[task.index(word):]
                break
        
        return {
            "core_question": core_question,
            "background": task.replace(core_question, "").strip(),
            "unknown_factors": self._identify_unknowns(task),
            "known_factors": self._identify_knowns(task)
        }
    
    def _generate_hypotheses(self, problem: Dict) -> List[Dict]:
        """假说生成"""
        hypotheses = []
        
        # 预定义的假说模式
        hypothesis_patterns = [
            "可能是{factor}导致了{outcome}",
            "{factor}与{outcome}之间存在相关性",
            "如果改变{factor}，{outcome}会发生变化",
            "{outcome}的根本原因是{factor}",
            "{factor}是影响{outcome}的关键变量"
        ]
        
        unknowns = problem.get("unknown_factors", ["因素 A", "因素 B"])
        knowns = problem.get("known_factors", ["结果 X"])
        
        # 生成假说
        for i, pattern in enumerate(hypothesis_patterns[:3]):  # 生成 3 个假说
            hypothesis = {
                "id": f"H{i+1}",
                "statement": pattern.format(
                    factor=random.choice(unknowns),
                    outcome=random.choice(knowns)
                ),
                "type": "causal" if "导致" in pattern or "原因" in pattern else "correlational",
                "confidence": random.uniform(0.3, 0.8),
                "testable": True,
                "rationale": f"基于{problem.get('core_question', '问题')}的分析"
            }
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def _design_experiments(self, hypotheses: List[Dict]) -> List[Dict]:
        """实验设计"""
        experiments = []
        
        for hypothesis in hypotheses:
            experiment = {
                "hypothesis_id": hypothesis["id"],
                "objective": f"验证假说{hypothesis['id']}: {hypothesis['statement']}",
                "methodology": self._select_methodology(hypothesis),
                "variables": {
                    "independent": "待确定的自变量",
                    "dependent": "待确定的因变量",
                    "controlled": ["环境变量", "时间因素"]
                },
                "data_collection": [
                    "定量数据收集",
                    "定性数据收集",
                    "对照组设置"
                ],
                "success_criteria": [
                    "统计显著性 p<0.05",
                    "效应量>0.3",
                    "可重复性验证"
                ],
                "estimated_duration": "1-2 周",
                "resources_needed": ["数据收集工具", "分析软件", "实验对象"]
            }
            experiments.append(experiment)
        
        return experiments
    
    def _select_methodology(self, hypothesis: Dict) -> str:
        """选择研究方法"""
        if hypothesis["type"] == "causal":
            return "控制实验 + 因果推断"
        else:
            return "相关性分析 + 回归模型"
    
    def _create_validation_plan(self, experiments: List[Dict]) -> Dict:
        """创建验证计划"""
        return {
            "phase_1": {
                "name": "初步验证",
                "duration": "1 周",
                "activities": [
                    "文献回顾",
                    "数据收集框架设计",
                    "小样本试点测试"
                ],
                "deliverables": ["验证报告", "数据收集工具"]
            },
            "phase_2": {
                "name": "全面验证",
                "duration": "2-3 周",
                "activities": [
                    "大规模数据收集",
                    "统计分析",
                    "假说检验"
                ],
                "deliverables": ["分析报告", "验证结论"]
            },
            "phase_3": {
                "name": "结论总结",
                "duration": "1 周",
                "activities": [
                    "结果解释",
                    "局限性分析",
                    "后续研究方向"
                ],
                "deliverables": ["最终报告", "研究论文"]
            }
        }
    
    def _summarize_discovery(self, validation_plan: Dict, task: str) -> Dict:
        """总结发现"""
        return {
            "research_question": task,
            "proposed_hypotheses": 3,
            "experimental_approach": "混合方法（定量 + 定性）",
            "timeline": "4-5 周",
            "expected_outcomes": [
                "验证/证伪假说",
                "发现新的关联关系",
                "提出理论模型"
            ],
            "potential_impact": [
                "理论贡献",
                "实践指导",
                "后续研究基础"
            ],
            "limitations": [
                "样本代表性",
                "因果推断局限",
                "外部效度"
            ],
            "next_steps": [
                "启动 phase_1 初步验证",
                "收集相关文献",
                "设计数据收集工具"
            ]
        }
    
    def _assess_confidence(self, discovery: Dict) -> float:
        """评估置信度"""
        # 基于发现完整性评估
        completeness = 0.0
        
        if discovery.get("research_question"):
            completeness += 0.2
        if discovery.get("proposed_hypotheses", 0) >= 3:
            completeness += 0.3
        if discovery.get("experimental_approach"):
            completeness += 0.2
        if discovery.get("timeline"):
            completeness += 0.1
        if discovery.get("next_steps"):
            completeness += 0.2
        
        return min(1.0, completeness)
    
    def _identify_unknowns(self, task: str) -> List[str]:
        """识别未知因素"""
        # 简化实现
        return ["未知因素 A", "未知因素 B", "潜在变量 C"]
    
    def _identify_knowns(self, task: str) -> List[str]:
        """识别已知因素"""
        # 简化实现
        return ["已知结果 X", "观察现象 Y"]


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        generator = HypothesisGenerator(confidence_threshold=0.5)
        
        task = "为什么用户留存率下降？"
        result = await generator.discover(task)
        
        print("\n=== 探索性发现结果 ===")
        print(f"核心问题：{result.get('problem', {}).get('core_question', 'N/A')}")
        print(f"生成假说数：{len(result.get('hypotheses', []))}")
        print(f"实验设计数：{len(result.get('experiments', []))}")
        print(f"验证阶段：{len(result.get('validation_plan', {}))}个阶段")
        print(f"置信度：{result.get('confidence', 0):.2f}")
        
        if result.get("hypotheses"):
            print("\n生成的假说:")
            for i, hyp in enumerate(result["hypotheses"], 1):
                print(f"  H{i}: {hyp['statement']} (置信度：{hyp['confidence']:.2f})")
    
    asyncio.run(demo())
