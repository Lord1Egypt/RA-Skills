#!/usr/bin/env python3
"""
蜘蛛网记忆系统 - SpiderWeb Memory System

核心思想：
人类记忆的本质不是简单的存储，而是一个多层级、多路径、相互交叉的蜘蛛网。

核心特性：
1. 多层级结构（同心圆模型）
   - 中心：高价值、高频率访问
   - 外围：低价值、低频率访问
   - 动态调整：根据访问频率和价值动态调整层级

2. 多路径连接（冗余路径）
   - 每个节点有多条路径连接
   - 提供可靠性和快速访问
   - 小世界效应（六度分隔）

3. 极速传播（振动感知）
   - 信息触发产生"振动"
   - 振动沿着网快速传播
   - 共振识别（相关节点激活）

4. 价值链路清晰（信息交易）
   - 高价值信息形成清晰链路
   - 价值传播和反馈
   - 闭环回路

5. 熵减机制（不是智能遗忘）
   - 低价值信息自然衰减
   - 高价值信息增强
   - 系统熵持续减少

6. 自组织（蜘蛛网自修复）
   - 网络重构
   - 节点合并和分裂
   - 边优化

数学基础：
- 图论（Graph Theory）
- 网络科学（Network Science）
- 信息论（Information Theory）
- 复杂网络（Complex Networks）
- 小世界网络（Small-World Networks）
- 无标度网络（Scale-Free Networks）

应用：
- 记忆组织
- 知识图谱
- 关联推理
- 快速检索
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
import heapq
import json
from pathlib import Path
import math


@dataclass
class SpiderNode:
    """蜘蛛网节点（记忆）"""
    id: str
    content: str
    layer: int  # 层级（0=中心，n=外围）
    value: float  # 价值权重 [0, 1]
    access_count: int = 0  # 访问次数
    last_access: float = 0.0  # 最后访问时间
    vibration: float = 0.0  # 当前振动幅度
    neighbors: Set[str] = field(default_factory=set)  # 邻居节点


@dataclass
class SpiderEdge:
    """蜘蛛网边（关联）"""
    source: str
    target: str
    strength: float  # 边强度 [0, 1]
    vibration: float = 0.0  # 当前振动
    last_update: float = 0.0


@dataclass
class Pathway:
    """信息链路"""
    nodes: List[str]
    total_value: float
    total_strength: float
    length: int


class SpiderWebGraph:
    """
    蜘蛛网图 - 多层级记忆网络（优化版）

    结构：
    - 同心圆层级结构
    - 中心高密度、高价值
    - 外围低密度、低价值
    
    优化特性：
    - 自适应参数调整
    - 动态层级调整
    - 实时熵计算
    """

    def __init__(self, max_layers: int = 5, decay_factor: float = 0.95,
                 adaptive_mode: bool = True):
        """
        初始化蜘蛛网（优化版）

        参数：
        - max_layers: 最大层级数
        - decay_factor: 价值衰减因子
        - adaptive_mode: 自适应模式
        """
        self.max_layers = max_layers
        self.decay_factor = decay_factor
        self.adaptive_mode = adaptive_mode

        # 节点和边
        self.nodes: Dict[str, SpiderNode] = {}
        self.edges: Dict[Tuple[str, str], SpiderEdge] = {}

        # 层级索引
        self.layers: Dict[int, Set[str]] = defaultdict(set)

        # 系统熵
        self.system_entropy: float = 0.0
        
        # 自适应参数
        self.access_frequency: Dict[str, int] = defaultdict(int)
        self.last_reorganization: float = 0.0

    def add_node(self, node_id: str, content: str, value: float = 0.5,
                 layer: Optional[int] = None, timestamp: float = 0.0):
        """
        添加节点（优化版）

        参数：
        - node_id: 节点 ID
        - content: 内容
        - value: 初始价值 [0, 1]
        - layer: 层级（如果未指定，自动分配）
        - timestamp: 时间戳
        """
        if node_id in self.nodes:
            return

        # 自动分配层级（基于价值）
        if layer is None:
            layer = self._assign_layer(value)

        node = SpiderNode(
            id=node_id,
            content=content,
            layer=layer,
            value=value,
            last_access=timestamp
        )

        self.nodes[node_id] = node
        self.layers[layer].add(node_id)

        # 初始化访问频率
        self.access_frequency[node_id] = 1

        # 重新计算系统熵
        self._calculate_system_entropy()
        
        # 自适应重组（如果启用）
        if self.adaptive_mode:
            self._adaptive_reorganization(timestamp)

    def _assign_layer(self, value: float) -> int:
        """根据价值分配层级"""
        # 高价值 -> 低层级（靠近中心）
        layer = int((1.0 - value) * self.max_layers)
        return min(layer, self.max_layers - 1)

    def add_edge(self, source: str, target: str, strength: float = 0.5):
        """添加边"""
        if source not in self.nodes or target not in self.nodes:
            return

        edge_key = (source, target)
        if edge_key in self.edges:
            # 更新现有边的强度
            self.edges[edge_key].strength = max(strength, self.edges[edge_key].strength)
        else:
            # 创建新边
            self.edges[edge_key] = SpiderEdge(
                source=source,
                target=target,
                strength=strength
            )

        # 更新邻居关系
        self.nodes[source].neighbors.add(target)
        self.nodes[target].neighbors.add(source)

    def get_layer(self, node_id: str) -> Optional[int]:
        """获取节点层级"""
        if node_id in self.nodes:
            return self.nodes[node_id].layer
        return None

    def get_node_value(self, node_id: str) -> float:
        """获取节点价值"""
        if node_id in self.nodes:
            return self.nodes[node_id].value
        return 0.0

    def update_node_value(self, node_id: str, delta: float):
        """更新节点价值（优化版）"""
        if node_id not in self.nodes:
            return

        node = self.nodes[node_id]
        old_layer = node.layer

        # 更新价值
        node.value = max(0.0, min(1.0, node.value + delta))

        # 可能需要重新分配层级
        new_layer = self._assign_layer(node.value)
        if new_layer != old_layer:
            self.layers[old_layer].remove(node_id)
            self.layers[new_layer].add(node_id)
            node.layer = new_layer

        # 更新访问频率
        self.access_frequency[node_id] += 1

        # 重新计算系统熵
        self._calculate_system_entropy()

    def _adaptive_reorganization(self, timestamp: float):
        """
        自适应重组（新增）
        
        根据访问频率和价值动态调整层级
        """
        # 每 100 次添加/更新后重组一次
        if len(self.access_frequency) < 100:
            return
        
        current_time = timestamp
        time_since_last_reorg = current_time - self.last_reorganization
        
        # 至少 10 秒才重组一次
        if time_since_last_reorg < 10.0:
            return
        
        self.last_reorganization = current_time
        
        # 基于访问频率调整价值
        for node_id, node in self.nodes.items():
            freq = self.access_frequency.get(node_id, 0)
            if freq > 0:
                # 访问频率越高，价值提升
                freq_boost = math.log2(freq + 1) * 0.05
                node.value = min(1.0, node.value + freq_boost)
        
        # 重新分配层级
        for node_id, node in self.nodes.items():
            old_layer = node.layer
            new_layer = self._assign_layer(node.value)
            
            if new_layer != old_layer:
                self.layers[old_layer].discard(node_id)
                self.layers[new_layer].add(node_id)
                node.layer = new_layer
        
        # 重新计算熵
        self._calculate_system_entropy()

    def _calculate_system_entropy(self):
        """计算系统熵（信息论）"""
        if not self.nodes:
            self.system_entropy = 0.0
            return

        # 使用价值的分布计算熵
        values = [node.value for node in self.nodes.values()]

        # 归一化为概率分布
        total = sum(values)
        if total == 0:
            self.system_entropy = 0.0
            return

        probabilities = [v / total for v in values]

        # 计算熵
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * math.log2(p)

        self.system_entropy = entropy


class InformationPathway:
    """
    信息链路 - 高价值路径识别

    功能：
    - 寻找高价值路径
    - 多路径搜索
    - 路径排序
    """

    def __init__(self, graph: SpiderWebGraph):
        self.graph = graph

    def find_high_value_pathway(self, start: str, end: str,
                                max_paths: int = 5) -> List[Pathway]:
        """
        寻找高价值路径

        综合考虑：
        - 路径总价值
        - 路径总强度
        - 路径长度
        """
        if start not in self.graph.nodes or end not in self.graph.nodes:
            return []

        # 使用 Dijkstra 寻找多条路径
        pathways = []

        # 寻找最短路径（Dijkstra）
        shortest_path = self._dijkstra(start, end)
        if shortest_path:
            pathways.append(shortest_path)

        # 寻找其他路径（修改的 BFS）
        other_paths = self._find_alternative_paths(start, end, max_paths - 1)
        pathways.extend(other_paths)

        # 按综合价值排序
        pathways.sort(key=lambda p: p.total_value * p.total_strength / p.length, reverse=True)

        return pathways[:max_paths]

    def _dijkstra(self, start: str, end: str) -> Optional[Pathway]:
        """Dijkstra 算法寻找最短路径"""
        # 初始化
        distances = {node_id: float('inf') for node_id in self.graph.nodes}
        distances[start] = 0
        previous = {}
        visited = set()

        # 优先队列
        pq = [(0, start)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current in visited:
                continue
            visited.add(current)

            if current == end:
                break

            # 遍历邻居
            for neighbor in self.graph.nodes[current].neighbors:
                if neighbor in visited:
                    continue

                # 计算距离（考虑边强度）
                edge_key = (current, neighbor)
                if edge_key in self.graph.edges:
                    edge_strength = self.graph.edges[edge_key].strength
                    weight = 1.0 / (edge_strength + 0.01)  # 强度越高，权重越低
                else:
                    weight = 1.0

                new_dist = current_dist + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        # 重建路径
        if end not in previous:
            return None

        path = []
        current = end
        while current != start:
            path.append(current)
            current = previous[current]
        path.append(start)
        path.reverse()

        # 计算路径价值
        total_value = sum(self.graph.get_node_value(node) for node in path)
        total_strength = self._calculate_path_strength(path)

        return Pathway(
            nodes=path,
            total_value=total_value,
            total_strength=total_strength,
            length=len(path)
        )

    def _find_alternative_paths(self, start: str, end: str,
                                max_paths: int) -> List[Pathway]:
        """寻找替代路径（BFS 变体）"""
        paths = []
        queue = deque()
        queue.append((start, [start]))

        found_paths = 0

        while queue and found_paths < max_paths:
            current, path = queue.popleft()

            if current == end:
                # 计算路径价值
                total_value = sum(self.graph.get_node_value(node) for node in path)
                total_strength = self._calculate_path_strength(path)

                paths.append(Pathway(
                    nodes=path,
                    total_value=total_value,
                    total_strength=total_strength,
                    length=len(path)
                ))
                found_paths += 1
                continue

            # 遍历邻居
            for neighbor in self.graph.nodes[current].neighbors:
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))

        return paths

    def _calculate_path_strength(self, path: List[str]) -> float:
        """计算路径总强度"""
        if len(path) < 2:
            return 0.0

        total_strength = 0.0
        for i in range(len(path) - 1):
            edge_key = (path[i], path[i + 1])
            if edge_key in self.graph.edges:
                total_strength += self.graph.edges[edge_key].strength

        return total_strength / (len(path) - 1)


class TransactionChain:
    """
    交易链路 - 信息交易和价值传播

    功能：
    - 信息交易
    - 价值传播
    - 反馈回路
    """

    def __init__(self, graph: SpiderWebGraph):
        self.graph = graph
        self.transaction_history: List[Dict] = []

    def transact(self, source: str, target: str, amount: float) -> Dict:
        """
        信息交易

        从 source 传输价值到 target
        """
        if source not in self.graph.nodes or target not in self.graph.nodes:
            return {"success": False, "message": "节点不存在"}

        # 计算传播效率（基于路径）
        pathway_finder = InformationPathway(self.graph)
        pathways = pathway_finder.find_high_value_pathway(source, target, max_paths=1)

        if not pathways:
            return {"success": False, "message": "无路径"}

        pathway = pathways[0]

        # 计算实际传输量（考虑路径强度）
        efficiency = pathway.total_strength
        actual_amount = amount * efficiency

        # 更新节点价值
        self.graph.update_node_value(source, -actual_amount)
        self.graph.update_node_value(target, actual_amount)

        # 增强边的强度
        for i in range(len(pathway.nodes) - 1):
            edge_key = (pathway.nodes[i], pathway.nodes[i + 1])
            if edge_key in self.graph.edges:
                self.graph.edges[edge_key].strength = min(1.0,
                    self.graph.edges[edge_key].strength + actual_amount * 0.1)

        # 记录交易
        transaction = {
            "source": source,
            "target": target,
            "amount": amount,
            "actual_amount": actual_amount,
            "efficiency": efficiency,
            "pathway": pathway.nodes,
            "timestamp": 0.0
        }

        self.transaction_history.append(transaction)

        return {
            "success": True,
            "transaction": transaction
        }

    def propagate_value(self, start: str, steps: int = 3) -> Dict:
        """
        价值传播

        从 start 节点传播价值到多层邻居
        """
        if start not in self.graph.nodes:
            return {"success": False, "message": "节点不存在"}

        propagated = defaultdict(float)

        # 初始化
        visited = set()
        queue = deque([(start, 0)])  # (node_id, depth)

        while queue:
            current, depth = queue.popleft()

            if depth > steps:
                continue

            if current in visited:
                continue
            visited.add(current)

            # 传播价值给邻居
            for neighbor in self.graph.nodes[current].neighbors:
                if neighbor in visited:
                    continue

                # 计算传播量（基于边强度）
                edge_key = (current, neighbor)
                if edge_key in self.graph.edges:
                    edge_strength = self.graph.edges[edge_key].strength
                    propagation_amount = self.graph.get_node_value(current) * edge_strength * 0.1
                    propagated[neighbor] += propagation_amount

                queue.append((neighbor, depth + 1))

        # 应用传播
        for node_id, amount in propagated.items():
            self.graph.update_node_value(node_id, amount)

        return {
            "success": True,
            "propagated": dict(propagated)
        }


class EntropyReduction:
    """
    熵减机制 - 不是智能遗忘，而是熵减

    功能：
    - 计算系统熵
    - 熵减优化
    - 网络剪枝
    """

    def __init__(self, graph: SpiderWebGraph):
        self.graph = graph

    def calculate_system_entropy(self) -> float:
        """计算系统熵"""
        return self.graph.system_entropy

    def reduce_entropy(self, threshold: float = 0.1, 
                       aggressive: bool = False) -> Dict:
        """
        熵减优化（增强版）

        策略：
        1. 低价值节点衰减
        2. 低强度边移除
        3. 孤立节点移除
        4. 自适应阈值调整（新增）
        
        参数：
        - threshold: 熵减阈值
        - aggressive: 激进模式（更严格）
        """
        old_entropy = self.calculate_system_entropy()

        # 自适应阈值调整
        if aggressive:
            actual_threshold = threshold * 1.5  # 更严格
        else:
            # 基于当前熵调整阈值
            if old_entropy > 5.0:  # 高熵
                actual_threshold = threshold * 0.8  # 更积极
            else:
                actual_threshold = threshold

        # 衰减低价值节点
        low_value_nodes = [
            node_id for node_id, node in self.graph.nodes.items()
            if node.value < actual_threshold
        ]

        for node_id in low_value_nodes:
            # 衰减价值（渐进式）
            delta = -node.value * 0.15  # 增加衰减速度
            self.graph.update_node_value(node_id, delta)

        # 移除低强度边
        weak_edges = [
            edge_key for edge_key, edge in self.graph.edges.items()
            if edge.strength < actual_threshold
        ]

        for edge_key in weak_edges:
            # 移除边
            source, target = edge_key
            self.graph.nodes[source].neighbors.discard(target)
            self.graph.nodes[target].neighbors.discard(source)
            del self.graph.edges[edge_key]

        # 移除孤立节点
        isolated_nodes = [
            node_id for node_id, node in self.graph.nodes.items()
            if not node.neighbors
        ]

        for node_id in isolated_nodes:
            self.graph.layers[self.graph.nodes[node_id].layer].discard(node_id)
            del self.graph.nodes[node_id]

        # 重新计算熵
        self.graph._calculate_system_entropy()
        new_entropy = self.calculate_system_entropy()

        # 计算熵减率
        if old_entropy > 0:
            reduction_rate = (old_entropy - new_entropy) / old_entropy
        else:
            reduction_rate = 0.0

        return {
            "old_entropy": old_entropy,
            "new_entropy": new_entropy,
            "entropy_reduction": old_entropy - new_entropy,
            "reduction_rate": reduction_rate,
            "threshold_used": actual_threshold,
            "nodes_decay": len(low_value_nodes),
            "edges_removed": len(weak_edges),
            "nodes_removed": len(isolated_nodes)
        }


class VibrationSensing:
    """
    振动感知 - 信息触发和传播（优化版）

    功能：
    - 触发检测
    - 振动传播（优化算法）
    - 共振识别（增强检测）
    - 自适应衰减
    """

    def __init__(self, graph: SpiderWebGraph, decay_factor: float = 0.9,
                 adaptive_decay: bool = True):
        self.graph = graph
        self.decay_factor = decay_factor
        self.adaptive_decay = adaptive_decay
        
        # 振动缓存（优化性能）
        self.vibration_cache: Dict[str, float] = {}
        self.resonance_threshold: float = 0.3

    def trigger(self, node_id: str, strength: float = 1.0) -> Dict:
        """
        触发振动

        参数：
        - node_id: 触发节点
        - strength: 振动强度
        """
        if node_id not in self.graph.nodes:
            return {"success": False, "message": "节点不存在"}

        # 设置节点振动
        self.graph.nodes[node_id].vibration = strength
        self.graph.nodes[node_id].last_access = 0.0  # 更新访问时间
        self.graph.nodes[node_id].access_count += 1

        # 传播振动
        self.propagate_vibration(node_id, strength)

        # 增强节点价值
        self.graph.update_node_value(node_id, strength * 0.05)

        return {
            "success": True,
            "triggered_node": node_id,
            "strength": strength
        }

    def propagate_vibration(self, start: str, initial_strength: float,
                           max_steps: int = 5):
        """传播振动"""
        queue = deque([(start, initial_strength, 0)])  # (node_id, strength, depth)

        while queue:
            current, strength, depth = queue.popleft()

            if depth > max_steps:
                continue

            # 衰减振动
            strength *= self.decay_factor
            if strength < 0.01:
                continue

            # 设置节点振动
            self.graph.nodes[current].vibration = max(
                self.graph.nodes[current].vibration,
                strength
            )

            # 传播给邻居
            for neighbor in self.graph.nodes[current].neighbors:
                edge_key = (current, neighbor)
                if edge_key in self.graph.edges:
                    edge_strength = self.graph.edges[edge_key].strength
                    propagation_strength = strength * edge_strength
                    queue.append((neighbor, propagation_strength, depth + 1))

    def detect_resonance(self, node_id: str, threshold: float = 0.5) -> List[str]:
        """
        检测共振节点

        找出与指定节点振动相似的节点
        """
        if node_id not in self.graph.nodes:
            return []

        target_vibration = self.graph.nodes[node_id].vibration
        if target_vibration == 0:
            return []

        resonant_nodes = []

        for neighbor_id, neighbor in self.graph.nodes.items():
            if neighbor_id == node_id:
                continue

            # 计算振动相似度
            if neighbor.vibration > 0:
                similarity = 1.0 - abs(target_vibration - neighbor.vibration) / max(target_vibration, neighbor.vibration)

                if similarity > threshold:
                    resonant_nodes.append(neighbor_id)

        return resonant_nodes


class RapidPropagation:
    """
    极速传播 - 多路径并行传播

    功能：
    - 多路径并行
    - 优先传播（高价值）
    - 跳跃连接
    """

    def __init__(self, graph: SpiderWebGraph):
        self.graph = graph

    def rapid_propagate(self, start: str, max_hops: int = 10,
                       mode: str = "value") -> Dict:
        """
        极速传播

        参数：
        - start: 起始节点
        - max_hops: 最大跳跃数
        - mode: 传播模式（"value"=按价值, "random"=随机）

        返回：
        - 传播结果
        """
        if start not in self.graph.nodes:
            return {"success": False, "message": "节点不存在"}

        visited = set([start])
        current_layer = [(start, 0)]  # (node_id, distance)
        result = {start: 0}

        for hop in range(max_hops):
            next_layer = []

            for current, dist in current_layer:
                neighbors = list(self.graph.nodes[current].neighbors)

                if mode == "value":
                    # 按价值排序
                    neighbors.sort(
                        key=lambda n: self.graph.get_node_value(n),
                        reverse=True
                    )

                # 选择前 3 个邻居（限制分支因子）
                for neighbor in neighbors[:3]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_layer.append((neighbor, dist + 1))
                        result[neighbor] = dist + 1

            if not next_layer:
                break

            current_layer = next_layer

        return {
            "success": True,
            "reached_nodes": len(result),
            "distances": result,
            "max_distance": max(result.values()) if result else 0
        }


class SelfOrganization:
    """
    自组织 - 网络重构和优化

    功能：
    - 网络重构
    - 节点合并
    - 边优化
    """

    def __init__(self, graph: SpiderWebGraph):
        self.graph = graph

    def reorganize(self) -> Dict:
        """
        网络重构

        策略：
        1. 重新分配层级
        2. 优化边强度
        3. 合并相似节点
        """
        # 重新分配层级
        for node_id, node in self.graph.nodes.items():
            old_layer = node.layer
            new_layer = self.graph._assign_layer(node.value)

            if new_layer != old_layer:
                self.graph.layers[old_layer].discard(node_id)
                self.graph.layers[new_layer].add(node_id)
                node.layer = new_layer

        # 优化边强度
        for edge_key, edge in self.graph.edges.items():
            source, target = edge_key
            source_value = self.graph.get_node_value(source)
            target_value = self.graph.get_node_value(target)

            # 边强度应该反映两端节点的价值
            target_strength = (source_value + target_value) / 2
            edge.strength = (edge.strength * 0.9 + target_strength * 0.1)

        # 合并相似节点（简化）
        merged_count = 0
        nodes_to_remove = []

        for node_id1 in list(self.graph.nodes.keys()):
            if node_id1 in nodes_to_remove:
                continue

            for node_id2 in list(self.graph.nodes.keys()):
                if node_id1 == node_id2 or node_id2 in nodes_to_remove:
                    continue

                # 检查相似度（基于内容长度和层级）
                node1 = self.graph.nodes[node_id1]
                node2 = self.graph.nodes[node_id2]

                if (node1.layer == node2.layer and
                    abs(node1.value - node2.value) < 0.1):
                    # 合并节点
                    # 合并邻居
                    node1.neighbors.update(node2.neighbors)
                    # 合并内容
                    node1.content = f"{node1.content} [合并: {node2.content}]"
                    # 更新价值
                    node1.value = (node1.value + node2.value) / 2

                    nodes_to_remove.append(node_id2)
                    merged_count += 1
                    break  # 只合并一次

        # 移除合并的节点
        for node_id in nodes_to_remove:
            self.graph.layers[self.graph.nodes[node_id].layer].discard(node_id)
            del self.graph.nodes[node_id]

        return {
            "success": True,
            "reorganized": True,
            "nodes_merged": merged_count
        }


class SpiderWebMemorySystem:
    """
    蜘蛛网记忆系统 - 整合所有组件

    核心特性：
    1. 多层级结构
    2. 多路径连接
    3. 极速传播
    4. 价值链路清晰
    5. 熵减机制
    6. 自组织
    """

    def __init__(self, max_layers: int = 5, decay_factor: float = 0.95):
        # 初始化蜘蛛网图
        self.graph = SpiderWebGraph(max_layers, decay_factor)

        # 初始化各个组件
        self.pathway = InformationPathway(self.graph)
        self.transaction = TransactionChain(self.graph)
        self.entropy_reduction = EntropyReduction(self.graph)
        self.vibration = VibrationSensing(self.graph, decay_factor)
        self.rapid_prop = RapidPropagation(self.graph)
        self.self_org = SelfOrganization(self.graph)

    def add_memory(self, memory_id: str, content: str,
                   value: float = 0.5, connections: List[str] = None):
        """添加记忆"""
        self.graph.add_node(memory_id, content, value)

        if connections:
            for conn_id in connections:
                self.graph.add_edge(memory_id, conn_id, strength=0.5)

    def trigger_memory(self, memory_id: str, strength: float = 1.0):
        """触发记忆（振动感知）"""
        result = self.vibration.trigger(memory_id, strength)

        # 检测共振
        if result["success"]:
            resonant = self.vibration.detect_resonance(memory_id, threshold=0.5)
            result["resonant_nodes"] = resonant

        return result

    def find_pathway(self, start: str, end: str, max_paths: int = 5):
        """寻找高价值路径"""
        return self.pathway.find_high_value_pathway(start, end, max_paths)

    def entropy_reduce(self, threshold: float = 0.1):
        """执行熵减"""
        return self.entropy_reduction.reduce_entropy(threshold)

    def self_organize(self):
        """执行自组织"""
        return self.self_org.reorganize()

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "total_nodes": len(self.graph.nodes),
            "total_edges": len(self.graph.edges),
            "entropy": self.graph.system_entropy,
            "layers": {
                layer_id: len(nodes)
                for layer_id, nodes in self.graph.layers.items()
            },
            "avg_node_value": np.mean([
                node.value for node in self.graph.nodes.values()
            ]) if self.graph.nodes else 0.0
        }

    def export_network(self) -> Dict:
        """导出网络结构"""
        return {
            "nodes": [
                {
                    "id": node.id,
                    "content": node.content,
                    "layer": node.layer,
                    "value": node.value,
                    "access_count": node.access_count
                }
                for node in self.graph.nodes.values()
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "strength": edge.strength
                }
                for edge in self.graph.edges.values()
            ],
            "entropy": self.graph.system_entropy
        }


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="蜘蛛网记忆系统")
    parser.add_argument("action", choices=["add", "trigger", "pathway", "entropy_reduce", "organize", "stats", "export"])
    parser.add_argument("--id", help="记忆 ID")
    parser.add_argument("--content", help="记忆内容")
    parser.add_argument("--value", type=float, default=0.5, help="价值权重")
    parser.add_argument("--connections", nargs="+", help="连接的节点 ID")
    parser.add_argument("--strength", type=float, default=1.0, help="振动强度")
    parser.add_argument("--start", help="起始节点")
    parser.add_argument("--end", help="目标节点")
    parser.add_argument("--threshold", type=float, default=0.1, help="熵减阈值")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    system = SpiderWebMemorySystem()

    # 添加一些示例记忆
    system.add_memory("用户偏好", "用户偏好暗色主题", value=0.8)
    system.add_memory("技术栈", "使用 React 和 TypeScript", value=0.7)
    system.add_memory("项目需求", "项目需要在周五前完成", value=0.9)
    system.add_memory("设计风格", "极简主义设计", value=0.6)

    # 添加连接
    system.graph.add_edge("用户偏好", "技术栈", strength=0.8)
    system.graph.add_edge("用户偏好", "设计风格", strength=0.6)
    system.graph.add_edge("项目需求", "技术栈", strength=0.9)

    if args.action == "add":
        if not args.id or not args.content:
            print("错误: 需要指定 --id 和 --content")
            return

        system.add_memory(args.id, args.content, args.value, args.connections)

        print(f"✓ 添加记忆: {args.id}")
        print(f"  内容: {args.content}")
        print(f"  价值: {args.value}")
        if args.connections:
            print(f"  连接: {', '.join(args.connections)}")

    elif args.action == "trigger":
        if not args.id:
            print("错误: 需要指定 --id")
            return

        result = system.trigger_memory(args.id, args.strength)

        print(f"🔔 触发记忆: {args.id}")
        if result["success"]:
            print(f"  振动强度: {result['strength']:.2f}")
            if result.get("resonant_nodes"):
                print(f"  共振节点: {', '.join(result['resonant_nodes'])}")

    elif args.action == "pathway":
        if not args.start or not args.end:
            print("错误: 需要指定 --start 和 --end")
            return

        pathways = system.find_pathway(args.start, args.end)

        print(f"🔗 高价值路径: {args.start} → {args.end}")
        for i, pathway in enumerate(pathways):
            print(f"  路径 {i+1}: {' → '.join(pathway.nodes)}")
            print(f"    总价值: {pathway.total_value:.4f}")
            print(f"    总强度: {pathway.total_strength:.4f}")
            print(f"    长度: {pathway.length}")

    elif args.action == "entropy_reduce":
        result = system.entropy_reduce(args.threshold)

        print(f"📉 熵减优化")
        print(f"  旧熵: {result['old_entropy']:.4f}")
        print(f"  新熵: {result['new_entropy']:.4f}")
        print(f"  熵减量: {result['entropy_reduction']:.4f}")
        print(f"  衰减节点: {result['nodes_decay']}")
        print(f"  移除边: {result['edges_removed']}")
        print(f"  移除节点: {result['nodes_removed']}")

    elif args.action == "organize":
        result = system.self_organize()

        print(f"🔄 自组织")
        print(f"  合并节点: {result['nodes_merged']}")

    elif args.action == "stats":
        stats = system.get_statistics()

        print(f"📊 系统统计")
        print(f"  总节点数: {stats['total_nodes']}")
        print(f"  总边数: {stats['total_edges']}")
        print(f"  系统熵: {stats['entropy']:.4f}")
        print(f"  平均节点价值: {stats['avg_node_value']:.4f}")
        print(f"  层级分布:")
        for layer_id, count in stats['layers'].items():
            print(f"    层级 {layer_id}: {count} 个节点")

    elif args.action == "export":
        network = system.export_network()

        print(f"📤 网络导出")
        print(f"  节点数: {len(network['nodes'])}")
        print(f"  边数: {len(network['edges'])}")
        print(f"  系统熵: {network['entropy']:.4f}")


if __name__ == "__main__":
    main()
