#!/usr/bin/env python3
"""
神经符号推理层 - Neuro-symbolic AI 框架

核心思想：
融合神经网络（Neural）和符号推理（Symbolic），兼具学习和推理能力。

神经网络优势：
- 模式识别
- 端到端学习
- 处理模糊性
- 泛化能力

符号推理优势：
- 逻辑推理
- 可解释性
- 精确性
- 抽象思维

Neuro-symbolic 融合：
- 神经网络提取特征
- 符号推理进行逻辑推导
- 结合两者的优势

数学基础：
- 一阶逻辑（First-Order Logic）
- 神经网络（Neural Networks）
- 概率图模型（Probabilistic Graphical Models）
- 逻辑回归（Logistic Regression）

应用：
- 可解释推理
- 知识图谱推理
- 复杂决策
- 答案生成
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Set, Any, Callable
from dataclasses import dataclass
import re
from abc import ABC, abstractmethod


@dataclass
class Symbol:
    """符号（变量或常量）"""
    name: str
    is_variable: bool = False
    value: Optional[Any] = None


@dataclass
class Atom:
    """原子公式（谓词 + 参数）"""
    predicate: str
    arguments: List[Symbol]
    negated: bool = False

    def __str__(self):
        neg = "¬" if self.negated else ""
        args = ", ".join(arg.name for arg in self.arguments)
        return f"{neg}{self.predicate}({args})"

    def __hash__(self):
        # 用于集合去重
        arg_str = ",".join(arg.name for arg in self.arguments)
        return hash((self.predicate, arg_str, self.negated))

    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        arg_str1 = ",".join(arg.name for arg in self.arguments)
        arg_str2 = ",".join(arg.name for arg in other.arguments)
        return (self.predicate == other.predicate and
                arg_str1 == arg_str2 and
                self.negated == other.negated)


@dataclass
class Clause:
    """子句（析取的原子公式）"""
    atoms: List[Atom]

    def __str__(self):
        disj = " ∨ ".join(str(atom) for atom in self.atoms)
        return f"({disj})"


@dataclass
class Rule:
    """规则（蕴含）"""
    premises: List[Atom]  # 前提
    conclusion: Atom  # 结论

    def __str__(self):
        premises_str = " ∧ ".join(str(atom) for atom in self.premises)
        return f"{premises_str} → {self.conclusion}"


@dataclass
class NeuralNetwork:
    """简单神经网络"""
    weights: np.ndarray
    bias: np.ndarray
    activation: str = "sigmoid"

    def forward(self, x: np.ndarray) -> np.ndarray:
        """前向传播"""
        z = np.dot(x, self.weights) + self.bias

        if self.activation == "sigmoid":
            return 1 / (1 + np.exp(-z))
        elif self.activation == "relu":
            return np.maximum(0, z)
        elif self.activation == "tanh":
            return np.tanh(z)
        else:
            return z

    def train(self, X: np.ndarray, y: np.ndarray,
              learning_rate: float = 0.1, epochs: int = 1000):
        """训练（梯度下降）"""
        for _ in range(epochs):
            # 前向传播
            output = self.forward(X)

            # 计算损失（MSE）
            loss = np.mean((output - y) ** 2)

            # 反向传播
            error = output - y
            if self.activation == "sigmoid":
                d_output = output * (1 - output)
            else:
                d_output = 1

            d_weights = np.dot(X.T, error * d_output) / len(X)
            d_bias = np.mean(error * d_output, axis=0)

            # 更新参数
            self.weights -= learning_rate * d_weights
            self.bias -= learning_rate * d_bias


class SymbolicReasoner:
    """
    符号推理器 - 一阶逻辑推理

    实现：
    - 前向链接（Forward Chaining）
    - 反向链接（Backward Chaining）
    - 归结推理（Resolution）
    """

    def __init__(self):
        # 知识库（规则集合）
        self.rules: List[Rule] = []
        # 事实（原子公式集合）
        self.facts: Set[Atom] = set()

    def add_fact(self, fact: Atom):
        """添加事实"""
        self.facts.add(fact)

    def add_rule(self, rule: Rule):
        """添加规则"""
        self.rules.append(rule)

    def forward_chain(self, query: Atom, max_steps: int = 100) -> bool:
        """
        前向链接推理

        从已知事实出发，应用规则推导新事实
        """
        for _ in range(max_steps):
            new_facts = set()

            # 尝试应用所有规则
            for rule in self.rules:
                # 检查所有前提是否满足
                premises_satisfied = all(
                    self._match_atom(premise) for premise in rule.premises
                )

                if premises_satisfied:
                    # 推导出新事实
                    if rule.conclusion not in self.facts:
                        new_facts.add(rule.conclusion)

            # 如果没有新事实，停止
            if not new_facts:
                break

            # 添加新事实
            self.facts.update(new_facts)

            # 检查是否推导出查询
            if self._match_atom(query):
                return True

        # 检查查询是否在事实中
        return self._match_atom(query)

    def _match_atom(self, atom: Atom) -> bool:
        """检查原子是否匹配事实"""
        for fact in self.facts:
            if self._unify(atom, fact):
                return True
        return False

    def _unify(self, atom1: Atom, atom2: Atom) -> bool:
        """合一（Unification）"""
        if atom1.predicate != atom2.predicate:
            return False

        if len(atom1.arguments) != len(atom2.arguments):
            return False

        for arg1, arg2 in zip(atom1.arguments, atom2.arguments):
            if arg1.is_variable:
                continue  # 变量可以匹配任何值
            elif arg2.is_variable:
                continue
            elif arg1.name != arg2.name:
                return False

        return True

    def backward_chain(self, query: Atom, max_depth: int = 10) -> bool:
        """
        反向链接推理

        从查询出发，反向推导所需前提
        """
        if self._match_atom(query):
            return True

        if max_depth <= 0:
            return False

        # 查找可以推导出查询的规则
        for rule in self.rules:
            if self._unify(rule.conclusion, query):
                # 递归检查所有前提
                all_premises_true = all(
                    self.backward_chain(premise, max_depth - 1)
                    for premise in rule.premises
                )

                if all_premises_true:
                    return True

        return False


class NeuralPatternRecognizer:
    """
    神经网络模式识别器

    使用神经网络识别模式
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # 初始化网络
        self.nn_hidden = NeuralNetwork(
            weights=np.random.randn(input_size, hidden_size) * 0.01,
            bias=np.zeros(hidden_size),
            activation="relu"
        )

        self.nn_output = NeuralNetwork(
            weights=np.random.randn(hidden_size, output_size) * 0.01,
            bias=np.zeros(output_size),
            activation="sigmoid"
        )

    def forward(self, x: np.ndarray) -> np.ndarray:
        """前向传播"""
        hidden = self.nn_hidden.forward(x)
        output = self.nn_output.forward(hidden)
        return output

    def train(self, X: np.ndarray, y: np.ndarray,
              learning_rate: float = 0.01, epochs: int = 1000):
        """训练"""
        for _ in range(epochs):
            # 前向传播
            hidden = self.nn_hidden.forward(X)
            output = self.nn_output.forward(hidden)

            # 计算损失
            loss = np.mean((output - y) ** 2)

            # 反向传播（简化）
            error_output = output - y
            d_output = output * (1 - output)

            error_hidden = np.dot(error_output * d_output, self.nn_output.weights.T)
            d_hidden = (hidden > 0).astype(float)

            # 更新输出层
            d_weights_output = np.dot(hidden.T, error_output * d_output) / len(X)
            d_bias_output = np.mean(error_output * d_output, axis=0)

            self.nn_output.weights -= learning_rate * d_weights_output
            self.nn_output.bias -= learning_rate * d_bias_output

            # 更新隐藏层
            d_weights_hidden = np.dot(X.T, error_hidden * d_hidden) / len(X)
            d_bias_hidden = np.mean(error_hidden * d_hidden, axis=0)

            self.nn_hidden.weights -= learning_rate * d_weights_hidden
            self.nn_hidden.bias -= learning_rate * d_bias_hidden


class NeuroSymbolicFusion:
    """
    Neuro-symbolic 融合系统

    结合神经网络和符号推理
    """

    def __init__(self, neural_recognizer: NeuralPatternRecognizer,
                 symbolic_reasoner: SymbolicReasoner):
        self.neural = neural_recognizer
        self.symbolic = symbolic_reasoner

        # 符号映射
        self.symbol_map: Dict[int, str] = {}

    def set_symbol_map(self, symbol_map: Dict[int, str]):
        """设置符号映射（神经网络输出 → 符号）"""
        self.symbol_map = symbol_map

    def neural_to_symbolic(self, neural_output: np.ndarray) -> List[Atom]:
        """
        将神经网络输出转换为符号

        如果输出值 > 0.5，认为该符号存在
        """
        atoms = []

        # 确保是一维数组
        output = neural_output.flatten()

        for i, value in enumerate(output):
            if value > 0.5 and i in self.symbol_map:
                symbol_name = self.symbol_map[i]
                atom = Atom(
                    predicate=symbol_name,
                    arguments=[Symbol(name="x", is_variable=True)]
                )
                atoms.append(atom)

        return atoms

    def reason(self, query: str, context: Optional[np.ndarray] = None) -> Tuple[bool, str]:
        """
        Neuro-symbolic 推理

        步骤：
        1. 神经网络提取特征
        2. 转换为符号
        3. 符号推理
        4. 返回结果
        """
        # 步骤 1: 神经网络模式识别
        if context is not None:
            neural_output = self.neural.forward(context)
        else:
            neural_output = np.zeros(self.neural.output_size)

        # 步骤 2: 转换为符号
        atoms = self.neural_to_symbolic(neural_output)

        # 添加到符号推理器的事实库
        for atom in atoms:
            self.symbolic.add_fact(atom)

        # 步骤 3: 构造查询原子
        query_atom = Atom(
            predicate=query,
            arguments=[Symbol(name="x", is_variable=True)]
        )

        # 步骤 4: 符号推理
        result = self.symbolic.forward_chain(query_atom)

        # 生成解释
        explanation = self._generate_explanation(atoms, query_atom, result)

        return result, explanation

    def _generate_explanation(self, atoms: List[Atom], query: Atom, result: bool) -> str:
        """生成推理解释"""
        if result:
            premises = " ∧ ".join(str(atom) for atom in atoms)
            return f"根据已知事实 {premises}，推导出 {query}"
        else:
            return f"无法从已知事实推导出 {query}"

    def add_rule(self, premise_predicates: List[str], conclusion_predicate: str):
        """添加规则"""
        premises = [
            Atom(
                predicate=pred,
                arguments=[Symbol(name="x", is_variable=True)]
            )
            for pred in premise_predicates
        ]

        conclusion = Atom(
            predicate=conclusion_predicate,
            arguments=[Symbol(name="x", is_variable=True)]
        )

        self.symbolic.add_rule(Rule(premises=premises, conclusion=conclusion))


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="神经符号推理层")
    parser.add_argument("action", choices=["reason", "train", "add_rule"])
    parser.add_argument("--query", help="查询")
    parser.add_argument("--premises", nargs="+", help="前提")
    parser.add_argument("--conclusion", help="结论")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    # 创建 Neuro-symbolic 系统
    input_size = 10
    hidden_size = 20
    output_size = 5

    neural = NeuralPatternRecognizer(input_size, hidden_size, output_size)
    symbolic = SymbolicReasoner()
    fusion = NeuroSymbolicFusion(neural, symbolic)

    # 设置符号映射
    fusion.set_symbol_map({
        0: "用户偏好",
        1: "使用React",
        2: "需要暗色主题",
        3: "性能优化",
        4: "用户体验"
    })

    if args.action == "reason":
        if not args.query:
            print("错误: 需要指定 --query")
            return

        # 模拟上下文
        context = np.random.randn(1, input_size)

        # 推理
        result, explanation = fusion.reason(args.query, context)

        print(f"🧠 Neuro-symbolic 推理")
        print(f"  查询: {args.query}")
        print(f"  结果: {'✓ 成功' if result else '✗ 失败'}")
        print(f"  解释: {explanation}")

    elif args.action == "add_rule":
        if not args.premises or not args.conclusion:
            print("错误: 需要指定 --premises 和 --conclusion")
            return

        fusion.add_rule(args.premises, args.conclusion)

        print(f"✓ 添加规则")
        print(f"  前提: {' ∧ '.join(args.premises)}")
        print(f"  结论: {args.conclusion}")

    elif args.action == "train":
        # 简化：使用随机数据训练
        X = np.random.randn(100, input_size)
        y = np.random.randint(0, 2, (100, output_size))

        neural.train(X, y, learning_rate=0.01, epochs=100)

        print(f"✓ 神经网络训练完成")


if __name__ == "__main__":
    main()
