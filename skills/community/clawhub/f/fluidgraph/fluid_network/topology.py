# -*- coding: utf-8 -*-
"""网络拓扑：建图、建树、以及"能否确定性求解"的判定。

这一层被 :mod:`fluid_network.solver`（求解）与 :mod:`fluid_network.paths`
（流路分析）共用 —— 两者都必须先按工况把阀门展开成图，再以泵为根建树。
把它单独抽出来，是为了让"支持什么拓扑"这个判断只有一处实现。

一阶段能确定性求解的网络
------------------------
**以泵为根的树**：可见元件每条都是割边。此时

    Q(e) = 下游子树内全部负载需求之和

是节点流量守恒 ``ΣQ_in = ΣQ_out`` 的直接推论，不需要迭代。

一旦出现环 —— 闭环绕流、平行冗余通路、同一对节点上的重边 —— 环上各支路
"该分多少流量"就必须联立方程求解。此时 :func:`build_topology` 会抛
:class:`~fluid_network.exceptions.TopologyError`；如果只想探测、不想抛异常，
用 :func:`fluid_network.topology.has_cycle` 或捕获异常后用
:func:`TopologySummary.from_error` 记录。
"""

from __future__ import annotations

import math
from collections import deque
from typing import Iterable, Mapping

from .exceptions import TopologyError
from .models import Network, Scenario

__all__ = [
    "DirectedEdge",
    "Topology",
    "TopologyViolation",
    "build_edges",
    "build_adjacency",
    "build_topology",
    "has_cycle",
]


class DirectedEdge:
    """求解 / 分析过程中使用的"定向元件"表示。

    命名的历史包袱：这里的 ``node_a`` / ``node_b`` 在 :class:`Topology` 建好之前
    只是元件在 TOML 里的**书写顺序**，不代表真实流向。建树之后，
    ``node_a`` 才是上游端、``node_b`` 才是下游端。
    """

    __slots__ = ("element", "node_a", "node_b", "is_pipe", "active")

    def __init__(self, element, node_a: str, node_b: str, is_pipe: bool, active: bool = True) -> None:
        self.element = element      # Pipe | Valve
        self.node_a = node_a        # 上游端（建树后确定）
        self.node_b = node_b        # 下游端（建树后确定）
        self.is_pipe = is_pipe
        self.active = active

    @property
    def id(self) -> str:
        return self.element.id

    @property
    def kind(self) -> str:
        return "pipe" if self.is_pipe else "valve"

    @property
    def resistance(self) -> float:
        """流阻 R。理想阀为 0。"""
        return self.element.resistance if self.is_pipe else 0.0

    def area(self) -> float:
        return self.element.area if self.is_pipe else math.nan

    def other(self, node_id: str) -> str:
        """给定一端，返回另一端。"""
        return self.node_b if node_id == self.node_a else self.node_a

    def __repr__(self) -> str:  # pragma: no cover - 仅调试用
        return f"<{self.kind} {self.id} {self.node_a}->{self.node_b}>"


class Topology:
    """以泵为根展开出的树状拓扑。"""

    __slots__ = ("root", "parent_edge", "children", "order", "edges", "adjacency", "node_ids")

    def __init__(
        self,
        root: str,
        parent_edge: dict[str, DirectedEdge],
        children: dict[str, list[tuple[str, DirectedEdge]]],
        order: list[str],
        edges: list[DirectedEdge],
        adjacency: dict[str, list[tuple[str, DirectedEdge]]],
        node_ids: list[str],
    ) -> None:
        self.root = root                        # 泵节点 id
        self.parent_edge = parent_edge          # node -> 父边（根没有）
        self.children = children                # node -> [(子节点, 边), ...]
        self.order = order                      # BFS 顺序（即自顶向下）
        self.edges = edges                      # 全部可见元件
        self.adjacency = adjacency              # node -> [(邻居, 边), ...]
        self.node_ids = node_ids                # 网络里的全部节点 id

    @property
    def reachable(self) -> set[str]:
        """从泵出发可达的节点集合。"""
        return set(self.order)

    @property
    def isolated(self) -> list[str]:
        """从泵出发不可达的节点（多半是被关闭的阀门切断）。"""
        return [n for n in self.node_ids if n not in self.parent_edge and n != self.root]

    def edge(self, element_id: str) -> DirectedEdge:
        for edge in self.edges:
            if edge.id == element_id:
                return edge
        raise KeyError(element_id)

    def path_to(self, node_id: str) -> list[DirectedEdge] | None:
        """返回 泵 → node 路径上的元件序列；不可达则返回 ``None``。"""
        if node_id != self.root and node_id not in self.parent_edge:
            return None
        chain: list[DirectedEdge] = []
        cursor = node_id
        while cursor != self.root:
            edge = self.parent_edge[cursor]
            chain.append(edge)
            cursor = edge.other(cursor)
        chain.reverse()   # 从泵端到负载端
        return chain

    def node_path_to(self, node_id: str) -> list[str] | None:
        """返回 泵 → node 的节点序列（含首尾）；不可达则返回 ``None``。"""
        edges = self.path_to(node_id)
        if edges is None:
            return None
        nodes = [self.root]
        for edge in edges:
            nodes.append(edge.other(nodes[-1]))
        return nodes


class TopologyViolation(TopologyError):
    """拓扑在一阶段模型下不可求解（含环 / 平行冗余通路）。

    单独建模是为了让上层能**区分**"拓扑不支持"与"其它求解错误" ——
    分析层据此把负载标成 ``UNSUPPORTED`` 而不是笼统地失败。
    """

    def __init__(self, message: str, offending_elements: Iterable[str] = ()) -> None:
        self.offending_elements = tuple(sorted(offending_elements))
        super().__init__(message)


# --------------------------------------------------------------------------- #
# 建图
# --------------------------------------------------------------------------- #
def build_edges(network: Network, scenario: Scenario) -> list[DirectedEdge]:
    """按工况把管路与阀门展开成无向边。

    关闭的阀门**直接从图中移除** —— 它的下游元件因此自然变成不可达，
    这正是"阀门关闭"的语义。
    """
    edges: list[DirectedEdge] = []
    for pipe in network.pipes:
        edges.append(DirectedEdge(pipe, pipe.from_node, pipe.to_node, is_pipe=True))
    for valve in network.valves:
        if not scenario.valve_open(valve.id):
            continue
        edges.append(DirectedEdge(valve, valve.from_node, valve.to_node, is_pipe=False))
    return edges


def build_adjacency(
    node_ids: Iterable[str], edges: Iterable[DirectedEdge]
) -> dict[str, list[tuple[str, DirectedEdge]]]:
    adjacency: dict[str, list[tuple[str, DirectedEdge]]] = {n: [] for n in node_ids}
    for edge in edges:
        adjacency[edge.node_a].append((edge.node_b, edge))
        adjacency[edge.node_b].append((edge.node_a, edge))
    return adjacency


# --------------------------------------------------------------------------- #
# 环检测（Tarjan 桥检测）
# --------------------------------------------------------------------------- #
def _find_non_bridge(nodes: set[str], edges: list[DirectedEdge]) -> set[str]:
    """返回**可达子图**中所有"不是割边（桥）"的元件 id。

    无向图里，"每条边都是桥"等价于"图上没有环"，也就是**可达部分是一棵树**。
    这恰好是本阶段求解器能确定性求解的充要条件。

    实现用 Tarjan 的桥检测（DFS + ``disc``/``low``）。两个容易踩的点：

    1. **必须按"边的序号"而不是"父节点"跳过回路**，否则同一对节点之间的
       重边会被误判成树边，两条都逃过检测。
    2. **不可达的元件不能进入判定**：它们不在从泵出发的子图里，DFS 根本不会
       遍历到，若不过滤就会被当成"非割边"而误报。这些元件本来就不参与计算，
       不属于"拓扑不支持"的范畴。
    """
    # 只保留两端都可达的元件
    active = [edge for edge in edges if edge.node_a in nodes and edge.node_b in nodes]

    adjacency: dict[str, list[tuple[str, int]]] = {}
    for index, edge in enumerate(active):
        adjacency.setdefault(edge.node_a, []).append((edge.node_b, index))
        adjacency.setdefault(edge.node_b, []).append((edge.node_a, index))

    disc: dict[str, int] = {}
    low: dict[str, int] = {}
    bridge_indices: set[int] = set()
    timer = 0

    for start in nodes:
        if start in disc or start not in adjacency:
            continue
        # 迭代式 DFS，避免深网络下递归爆栈。栈元素：(节点, 入边序号, 子边游标)
        disc[start] = low[start] = timer
        timer += 1
        stack: list[tuple[str, int, int]] = [(start, -1, 0)]

        while stack:
            node, in_edge, cursor = stack.pop()
            neighbours = adjacency[node]

            if cursor < len(neighbours):
                stack.append((node, in_edge, cursor + 1))
                neighbour, edge_index = neighbours[cursor]
                if edge_index == in_edge:
                    continue  # 沿同一条边回去
                if neighbour in disc:
                    low[node] = min(low[node], disc[neighbour])   # 回边
                else:
                    disc[neighbour] = low[neighbour] = timer
                    timer += 1
                    stack.append((neighbour, edge_index, 0))
                continue

            # 子树遍历完毕，回溯更新父节点的 low 并判定桥
            if in_edge != -1:
                parent_edge = active[in_edge]
                parent = parent_edge.node_b if parent_edge.node_a == node else parent_edge.node_a
                low[parent] = min(low[parent], low[node])
                if low[node] > disc[parent]:
                    bridge_indices.add(in_edge)

    return {edge.id for index, edge in enumerate(active) if index not in bridge_indices}


def has_cycle(network: Network, scenario: Scenario) -> tuple[bool, set[str]]:
    """探测工况展开后的可达子图是否含环。

    返回 ``(是否含环, 位于环上的元件 id 集合)``。**不抛异常**，
    也不做可达性 BFS —— 供分析层在求解失败后描述"为什么不支持"。
    """
    try:
        root = network.pump.id
    except TopologyError:
        # 没有唯一的泵 —— 这本身也是一种拓扑不支持，交由调用方处理。
        return False, set()

    edges = build_edges(network, scenario)
    adjacency = build_adjacency((n.id for n in network.nodes), edges)

    visited = {root}
    queue: deque[str] = deque([root])
    while queue:
        node_id = queue.popleft()
        for neighbour, _ in adjacency[node_id]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    if len(visited) == len(network.nodes):
        return False, set()   # 泵到不了任何别处
    offending = _find_non_bridge(visited, edges)
    return bool(offending), offending


# --------------------------------------------------------------------------- #
# 建树
# --------------------------------------------------------------------------- #
def build_topology(network: Network, scenario: Scenario) -> Topology:
    """按工况展开网络，以泵为根建树，并校验拓扑可解。

    抛出的异常都是 :class:`~fluid_network.exceptions.TopologyError` 的子类，
    其中"含环 / 平行冗余通路"是 :class:`TopologyViolation`。
    """
    pump = network.pump   # 无泵 / 多泵在这里抛 TopologyError
    node_ids = [n.id for n in network.nodes]

    edges = build_edges(network, scenario)
    if not edges:
        raise TopologyError("网络中没有任何可参与计算的管路或阀门")

    adjacency = build_adjacency(node_ids, edges)

    # -- 以泵为根 BFS，建树 ------------------------------------------ #
    parent_edge: dict[str, DirectedEdge] = {}
    children: dict[str, list[tuple[str, DirectedEdge]]] = {n: [] for n in node_ids}
    visited: set[str] = {pump.id}
    order: list[str] = []
    queue: deque[str] = deque([pump.id])

    while queue:
        node_id = queue.popleft()
        order.append(node_id)
        for neighbour, edge in adjacency[node_id]:
            if neighbour not in visited:
                visited.add(neighbour)
                # 统一朝向：让 node_a 指向上游、node_b 指向下游
                if edge.node_a != node_id:
                    edge.node_a, edge.node_b = edge.node_b, edge.node_a
                parent_edge[neighbour] = edge
                children[node_id].append((neighbour, edge))
                queue.append(neighbour)

    if len(visited) == len(network.nodes) == 1 or not order:
        raise TopologyError("从泵出发无法到达任何节点，请检查网络连接")

    # -- 拓扑可行性判定 ---------------------------------------------- #
    # 求解依赖一条关键性质：**每条边的流量 = 它下游全部负载需求之和**。
    # 这条性质在且仅在**可达子图是一棵树**时成立（树上的每条边都是割边，
    # 下游那半的水只能靠它送）。
    #
    # 一旦出现环（闭环绕流、平行冗余通路、同一对节点上的重边），情况就变了：
    #   * 闭环绕流 A→B→C→A —— 环上每条边都不再是割边；
    #   * P1→L1 与 P1→J1→L1 —— 给 L1 送水的通路不止一条，
    #     串联路径上各段流量相等，但"两段各占多少需求之和"是未知的；
    #   * 同一对节点之间的两根管 —— 两管互为备份。
    # 这三者的共同点是：环上各边该分多少流量需要联立方程求解，已经超出了
    # "自底向上累加需求"能给出的信息。直接拒绝，而不是给一个错误结果。
    #
    # 注意 P1→J1→{L1, L2} 这种并联分支**不是环**：J1→L1 与 J1→L2 是两条
    # 互不相交的通路，各自都是割边，正常求解。
    offending = _find_non_bridge(visited, edges)
    if offending:
        ids = ", ".join(sorted(offending))
        raise TopologyViolation(
            f"检测到非树状拓扑：元件 {ids} 位于环上（网络中存在回路或平行冗余通路），"
            "环上各支路的分流量需要联立方程迭代求解；"
            "当前模型只支持树状（串联/并联）网络，暂不支持该结构",
            offending,
        )

    return Topology(pump.id, parent_edge, children, order, edges, adjacency, node_ids)
