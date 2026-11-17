# -*- coding: utf-8 -*-
"""基础稳态求解器。

算法
----
可求解的网络是一棵以泵为根的**树**（串联链路 + 并联支路），每条元件都是
割边。这类网络的求解是确定性的，不需要牛顿迭代：

1. **展开 + 建树** —— 见 :mod:`fluid_network.topology`。按工况决定阀门通断，
   以泵为根 BFS，并用 Tarjan 桥检测确认可达子图确实是树。
2. **自底向上求流量**：``Q(e) = 下游子树中全部负载的目标需求之和``。
   这是节点流量守恒 ``ΣQ_in = ΣQ_out`` 的直接推论 —— 一根管子必须把它下游
   所有负载要吃的水都送过去。
3. **自顶向下求压力**：``P_child = P_parent − R·Q²``（阀门 R = 0）。
   由于压降恒为正，压力必然沿真实流向单调递减。
4. **供液结算**：负载**实际取用**的流量为 ``min(目标需求, supply_limit)``。
   未设上限时即为目标需求（等价于第一阶段行为）。
5. **派生量**：``V = Q/A``、``ΔP = R·Q²``，并按 ``required_flow`` /
   ``min_flow`` / ``min_pressure`` 给出 :class:`~fluid_network.models.LoadStatus`。

被关闭的阀门直接从图中移除，其下游元件自然成为不可达（isolated）。

所有公式严格来自需求文档定义的简化模型，未引入任何摩擦因子、密度或雷诺数。
"""

from __future__ import annotations

from typing import Mapping

from .exceptions import NotFoundError, TopologyError
from .models import (
    Network,
    Node,
    NodeResult,
    NodeType,
    PipeResult,
    Scenario,
    SolverResult,
    Valve,
    ValveResult,
)
from .paths import FlowPathAnalyzer
from .reliability import ReliabilityAnalyzer
from .topology import Topology, build_topology

__all__ = ["Solver", "evaluate_load"]


def evaluate_load(
    *,
    pressure: float | None,
    flow: float,
    min_pressure: float | None,
    min_flow: float | None,
    reachable: bool,
) -> tuple[bool, str]:
    """按 ``pressure >= min_pressure AND flow >= min_flow`` 判定，返回 ``(functional, 说明)``。

    .. deprecated::
        保留是为了兼容第一阶段的外部调用。新代码请用
        :func:`fluid_network.reliability.evaluate_load_reliability` ——
        它会额外给出 :class:`~fluid_network.models.LoadStatus`。
        本函数的判定语义与之一致。
    """
    if not reachable or pressure is None:
        return False, "负载被切断（上游阀门关闭或网络不连通），未获得供液"

    reasons: list[str] = []
    if pressure < (min_pressure or 0.0):
        reasons.append(f"压力 {pressure:,.0f} Pa 低于最低要求 {min_pressure:,.0f} Pa")
    if flow < (min_flow or 0.0):
        threshold = f"{min_flow:.6g} m3/s" if min_flow is not None else "要求值"
        reasons.append(f"流量 {flow:.6g} m3/s 低于最低要求 {threshold}")
    if reasons:
        return False, "；".join(reasons)
    return True, "满足压力与流量要求"


class Solver:
    """把 :class:`Network` + :class:`Scenario` 解成 :class:`SolverResult`。

    求解器**不负责**拓扑合法性以外的业务判断 —— 它只产出数值与状态；
    要把结果组织成对外的统一结构，用 :class:`~fluid_network.analysis.AnalysisBuilder`。
    """

    def __init__(self) -> None:
        self._path_analyzer = FlowPathAnalyzer()
        self._reliability = ReliabilityAnalyzer()

    def solve(self, network: Network, scenario: Scenario) -> SolverResult:
        self._validate_scenario(network, scenario)

        # 1) 按工况展开拓扑（含泵唯一性 / 树状校验） --------------------- #
        topology = build_topology(network, scenario)
        pump = network.node(topology.root)

        # 2) 流量：自底向上累加下游需求 ---------------------------------- #
        edge_flow, node_inflow, node_outflow = self._compute_flows(network, topology)

        # 3) 压力：自顶向下施加 ΔP = R·Q² -------------------------------- #
        pressure, edge_drop = self._compute_pressures(network, pump, topology, edge_flow)

        # 4) 供液结算：实际取用 = min(目标需求, 供液上限) ----------------- #
        supplied = self._settle_supply(network, topology, edge_flow)

        # 5) 流路 + 可靠性判定 ------------------------------------------- #
        reachable = topology.reachable
        isolated = topology.isolated
        paths = self._path_analyzer.analyze(network, scenario, topology)
        reachable_map = {load.id: paths[load.id].reachable for load in network.loads}

        verdicts = self._reliability.evaluate(
            network,
            pressures=pressure,
            flows=supplied,
            paths=paths,
            topology_supported=True,
            isolated_nodes=set(isolated),
        )
        load_results = self._reliability.to_load_results(
            network, verdicts, pressure, supplied, reachable_map
        )

        # 6) 组装结果 ---------------------------------------------------- #
        return SolverResult(
            network_id=network.id,
            scenario_id=scenario.id,
            scenario_name=scenario.display_name,
            node_results=self._build_node_results(network, topology, pressure, node_inflow, node_outflow),
            pipe_results={
                p.id: self._build_pipe_result(p, edge_flow, edge_drop, pressure)
                for p in network.pipes
                if p.id in edge_flow
            },
            valve_results={
                v.id: self._build_valve_result(v, scenario, edge_flow)
                for v in network.valves
            },
            load_results=load_results,
            paths=paths,
            warnings=self._collect_warnings(network, scenario, isolated, pressure),
        )

    # ------------------------------------------------------------------ #
    # 0) 输入校验
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_scenario(network: Network, scenario: Scenario) -> None:
        valve_ids = {v.id for v in network.valves}
        unknown = sorted(set(scenario.valve_states) - valve_ids)
        if unknown:
            raise NotFoundError(
                f"工况 '{scenario.id}' 引用了不存在的阀门：{', '.join(unknown)}"
            )

    # ------------------------------------------------------------------ #
    # 流量
    # ------------------------------------------------------------------ #
    @staticmethod
    def _compute_flows(
        network: Network, topology: Topology
    ) -> tuple[dict[str, float], dict[str, float], dict[str, float]]:
        """自底向上累加下游负载需求，得到每条边的流量。

        ``Q(e) = 以 e 的下游端为根的子树内全部负载目标需求之和``。
        注意用的是 ``required_flow``（需求），不是 ``min_flow``（阈值）——
        两者在第二阶段已经解耦。

        返回 ``(edge_id -> Q, node_id -> ΣQ_in, node_id -> ΣQ_out)``。
        """
        demand: dict[str, float] = {n.id: 0.0 for n in network.nodes}
        for load in network.loads:
            demand[load.id] = load.demand

        subtree: dict[str, float] = {}
        edge_flow: dict[str, float] = {}

        for node_id in reversed(topology.order):   # 自底向上
            total = demand[node_id] + sum(subtree[c] for c, _ in topology.children[node_id])
            subtree[node_id] = total
            edge = topology.parent_edge.get(node_id)
            if edge is not None:
                edge_flow[edge.id] = total

        inflow = {n.id: 0.0 for n in network.nodes}
        outflow = {n.id: 0.0 for n in network.nodes}
        for child, edge in topology.parent_edge.items():
            flow = edge_flow[edge.id]
            # 建树时已统一朝向：node_a 是上游、node_b 是下游
            inflow[child] += flow
            outflow[edge.node_a] += flow

        return edge_flow, inflow, outflow

    # ------------------------------------------------------------------ #
    # 压力
    # ------------------------------------------------------------------ #
    @staticmethod
    def _compute_pressures(
        network: Network,
        pump: Node,
        topology: Topology,
        edge_flow: Mapping[str, float],
    ) -> tuple[dict[str, float | None], dict[str, float]]:
        """自顶向下计算 ``P_child = P_parent − R·Q²``。

        由于所有边的压降都为正，压力必然沿真实流向单调递减。
        """
        pressure: dict[str, float | None] = {n.id: None for n in network.nodes}
        pressure[pump.id] = float(pump.pressure)
        edge_drop: dict[str, float] = {}

        for node_id in topology.order:   # BFS 顺序即自顶向下
            p_node = pressure[node_id]
            if p_node is None:   # 理论上不会发生：order 中的节点都可从泵到达
                continue
            for child, edge in topology.children[node_id]:
                q = edge_flow.get(edge.id, 0.0)
                drop = edge.resistance * q * q
                edge_drop[edge.id] = drop
                pressure[child] = p_node - drop

        return pressure, edge_drop

    # ------------------------------------------------------------------ #
    # 供液结算
    # ------------------------------------------------------------------ #
    @staticmethod
    def _settle_supply(
        network: Network, topology: Topology, edge_flow: Mapping[str, float]
    ) -> dict[str, float]:
        """结算每个负载**实际取用**的流量。

        ``实际取用 = min(目标需求, supply_limit)``，未设上限时即为目标需求。

        这里刻意**不**修改管路的 ``edge_flow`` —— 管路仍按目标需求输送。
        原因：流量在物理上由管子送到负载点，负载能取多少是负载自己的事；
        而且当前模型没有"反向抑制泵"的机制，把上游流量也改小属于凭空造公式。
        两者不一致的情形会在 warnings 里明确提示。
        """
        reachable = topology.reachable
        supplied: dict[str, float] = {}
        for load in network.loads:
            if load.id not in reachable:
                supplied[load.id] = 0.0
                continue
            # 该负载的上游边流量即"送到门口"的量
            edge = topology.parent_edge.get(load.id)
            delivered = edge_flow.get(edge.id, 0.0) if edge is not None else 0.0
            supplied[load.id] = load.supplied_flow(delivered)
        return supplied

    # ------------------------------------------------------------------ #
    # 结果组装
    # ------------------------------------------------------------------ #
    @staticmethod
    def _build_node_results(
        network: Network,
        topology: Topology,
        pressure: Mapping[str, float | None],
        inflow: Mapping[str, float],
        outflow: Mapping[str, float],
    ) -> dict[str, NodeResult]:
        reachable = topology.reachable
        results: dict[str, NodeResult] = {}
        for node in network.nodes:
            is_reachable = node.id in reachable
            results[node.id] = NodeResult(
                node_id=node.id,
                pressure=pressure.get(node.id) if is_reachable else None,
                status="ok" if is_reachable else "isolated",
                node_type=node.type,
                inflow=inflow.get(node.id, 0.0),
                outflow=outflow.get(node.id, 0.0),
                demand=node.demand if node.type is NodeType.LOAD else 0.0,
            )
        return results

    @staticmethod
    def _build_pipe_result(
        pipe,
        edge_flow: Mapping[str, float],
        edge_drop: Mapping[str, float],
        pressure: Mapping[str, float | None],
    ) -> PipeResult:
        q = edge_flow[pipe.id]
        return PipeResult(
            pipe_id=pipe.id,
            from_node=pipe.from_node,
            to_node=pipe.to_node,
            flow=q,
            velocity=q / pipe.area,
            pressure_drop=edge_drop.get(pipe.id, pipe.resistance * q * q),
            active=True,
            from_pressure=pressure.get(pipe.from_node),
            to_pressure=pressure.get(pipe.to_node),
        )

    @staticmethod
    def _build_valve_result(
        valve: Valve,
        scenario: Scenario,
        edge_flow: Mapping[str, float],
    ) -> ValveResult:
        is_open = scenario.valve_open(valve.id)
        # 阀门开启但下游被切断时流量为 0 —— edge_flow 里没有它就说明没走通。
        flow = edge_flow.get(valve.id, 0.0) if is_open else 0.0
        return ValveResult(
            valve_id=valve.id,
            is_open=is_open,
            flow=flow,
            pressure_drop=0.0,   # 理想阀不产生压降
            active=is_open and valve.id in edge_flow,
        )

    @staticmethod
    def _collect_warnings(
        network: Network,
        scenario: Scenario,
        isolated: list[str],
        pressure: Mapping[str, float | None],
    ) -> tuple[str, ...]:
        warnings: list[str] = []

        if isolated:
            warnings.append(f"工况 '{scenario.id}' 下有节点被切断：{', '.join(sorted(isolated))}")

        for load in network.loads:
            p = pressure.get(load.id)
            if p is not None and p < 0:
                warnings.append(
                    f"负载 '{load.id}' 压力为负（{p:,.0f} Pa），超出简化模型适用范围，结果仅供参考"
                )
            # 阈值高于需求时流量判据恒不成立，属于配置值得警惕
            if load.supply_limit is None and load.required_flow is not None:
                if load.required_flow < (load.min_flow or 0.0):
                    warnings.append(
                        f"负载 '{load.id}' 的 required_flow ({load.required_flow:.6g}) "
                        f"低于 min_flow ({load.min_flow:.6g})，该负载在当前工况下必然流量不足"
                    )
            if load.supply_limit is not None and load.supply_limit < (load.min_flow or 0.0):
                warnings.append(
                    f"负载 '{load.id}' 的 supply_limit ({load.supply_limit:.6g}) "
                    f"低于 min_flow ({load.min_flow:.6g})，供液受限，必然流量不足"
                )

        if scenario.failures:
            warnings.append(
                f"工况 '{scenario.id}' 声明了 {len(scenario.failures)} 项 failure，"
                "当前求解器暂不消费该字段（已保留供后续扩展）"
            )
        if scenario.actions:
            warnings.append(
                f"工况 '{scenario.id}' 声明了 {len(scenario.actions)} 项 action，"
                "当前求解器暂不消费该字段（已保留供后续扩展）"
            )
        return tuple(warnings)
