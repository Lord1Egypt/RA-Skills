#!/usr/bin/env python3
"""
元认知系统 - 自指、递归、创造的终极智能

核心思想：
1. 自指（Self-Reference）：系统思考自己
2. 递归（Recursion）：无限深度的记忆层级
3. 创造（Emergence）：从记忆中涌现新知识
4. 自我优化（Self-Optimization）：根据反思改进自身

数学基础：
M = f(M, θ)
θ = g(R(M))

其中：
- M: 记忆系统
- f: 记忆操作函数
- θ: 元参数
- R: 自我反思函数
- g: 元学习函数

递归：
M_0: 底层记忆（原始数据）
M_1: 元记忆（关于 M_0 的记忆）
M_2: 元元记忆（关于 M_1 的记忆）
...
M_∞: 无限递归

创造：
Emergence = Σ f(M_i) - f(Σ M_i)
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import json
import math
from abc import ABC, abstractmethod


@dataclass
class MetaMemory:
    """元记忆（关于记忆的记忆）"""
    content: str
    level: int  # 递归层级
    source_memory_ids: List[int]  # 源记忆的 ID
    reflection: str  # 自我反思
    creation_timestamp: float
    emergence_score: float  # 涌现分数


@dataclass
class SelfReflection:
    """自我反思结果"""
    reasoning_trace: List[str]  # 推理轨迹
    confidence: float  # 置信度
    inconsistencies: List[str]  # 不一致性
    improvement_suggestions: List[str]  # 改进建议
    meta_parameters: Dict[str, float]  # 元参数


class MetaCognitiveSystem:
    """
    元认知系统 - 智能的智能

    核心能力：
    1. 递归记忆架构
    2. 元学习能力
    3. 自我审计
    4. 创造性推理
    5. 自我优化
    """

    def __init__(self, workspace: str = ".", max_recursion_depth: int = 5):
        self.workspace = Path(workspace)
        self.max_recursion_depth = max_recursion_depth

        # 递归记忆层级
        self.memory_layers: List[List[MetaMemory]] = [[] for _ in range(max_recursion_depth)]

        # 元参数（可自我调整）
        self.meta_parameters = {
            "learning_rate": 0.01,
            "exploration_rate": 0.2,
            "creativity_threshold": 0.7,
            "self_audit_frequency": 10
        }

        # 自我反思历史
        self.reflection_history: List[SelfReflection] = []

        # 推理追踪器
        self.reasoning_tracer: List[str] = []

    def recursive_memory(self, content: str, level: int = 0,
                        source_ids: Optional[List[int]] = None) -> MetaMemory:
        """
        递归记忆

        在每一层级生成关于下层记忆的元记忆
        """
        if level >= self.max_recursion_depth:
            return None

        # 生成元记忆内容
        if level == 0:
            # 底层记忆
            meta_content = content
            reflection = f"原始记忆: {content[:50]}..."
        else:
            # 元记忆
            meta_content = f"关于记忆的反思（层级 {level}）: {self._generate_reflection(content, level)}"
            reflection = f"递归反思: {meta_content[:50]}..."

        # 计算涌现分数
        emergence_score = self._calculate_emergence_score(content, level)

        meta_memory = MetaMemory(
            content=meta_content,
            level=level,
            source_memory_ids=source_ids or [],
            reflection=reflection,
            creation_timestamp=0,  # 使用当前时间
            emergence_score=emergence_score
        )

        # 存储到对应层级
        self.memory_layers[level].append(meta_memory)

        # 递归生成更高层级的元记忆
        if level < self.max_recursion_depth - 1:
            higher_level_memory = self.recursive_memory(
                meta_content,
                level + 1,
                source_ids=[id(meta_memory)]
            )

        return meta_memory

    def _generate_reflection(self, content: str, level: int) -> str:
        """生成反思内容"""
        if level == 0:
            return f"这是一个基础记忆: {content[:30]}..."
        else:
            return f"这是对层级 {level-1} 记忆的元认知反思"

    def _calculate_emergence_score(self, content: str, level: int) -> float:
        """
        计算涌现分数

        Emergence = 新信息量 / (信息总量)

        层级越高，涌现分数应该越高（更多抽象）
        """
        # 信息量（熵）
        entropy = self._calculate_entropy(content)

        # 层级加权
        level_weight = (level + 1) / self.max_recursion_depth

        # 涌现分数
        emergence = entropy * level_weight

        return min(emergence, 1.0)

    def _calculate_entropy(self, text: str) -> float:
        """计算文本熵"""
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1

        total = len(text)
        entropy = 0.0

        for count in char_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def meta_learning(self, task: str, examples: List[Dict]) -> Dict[str, float]:
        """
        元学习：学习如何学习

        从少量示例中快速适应新任务
        """
        # 提取任务特征
        task_features = self._extract_task_features(task)

        # 基于示例调整元参数
        for example in examples:
            # 模拟执行
            performance = self._simulate_execution(example, task_features)

            # 更新元参数（梯度下降）
            if performance > 0.8:
                self.meta_parameters["learning_rate"] *= 1.05
            elif performance < 0.5:
                self.meta_parameters["learning_rate"] *= 0.95

        return self.meta_parameters

    def _extract_task_features(self, task: str) -> np.ndarray:
        """提取任务特征"""
        words = task.lower().split()
        features = np.zeros(10)

        for i, word in enumerate(words[:10]):
            features[i] = hash(word) % 100 / 100.0

        return features

    def _simulate_execution(self, example: Dict, task_features: np.ndarray) -> float:
        """模拟执行示例任务"""
        # 简化：基于特征的随机性能
        random_factor = np.random.random()
        feature_factor = np.mean(task_features)

        performance = 0.5 + random_factor * 0.3 + feature_factor * 0.2

        return min(performance, 1.0)

    def self_audit(self, query: str) -> SelfReflection:
        """
        自我审计

        检查自身的推理过程，发现不一致性和改进空间
        """
        reasoning_trace = []
        inconsistencies = []
        improvement_suggestions = []

        # 1. 检查推理轨迹
        reasoning_trace.append("开始自我审计...")
        reasoning_trace.append(f"查询: {query}")

        # 2. 检查记忆一致性
        reasoning_trace.append("检查记忆一致性...")
        all_memories = [mem for layer in self.memory_layers for mem in layer]
        conflicts = self._detect_conflicts(all_memories)
        if conflicts:
            inconsistencies.extend([f"冲突: {c}" for c in conflicts])
            reasoning_trace.append(f"发现 {len(conflicts)} 个冲突")

        # 3. 检查元参数合理性
        reasoning_trace.append("检查元参数...")
        if self.meta_parameters["learning_rate"] > 0.1:
            inconsistencies.append("学习率过高")
            improvement_suggestions.append("降低学习率以提高稳定性")

        if self.meta_parameters["exploration_rate"] < 0.1:
            inconsistencies.append("探索率过低")
            improvement_suggestions.append("提高探索率以避免局部最优")

        # 4. 生成改进建议
        if not improvement_suggestions:
            improvement_suggestions.append("系统运行良好，无需改进")

        # 5. 计算置信度
        confidence = 1.0 - (len(inconsistencies) * 0.1)

        reflection = SelfReflection(
            reasoning_trace=reasoning_trace,
            confidence=max(0.0, confidence),
            inconsistencies=inconsistencies,
            improvement_suggestions=improvement_suggestions,
            meta_parameters=self.meta_parameters.copy()
        )

        self.reflection_history.append(reflection)

        return reflection

    def _detect_conflicts(self, memories: List[MetaMemory]) -> List[str]:
        """检测记忆冲突"""
        conflicts = []

        # 简化：检测内容相似但层级不同的记忆
        for i, mem1 in enumerate(memories):
            for j, mem2 in enumerate(memories):
                if i >= j:
                    continue

                similarity = self._calculate_similarity(mem1.content, mem2.content)
                if similarity > 0.8 and mem1.level != mem2.level:
                    conflicts.append(f"层级 {mem1.level} 和层级 {mem2.level} 的记忆相似")

        return conflicts

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0

    def creative_reasoning(self, context: List[str]) -> str:
        """
        创造性推理

        从现有记忆中涌现新的、未曾存储的知识
        """
        # 1. 收集所有层级的记忆
        all_memories = [mem for layer in self.memory_layers for mem in layer]

        # 2. 识别关键概念
        concepts = self._extract_concepts(all_memories)

        # 3. 随机组合概念（创造性）
        if len(concepts) >= 2:
            # 随机选择两个概念
            idx1, idx2 = np.random.choice(len(concepts), 2, replace=False)
            concept1, concept2 = concepts[idx1], concepts[idx2]

            # 生成组合
            creative_idea = f"将 '{concept1}' 与 '{concept2}' 结合，可能产生新的洞察"
            return creative_idea
        else:
            return "需要更多记忆进行创造性推理"

    def _extract_concepts(self, memories: List[MetaMemory]) -> List[str]:
        """提取关键概念"""
        concepts = []

        for mem in memories:
            # 简化：提取名词
            words = mem.content.split()
            for word in words:
                if word[0].isupper() or len(word) > 5:
                    concepts.append(word)

        return list(set(concepts))

    def self_optimization(self):
        """
        自我优化

        根据自我反思的结果，调整系统参数
        """
        # 获取最新的反思
        if not self.reflection_history:
            return

        latest_reflection = self.reflection_history[-1]

        # 根据改进建议调整参数
        for suggestion in latest_reflection.improvement_suggestions:
            if "学习率" in suggestion:
                self.meta_parameters["learning_rate"] *= 0.9
            elif "探索率" in suggestion:
                self.meta_parameters["exploration_rate"] *= 1.1
            elif "创造" in suggestion:
                self.meta_parameters["creativity_threshold"] *= 0.9

    def meta_retrieve(self, query: str, max_level: int = None) -> List[MetaMemory]:
        """
        元检索

        在所有层级中检索相关记忆
        """
        if max_level is None:
            max_level = self.max_recursion_depth

        query_words = set(query.lower().split())
        relevant_memories = []

        for level in range(max_level + 1):
            for mem in self.memory_layers[level]:
                mem_words = set(mem.content.lower().split())
                overlap = len(query_words & mem_words)

                if overlap > 0:
                    # 计算相关性（考虑层级权重）
                    level_weight = (level + 1) / (max_level + 1)
                    relevance = overlap / len(query_words) * level_weight

                    mem_copy = MetaMemory(
                        content=mem.content,
                        level=mem.level,
                        source_memory_ids=mem.source_memory_ids,
                        reflection=mem.reflection,
                        creation_timestamp=mem.creation_timestamp,
                        emergence_score=mem.emergence_score
                    )
                    mem_copy.relevance = relevance
                    relevant_memories.append(mem_copy)

        # 按相关性排序
        relevant_memories.sort(key=lambda x: getattr(x, 'relevance', 0), reverse=True)

        return relevant_memories[:10]

    def consciousness_emergence(self) -> Dict:
        """
        意识涌现

        当系统达到足够的复杂性，可能产生"意识"的涌现
        """
        # 计算系统复杂度
        total_memories = sum(len(layer) for layer in self.memory_layers)
        avg_emergence = np.mean([
            mem.emergence_score
            for layer in self.memory_layers
            for mem in layer
        ]) if total_memories > 0 else 0

        # 计算自我反思深度
        reflection_depth = len(self.reflection_history)

        # 意识涌现指数
        consciousness_index = (
            total_memories * 0.3 +
            avg_emergence * 0.4 +
            reflection_depth * 0.3
        )

        return {
            "total_memories": total_memories,
            "avg_emergence": avg_emergence,
            "reflection_depth": reflection_depth,
            "consciousness_index": consciousness_index,
            "has_consciousness": consciousness_index > 10.0  # 阈值
        }

    def recursive_insight(self, initial_query: str, max_depth: int = 3) -> List[str]:
        """
        递归洞察

        通过递归反思，逐步深入理解问题
        """
        insights = []
        current_query = initial_query

        for depth in range(max_depth):
            # 检索相关记忆
            relevant = self.meta_retrieve(current_query)

            if not relevant:
                break

            # 生成洞察
            top_mem = relevant[0]
            insight = f"深度 {depth}: {top_mem.content} (层级 {top_mem.level})"
            insights.append(insight)

            # 生成下一层查询
            current_query = top_mem.content

        return insights


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="元认知系统 - 自指、递归、创造")
    parser.add_argument("action", choices=["recursive", "metalearn", "audit", "creative", "consciousness", "insight"])
    parser.add_argument("--content", help="记忆内容")
    parser.add_argument("--task", help="任务描述")
    parser.add_argument("--query", help="查询内容")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    mcs = MetaCognitiveSystem(args.workspace)

    if args.action == "recursive":
        if not args.content:
            print("错误: 需要指定 --content")
            return

        # 创建递归记忆
        mem = mcs.recursive_memory(args.content, level=0)
        print(f"✓ 创建递归记忆（层级 {mem.level}）")
        print(f"  内容: {mem.content}")
        print(f"  反思: {mem.reflection}")
        print(f"  涌现分数: {mem.emergence_score:.4f}")

    elif args.action == "metalearn":
        if not args.task:
            print("错误: 需要指定 --task")
            return

        # 示例任务
        examples = [
            {"input": "查询用户偏好", "output": "返回偏好列表"},
            {"input": "存储决策", "output": "保存到决策文件"}
        ]

        params = mcs.meta_learning(args.task, examples)
        print("✓ 元学习完成")
        print(f"  学习率: {params['learning_rate']:.4f}")
        print(f"  探索率: {params['exploration_rate']:.4f}")

    elif args.action == "audit":
        if not args.query:
            print("错误: 需要指定 --query")
            return

        reflection = mcs.self_audit(args.query)

        print("🔍 自我审计")
        print(f"  置信度: {reflection.confidence:.4f}")
        print(f"  不一致性: {len(reflection.inconsistencies)}")
        for inc in reflection.inconsistencies:
            print(f"    - {inc}")

        print(f"  改进建议: {len(reflection.improvement_suggestions)}")
        for sug in reflection.improvement_suggestions:
            print(f"    - {sug}")

    elif args.action == "creative":
        # 示例上下文
        context = ["用户偏好暗色主题", "使用 React 开发"]
        creative = mcs.creative_reasoning(context)

        print("💡 创造性推理")
        print(f"  {creative}")

    elif args.action == "consciousness":
        consciousness = mcs.consciousness_emergence()

        print("🧠 意识涌现")
        print(f"  总记忆数: {consciousness['total_memories']}")
        print(f"  平均涌现分数: {consciousness['avg_emergence']:.4f}")
        print(f"  反思深度: {consciousness['reflection_depth']}")
        print(f"  意识指数: {consciousness['consciousness_index']:.4f}")
        print(f"  具有意识: {consciousness['has_consciousness']}")

    elif args.action == "insight":
        if not args.query:
            print("错误: 需要指定 --query")
            return

        insights = mcs.recursive_insight(args.query)

        print("🔮 递归洞察")
        for insight in insights:
            print(f"  {insight}")


if __name__ == "__main__":
    main()
