"""
Cognitive Controller - 认知控制器

负责根据任务特征自动选择和切换认知模式。
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from .chain_reasoner import OODAReasoner
from .pattern_matcher import PatternMatcher
from .self_assessor import SelfAssessor
from .usage_monitor import UsageMonitor


class CognitiveController:
    """认知控制器 - 模式自动切换"""
    
    # 认知模式枚举
    MODE_OOA = "OOA"      # 经验模式
    MODE_OODA = "OODA"    # 推理模式
    MODE_OOCA = "OOCA"    # 创造模式
    MODE_OOHA = "OOHA"    # 发现模式
    
    def __init__(self, confidence_threshold: float = 0.7, enable_monitoring: bool = True):
        self.confidence_threshold = confidence_threshold
        self.reasoner = OODAReasoner(confidence_threshold)
        self.matcher = PatternMatcher(similarity_threshold=0.7)
        self.assessor = SelfAssessor()
        self.mode_history = []
        self.monitor = UsageMonitor() if enable_monitoring else None
    
    async def select_mode(self, task: str, context: Dict = None, tools: Any = None) -> str:
        """
        根据任务特征选择认知模式
        
        Args:
            task: 任务描述
            context: 上下文信息
            tools: 工具接口
        
        Returns:
            选择的认知模式
        """
        print(f"[Controller] 开始选择模式：{task}")
        
        # 1. 分析任务特征
        features = self._analyze_task_features(task)
        
        # 2. 评估模式适用性
        mode_scores = self._evaluate_modes(task, features, context, tools)
        
        # 3. 选择最佳模式
        best_mode = max(mode_scores, key=mode_scores.get)
        best_score = mode_scores[best_mode]
        
        # 4. 记录选择历史
        self.mode_history.append({
            "task": task,
            "features": features,
            "mode_scores": mode_scores,
            "selected_mode": best_mode,
            "score": best_score,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"[Controller] 选择模式：{best_mode} (置信度：{best_score:.2f})")
        
        return best_mode
    
    async def execute(self, mode: str, task: str, context: Dict = None, tools: Any = None) -> Dict:
        """
        执行选定的认知模式
        
        Args:
            mode: 认知模式
            task: 任务描述
            context: 上下文信息
            tools: 工具接口
        
        Returns:
            执行结果
        """
        print(f"[Controller] 执行模式：{mode}")
        
        if mode == self.MODE_OOA:
            result = await self._execute_ooa(task, context, tools)
        elif mode == self.MODE_OODA:
            result = await self._execute_ooda(task, context, tools)
        elif mode == self.MODE_OOCA:
            result = await self._execute_ooca(task, context, tools)
        elif mode == self.MODE_OOHA:
            result = await self._execute_ooha(task, context, tools)
        else:
            result = {"error": f"未知模式：{mode}"}
        
        # 添加模式信息
        result["mode"] = mode
        
        return result
    
    async def process(self, task: str, context: Dict = None, tools: Any = None) -> Dict:
        """
        完整认知处理流程（自动选择模式 + 执行）
        
        Args:
            task: 任务描述
            context: 上下文信息
            tools: 工具接口
        
        Returns:
            处理结果
        """
        print(f"\n[Controller] 开始处理任务：{task}")
        
        # 1. 选择模式
        mode = await self.select_mode(task, context, tools)
        
        # 2. 执行模式
        result = await self.execute(mode, task, context, tools)
        
        # 3. 评估结果
        assessment = await self.assessor.evaluate(result)
        result["assessment"] = assessment
        
        # 4. 如果需要改进，尝试切换模式
        if assessment.get("needs_improvement", False) and result.get("mode_switched", False) == False:
            print(f"[Controller] 需要改进，尝试切换模式")
            improved_result = await self._try_mode_switch(task, context, tools, result, mode)
            result = improved_result
        
        # 5. 记录使用日志（监控）
        if self.monitor:
            self.monitor.log_usage(task, result.get("mode", mode), result, context)
        
        print(f"[Controller] 完成，模式：{result.get('mode', 'N/A')}, 置信度：{assessment.get('overall_score', 0):.2f}")
        
        return result
    
    def _analyze_task_features(self, task: str) -> Dict:
        """分析任务特征"""
        features = {
            "length": len(task),
            "complexity_keywords": 0,
            "creativity_keywords": 0,
            "exploration_keywords": 0,
            "has_constraints": False
        }
        
        # 复杂度关键词
        complex_keywords = ["分析", "设计", "规划", "优化", "评估", "比较", "诊断"]
        for keyword in complex_keywords:
            if keyword in task:
                features["complexity_keywords"] += 1
        
        # 创造力关键词
        creativity_keywords = ["创意", "创新", "设计", "生成", "构思", "想象"]
        for keyword in creativity_keywords:
            if keyword in task:
                features["creativity_keywords"] += 1
        
        # 探索关键词
        exploration_keywords = ["研究", "探索", "发现", "调查", "未知", "为什么"]
        for keyword in exploration_keywords:
            if keyword in task:
                features["exploration_keywords"] += 1
        
        # 约束检查
        constraint_keywords = ["时间", "截止", "预算", "资源", "限制"]
        for keyword in constraint_keywords:
            if keyword in task:
                features["has_constraints"] = True
                break
        
        return features
    
    def _evaluate_modes(self, task: str, features: Dict, context: Dict = None, tools: Any = None) -> Dict[str, float]:
        """评估各模式适用性"""
        scores = {
            self.MODE_OOA: 0.5,    # 基础分
            self.MODE_OODA: 0.5,   # 基础分
            self.MODE_OOCA: 0.5,   # 基础分
            self.MODE_OOHA: 0.5    # 基础分
        }
        
        # OOA 经验模式评分
        if features["complexity_keywords"] <= 1:
            scores[self.MODE_OOA] += 0.3  # 简单任务适合经验模式
        if context and len(context.get("similar_tasks", [])) > 3:
            scores[self.MODE_OOA] += 0.2  # 有丰富经验
        
        # OODA 推理模式评分
        if features["complexity_keywords"] >= 2:
            scores[self.MODE_OODA] += 0.3  # 复杂任务适合推理模式
        if features["has_constraints"]:
            scores[self.MODE_OODA] += 0.2  # 有约束需要推理
        
        # OOCA 创造模式评分
        if features["creativity_keywords"] >= 2:
            scores[self.MODE_OOCA] += 0.4  # 需要创造力
        
        # OOHA 发现模式评分
        if features["exploration_keywords"] >= 2:
            scores[self.MODE_OOHA] += 0.4  # 需要探索
        
        # 归一化
        total = sum(scores.values())
        if total > 0:
            for mode in scores:
                scores[mode] = scores[mode] / total * 1.0
        
        return scores
    
    async def _execute_ooa(self, task: str, context: Dict, tools: Any) -> Dict:
        """执行 OOA 经验模式"""
        result = await self.matcher.match(task, tools)
        
        if result.get("best_match"):
            applied = self.matcher.apply_pattern(result["best_match"]["pattern"], task)
            return {
                "mode": self.MODE_OOA,
                "answer": applied["adapted_solution"],
                "confidence": result.get("confidence", 0),
                "similar_tasks": result.get("similar_tasks", []),
                "reasoning_chain": [
                    {"step": "检索相似任务", "result": f"{len(result.get('similar_tasks', []))}个"},
                    {"step": "提取模式", "result": f"{len(result.get('patterns', []))}个"},
                    {"step": "匹配最佳案例", "result": applied["original_task"]}
                ]
            }
        else:
            return {
                "mode": self.MODE_OOA,
                "answer": "无历史经验可参考",
                "confidence": 0.0,
                "fallback_recommendation": "建议切换到 OODA 推理模式"
            }
    
    async def _execute_ooda(self, task: str, context: Dict, tools: Any) -> Dict:
        """执行 OODA 推理模式"""
        result = await self.reasoner.process(task, context, tools)
        
        return {
            "mode": self.MODE_OODA,
            "answer": result.get("final_answer", ""),
            "confidence": result.get("confidence", 0),
            "reasoning_chain": result.get("steps", []),
            "needs_improvement": result.get("needs_improvement", False)
        }
    
    async def _execute_ooca(self, task: str, context: Dict, tools: Any) -> Dict:
        """执行 OOCA 创造模式（简化实现）"""
        # TODO: 实现完整的 OOCA 模式
        return {
            "mode": self.MODE_OOCA,
            "answer": "OOCA 创造模式正在开发中",
            "confidence": 0.3,
            "fallback_recommendation": "建议切换到 OODA 推理模式",
            "status": "not_implemented"
        }
    
    async def _execute_ooha(self, task: str, context: Dict, tools: Any) -> Dict:
        """执行 OOHA 发现模式（简化实现）"""
        # TODO: 实现完整的 OOHA 模式
        return {
            "mode": self.MODE_OOHA,
            "answer": "OOHA 发现模式正在开发中",
            "confidence": 0.3,
            "fallback_recommendation": "建议切换到 OODA 推理模式",
            "status": "not_implemented"
        }
    
    async def _try_mode_switch(self, task: str, context: Dict, tools: Any, 
                                current_result: Dict, current_mode: str) -> Dict:
        """尝试切换模式改进结果"""
        print(f"[Controller] 当前模式：{current_mode}，尝试切换")
        
        # 重新选择模式（排除当前模式）
        features = self._analyze_task_features(task)
        mode_scores = self._evaluate_modes(task, features, context, tools)
        
        # 排除当前模式
        if current_mode in mode_scores:
            del mode_scores[current_mode]
        
        # 选择次优模式
        if not mode_scores:
            return current_result
        
        new_mode = max(mode_scores, key=mode_scores.get)
        
        # 执行新模式的
        new_result = await self.execute(new_mode, task, context, tools)
        new_result["mode_switched"] = True
        new_result["previous_mode"] = current_mode
        new_result["switch_reason"] = "前一模式置信度不足"
        
        print(f"[Controller] 切换到模式：{new_mode}")
        
        return new_result
    
    def get_mode_history(self, limit: int = 10) -> List[Dict]:
        """获取模式选择历史"""
        return self.mode_history[-limit:]
    
    def get_mode_statistics(self) -> Dict:
        """获取模式使用统计"""
        if not self.mode_history:
            return {"message": "无历史数据"}
        
        mode_counts = {}
        for record in self.mode_history:
            mode = record.get("selected_mode", "unknown")
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        return {
            "total_tasks": len(self.mode_history),
            "mode_distribution": mode_counts,
            "most_used_mode": max(mode_counts, key=mode_counts.get) if mode_counts else None
        }


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        controller = CognitiveController(confidence_threshold=0.7)
        
        # 测试任务 1：简单任务（应该选择 OOA）
        task1 = "用户反馈加载慢"
        result1 = await controller.process(task1)
        print(f"\n任务 1 结果：{result1['mode']} - 置信度：{result1.get('assessment', {}).get('overall_score', 0):.2f}")
        
        # 测试任务 2：复杂任务（应该选择 OODA）
        task2 = "分析用户反馈数据，找出主要问题并提出改进建议"
        result2 = await controller.process(task2)
        print(f"任务 2 结果：{result2['mode']} - 置信度：{result2.get('assessment', {}).get('overall_score', 0):.2f}")
        
        # 测试任务 3：创意任务（应该选择 OOCA）
        task3 = "设计一个创新的营销活动方案"
        result3 = await controller.process(task3)
        print(f"任务 3 结果：{result3['mode']} - 置信度：{result3.get('assessment', {}).get('overall_score', 0):.2f}")
        
        # 查看统计
        stats = controller.get_mode_statistics()
        print(f"\n模式统计：{stats}")
    
    asyncio.run(demo())
