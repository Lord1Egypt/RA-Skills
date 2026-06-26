"""
Creative Explorer - 创造模式（OOCA）

基于联想驱动的创造性问题解决。
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime


class CreativeExplorer:
    """创造性探索器 - OOCA 创造模式"""
    
    def __init__(self, creativity_threshold: float = 0.6):
        self.creativity_threshold = creativity_threshold
        self.idea_pool = []
    
    async def explore(self, task: str, context: Dict = None, tools: Any = None) -> Dict:
        """
        执行创造性探索
        
        Args:
            task: 任务描述
            context: 上下文信息
            tools: 工具接口
        
        Returns:
            创造性解决方案
        """
        print(f"[OOCA] 开始创造性探索：{task}")
        
        # 1. 概念分解
        concepts = self._decompose_concepts(task)
        
        # 2. 联想生成
        associations = self._generate_associations(concepts)
        
        # 3. 概念融合
        fused_ideas = self._fuse_concepts(associations)
        
        # 4. 创意评估
        evaluated_ideas = self._evaluate_ideas(fused_ideas)
        
        # 5. 方案生成
        solution = self._generate_solution(evaluated_ideas, task)
        
        result = {
            "mode": "OOCA",
            "concepts": concepts,
            "associations": associations,
            "fused_ideas": fused_ideas,
            "evaluated_ideas": evaluated_ideas,
            "solution": solution,
            "creativity_score": self._assess_creativity(solution),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"[OOCA] 完成，创造力评分：{result['creativity_score']:.2f}")
        
        return result
    
    def _decompose_concepts(self, task: str) -> List[str]:
        """概念分解"""
        # 简单实现：提取关键词
        # 实际实现应该使用 NLP 技术
        
        # 移除常见停用词
        stop_words = ["的", "了", "在", "是", "我", "有", "和", "就", "不", "与"]
        words = [w for w in task if w not in stop_words]
        
        # 提取 3-5 个核心概念
        concepts = words[:5]
        
        return concepts
    
    def _generate_associations(self, concepts: List[str]) -> Dict[str, List[str]]:
        """联想生成"""
        associations = {}
        
        # 预定义的联想库（简化实现）
        association_db = {
            "用户": ["体验", "需求", "反馈", "行为", "场景"],
            "数据": ["分析", "可视化", "趋势", "模式", "洞察"],
            "产品": ["功能", "设计", "优化", "迭代", "创新"],
            "营销": ["渠道", "内容", "转化", "品牌", "传播"],
            "设计": ["视觉", "交互", "用户体验", "美学", "功能"]
        }
        
        for concept in concepts:
            # 查找预定义联想
            if concept in association_db:
                associations[concept] = association_db[concept]
            else:
                # 生成随机联想（简化）
                associations[concept] = [
                    f"{concept}相关 1",
                    f"{concept}相关 2",
                    f"{concept}相关 3"
                ]
        
        return associations
    
    def _fuse_concepts(self, associations: Dict[str, List[str]]) -> List[Dict]:
        """概念融合"""
        fused_ideas = []
        
        concepts = list(associations.keys())
        
        # 生成概念组合
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                concept1 = concepts[i]
                concept2 = concepts[j]
                
                # 随机选择联想进行融合
                assoc1 = random.choice(associations[concept1])
                assoc2 = random.choice(associations[concept2])
                
                fused_ideas.append({
                    "type": "concept_fusion",
                    "elements": [concept1, concept2],
                    "associations": [assoc1, assoc2],
                    "fusion_idea": f"将{concept1}的{assoc1}与{concept2}的{assoc2}结合"
                })
        
        return fused_ideas
    
    def _evaluate_ideas(self, fused_ideas: List[Dict]) -> List[Dict]:
        """创意评估"""
        evaluated = []
        
        for idea in fused_ideas:
            # 评估维度
            novelty = random.uniform(0.5, 1.0)  # 新颖性
            feasibility = random.uniform(0.5, 1.0)  # 可行性
            impact = random.uniform(0.5, 1.0)  # 影响力
            
            # 综合评分
            overall_score = (novelty + feasibility + impact) / 3
            
            evaluated.append({
                **idea,
                "evaluation": {
                    "novelty": novelty,
                    "feasibility": feasibility,
                    "impact": impact,
                    "overall_score": overall_score
                },
                "recommendation": "推荐" if overall_score >= self.creativity_threshold else "保留"
            })
        
        # 按评分排序
        evaluated.sort(key=lambda x: x["evaluation"]["overall_score"], reverse=True)
        
        return evaluated
    
    def _generate_solution(self, evaluated_ideas: List[Dict], task: str) -> Dict:
        """生成解决方案"""
        # 选择前 3 个最佳创意
        top_ideas = evaluated_ideas[:3]
        
        # 生成综合方案
        solution = {
            "task": task,
            "recommended_approach": top_ideas[0]["fusion_idea"] if top_ideas else "无推荐方案",
            "alternative_approaches": [idea["fusion_idea"] for idea in top_ideas[1:]],
            "key_concepts": list(set(
                concept for idea in top_ideas 
                for concept in idea.get("elements", [])
            )),
            "creativity_highlights": [
                f"新颖性：{idea['evaluation']['novelty']:.2f}" 
                for idea in top_ideas
            ],
            "implementation_notes": [
                "建议先验证可行性",
                "考虑资源约束",
                "小范围试点测试"
            ]
        }
        
        return solution
    
    def _assess_creativity(self, solution: Dict) -> float:
        """评估创造力"""
        # 基于解决方案的多样性评估
        concept_count = len(solution.get("key_concepts", []))
        approach_count = 1 + len(solution.get("alternative_approaches", []))
        
        # 创造力评分
        creativity = min(1.0, (concept_count * 0.1 + approach_count * 0.2))
        
        return creativity


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        explorer = CreativeExplorer(creativity_threshold=0.6)
        
        task = "设计一个创新的营销活动方案"
        result = await explorer.explore(task)
        
        print("\n=== 创造性探索结果 ===")
        print(f"核心概念：{result.get('concepts', [])}")
        print(f"生成创意数：{len(result.get('fused_ideas', []))}")
        print(f"推荐方案：{result.get('solution', {}).get('recommended_approach', 'N/A')}")
        print(f"创造力评分：{result.get('creativity_score', 0):.2f}")
        
        if result.get("solution", {}).get("alternative_approaches"):
            print("\n替代方案:")
            for i, approach in enumerate(result["solution"]["alternative_approaches"], 1):
                print(f"  {i}. {approach}")
    
    asyncio.run(demo())
