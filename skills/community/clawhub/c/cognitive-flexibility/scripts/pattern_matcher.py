"""
Pattern Matcher - 经验模式（OOA）

基于记忆驱动的模式匹配和案例检索。
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class PatternMatcher:
    """模式匹配器 - OOA 经验模式"""
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold
        self.patterns = []
        self.cases = []
    
    async def match(self, task: str, tools: Any = None) -> Dict:
        """
        匹配历史模式和案例
        
        Args:
            task: 当前任务
            tools: 工具接口
        
        Returns:
            匹配结果
        """
        print(f"[OOA] 开始模式匹配：{task}")
        
        # 1. 检索相似任务
        similar_tasks = await self._retrieve_similar_tasks(task, tools)
        
        # 2. 提取模式
        patterns = self._extract_patterns(similar_tasks)
        
        # 3. 匹配最佳案例
        best_match = self._find_best_match(task, patterns)
        
        # 4. 评估适用性
        applicability = self._evaluate_applicability(best_match, task)
        
        result = {
            "mode": "OOA",
            "similar_tasks": similar_tasks,
            "patterns": patterns,
            "best_match": best_match,
            "applicability": applicability,
            "confidence": applicability["score"],
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"[OOA] 完成，匹配度：{applicability['score']:.2f}")
        
        return result
    
    async def _retrieve_similar_tasks(self, task: str, tools: Any = None) -> List[Dict]:
        """检索相似任务"""
        similar_tasks = []
        
        # 使用 memory_search 检索
        if tools and hasattr(tools, 'memory_search'):
            memories = await tools.memory_search(query=task, maxResults=10)
            similar_tasks = memories.get('results', [])
        
        # 过滤高相似度任务
        filtered = []
        for task_item in similar_tasks:
            similarity = self._calculate_similarity(task, task_item)
            if similarity >= self.similarity_threshold:
                task_item['similarity'] = similarity
                filtered.append(task_item)
        
        # 按相似度排序
        filtered.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        
        return filtered[:5]  # 返回前 5 个
    
    def _extract_patterns(self, similar_tasks: List[Dict]) -> List[Dict]:
        """从相似任务中提取模式"""
        patterns = []
        
        for task in similar_tasks:
            # 提取任务模式
            pattern = {
                "task_type": task.get("task_type", "unknown"),
                "solution_approach": task.get("solution_approach", ""),
                "success_factors": task.get("success_factors", []),
                "pitfalls": task.get("pitfalls", []),
                "similarity": task.get("similarity", 0)
            }
            patterns.append(pattern)
        
        return patterns
    
    def _find_best_match(self, task: str, patterns: List[Dict]) -> Optional[Dict]:
        """找到最佳匹配模式"""
        if not patterns:
            return None
        
        # 选择相似度最高的模式
        best = max(patterns, key=lambda p: p.get('similarity', 0))
        
        return {
            "pattern": best,
            "confidence": best.get('similarity', 0)
        }
    
    def _evaluate_applicability(self, best_match: Optional[Dict], current_task: str) -> Dict:
        """评估模式适用性"""
        if not best_match:
            return {
                "score": 0.0,
                "level": "无匹配",
                "recommendation": "无历史经验可参考，建议使用其他认知模式"
            }
        
        pattern = best_match.get("pattern", {})
        similarity = pattern.get("similarity", 0)
        
        # 评估适用性
        if similarity >= 0.9:
            level = "高"
            recommendation = "高度匹配，可直接应用历史经验"
        elif similarity >= 0.7:
            level = "中"
            recommendation = "中度匹配，可参考历史经验但需调整"
        else:
            level = "低"
            recommendation = "低度匹配，建议谨慎参考或切换模式"
        
        return {
            "score": similarity,
            "level": level,
            "recommendation": recommendation,
            "success_factors": pattern.get("success_factors", []),
            "pitfalls": pattern.get("pitfalls", [])
        }
    
    def _calculate_similarity(self, task1: str, task2: Dict) -> float:
        """计算任务相似度（简单实现）"""
        # 实际实现应该使用更复杂的相似度算法
        # 这里使用简单的关键词重叠度
        
        task1_keywords = set(task1.lower().split())
        task2_text = task2.get("text", "") or task2.get("task", "")
        task2_keywords = set(task2_text.lower().split())
        
        if not task1_keywords or not task2_keywords:
            return 0.0
        
        intersection = task1_keywords & task2_keywords
        union = task1_keywords | task2_keywords
        
        return len(intersection) / len(union) if union else 0.0
    
    def apply_pattern(self, pattern: Dict, current_task: str) -> Dict:
        """应用模式到当前任务"""
        return {
            "original_task": current_task,
            "applied_pattern": pattern,
            "adapted_solution": self._adapt_solution(pattern, current_task),
            "expected_outcome": pattern.get("success_factors", []),
            "risks": pattern.get("pitfalls", [])
        }
    
    def _adapt_solution(self, pattern: Dict, current_task: str) -> str:
        """调整解决方案以适应当前任务"""
        # 简单实现：直接返回模式的解决方案
        # 实际实现需要根据当前任务调整
        
        approach = pattern.get("solution_approach", "")
        return f"基于历史经验：{approach}"


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        matcher = PatternMatcher(similarity_threshold=0.7)
        
        task = "分析用户反馈数据，找出主要问题"
        result = await matcher.match(task)
        
        print("\n=== 模式匹配结果 ===")
        print(f"模式：{result.get('mode', 'N/A')}")
        print(f"置信度：{result.get('confidence', 0):.2f}")
        print(f"相似任务数：{len(result.get('similar_tasks', []))}")
        print(f"提取模式数：{len(result.get('patterns', []))}")
        
        if result.get("best_match"):
            print(f"\n最佳匹配：{result['best_match']['pattern'].get('task_type', 'N/A')}")
            print(f"适用性：{result.get('applicability', {}).get('recommendation', 'N/A')}")
    
    asyncio.run(demo())
