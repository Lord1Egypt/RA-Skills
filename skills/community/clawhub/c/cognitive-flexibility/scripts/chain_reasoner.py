"""
OODA Reasoner - 知识驱动推理模式

基于 OODA 循环（Observe-Orient-Decide-Act）实现链式推理能力。
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class OODAReasoner:
    """OODA 推理器 - 知识驱动推理模式"""
    
    def __init__(self, confidence_threshold: float = 0.7):
        self.confidence_threshold = confidence_threshold
        self.reasoning_chain = []
        self.memories = []
    
    async def observe(self, task: str, tools: Any = None) -> Dict:
        """
        观察阶段：检索相关知识
        
        Args:
            task: 任务描述
            tools: 工具接口（包含 memory_search 等）
        
        Returns:
            观察结果字典
        """
        print(f"[OODA] 观察阶段：{task}")
        
        # 调用 memory_search 检索历史经验
        if tools and hasattr(tools, 'memory_search'):
            memories = await tools.memory_search(query=task, maxResults=5)
            self.memories = memories.get('results', [])
        else:
            self.memories = []
        
        return {
            "task": task,
            "relevant_memories": self.memories,
            "context": self._extract_context(self.memories),
            "timestamp": datetime.now().isoformat()
        }
    
    async def orient(self, observation: Dict) -> Dict:
        """
        判断阶段：分析情境
        
        Args:
            observation: 观察结果
        
        Returns:
            情境分析结果
        """
        print("[OODA] 判断阶段：分析情境")
        
        task = observation.get("task", "")
        memories = observation.get("relevant_memories", [])
        
        # 分析任务复杂度
        complexity = self._assess_complexity(task, memories)
        
        # 识别关键约束
        constraints = self._identify_constraints(task)
        
        # 评估可用资源
        resources = self._evaluate_resources(memories)
        
        return {
            **observation,
            "situation_analysis": {
                "complexity": complexity,
                "constraints": constraints,
                "resources": resources
            },
            "complexity_score": complexity["score"]
        }
    
    async def decide(self, orientation: Dict) -> Dict:
        """
        决策阶段：制定推理策略
        
        Args:
            orientation: 情境分析结果
        
        Returns:
            推理策略
        """
        print("[OODA] 决策阶段：制定策略")
        
        complexity = orientation.get("complexity_score", 0)
        
        # 根据复杂度选择推理策略
        if complexity > 0.8:
            strategy = "deep_reasoning"  # 深度推理
        elif complexity > 0.5:
            strategy = "standard_reasoning"  # 标准推理
        else:
            strategy = "quick_reasoning"  # 快速推理
        
        # 制定推理链
        reasoning_chain = self._build_reasoning_chain(strategy, orientation)
        
        return {
            **orientation,
            "strategy": strategy,
            "reasoning_chain": reasoning_chain,
            "estimated_steps": len(reasoning_chain)
        }
    
    async def act(self, decision: Dict, tools: Any = None) -> Dict:
        """
        行动阶段：执行推理
        
        Args:
            decision: 推理策略
            tools: 工具接口
        
        Returns:
            推理结果
        """
        print(f"[OODA] 行动阶段：执行{decision.get('strategy', 'unknown')}策略")
        
        reasoning_chain = decision.get("reasoning_chain", [])
        result = {
            "steps": [],
            "confidence": 0.0,
            "final_answer": None
        }
        
        # 执行推理链
        for i, step in enumerate(reasoning_chain):
            step_result = await self._execute_step(step, tools)
            result["steps"].append(step_result)
            
            # 更新置信度
            result["confidence"] = self._update_confidence(
                result["confidence"], 
                step_result["confidence"]
            )
        
        # 生成最终答案
        result["final_answer"] = self._synthesize_answer(result["steps"])
        
        # 检查是否需要改进
        if result["confidence"] < self.confidence_threshold:
            result["needs_improvement"] = True
            result["improvement_suggestions"] = self._suggest_improvements(result)
        else:
            result["needs_improvement"] = False
        
        return result
    
    async def process(self, task: str, context: Dict = None, tools: Any = None) -> Dict:
        """
        完整 OODA 推理流程
        
        Args:
            task: 任务描述
            context: 上下文信息
            tools: 工具接口
        
        Returns:
            推理结果
        """
        print(f"\n[OODA] 开始处理任务：{task}")
        
        # 1. 观察
        observation = await self.observe(task, tools)
        
        # 2. 判断
        orientation = await self.orient(observation)
        
        # 3. 决策
        decision = await self.decide(orientation)
        
        # 4. 行动
        result = await self.act(decision, tools)
        
        # 记录推理链
        self.reasoning_chain = decision.get("reasoning_chain", [])
        
        print(f"[OODA] 完成，置信度：{result.get('confidence', 0):.2f}")
        
        return result
    
    def _extract_context(self, memories: List) -> Dict:
        """从记忆中提取上下文"""
        context = {
            "similar_tasks": [],
            "lessons_learned": [],
            "best_practices": []
        }
        
        for memory in memories:
            if "similar_task" in memory:
                context["similar_tasks"].append(memory)
            if "lesson" in memory:
                context["lessons_learned"].append(memory)
            if "best_practice" in memory:
                context["best_practices"].append(memory)
        
        return context
    
    def _assess_complexity(self, task: str, memories: List) -> Dict:
        """评估任务复杂度"""
        # 简单启发式：任务长度 + 关键词 + 历史经验
        score = 0.5  # 基础分
        
        # 任务长度
        if len(task) > 100:
            score += 0.2
        elif len(task) > 50:
            score += 0.1
        
        # 复杂度关键词
        complex_keywords = ["分析", "设计", "规划", "优化", "评估", "比较"]
        for keyword in complex_keywords:
            if keyword in task:
                score += 0.05
        
        # 历史经验
        if len(memories) > 3:
            score -= 0.1  # 有丰富经验，降低复杂度
        
        return {
            "score": min(1.0, max(0.0, score)),
            "level": "高" if score > 0.7 else "中" if score > 0.4 else "低",
            "factors": {
                "task_length": len(task),
                "memory_count": len(memories),
                "keyword_matches": sum(1 for k in complex_keywords if k in task)
            }
        }
    
    def _identify_constraints(self, task: str) -> List[str]:
        """识别任务约束"""
        constraints = []
        
        # 时间约束
        if "时间" in task or "截止" in task or "尽快" in task:
            constraints.append("时间限制")
        
        # 资源约束
        if "资源" in task or "预算" in task or "成本" in task:
            constraints.append("资源限制")
        
        # 质量约束
        if "质量" in task or "准确" in task or "精确" in task:
            constraints.append("质量要求")
        
        return constraints if constraints else ["无明显约束"]
    
    def _evaluate_resources(self, memories: List) -> Dict:
        """评估可用资源"""
        return {
            "memory_count": len(memories),
            "similar_tasks": len([m for m in memories if "similar_task" in m]),
            "lessons_available": len([m for m in memories if "lesson" in m])
        }
    
    def _build_reasoning_chain(self, strategy: str, orientation: Dict) -> List[Dict]:
        """构建推理链"""
        chain = []
        
        if strategy == "deep_reasoning":
            chain = [
                {"type": "decompose", "description": "分解任务为子问题"},
                {"type": "retrieve", "description": "检索相关知识"},
                {"type": "analyze", "description": "分析每个子问题"},
                {"type": "synthesize", "description": "综合各子问题答案"},
                {"type": "verify", "description": "验证最终答案"}
            ]
        elif strategy == "standard_reasoning":
            chain = [
                {"type": "retrieve", "description": "检索相关知识"},
                {"type": "analyze", "description": "分析问题"},
                {"type": "solve", "description": "解决问题"},
                {"type": "verify", "description": "验证答案"}
            ]
        else:  # quick_reasoning
            chain = [
                {"type": "retrieve", "description": "检索相关知识"},
                {"type": "solve", "description": "快速解决问题"}
            ]
        
        return chain
    
    async def _execute_step(self, step: Dict, tools: Any = None) -> Dict:
        """执行推理链中的单步"""
        step_type = step.get("type", "unknown")
        
        # 模拟执行（实际实现需要调用相应工具）
        result = {
            "step_type": step_type,
            "description": step.get("description", ""),
            "status": "completed",
            "confidence": 0.8,
            "output": f"完成{step_type}步骤"
        }
        
        # 根据步骤类型执行不同操作
        if step_type == "retrieve" and tools and hasattr(tools, 'memory_search'):
            # 实际检索逻辑
            pass
        elif step_type == "analyze":
            # 分析逻辑
            pass
        elif step_type == "synthesize":
            # 综合逻辑
            pass
        
        return result
    
    def _update_confidence(self, current: float, new: float) -> float:
        """更新置信度（加权平均）"""
        return current * 0.7 + new * 0.3
    
    def _synthesize_answer(self, steps: List[Dict]) -> str:
        """综合各步骤结果生成最终答案"""
        outputs = [step.get("output", "") for step in steps]
        return "\n\n".join(outputs)
    
    def _suggest_improvements(self, result: Dict) -> List[str]:
        """提供改进建议"""
        suggestions = []
        
        if result.get("confidence", 0) < 0.5:
            suggestions.append("置信度较低，建议检索更多相关知识")
        
        if len(result.get("steps", [])) < 2:
            suggestions.append("推理步骤较少，建议增加分析深度")
        
        if not result.get("final_answer"):
            suggestions.append("未生成最终答案，建议重新执行")
        
        return suggestions if suggestions else ["无明显改进建议"]


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        reasoner = OODAReasoner(confidence_threshold=0.7)
        
        task = "分析用户反馈数据，找出主要问题并提出改进建议"
        result = await reasoner.process(task)
        
        print("\n=== 推理结果 ===")
        print(f"置信度：{result.get('confidence', 0):.2f}")
        print(f"需要改进：{result.get('needs_improvement', False)}")
        print(f"最终答案：{result.get('final_answer', 'N/A')}")
        
        if result.get("improvement_suggestions"):
            print("\n改进建议:")
            for suggestion in result["improvement_suggestions"]:
                print(f"  - {suggestion}")
    
    asyncio.run(demo())
