# -*- coding: utf-8 -*-
"""流路分析（Flow Path Analysis）。

职责
----
回答一个纯粹的**拓扑问题**：在当前工况下，泵能不能把水送到某个负载？
如果能，走的是哪条路？

这一层**不做任何物理计算** —— 不看压力、不算流量。它只关心"通不通"、
"怎么走"。所有涉及数值的判定都在 :mod:`fluid_network.reliability` 里。

四条能力
--------
1. 按 :class:`~fluid_network.models.Scenario` 应用阀门开关状态（在
   :mod:`fluid_network.topology` 里完成，关闭的阀门从图中移除）。
2. 构建当前工况下的有效拓扑。
3. 判断泵到每个负载是否可达，可达则给出完整流路。
4. 对不可达的负载，指出**是哪一只阀门把它切断的** —— 只给"失败"没有
   诊断价值，能定位到具体元件才是可用的分析。
"""

from __future__ import annotations

from collections import deque
from typing import Mapping

from .models import Network, PathResult, Scenario
from .topology import Topology, build_adjacency, build_edges, build_topology

__all__ = ["FlowPathAnalyzer"]

_ALL_OPEN = Scenario(id="__all_open__", name="阀门全开（仅用于切断点定位）")


class FlowPathAnalyzer:
    """构建工况拓扑并分析泵到各负载的流路。"""

    def build(self, network: Network, scenario: Scenario) -> Topology:
        """构建当前工况下的有效拓扑。

        含环 / 平行冗余通路时抛 :class:`~fluid_network.topology.TopologyViolation`，
        调用方可以据此把负载标成 ``UNSUPPORTED``。
        """
        return build_topology(network, scenario)

    # ------------------------------------------------------------------ #
    def analyze(
        self,
        network: Network,
        scenario: Scenario,
        topology: Topology | None = None,
    ) -> dict[str, PathResult]:
        """为网络里的每个负载产出流路分析结果。

        ``topology`` 可由调用方传入 —— 求解器与分析层需要**同一个**拓扑视图，
        重复构建既浪费又可能产生不一致。不传则在这里自行构建（等价于
        ``normal`` 之外的场景，或单独使用本分析器时）。
        """
        if topology is None:
            topology = self.build(network, scenario)

        closed_valves = self.closed_valve_ids(network, scenario)
        reachable_nodes = topology.reachable
        full_adjacency = build_adjacency((n.id for n in network.nodes), build_edges(network, _ALL_OPEN))

        results: dict[str, PathResult] = {}
        for load in network.loads:
            results[load.id] = self._analyze_load(
                load.id, topology, closed_valves, reachable_nodes, full_adjacency
            )
        return results

    # ------------------------------------------------------------------ #
    @staticmethod
    def closed_valve_ids(network: Network, scenario: Scenario) -> tuple[str, ...]:
        """当前工况下处于关闭状态的阀门 id。"""
        return tuple(v.id for v in network.valves if not scenario.valve_open(v.id))

    @staticmethod
    def _analyze_load(
        load_id: str,
        topology: Topology,
        closed_valves: tuple[str, ...],
        reachable_nodes: set[str],
        full_adjacency: Mapping[str, list],
    ) -> PathResult:
        edges = topology.path_to(load_id)

        if edges is not None:
            node_path = topology.node_path_to(load_id) or []
            return PathResult(
                load_id=load_id,
                reachable=True,
                path=tuple(edge.id for edge in edges),
                node_path=tuple(node_path),
                reason=f"从泵到 '{load_id}' 存在有效流路，共 {len(edges)} 个元件",
            )

        # -- 不可达：定位是哪只阀门切断的 ----------------------------- #
        isolation_point = _find_isolation_point(load_id, reachable_nodes, full_adjacency, closed_valves)
        if isolation_point is not None:
            reason = (
                f"负载 '{load_id}' 不可达：阀门 '{isolation_point}' 处于关闭状态，"
                "该流路已从计算中移除"
            )
        elif closed_valves:
            reason = (
                f"负载 '{load_id}' 不可达；当前工况关闭的阀门为 "
                f"{', '.join(closed_valves)}，但未定位到直接切断点"
            )
        else:
            reason = f"负载 '{load_id}' 不可达：网络中没有从泵通往它的通路"

        return PathResult(
            load_id=load_id,
            reachable=False,
            isolation_point=isolation_point,
            reason=reason,
        )


def _find_isolation_point(
    load_id: str,
    reachable_nodes: set[str],
    full_adjacency: Mapping[str, list],
    closed_valves: tuple[str, ...],
) -> str | None:
    """定位把 ``load_id`` 从泵侧切断的那只阀门。

    做法：在**阀门开关被忽略的完整图**上，从负载出发做 BFS 到第一个可达
    节点为止，沿途见到的第一只已关闭阀门就是切断点。

    之所以不能在工况拓扑上找：关闭的阀门已经被移除了，图上根本看不到它，
    只能看到"路突然断了"。必须回到完整图才能指出断在哪。
    """
    if not closed_valves:
        return None

    closed = set(closed_valves)
    visited = {load_id}
    queue: deque[str] = deque([load_id])

    while queue:
        node_id = queue.popleft()
        for neighbour, edge in full_adjacency.get(node_id, ()):
            if edge.id in closed:
                # 这只阀门就在"不可达区域 -> 已连通区域"的边界上
                if neighbour in reachable_nodes:
                    return edge.id
                continue
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return None
