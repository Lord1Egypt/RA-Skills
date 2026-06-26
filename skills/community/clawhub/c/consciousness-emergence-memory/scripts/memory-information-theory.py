#!/usr/bin/env python3
"""
信息论核心 - 第一性原理设计的记忆系统

基于信息论的极致记忆管理：
- Kolmogorov 复杂度计算记忆价值
- 最小描述长度（MDL）进行记忆压缩
- 互信息最大化进行记忆选择
- 熵减最优路径
"""
import math
import re
import json
import zlib
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import numpy as np


@dataclass
class InformationValue:
    """信息价值度量"""
    kolmogorov_complexity: float  # Kolmogorov 复杂度
    description_length: float      # 最小描述长度
    mutual_information: float      # 互信息
    entropy_reduction: float       # 熵减量
    computational_benefit: float   # 计算收益
    total_value: float            # 总价值（熵加权）


class InformationTheoryCore:
    """
    信息论核心 - 第一性原理的记忆价值计算

    核心思想：
    记忆的价值 = 熵减 - 存储成本

    Value(I) = H_before - H_after - Cost_storage

    其中：
    - H: 熵（不确定性）
    - Cost_storage: 存储成本（基于 MDL）
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.language_model = None  # 可选：加载语言模型估计复杂度

    def calculate_kolmogorov_complexity(self, text: str) -> float:
        """
        计算 Kolmogorov 复杂度（近似）

        K(x) = min {|p|: U(p) = x}

        由于 Kolmogorov 复杂度不可计算，使用近似：
        - 压缩长度
        - 算法信息内容
        """
        # 方法 1: 压缩长度（近似）
        compressed = zlib.compress(text.encode())
        k_complexity = len(compressed)

        # 方法 2: 算法复杂度（基于模式）
        pattern_complexity = self._estimate_pattern_complexity(text)

        # 综合估计
        estimated_k = k_complexity * 0.7 + pattern_complexity * 0.3

        return estimated_k

    def estimate_pattern_complexity(self, text: str) -> float:
        """
        估计文本的模式复杂度

        基于以下特征：
        - 重复模式（降低复杂度）
        - 结构化程度（降低复杂度）
        - 信息密度（提高复杂度）
        """
        words = text.split()
        unique_words = set(words)

        # 重复度
        repetition_rate = 1 - len(unique_words) / len(words) if words else 0

        # 结构化程度（基于标点和格式）
        structure_score = self._detect_structure(text)

        # 信息密度（每词的信息量）
        avg_word_length = np.mean([len(w) for w in words]) if words else 0

        # 模式复杂度：重复越多、结构越好，复杂度越低
        pattern_complexity = len(text) * (1 - repetition_rate * 0.3) * (1 - structure_score * 0.2)

        return pattern_complexity

    def _detect_structure(self, text: str) -> float:
        """检测文本的结构化程度"""
        score = 0.0

        # 检测列表
        if re.search(r'^[\-\*\d+\.]', text, re.MULTILINE):
            score += 0.3

        # 检测标题
        if re.search(r'^#+\s', text, re.MULTILINE):
            score += 0.3

        # 检测代码块
        if '```' in text:
            score += 0.2

        # 检测表格
        if '|' in text:
            score += 0.2

        return min(score, 1.0)

    def calculate_mutual_information(self, text: str, context: List[str]) -> float:
        """
        计算互信息

        I(X; Y) = H(X) - H(X|Y)

        衡量文本与上下文之间的信息共享量
        """
        if not context:
            return 0.0

        # 计算文本的熵
        entropy_text = self._calculate_entropy(text)

        # 计算条件熵（给定上下文后的不确定性）
        entropy_conditional = self._calculate_conditional_entropy(text, context)

        # 互信息
        mutual_info = entropy_text - entropy_conditional

        return max(0.0, mutual_info)

    def _calculate_entropy(self, text: str) -> float:
        """
        计算香农熵

        H(X) = -Σ p(x) log p(x)
        """
        # 字符级别熵
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

    def _calculate_conditional_entropy(self, text: str, context: List[str]) -> float:
        """
        计算条件熵（近似）

        H(X|Y) = H(X, Y) - H(Y)
        """
        # 简化：上下文中的常见词降低条件熵
        context_words = set()
        for ctx in context:
            context_words.update(ctx.split())

        text_words = text.split()
        known_words = sum(1 for w in text_words if w in context_words)

        # 已知单词比例越高，条件熵越低
        known_ratio = known_words / len(text_words) if text_words else 0
        conditional_entropy = self._calculate_entropy(text) * (1 - known_ratio * 0.5)

        return conditional_entropy

    def calculate_minimum_description_length(self, text: str) -> float:
        """
        计算最小描述长度（MDL）

        MDL = L(M) + L(D | M)

        其中：
        - L(M): 模型长度（模式的描述长度）
        - L(D | M): 数据在模型下的描述长度

        最优记忆是 MDL 最小的记忆
        """
        # 估计模型长度（模式的简洁性）
        model_length = self._estimate_model_length(text)

        # 估计数据在模型下的描述长度
        data_length = self._estimate_data_length(text)

        mdl = model_length + data_length

        return mdl

    def _estimate_model_length(self, text: str) -> float:
        """
        估计模型长度

        模型越简单，模型长度越短
        """
        # 检测模式
        patterns = self._extract_patterns(text)

        # 模型长度 = 模式数量的对数
        model_length = math.log2(len(patterns) + 1)

        return model_length

    def _extract_patterns(self, text: str) -> List[str]:
        """提取文本中的模式"""
        patterns = []

        # 提取重复的 n-grams
        words = text.split()
        n = 3  # 3-grams

        for i in range(len(words) - n + 1):
            ngram = " ".join(words[i:i+n])
            if words.count(ngram.split()[0]) > 1:  # 重复出现
                patterns.append(ngram)

        return list(set(patterns))

    def _estimate_data_length(self, text: str) -> float:
        """
        估计数据长度

        数据在模型下的编码长度
        """
        # 简化：使用压缩长度作为数据长度的估计
        compressed = zlib.compress(text.encode())
        return len(compressed)

    def calculate_entropy_reduction(self, text: str, current_entropy: float) -> float:
        """
        计算熵减量

        Reduction = H_before - H_after

        记忆存储后，系统的总熵应该减少
        """
        # 存储记忆后，不确定性降低
        new_entropy = current_entropy * 0.9  # 假设记忆减少 10% 的不确定性

        entropy_reduction = current_entropy - new_entropy

        return entropy_reduction

    def calculate_computational_benefit(self, text: str, access_frequency: float = 1.0) -> float:
        """
        计算计算收益

        Benefit = Cost_saved × Frequency

        记忆的价值在于避免重复计算
        """
        # 估计不记忆时需要重复计算的成本
        # 简化：基于文本长度和复杂度
        recompute_cost = len(text) * self.estimate_pattern_complexity(text) / 1000

        # 计算收益 = 节省的成本 × 访问频率
        computational_benefit = recompute_cost * access_frequency

        return computational_benefit

    def evaluate_memory_value(self, text: str, context: Optional[List[str]] = None,
                             access_frequency: float = 1.0) -> InformationValue:
        """
        综合评估记忆价值

        Value = (熵减量 + 互信息 + 计算收益) - 存储成本

        使用熵加权平衡各项指标
        """
        if context is None:
            context = []

        # 1. Kolmogorov 复杂度
        k_complexity = self.calculate_kolmogorov_complexity(text)

        # 2. 最小描述长度（存储成本）
        mdl = self.calculate_minimum_description_length(text)

        # 3. 互信息
        mutual_info = self.calculate_mutual_information(text, context)

        # 4. 熵减量
        current_entropy = self._calculate_entropy(" ".join(context + [text]))
        entropy_reduction = self.calculate_entropy_reduction(text, current_entropy)

        # 5. 计算收益
        computational_benefit = self.calculate_computational_benefit(text, access_frequency)

        # 6. 总价值（熵加权）
        # Value = (熵减 × 0.4 + 互信息 × 0.3 + 计算收益 × 0.3) / 存储成本
        value_numerator = (entropy_reduction * 0.4 +
                          mutual_info * 0.3 +
                          computational_benefit * 0.3)

        storage_cost = mdl / 1000  # 归一化
        total_value = value_numerator / (storage_cost + 0.1)  # 避免除零

        return InformationValue(
            kolmogorov_complexity=k_complexity,
            description_length=mdl,
            mutual_information=mutual_info,
            entropy_reduction=entropy_reduction,
            computational_benefit=computational_benefit,
            total_value=total_value
        )

    def optimal_memory_selection(self, candidates: List[Dict], budget: int) -> List[Dict]:
        """
        最优记忆选择（背包问题）

        在存储预算约束下，选择价值最大的记忆组合

        Maximize: Σ Value_i
        Subject to: Σ MDL_i ≤ Budget
        """
        # 计算每个候选的价值
        for candidate in candidates:
            candidate["info_value"] = self.evaluate_memory_value(
                candidate["content"],
                candidate.get("context", []),
                candidate.get("access_frequency", 1.0)
            )

        # 动态规划求解背包问题
        # 简化实现：贪心算法（按价值密度排序）
        candidates_with_density = []
        for candidate in candidates:
            value = candidate["info_value"].total_value
            cost = candidate["info_value"].description_length
            density = value / cost if cost > 0 else 0
            candidates_with_density.append({
                "candidate": candidate,
                "density": density,
                "value": value,
                "cost": cost
            })

        # 按价值密度降序排序
        candidates_with_density.sort(key=lambda x: x["density"], reverse=True)

        # 贪心选择
        selected = []
        total_cost = 0

        for item in candidates_with_density:
            if total_cost + item["cost"] <= budget:
                selected.append(item["candidate"])
                total_cost += item["cost"]

        return selected

    def compress_memories(self, memories: List[Dict]) -> List[Dict]:
        """
        基于信息论的最优压缩

        识别冗余和相关性，进行智能压缩
        """
        if not memories:
            return []

        # 1. 计算记忆之间的互信息
        mutual_info_matrix = np.zeros((len(memories), len(memories)))

        for i, mem1 in enumerate(memories):
            for j, mem2 in enumerate(memories):
                if i != j:
                    mi = self.calculate_mutual_information(
                        mem1["content"],
                        [mem2["content"]]
                    )
                    mutual_info_matrix[i][j] = mi

        # 2. 识别高互信息的记忆组（可以合并）
        groups = []
        used = set()

        for i in range(len(memories)):
            if i in used:
                continue

            group = [i]
            used.add(i)

            for j in range(i + 1, len(memories)):
                if j not in used and mutual_info_matrix[i][j] > 0.5:  # 阈值
                    group.append(j)
                    used.add(j)

            groups.append(group)

        # 3. 压缩每个组
        compressed = []
        for group in groups:
            if len(group) == 1:
                compressed.append(memories[group[0]])
            else:
                # 合并高相关的记忆
                merged_content = self._merge_memories([memories[i] for i in group])
                compressed.append({
                    "content": merged_content,
                    "type": "compressed",
                    "source_count": len(group)
                })

        return compressed

    def _merge_memories(self, memories: List[Dict]) -> str:
        """合并相关的记忆"""
        # 提取共同主题
        all_content = " ".join([m["content"] for m in memories])

        # 使用信息熵最高的句子作为摘要
        sentences = all_content.split(". ")
        if not sentences:
            return all_content

        # 计算每个句子的熵
        sentence_entropies = []
        for sentence in sentences:
            entropy = self._calculate_entropy(sentence)
            sentence_entropies.append((sentence, entropy))

        # 选择熵最高的句子（信息量最大）
        sentence_entropies.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_entropies[:3]]

        merged = ". ".join(top_sentences)
        return merged


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="信息论核心 - 第一性原理记忆系统")
    parser.add_argument("action", choices=["evaluate", "select", "compress"])
    parser.add_argument("--content", help="记忆内容")
    parser.add_argument("--context", nargs="+", help="上下文")
    parser.add_argument("--budget", type=int, default=10000, help="存储预算")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    core = InformationTheoryCore(args.workspace)

    if args.action == "evaluate":
        if not args.content:
            print("错误: 需要指定 --content")
            return

        info_value = core.evaluate_memory_value(
            args.content,
            args.context or []
        )

        print("📊 信息价值评估")
        print(f"Kolmogorov 复杂度: {info_value.kolmogorov_complexity:.2f}")
        print(f"最小描述长度: {info_value.description_length:.2f}")
        print(f"互信息: {info_value.mutual_information:.4f}")
        print(f"熵减量: {info_value.entropy_reduction:.4f}")
        print(f"计算收益: {info_value.computational_benefit:.2f}")
        print(f"总价值: {info_value.total_value:.4f}")

    elif args.action == "select":
        # 示例：从多个候选中选择最优记忆
        candidates = [
            {"content": "用户偏好暗色主题", "context": [], "access_frequency": 5},
            {"content": "使用 React 作为前端框架", "context": [], "access_frequency": 3},
            {"content": "项目需要在周五前完成", "context": [], "access_frequency": 1},
        ]

        selected = core.optimal_memory_selection(candidates, args.budget)

        print(f"✓ 选择了 {len(selected)} 个记忆（预算: {args.budget}）")
        for mem in selected:
            print(f"  - {mem['content']} (价值: {mem['info_value'].total_value:.4f})")

    elif args.action == "compress":
        # 示例：压缩记忆
        memories = [
            {"content": "用户喜欢暗色主题"},
            {"content": "用户偏好黑色背景"},
            {"content": "用户使用深色模式"},
            {"content": "使用 React 开发前端"},
            {"content": "选择 React 作为框架"},
        ]

        compressed = core.compress_memories(memories)

        print(f"✓ 压缩后: {len(memories)} → {len(compressed)}")
        for mem in compressed:
            print(f"  - {mem['content']}")


if __name__ == "__main__":
    main()
