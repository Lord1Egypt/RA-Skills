#!/usr/bin/env python3
"""
高级信息论 - Advanced Information Theory

核心思想：
超越基础的熵和压缩，实现更精确的信息论算法。

数学基础：
1. Normalized Compression Distance (NCD)
   - 比 Lempel-Ziv 更精确的相似度度量
   - 基于 Kolmogorov 复杂度
   - 无监督聚类和分类

2. Algorithmic Probability (Solomonoff)
   - 算法概率理论
   - 预测最可能的序列
   - 归纳推理

3. Minimum Description Length (MDL)
   - 最小描述长度原则
   - 模型选择
   - 过拟合检测

4. Mutual Information Maximization
   - 互信息最大化
   - 特征选择
   - 信息瓶颈

应用：
- 高级压缩
- 相似度度量
- 模型选择
- 预测
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import zlib
import json
from pathlib import Path
from collections import Counter


@dataclass
class NCDScore:
    """NCD 分数"""
    distance: float
    similarity: float
    normalized_similarity: float


@dataclass
class AlgorithmicProbabilityResult:
    """算法概率结果"""
    probability: float
    complexity: float
    surprise: float


@dataclass
class MDLResult:
    """MDL 结果"""
    selected_model: str
    description_length: float
    model_cost: float
    data_cost: float


class NormalizedCompressionDistance:
    """
    Normalized Compression Distance (NCD)

    比 Lempel-Ziv 更精确的 Kolmogorov 复杂度近似

    公式：
    NCD(x, y) = [C(xy) - min(C(x), C(y))] / max(C(x), C(y))

    其中：
    - C(x): 字符串 x 的压缩长度
    - xy: x 和 y 的连接

    特性：
    - NCD(x, x) = 0
    - NCD(x, y) ∈ [0, 1]
    - 对称性：NCD(x, y) = NCD(y, x)
    """
    def __init__(self):
        self.compression_cache: Dict[str, int] = {}

    def compress(self, data: str) -> int:
        """压缩并返回长度"""
        if data in self.compression_cache:
            return self.compression_cache[data]

        compressed = zlib.compress(data.encode())
        length = len(compressed)

        self.compression_cache[data] = length
        return length

    def calculate_ncd(self, x: str, y: str) -> NCDScore:
        """
        计算 NCD

        参数：
        - x: 字符串 1
        - y: 字符串 2

        返回：
        - NCDScore: NCD 分数
        """
        cx = self.compress(x)
        cy = self.compress(y)
        cxy = self.compress(x + y)

        min_c = min(cx, cy)
        max_c = max(cx, cy)

        if max_c == 0:
            ncd = 0.0
        else:
            ncd = (cxy - min_c) / max_c

        # 计算相似度
        similarity = 1.0 - ncd

        # 归一化相似度
        normalized_similarity = max(0.0, similarity)

        return NCDScore(
            distance=ncd,
            similarity=similarity,
            normalized_similarity=normalized_similarity
        )

    def calculate_all_pairwise(self, strings: List[str]) -> np.ndarray:
        """
        计算所有字符串对的 NCD

        返回：
        - 相似度矩阵
        """
        n = len(strings)
        similarity_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                ncd_score = self.calculate_ncd(strings[i], strings[j])
                similarity_matrix[i, j] = ncd_score.normalized_similarity

        return similarity_matrix


class AlgorithmicProbability:
    """
    算法概率（Algorithmic Probability）

    基于 Solomonoff 的归纳理论

    公式：
    P(x) = Σ p : U(p) = x* 2^(-|p|)

    其中：
    - U: 通用图灵机
    - p: 程序
    - |p|: 程序长度
    - x*: 以 x 开头的字符串

    近似：使用压缩长度
    """
    def __init__(self):
        self.program_cache: Dict[str, float] = {}

    def calculate_complexity(self, sequence: str) -> float:
        """
        计算 Kolmogorov 复杂度近似

        使用压缩长度
        """
        compressed = zlib.compress(sequence.encode())
        return len(compressed)

    def calculate_probability(self, sequence: str, n_examples: int = 100) -> AlgorithmicProbabilityResult:
        """
        计算算法概率

        近似：P(x) ∝ 2^(-K(x))

        其中 K(x) 是 Kolmogorov 复杂度
        """
        complexity = self.calculate_complexity(sequence)

        # 概率：2^(-复杂度)
        probability = 2 ** (-complexity / 100.0)  # 归一化

        # 惊奇度（Surprisal）= -log(P)
        if probability > 0:
            surprise = -np.log2(probability)
        else:
            surprise = float('inf')

        return AlgorithmicProbabilityResult(
            probability=probability,
            complexity=complexity,
            surprise=surprise
        )

    def predict_next(self, sequence: str, possible_continuations: List[str]) -> List[Tuple[str, float]]:
        """
        预测下一个最可能的延续

        选择使整体序列的算法概率最大的延续
        """
        predictions = []

        for continuation in possible_continuations:
            full_sequence = sequence + continuation
            prob_result = self.calculate_probability(full_sequence)

            predictions.append((continuation, prob_result.probability))

        # 按概率排序
        predictions.sort(key=lambda x: x[1], reverse=True)

        return predictions


class MDLModelSelector:
    """
    最小描述长度（MDL）模型选择器

    MDL 原则：最好的理论是能够以最短方式描述数据的理论

    公式：
    L(M, D) = L(M) + L(D | M)

    其中：
    - L(M, D): 模型 M 和数据 D 的总描述长度
    - L(M): 模型 M 的描述长度
    - L(D | M): 给定模型 M 时数据 D 的描述长度
    """
    def __init__(self):
        self.models: Dict[str, Dict] = {}

    def register_model(self, name: str, model_cost: float, encode_function: callable):
        """
        注册模型

        参数：
        - name: 模型名称
        - model_cost: 模型描述长度
        - encode_function: 编码函数（返回数据描述长度）
        """
        self.models[name] = {
            "model_cost": model_cost,
            "encode_function": encode_function
        }

    def select_best_model(self, data: str) -> MDLResult:
        """
        选择最佳模型（最小化总描述长度）

        返回：
        - MDLResult: 最佳模型及其描述长度
        """
        if not self.models:
            return MDLResult(
                selected_model="",
                description_length=float('inf'),
                model_cost=0.0,
                data_cost=0.0
            )

        best_model = None
        best_total_length = float('inf')
        best_model_cost = 0.0
        best_data_cost = 0.0

        for model_name, model_info in self.models.items():
            # 计算模型描述长度
            model_cost = model_info["model_cost"]

            # 计算数据描述长度
            encode_function = model_info["encode_function"]
            data_cost = encode_function(data)

            # 总描述长度
            total_length = model_cost + data_cost

            if total_length < best_total_length:
                best_total_length = total_length
                best_model = model_name
                best_model_cost = model_cost
                best_data_cost = data_cost

        return MDLResult(
            selected_model=best_model,
            description_length=best_total_length,
            model_cost=best_model_cost,
            data_cost=best_data_cost
        )


class MutualInformationMaximizer:
    """
    互信息最大化器

    互信息衡量两个随机变量之间的相互依赖

    公式：
    I(X; Y) = H(X) - H(X | Y) = H(Y) - H(Y | X)

    应用：
    - 特征选择
    - 信息瓶颈
    - 相似度度量
    """
    def __init__(self):
        pass

    def calculate_entropy(self, data: List) -> float:
        """计算熵"""
        if not data:
            return 0.0

        counter = Counter(data)
        total = len(data)

        entropy = 0.0
        for count in counter.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)

        return entropy

    def calculate_mutual_information(self, x: List, y: List) -> float:
        """
        计算互信息

        I(X; Y) = H(X) + H(Y) - H(X, Y)
        """
        if len(x) != len(y):
            raise ValueError("x 和 y 长度必须相同")

        # 边际熵
        h_x = self.calculate_entropy(x)
        h_y = self.calculate_entropy(y)

        # 联合熵
        joint = list(zip(x, y))
        h_xy = self.calculate_entropy(joint)

        # 互信息
        mutual_info = h_x + h_y - h_xy

        return mutual_info

    def select_features(self, features: Dict[str, List], target: List, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        特征选择：选择与目标互信息最大的特征

        参数：
        - features: 特征字典 {特征名: 特征值列表}
        - target: 目标值列表
        - top_k: 选择前 k 个特征

        返回：
        - 排序后的特征列表 [(特征名, 互信息)]
        """
        feature_scores = []

        for feature_name, feature_values in features.items():
            if len(feature_values) != len(target):
                continue

            mi = self.calculate_mutual_information(feature_values, target)
            feature_scores.append((feature_name, mi))

        # 按互信息排序
        feature_scores.sort(key=lambda x: x[1], reverse=True)

        return feature_scores[:top_k]


class AdvancedInformationTheoreticCore:
    """
    高级信息论核心 - 整合所有高级信息论算法

    包括：
    1. NCD（标准化压缩距离）
    2. Algorithmic Probability（算法概率）
    3. MDL（最小描述长度）
    4. Mutual Information（互信息）
    """
    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)

        # 初始化各个模块
        self.ncd = NormalizedCompressionDistance()
        self.alg_prob = AlgorithmicProbability()
        self.mdl = MDLModelSelector()
        self.mi = MutualInformationMaximizer()

    def compress_advanced(self, data: str, method: str = "ncd") -> Dict:
        """
        高级压缩

        参数：
        - data: 输入数据
        - method: 压缩方法（ncd, algorithmic）

        返回：
        - 压缩结果
        """
        if method == "ncd":
            # 使用 NCD 进行压缩
            compressed = zlib.compress(data.encode())

            result = {
                "method": "ncd",
                "original_length": len(data),
                "compressed_length": len(compressed),
                "compression_ratio": len(data) / len(compressed),
                "compressed_data": compressed.hex()
            }

        elif method == "algorithmic":
            # 使用算法概率进行压缩
            prob_result = self.alg_prob.calculate_probability(data)

            result = {
                "method": "algorithmic",
                "original_length": len(data),
                "complexity": prob_result.complexity,
                "probability": prob_result.probability,
                "surprise": prob_result.surprise
            }

        else:
            raise ValueError(f"未知的压缩方法: {method}")

        return result

    def evaluate_similarity(self, data1: str, data2: str) -> Dict:
        """
        评估相似度

        使用 NCD 计算相似度
        """
        ncd_score = self.ncd.calculate_ncd(data1, data2)

        return {
            "distance": ncd_score.distance,
            "similarity": ncd_score.similarity,
            "normalized_similarity": ncd_score.normalized_similarity
        }

    def select_best_model(self, data: str) -> Dict:
        """
        使用 MDL 选择最佳模型

        先注册一些示例模型
        """
        # 注册示例模型

        # 模型 1: 无压缩
        def encode_no_compression(data: str) -> float:
            return len(data.encode())

        # 模型 2: zlib 压缩
        def encode_zlib(data: str) -> float:
            compressed = zlib.compress(data.encode())
            return len(compressed)

        # 模型 3: 重复模式压缩
        def encode_pattern(data: str) -> float:
            # 简化：检测重复模式
            repeated = data.replace(data[:min(10, len(data))], "")
            compressed = zlib.compress(repeated.encode())
            return len(compressed) + 10  # 加上模式描述的开销

        self.mdl.register_model("no_compression", 1.0, encode_no_compression)
        self.mdl.register_model("zlib", 5.0, encode_zlib)
        self.mdl.register_model("pattern", 15.0, encode_pattern)

        # 选择最佳模型
        result = self.mdl.select_best_model(data)

        return {
            "selected_model": result.selected_model,
            "total_description_length": result.description_length,
            "model_cost": result.model_cost,
            "data_cost": result.data_cost
        }


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="高级信息论模块")
    parser.add_argument("action", choices=["ncd", "compress", "probability", "mdl", "mi"])
    parser.add_argument("--data", help="数据")
    parser.add_argument("--data1", help="数据 1")
    parser.add_argument("--data2", help="数据 2")
    parser.add_argument("--method", default="ncd", help="压缩方法")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    core = AdvancedInformationTheoreticCore(args.workspace)

    if args.action == "ncd":
        if not args.data1 or not args.data2:
            print("错误: 需要指定 --data1 和 --data2")
            return

        # 计算 NCD
        similarity = core.evaluate_similarity(args.data1, args.data2)

        print(f"📏 NCD 相似度度量")
        print(f"  数据 1: {args.data1[:50]}...")
        print(f"  数据 2: {args.data2[:50]}...")
        print(f"  NCD 距离: {similarity['distance']:.4f}")
        print(f"  相似度: {similarity['similarity']:.4f}")
        print(f"  归一化相似度: {similarity['normalized_similarity']:.4f}")

    elif args.action == "compress":
        if not args.data:
            print("错误: 需要指定 --data")
            return

        # 高级压缩
        result = core.compress_advanced(args.data, args.method)

        print(f"🗜️  高级压缩")
        print(f"  方法: {result['method']}")
        if "original_length" in result:
            print(f"  原始长度: {result['original_length']}")
            print(f"  压缩长度: {result['compressed_length']}")
            print(f"  压缩比: {result['compression_ratio']:.2f}")
        if "complexity" in result:
            print(f"  复杂度: {result['complexity']:.2f}")
            print(f"  概率: {result['probability']:.6f}")
            print(f"  惊奇度: {result['surprise']:.2f}")

    elif args.action == "probability":
        if not args.data:
            print("错误: 需要指定 --data")
            return

        # 算法概率
        prob_result = core.alg_prob.calculate_probability(args.data)

        print(f"🎲 算法概率")
        print(f"  数据: {args.data[:50]}...")
        print(f"  复杂度: {prob_result.complexity:.2f}")
        print(f"  概率: {prob_result.probability:.6f}")
        print(f"  惊奇度: {prob_result.surprise:.2f}")

    elif args.action == "mdl":
        if not args.data:
            print("错误: 需要指定 --data")
            return

        # MDL 模型选择
        result = core.select_best_model(args.data)

        print(f"📐 MDL 模型选择")
        print(f"  数据: {args.data[:50]}...")
        print(f"  最佳模型: {result['selected_model']}")
        print(f"  总描述长度: {result['total_description_length']:.2f}")
        print(f"  模型开销: {result['model_cost']:.2f}")
        print(f"  数据开销: {result['data_cost']:.2f}")

    elif args.action == "mi":
        # 互信息示例
        x = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
        z = [5, 4, 3, 2, 1, 5, 4, 3, 2, 1]

        mi_xy = core.mi.calculate_mutual_information(x, y)
        mi_xz = core.mi.calculate_mutual_information(x, z)

        print(f"🔗 互信息")
        print(f"  I(X; Y): {mi_xy:.4f}")
        print(f"  I(X; Z): {mi_xz:.4f}")
        print(f"  X 和 Y 更相关: {mi_xy > mi_xz}")


if __name__ == "__main__":
    main()
