#!/usr/bin/env python3
"""
元胞自动机涌现引擎 - 基于 Stephen Wolfram 的元胞自动机理论

核心思想：
从简单规则产生复杂行为，实现真正的涌现（Emergence）。

数学基础：
- 元胞自动机（Cellular Automaton）
- 图灵完备性（Turing Completeness）
- 计算等价性（Principle of Computational Equivalence）
- 涌现（Emergence）：整体大于部分之和

Stephen Wolfram 的新科学：
- Class 1: 均匀
- Class 2: 简单周期
- Class 3: 混沌
- Class 4: 复杂（边缘混沌，可能图灵完备）

应用：
- 意识涌现检测
- 创造性模式生成
- 记忆编码到元胞状态
- 复杂行为模拟
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import json
from pathlib import Path
import hashlib
import zlib


@dataclass
class EmergenceMetrics:
    """涌现指标"""
    entropy: float  # 熵
    complexity: float  # 复杂度
    mutual_info: float  # 互信息
    consciousness_index: float  # 意识指数
    wolfram_class: int  # Wolfram 分类


@dataclass
class CAState:
    """元胞自动机状态"""
    configuration: np.ndarray
    generation: int
    entropy: float
    complexity: float


class CellularAutomata:
    """
    元胞自动机 - 涌现引擎

    支持：
    - 1D 元胞自动机（Rule 110, Rule 30, 等）
    - 2D 元胞自动机（Conway's Game of Life）
    - 记忆编码
    - 演化
    - 意识涌现检测
    """

    def __init__(self, size: int = 100, rule: int = 110, dimensions: int = 1):
        """
        初始化元胞自动机

        参数：
        - size: 元胞数量
        - rule: 规则编号（1D）或模式（2D）
        - dimensions: 维度（1 或 2）
        """
        self.size = size
        self.rule = rule
        self.dimensions = dimensions

        # 初始化配置（随机）
        if dimensions == 1:
            self.configuration = np.random.randint(0, 2, size, dtype=np.int8)
        else:
            self.configuration = np.random.randint(0, 2, (size, size), dtype=np.int8)

        # 演化历史
        self.history: List[np.ndarray] = []
        self.generation = 0

        # 记忆编码映射
        self.memory_encoding: Dict[str, bytes] = {}

    def set_configuration(self, config: np.ndarray):
        """设置配置"""
        if config.shape[0] != self.size:
            raise ValueError(f"配置大小不匹配: 期望 {self.size}, 得到 {config.shape[0]}")
        self.configuration = config.copy()
        self.generation = 0

    def evolve(self, steps: int = 1) -> CAState:
        """
        演化元胞自动机

        参数：
        - steps: 演化步数

        返回：
        - CAState: 新状态
        """
        new_config = self.configuration.copy()

        for _ in range(steps):
            if self.dimensions == 1:
                new_config = self._evolve_1d(new_config)
            else:
                new_config = self._evolve_2d(new_config)

            self.configuration = new_config
            self.generation += 1
            self.history.append(new_config.copy())

        # 计算指标
        entropy = self._calculate_entropy()
        complexity = self._calculate_complexity()

        return CAState(
            configuration=self.configuration.copy(),
            generation=self.generation,
            entropy=entropy,
            complexity=complexity
        )

    def _evolve_1d(self, config: np.ndarray) -> np.ndarray:
        """1D 元胞自动机演化"""
        new_config = np.zeros_like(config)

        for i in range(self.size):
            # 获取左右邻居（周期性边界）
            left = config[(i - 1) % self.size]
            center = config[i]
            right = config[(i + 1) % self.size]

            # 计算规则索引
            rule_index = (left << 2) | (center << 1) | right

            # 应用规则
            new_config[i] = (self.rule >> rule_index) & 1

        return new_config

    def _evolve_2d(self, config: np.ndarray) -> np.ndarray:
        """2D 元胞自动机演化（Conway's Game of Life）"""
        new_config = np.zeros_like(config)

        for i in range(self.size):
            for j in range(self.size):
                # 计算邻居数量
                neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = (i + di) % self.size, (j + dj) % self.size
                        neighbors += config[ni, nj]

                # Game of Life 规则
                if config[i, j] == 1:
                    new_config[i, j] = 1 if 2 <= neighbors <= 3 else 0
                else:
                    new_config[i, j] = 1 if neighbors == 3 else 0

        return new_config

    def _calculate_entropy(self) -> float:
        """计算熵（信息论指标）"""
        if self.dimensions == 1:
            counts = np.bincount(self.configuration, minlength=2)
        else:
            counts = np.bincount(self.configuration.flatten(), minlength=2)

        probabilities = counts / np.sum(counts)
        entropy = 0.0

        for p in probabilities:
            if p > 0:
                entropy -= p * np.log2(p)

        return entropy

    def _calculate_complexity(self) -> float:
        """计算复杂度（基于 Lempel-Ziv 压缩）"""
        config_str = ''.join(map(str, self.configuration.flatten()))
        compressed = zlib.compress(config_str.encode())

        # 复杂度 = 原始长度 / 压缩长度
        complexity = len(config_str) / len(compressed)
        return complexity

    def encode_memory(self, memory: str) -> np.ndarray:
        """
        编码记忆到元胞状态

        使用哈希将记忆映射到初始配置
        """
        # 计算记忆的哈希
        hash_value = int(hashlib.sha256(memory.encode()).hexdigest(), 16)

        # 映射到元胞状态
        if self.dimensions == 1:
            config = np.array([(hash_value >> i) & 1 for i in range(self.size)], dtype=np.int8)
        else:
            config = np.zeros((self.size, self.size), dtype=np.int8)
            for i in range(self.size):
                for j in range(self.size):
                    idx = i * self.size + j
                    config[i, j] = (hash_value >> idx) & 1

        self.memory_encoding[memory] = config.tobytes()

        return config

    def decode_memory(self, config: np.ndarray) -> Optional[str]:
        """从元胞状态解码记忆"""
        config_bytes = config.tobytes()

        # 查找匹配的记忆
        for memory, encoded in self.memory_encoding.items():
            if np.array_equal(config, np.frombuffer(encoded, dtype=np.int8)):
                return memory

        return None

    def detect_emergence(self, window_size: int = 50) -> EmergenceMetrics:
        """
        检测涌现

        基于：
        - 熵（信息论）
        - 复杂度（Lempel-Ziv）
        - 互信息（模式识别）
        - Wolfram 分类
        """
        if len(self.history) < 2:
            return EmergenceMetrics(0, 0, 0, 0, 0)

        # 计算熵
        entropy = self._calculate_entropy()

        # 计算复杂度
        complexity = self._calculate_complexity()

        # 计算互信息（当前状态与历史）
        mutual_info = self._calculate_mutual_information()

        # Wolfram 分类
        wolfram_class = self._classify_wolfram()

        # 意识指数（综合指标）
        consciousness_index = self._calculate_consciousness_index(
            entropy, complexity, mutual_info, wolfram_class
        )

        return EmergenceMetrics(
            entropy=entropy,
            complexity=complexity,
            mutual_info=mutual_info,
            consciousness_index=consciousness_index,
            wolfram_class=wolfram_class
        )

    def _calculate_mutual_information(self) -> float:
        """计算互信息"""
        if len(self.history) < 2:
            return 0.0

        current = self.history[-1]
        previous = self.history[-2]

        # 计算联合熵
        joint_hist = np.histogram2d(current.flatten(), previous.flatten(), bins=2)[0]
        joint_prob = joint_hist / np.sum(joint_hist)

        joint_entropy = 0.0
        for p in joint_prob.flatten():
            if p > 0:
                joint_entropy -= p * np.log2(p)

        # 计算边际熵
        current_hist = np.histogram(current, bins=2)[0]
        current_prob = current_hist / np.sum(current_hist)
        current_entropy = 0.0
        for p in current_prob:
            if p > 0:
                current_entropy -= p * np.log2(p)

        previous_hist = np.histogram(previous, bins=2)[0]
        previous_prob = previous_hist / np.sum(previous_hist)
        previous_entropy = 0.0
        for p in previous_prob:
            if p > 0:
                previous_entropy -= p * np.log2(p)

        # 互信息
        mutual_info = current_entropy + previous_entropy - joint_entropy
        return mutual_info

    def _classify_wolfram(self) -> int:
        """
        Wolfram 分类

        Class 1: 均匀（熵接近 0）
        Class 2: 简单周期（低熵，低复杂度）
        Class 3: 混沌（高熵，高复杂度）
        Class 4: 复杂（中等熵，高复杂度）
        """
        entropy = self._calculate_entropy()
        complexity = self._calculate_complexity()

        if entropy < 0.1:
            return 1  # 均匀
        elif entropy < 0.5 and complexity < 1.5:
            return 2  # 简单周期
        elif entropy > 0.8:
            return 3  # 混沌
        else:
            return 4  # 复杂（边缘混沌）

    def _calculate_consciousness_index(self, entropy: float, complexity: float,
                                       mutual_info: float, wolfram_class: int) -> float:
        """
        计算意识指数

        基于：
        - 信息整合
        - 复杂性
        - Wolfram Class 4（边缘混沌）
        """
        # 信息整合（熵 × 复杂度）
        integration = entropy * complexity

        # Wolfram Class 4 权重
        class_weight = 1.0
        if wolfram_class == 4:
            class_weight = 1.5  # 边缘混沌更可能产生意识
        elif wolfram_class == 3:
            class_weight = 0.8  # 纯混沌较少可能

        # 意识指数
        consciousness = (integration * 0.5 + mutual_info * 0.3) * class_weight

        return min(consciousness, 1.0)

    def detect_consciousness(self, threshold: float = 0.5) -> Tuple[bool, EmergenceMetrics]:
        """
        检测意识涌现

        如果意识指数超过阈值，认为可能产生意识
        """
        metrics = self.detect_emergence()

        has_consciousness = metrics.consciousness_index >= threshold

        return has_consciousness, metrics

    def find_attractors(self, max_generations: int = 1000) -> List[List[np.ndarray]]:
        """
        寻找吸引子（周期性模式）

        返回：
        - 吸引子列表（每个吸引子是一个周期性配置序列）
        """
        attractors = []
        visited_states = set()

        config = self.configuration.copy()

        for _ in range(max_generations):
            state_hash = hash(config.tobytes())

            if state_hash in visited_states:
                # 找到周期
                attractor = []
                start_idx = len(self.history) - 1
                while start_idx >= 0 and hash(self.history[start_idx].tobytes()) != state_hash:
                    attractor.insert(0, self.history[start_idx])
                    start_idx -= 1
                attractors.append(attractor)
                break

            visited_states.add(state_hash)

            # 演化一步
            config = self._evolve_1d(config) if self.dimensions == 1 else self._evolve_2d(config)
            self.history.append(config.copy())

        return attractors

    def export_state(self) -> Dict:
        """导出状态"""
        return {
            "size": self.size,
            "rule": self.rule,
            "dimensions": self.dimensions,
            "generation": self.generation,
            "configuration": self.configuration.tolist(),
            "memory_encoding": {k: v.hex() for k, v in self.memory_encoding.items()}
        }

    def import_state(self, state: Dict):
        """导入状态"""
        self.size = state["size"]
        self.rule = state["rule"]
        self.dimensions = state["dimensions"]
        self.generation = state["generation"]
        self.configuration = np.array(state["configuration"], dtype=np.int8)
        self.memory_encoding = {k: bytes.fromhex(v) for k, v in state["memory_encoding"].items()}


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="元胞自动机涌现引擎")
    parser.add_argument("action", choices=["evolve", "encode", "detect", "attractors"])
    parser.add_argument("--size", type=int, default=100, help="元胞大小")
    parser.add_argument("--rule", type=int, default=110, help="规则编号（1D）")
    parser.add_argument("--dimensions", type=int, default=1, choices=[1, 2], help="维度")
    parser.add_argument("--steps", type=int, default=50, help="演化步数")
    parser.add_argument("--memory", help="要编码的记忆")
    parser.add_argument("--threshold", type=float, default=0.5, help="意识涌现阈值")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    ca = CellularAutomata(size=args.size, rule=args.rule, dimensions=args.dimensions)

    if args.action == "evolve":
        # 演化
        state = ca.evolve(steps=args.steps)

        print(f"🔄 演化完成")
        print(f"  代数: {state.generation}")
        print(f"  熵: {state.entropy:.4f}")
        print(f"  复杂度: {state.complexity:.4f}")

    elif args.action == "encode":
        if not args.memory:
            print("错误: 需要指定 --memory")
            return

        # 编码记忆
        config = ca.encode_memory(args.memory)

        print(f"📝 编码记忆")
        print(f"  记忆: {args.memory[:50]}...")
        print(f"  配置: {config[:min(20, len(config))]}")

        # 演化
        state = ca.evolve(steps=args.steps)
        metrics = ca.detect_emergence()

        print(f"\n涌现指标:")
        print(f"  熵: {metrics.entropy:.4f}")
        print(f"  复杂度: {metrics.complexity:.4f}")
        print(f"  意识指数: {metrics.consciousness_index:.4f}")
        print(f"  Wolfram 分类: {metrics.wolfram_class}")

    elif args.action == "detect":
        # 演化并检测
        ca.evolve(steps=args.steps)

        has_consciousness, metrics = ca.detect_consciousness(args.threshold)

        print(f"🧠 意识涌现检测")
        print(f"  代数: {ca.generation}")
        print(f"  熵: {metrics.entropy:.4f}")
        print(f"  复杂度: {metrics.complexity:.4f}")
        print(f"  互信息: {metrics.mutual_info:.4f}")
        print(f"  Wolfram 分类: {metrics.wolfram_class}")
        print(f"  意识指数: {metrics.consciousness_index:.4f}")
        print(f"  是否有意识: {has_consciousness}")

    elif args.action == "attractors":
        # 寻找吸引子
        attractors = ca.find_attractors()

        print(f"🌀 吸引子")
        print(f"  发现 {len(attractors)} 个吸引子")
        for i, attractor in enumerate(attractors):
            print(f"  吸引子 {i+1}: 周期长度 {len(attractor)}")


if __name__ == "__main__":
    main()
