# -*- coding: utf-8 -*-
"""统一分析流水线：把各层结果组装成对外的 :class:`AnalysisResult`。

位置与依赖方向::

        Scenario
           |
           v
    FlowPathAnalyzer  -->  Topology  （通不通、怎么走）
           |
           v
        Solver                    （有多少压力、多少流量）
           |
           v
    ReliabilityAnalyzer           （最终功能状态）
           |
           v
     AnalysisBuilder              （组装成一份可序列化的契约）
           |
           v
    AnalysisResult  --to_json()-->   outputs/<scenario>.json

设计意图
--------
:class:`AnalysisResult` 是**对外唯一的契约**。求解器 / 分析器内部的
``SolverResult``、``Topology``、``PathResult`` 都是过程产物，结构会随实现
演进；而 ``AnalysisResult`` 的字段一旦定下来就应当保持稳定 —— 未来的
HTML/JS 前端只依赖它。

因此本模块承担两件事：把内部结构**拍平**成基本类型，以及把"拓扑不支持"
这类异常路径也变成**合法的输出**（而不是让整个流程中断）。
"""

from __future__ import annotations

from typing import Mapping

from .exceptions import FluidNetworkError
from .models import (
    AnalysisLoad,
    AnalysisNode,
    AnalysisPipe,
    AnalysisResult,
    AnalysisSummary,
    AnalysisValve,
    LoadStatus,
    Network,
    NodeType,
    PathResult,
    Scenario,
    ScenarioInfo,
    SolverResult,
    TopologySummary,
)
from .paths import FlowPathAnalyzer
from .reliability import ReliabilityAnalyzer
from .solver import Solver
from .topology import Topology, TopologyViolation, has_cycle

__all__ = ["AnalysisBuilder"]

_SCHEMA_VERSION = "2.0"


class AnalysisBuilder:
    """把一次工况分析的全过程收敛成 :class:`AnalysisResult`。

    典型用法::

        builder = AnalysisBuilder()
        analysis = builder.build(network, scenario)
        Path("outputs").mkdir(exist_ok=True)
        Path(f"outputs/{scenario.id}.json").write_text(
            analysis.to_json(), encoding="utf-8"
        )
    """

    def __init__(self, solver: Solver | None = None) -> None:
        self._solver = solver or Solver()
        self._paths = FlowPathAnalyzer()
        self._reliability = ReliabilityAnalyzer()

    # ------------------------------------------------------------------ #
    def build(self, network: Network, scenario: Scenario) -> AnalysisResult:
        """跑完整条链，产出统一分析结果。

        拓扑不支持时**不抛异常** —— 而是产出 ``topology.supported = false``
        且全部负载为 ``UNSUPPORTED`` 的结果。原因：一个不可解的网络同样是
        有价值的分析结论，把它变成异常只会让调用方不得不写 try/except 才能
        拿到同样这些信息。
        """
        try:
            result = self._solver.solve(network, scenario)
        except TopologyViolation as exc:
            return self._unsupported(network, scenario, exc)
        except FluidNetworkError as exc:
            return self._failed(network, scenario, exc)

        topology = TopologySummary(
            connected=not result.node_results or all(
                nr.status == "ok" for nr in result.node_results.values()
            ),
            supported=True,
            isolated_nodes=tuple(
                sorted(nid for nid, nr in result.node_results.items() if nr.is_isolated)
            ),
        )

        return AnalysisResult(
            schema_version=_SCHEMA_VERSION,
            network_id=network.id,
            scenario=ScenarioInfo(id=scenario.id, name=scenario.display_name),
            topology=topology,
            paths=dict(result.paths),
            nodes=tuple(self._node_entry(n, result) for n in network.nodes if n.id in result.node_results),
            pipes=tuple(self._pipe_entries(network, result)),
            valves=tuple(self._valve_entries(network, result)),
            loads=tuple(self._load_entries(network, result)),
            summary=self._summarize(network, result),
            warnings=tuple(result.warnings),
            main_pipe_id=self._main_pipe_id(result),
        )

    # ------------------------------------------------------------------ #
    # 异常路径也产出合法结果
    # ------------------------------------------------------------------ #
    def _unsupported(
        self, network: Network, scenario: Scenario, exc: TopologyViolation
    ) -> AnalysisResult:
        """拓扑含环 / 平行冗余通路 —— 数值不可信，但结构信息仍然有用。"""
        offending = exc.offending_elements
        # 即便不可解，也要给出"哪些负载受影响"以及各节点的可达性
        cycle, on_cycle = has_cycle(network, scenario)
        offending = offending or tuple(sorted(on_cycle))

        closed_valves = self._paths.closed_valve_ids(network, scenario)
        topology = TopologySummary(
            connected=False,
            supported=False,
            isolated_nodes=(),
            unsupported_elements=offending,
            unsupported_reason=str(exc),
        )

        loads = tuple(
            AnalysisLoad(
                load_id=load.id,
                pressure=None,
                flow=None,
                functional=False,
                status=LoadStatus.UNSUPPORTED,
                min_pressure=load.min_pressure,
                min_flow=load.min_flow,
                required_flow=load.demand,
                reason="拓扑超出当前模型能力，无法给出可信的数值结果",
                reachable=False,
            )
            for load in network.loads
        )
        path_entries = {
            load.id: PathResult(
                load_id=load.id,
                reachable=False,
                reason="拓扑不支持，未进行流路分析",
            )
            for load in network.loads
        }

        warnings = [f"拓扑不支持：{exc}"]
        if closed_valves:
            warnings.append(f"当前工况关闭的阀门：{', '.join(closed_valves)}")

        return AnalysisResult(
            schema_version=_SCHEMA_VERSION,
            network_id=network.id,
            scenario=ScenarioInfo(id=scenario.id, name=scenario.display_name),
            topology=topology,
            paths=path_entries,
            nodes=tuple(
                AnalysisNode(
                    node_id=node.id,
                    node_type=node.type,
                    pressure=None,
                    status="unsupported",
                )
                for node in network.nodes
            ),
            pipes=tuple(
                AnalysisPipe(
                    pipe_id=pipe.id,
                    from_node=pipe.from_node,
                    to_node=pipe.to_node,
                    flow=None,
                    velocity=None,
                    pressure_drop=None,
                    resistance=pipe.resistance,
                    diameter=pipe.diameter,
                    active=pipe.id not in offending,
                )
                for pipe in network.pipes
            ),
            loads=loads,
            summary=AnalysisSummary(
                total_loads=len(loads),
                functional_loads=0,
                failed_loads=len(loads),
                isolated_loads=0,
                status_counts={LoadStatus.UNSUPPORTED.value: len(loads)},
            ),
            warnings=tuple(warnings),
        )

    def _failed(self, network: Network, scenario: Scenario, exc: FluidNetworkError) -> AnalysisResult:
        """其它求解错误（无泵、多泵、工况引用错误……）—— 同样产出合法结果。"""
        loads = tuple(
            AnalysisLoad(
                load_id=load.id,
                pressure=None,
                flow=None,
                functional=False,
                status=LoadStatus.FAILED,
                min_pressure=load.min_pressure,
                min_flow=load.min_flow,
                required_flow=load.demand,
                reason=f"求解失败：{exc}",
                reachable=False,
            )
            for load in network.loads
        )
        return AnalysisResult(
            schema_version=_SCHEMA_VERSION,
            network_id=network.id,
            scenario=ScenarioInfo(id=scenario.id, name=scenario.display_name),
            topology=TopologySummary(
                connected=False,
                supported=False,
                unsupported_reason=str(exc),
            ),
            paths={},
            nodes=tuple(
                AnalysisNode(node_id=n.id, node_type=n.type, pressure=None, status="failed")
                for n in network.nodes
            ),
            pipes=(),
            loads=loads,
            summary=AnalysisSummary(
                total_loads=len(loads),
                functional_loads=0,
                failed_loads=len(loads),
                status_counts={LoadStatus.FAILED.value: len(loads)},
            ),
            warnings=(f"求解失败：{exc}",),
        )

    # ------------------------------------------------------------------ #
    # 条目转换
    # ------------------------------------------------------------------ #
    @staticmethod
    def _node_entry(node, result: SolverResult) -> AnalysisNode:
        nr = result.node_results[node.id]
        return AnalysisNode(
            node_id=nr.node_id,
            node_type=nr.node_type or node.type,
            pressure=nr.pressure,
            status=nr.status,
            inflow=nr.inflow,
            outflow=nr.outflow,
            demand=nr.demand,
        )

    @staticmethod
    def _pipe_entries(network: Network, result: SolverResult) -> list[AnalysisPipe]:
        entries: list[AnalysisPipe] = []
        for pipe in network.pipes:
            pr = result.pipe_results.get(pipe.id)
            if pr is None:
                # 未被阀门切断的管路必然会出现在结果里；缺失说明它落在不可达区域
                entries.append(
                    AnalysisPipe(
                        pipe_id=pipe.id,
                        from_node=pipe.from_node,
                        to_node=pipe.to_node,
                        flow=None,
                        velocity=None,
                        pressure_drop=None,
                        resistance=pipe.resistance,
                        diameter=pipe.diameter,
                        active=False,
                    )
                )
                continue
            entries.append(
                AnalysisPipe(
                    pipe_id=pr.pipe_id,
                    from_node=pr.from_node,
                    to_node=pr.to_node,
                    flow=pr.flow,
                    velocity=pr.velocity,
                    pressure_drop=pr.pressure_drop,
                    resistance=pipe.resistance,
                    diameter=pipe.diameter,
                    active=True,
                    from_pressure=pr.from_pressure,
                    to_pressure=pr.to_pressure,
                )
            )
        return entries

    @staticmethod
    def _valve_entries(network: Network, result: SolverResult) -> list[AnalysisValve]:
        """把阀门结果摊平成分析条目。

        前端需要 ``is_open`` 才能正确绘制阀门开合与关闭标记 ——
        让它从"阀门是否出现在某条 ``isolation_point`` 里"去反推既脆弱又绕。
        """
        entries: list[AnalysisValve] = []
        for valve in network.valves:
            vr = result.valve_results.get(valve.id)
            if vr is None:
                continue
            entries.append(
                AnalysisValve(
                    valve_id=vr.valve_id,
                    from_node=valve.from_node,
                    to_node=valve.to_node,
                    is_open=vr.is_open,
                    flow=vr.flow,
                    active=vr.active,
                    pressure_drop=vr.pressure_drop,
                )
            )
        return entries

    @staticmethod
    def _main_pipe_id(result: SolverResult) -> str:
        """主干管 = 泵出口总流量所在的那条管路，即当前工况下流量最大的管路。

        **这个判断放在后端**：它依赖"哪条管路承载了全网需求"这一求解结果，
        属于分析结论，不该让每个前端各写一遍（也会导致多端不一致）。
        """
        if not result.pipe_results:
            return ""
        return max(result.pipe_results.values(), key=lambda p: p.flow).pipe_id

    @staticmethod
    def _load_entries(network: Network, result: SolverResult) -> list[AnalysisLoad]:
        entries: list[AnalysisLoad] = []
        for load in network.loads:
            lr = result.load_results[load.id]
            path = result.paths.get(load.id)
            entries.append(
                AnalysisLoad(
                    load_id=lr.load_id,
                    pressure=lr.pressure,
                    flow=lr.flow,
                    functional=lr.functional,
                    status=lr.status,
                    min_pressure=lr.min_pressure,
                    min_flow=lr.min_flow,
                    required_flow=lr.required_flow,
                    reason=lr.reason,
                    reachable=bool(path and path.reachable),
                    path=path.path if path else (),
                    node_path=path.node_path if path else (),
                )
            )
        return entries

    @staticmethod
    def _summarize(network: Network, result: SolverResult) -> AnalysisSummary:
        counts: dict[str, int] = {}
        for lr in result.load_results.values():
            counts[lr.status.value] = counts.get(lr.status.value, 0) + 1

        loads = list(result.load_results.values())
        return AnalysisSummary(
            total_loads=len(loads),
            functional_loads=sum(1 for lr in loads if lr.functional),
            failed_loads=sum(1 for lr in loads if not lr.functional),
            isolated_loads=sum(1 for lr in loads if lr.status is LoadStatus.ISOLATED),
            status_counts=counts,
        )
