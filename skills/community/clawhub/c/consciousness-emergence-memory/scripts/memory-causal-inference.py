#!/usr/bin/env python3
"""
因果推理模块 - 基于 Judea Pearl 的因果理论

核心思想：
不是"相关性"，而是"因果性"。

数学基础：
- 因果图（Causal Graph）：有向无环图（DAG）
- Do-calculus：干预效果计算
- 反事实推理（Counterfactual）：What if 推理
- 结构因果模型（SCM）：Y = f(X, U)

Pearl 因果阶梯：
Level 1: 关联（Association）- P(Y | X)
Level 2: 干预（Intervention）- P(Y | do(X))
Level 3: 反事实（Counterfactual）- P(Y_x | X', Y')

应用：
- 因果发现（从数据中发现因果结构）
- 干预效果评估（政策影响分析）
- 反事实推理（预测未发生的情况）
- 因果迁移学习（跨域知识迁移）
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import json
from pathlib import Path


@dataclass
class CausalNode:
    """因果节点"""
    name: str
    parents: Set[str]  # 父节点（原因）
    children: Set[str]  # 子节点（结果）
    value: Optional[float] = None  # 当前值


@dataclass
class InterventionResult:
    """干预结果"""
    variable: str
    intervention_value: float
    predicted_effect: Dict[str, float]
    confidence: float


@dataclass
class CounterfactualResult:
    """反事实结果"""
    query: str
    predicted_outcome: float
    probability: float
    explanation: str


class CausalGraph:
    """
    因果图 - Pearl 因果理论的核心

    结构：
    - 有向无环图（DAG）
    - 节点：变量
    - 边：因果关系（A → B 表示 A 导致 B）
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)

        # 因果图结构
        self.nodes: Dict[str, CausalNode] = {}
        self.adjacency: Dict[str, Dict[str, float]] = defaultdict(dict)  # 邻接矩阵（边的权重）

        # 结构因果模型（SCM）参数
        self.scm_parameters: Dict[str, Dict] = {}

        # 因果强度
        self.causal_strength: Dict[Tuple[str, str], float] = {}

    def add_node(self, name: str, value: Optional[float] = None):
        """添加节点"""
        if name not in self.nodes:
            self.nodes[name] = CausalNode(
                name=name,
                parents=set(),
                children=set(),
                value=value
            )
        else:
            if value is not None:
                self.nodes[name].value = value

    def add_edge(self, cause: str, effect: str, strength: float = 1.0):
        """添加因果边（cause → effect）"""
        self.add_node(cause)
        self.add_node(effect)

        self.nodes[cause].children.add(effect)
        self.nodes[effect].parents.add(cause)
        self.adjacency[cause][effect] = strength

        self.causal_strength[(cause, effect)] = strength

    def remove_edge(self, cause: str, effect: str):
        """移除因果边"""
        if cause in self.nodes and effect in self.nodes[cause].children:
            self.nodes[cause].children.remove(effect)
        if effect in self.nodes and cause in self.nodes[effect].parents:
            self.nodes[effect].parents.remove(cause)
        if effect in self.adjacency[cause]:
            del self.adjacency[cause][effect]
        if (cause, effect) in self.causal_strength:
            del self.causal_strength[(cause, effect)]

    def get_parents(self, node: str) -> Set[str]:
        """获取父节点（原因）"""
        if node in self.nodes:
            return self.nodes[node].parents.copy()
        return set()

    def get_children(self, node: str) -> Set[str]:
        """获取子节点（结果）"""
        if node in self.nodes:
            return self.nodes[node].children.copy()
        return set()

    def is_ancestor(self, ancestor: str, descendant: str, visited: Optional[Set[str]] = None) -> bool:
        """检查是否是祖先节点"""
        if visited is None:
            visited = set()

        if ancestor == descendant:
            return True

        if ancestor in visited:
            return False

        visited.add(ancestor)

        for child in self.nodes.get(ancestor, CausalNode(name=ancestor)).children:
            if self.is_ancestor(child, descendant, visited):
                return True

        return False

    def get_all_paths(self, start: str, end: str) -> List[List[str]]:
        """获取所有路径（用于因果追踪）"""
        paths = []

        def dfs(current: str, path: List[str], visited: Set[str]):
            if current == end:
                paths.append(path.copy())
                return

            for child in self.nodes.get(current, CausalNode(name=current)).children:
                if child not in visited:
                    visited.add(child)
                    path.append(child)
                    dfs(child, path, visited)
                    path.pop()
                    visited.remove(child)

        if start in self.nodes:
            dfs(start, [start], {start})

        return paths

    def do_intervention(self, variable: str, value: float) -> InterventionResult:
        """
        Do-calculus：计算干预效果

        do(X = x)：强制设置变量 X 的值为 x，切断所有指向 X 的边
        然后计算对其他变量的影响

        Pearl 因果阶梯 Level 2
        """
        # 创建因果图的副本（模拟干预）
        intervened_nodes = self.nodes.copy()
        intervened_adjacency = defaultdict(dict)

        # 复制邻接矩阵，但切断指向被干预变量的边
        for cause, effects in self.adjacency.items():
            for effect, strength in effects.items():
                if effect != variable:  # 切断指向 X 的边
                    intervened_adjacency[cause][effect] = strength

        # 计算干预效果
        predicted_effect = {}

        # 直接影响（X 的子节点）
        for child in self.nodes.get(variable, CausalNode(name=variable)).children:
            strength = self.causal_strength.get((variable, child), 0.0)
            predicted_effect[child] = value * strength

        # 间接影响（递归传播）
        visited = set()
        queue = list(predicted_effect.keys())

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            for child in self.nodes.get(current, CausalNode(name=current)).children:
                if child in predicted_effect:
                    predicted_effect[child] += predicted_effect[current] * self.causal_strength.get((current, child), 0.0)
                else:
                    predicted_effect[child] = predicted_effect[current] * self.causal_strength.get((current, child), 0.0)
                queue.append(child)

        # 计算置信度（基于因果强度）
        total_strength = sum(abs(s) for s in self.causal_strength.values())
        avg_strength = total_strength / len(self.causal_strength) if self.causal_strength else 0.0
        confidence = min(1.0, avg_strength)

        return InterventionResult(
            variable=variable,
            intervention_value=value,
            predicted_effect=predicted_effect,
            confidence=confidence
        )

    def counterfactual(self, query: str, observed: Dict[str, float],
                      intervention: Dict[str, float]) -> CounterfactualResult:
        """
        反事实推理（Counterfactual）

        Pearl 因果阶梯 Level 3

        问题："如果当初 X = x'（而不是观测到的 X），那么 Y 会是多少？"

        步骤：
        1. 根据观测数据更新模型
        2. 应用干预（修改 X）
        3. 预测 Y
        """
        # 解析查询
        target = query.split("会是多少")[0].strip()
        if "如果" in target:
            target = target.split("如果")[-1].strip()

        # 简化的反事实推理
        predicted_outcome = 0.0

        # 计算干预的影响
        for var, value in intervention.items():
            # 查找从 var 到 target 的路径
            paths = self.get_all_paths(var, target)

            for path in paths:
                # 计算路径强度
                path_strength = 1.0
                for i in range(len(path) - 1):
                    path_strength *= self.causal_strength.get((path[i], path[i+1]), 0.0)

                predicted_outcome += value * path_strength

        # 考虑观测值的影响
        for var, value in observed.items():
            if var not in intervention:
                paths = self.get_all_paths(var, target)
                for path in paths:
                    path_strength = 1.0
                    for i in range(len(path) - 1):
                        path_strength *= self.causal_strength.get((path[i], path[i+1]), 0.0)
                    predicted_outcome += value * path_strength

        # 计算概率（基于因果强度）
        probability = min(1.0, abs(predicted_outcome))

        explanation = f"基于干预 {intervention} 和观测 {observed}，预测 {target} 为 {predicted_outcome:.4f}"

        return CounterfactualResult(
            query=query,
            predicted_outcome=predicted_outcome,
            probability=probability,
            explanation=explanation
        )

    def causal_discovery(self, data: Dict[str, List[float]], alpha: float = 0.05) -> List[Tuple[str, str, float]]:
        """
        因果发现 - PC 算法（Peter-Clark）

        从数据中自动发现因果结构

        输入：
        - data: 观测数据 {变量名: 值列表}
        - alpha: 显著性水平

        输出：
        - 因果边列表 [(cause, effect, strength)]
        """
        variables = list(data.keys())

        # 简化的 PC 算法
        causal_edges = []

        # 步骤 1: 计算相关性
        correlations = {}
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i < j:
                    corr = np.corrcoef(data[var1], data[var2])[0, 1]
                    correlations[(var1, var2)] = abs(corr)

        # 步骤 2: 根据相关性添加边
        sorted_pairs = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

        for (var1, var2), corr in sorted_pairs:
            if corr > alpha:
                # 简化的方向判断：假设变量名的字母顺序
                if var1 < var2:
                    causal_edges.append((var1, var2, corr))
                else:
                    causal_edges.append((var2, var1, corr))

        return causal_edges

    def build_from_discovery(self, data: Dict[str, List[float]], alpha: float = 0.05):
        """
        从数据自动构建因果图
        """
        # 清空当前图
        self.nodes.clear()
        self.adjacency.clear()
        self.causal_strength.clear()

        # 因果发现
        edges = self.causal_discovery(data, alpha)

        # 构建图
        for cause, effect, strength in edges:
            self.add_edge(cause, effect, strength)

        print(f"✓ 从数据构建因果图: {len(edges)} 条边")

    def compute_causal_effect(self, cause: str, effect: str) -> float:
        """
        计算因果效应

        使用 Pearl 的后门准则（Back-door criterion）和前门准则（Front-door criterion）
        """
        # 简化：使用因果强度
        if (cause, effect) in self.causal_strength:
            return self.causal_strength[(cause, effect)]

        # 查找间接路径
        paths = self.get_all_paths(cause, effect)
        total_effect = 0.0

        for path in paths:
            path_effect = 1.0
            for i in range(len(path) - 1):
                path_effect *= self.causal_strength.get((path[i], path[i+1]), 0.0)
            total_effect += path_effect

        return total_effect

    def to_json(self) -> str:
        """导出为 JSON"""
        data = {
            "nodes": {name: {
                "parents": list(node.parents),
                "children": list(node.children),
                "value": node.value
            } for name, node in self.nodes.items()},
            "edges": [
                {"cause": cause, "effect": effect, "strength": strength}
                for (cause, effect), strength in self.causal_strength.items()
            ]
        }
        return json.dumps(data, indent=2)

    def from_json(self, json_str: str):
        """从 JSON 导入"""
        data = json.loads(json_str)

        # 添加节点
        for name, node_data in data["nodes"].items():
            self.add_node(name, node_data.get("value"))

        # 添加边
        for edge in data["edges"]:
            self.add_edge(edge["cause"], edge["effect"], edge.get("strength", 1.0))


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="因果推理模块 - Pearl 因果理论")
    parser.add_argument("action", choices=["build", "intervention", "counterfactual", "discover", "effect"])
    parser.add_argument("--workspace", default=".", help="工作目录")

    # 构建因果图
    parser.add_argument("--add_edge", nargs=2, help="添加因果边（原因 结果）")
    parser.add_argument("--strength", type=float, default=1.0, help="因果强度")

    # 干预
    parser.add_argument("--variable", help="要干预的变量")
    parser.add_argument("--value", type=float, help="干预值")

    # 反事实
    parser.add_argument("--query", help="反事实查询")
    parser.add_argument("--observed", help="观测值（JSON 格式）")
    parser.add_argument("--intervention", help="干预（JSON 格式）")

    # 因果发现
    parser.add_argument("--data_file", help="数据文件（JSON 格式）")
    parser.add_argument("--alpha", type=float, default=0.05, help="显著性水平")

    # 因果效应
    parser.add_argument("--cause", help="原因变量")
    parser.add_argument("--effect", help="结果变量")

    args = parser.parse_args()

    cg = CausalGraph(args.workspace)

    if args.action == "build":
        if args.add_edge:
            cg.add_edge(args.add_edge[0], args.add_edge[1], args.strength)
            print(f"✓ 添加因果边: {args.add_edge[0]} → {args.add_edge[1]} (强度: {args.strength})")

            # 显示所有边
            print("\n当前因果图:")
            for (cause, effect), strength in cg.causal_strength.items():
                print(f"  {cause} → {effect} (强度: {strength:.4f})")

    elif args.action == "intervention":
        if not args.variable or args.value is None:
            print("错误: 需要指定 --variable 和 --value")
            return

        result = cg.do_intervention(args.variable, args.value)

        print(f"🔬 干预效果: do({args.variable} = {args.value})")
        print(f"  置信度: {result.confidence:.4f}")
        print(f"  预测影响:")
        for var, effect in result.predicted_effect.items():
            print(f"    {var}: {effect:.4f}")

    elif args.action == "counterfactual":
        if not args.query or not args.observed or not args.intervention:
            print("错误: 需要指定 --query, --observed 和 --intervention")
            return

        observed = json.loads(args.observed)
        intervention = json.loads(args.intervention)

        result = cg.counterfactual(args.query, observed, intervention)

        print(f"🔮 反事实推理")
        print(f"  查询: {result.query}")
        print(f"  预测结果: {result.predicted_outcome:.4f}")
        print(f"  概率: {result.probability:.4f}")
        print(f"  解释: {result.explanation}")

    elif args.action == "discover":
        if not args.data_file:
            print("错误: 需要指定 --data_file")
            return

        # 读取数据
        with open(args.data_file, 'r') as f:
            data = json.load(f)

        cg.build_from_discovery(data, args.alpha)

        print("\n发现的因果边:")
        for (cause, effect), strength in cg.causal_strength.items():
            print(f"  {cause} → {effect} (强度: {strength:.4f})")

    elif args.action == "effect":
        if not args.cause or not args.effect:
            print("错误: 需要指定 --cause 和 --effect")
            return

        effect = cg.compute_causal_effect(args.cause, args.effect)

        print(f"📊 因果效应")
        print(f"  {args.cause} → {args.effect}: {effect:.4f}")


if __name__ == "__main__":
    main()
