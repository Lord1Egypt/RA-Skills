# -*- coding: utf-8 -*-
"""功能可靠性判定（Reliability / Functional Analysis）。

职责
----
把**流路分析结果**（通不通）与**求解结果**（压力/流量够不够）合并成每个负载
的最终功能状态。

判定优先级
----------
自上而下，命中即止 —— 顺序本身就是语义："送不到水"比"水压不够"更根本，
只报后者会掩盖真正的原因::

    1. 不可达                        -> ISOLATED
    2. 拓扑不支持，无法判定            -> UNSUPPORTED
    3. 可达但 pressure < min_pressure -> LOW_PRESSURE
    4. 可达、压力达标，flow < min_flow -> LOW_FLOW
    5. 两项都达标                     -> HEALTHY

``FAILED`` 是兜底值，表示"求解过程本身出了意料之外的问题"，不属于优先级链。

关于 LOW_FLOW 在当前模型下何时出现
----------------------------------
求解时流量由 ``required_flow``（需求）驱动，因此只要负载可达，
实际送达量就等于 ``min(required_flow, supply_limit)``。于是：

* 未设 ``supply_limit`` 时，送达量恒等于 ``required_flow``。
  此时若 ``required_flow >= min_flow``（阈值不该高于需求）则状态必为
  HEALTHY —— LOW_FLOW 不会出现，判据也不会给出假阳性。
* 设置了 ``supply_limit < min_flow`` 时，送到的水确实不够用 ——
  这才是 LOW_FLOW 的真实来源。

换句话说，LOW_FLOW 不是"理论上可能存在但永远测不到"的分支：
它是**供液受限**这一真实工况的判定结果。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .models import LoadResult, LoadStatus, Network, Node, PathResult

__all__ = ["ReliabilityAnalyzer", "evaluate_load_reliability"]


@dataclass(frozen=True)
class ReliabilityVerdict:
    """单个负载的可靠性判定结果。"""

    load_id: str
    status: LoadStatus
    functional: bool
    reason: str

    def to_dict(self) -> dict:
        return {
            "load_id": self.load_id,
            "status": self.status.value,
            "functional": self.functional,
            "reason": self.reason,
        }


def evaluate_load_reliability(
    *,
    load: Node,
    reachable: bool,
    pressure: float | None,
    flow: float,
    topology_supported: bool = True,
) -> ReliabilityVerdict:
    """按上文优先级判定单个负载。

    参数都是"已经算出来的事实"，本函数**不做任何计算**，只做归类 ——
    这样判定规则可以被独立测试，不依赖求解器。
    """
    # 1) 不可达 —— 最高优先级
    if not reachable or pressure is None:
        return ReliabilityVerdict(
            load_id=load.id,
            status=LoadStatus.ISOLATED,
            functional=False,
            reason="负载不可达（上游阀门关闭或网络不连通），未获得供液",
        )

    # 2) 拓扑不支持，数值不可信，不给具体结论
    if not topology_supported:
        return ReliabilityVerdict(
            load_id=load.id,
            status=LoadStatus.UNSUPPORTED,
            functional=False,
            reason="网络拓扑超出当前模型能力（存在回路或平行冗余通路），无法判定",
        )

    min_pressure = load.min_pressure or 0.0
    min_flow = load.min_flow or 0.0

    # 3) 压力不足
    if pressure < min_pressure:
        return ReliabilityVerdict(
            load_id=load.id,
            status=LoadStatus.LOW_PRESSURE,
            functional=False,
            reason=(
                f"压力不足：{pressure:,.0f} Pa 低于最低要求 {min_pressure:,.0f} Pa"
                f"（缺口 {min_pressure - pressure:,.0f} Pa）"
            ),
        )

    # 4) 流量不足
    if flow < min_flow:
        return ReliabilityVerdict(
            load_id=load.id,
            status=LoadStatus.LOW_FLOW,
            functional=False,
            reason=(
                f"流量不足：{flow:.6g} m3/s 低于最低要求 {min_flow:.6g} m3/s"
                f"（缺口 {min_flow - flow:.6g} m3/s）"
            ),
        )

    # 5) 正常
    return ReliabilityVerdict(
        load_id=load.id,
        status=LoadStatus.HEALTHY,
        functional=True,
        reason=(
            f"功能正常：压力 {pressure:,.0f} Pa >= {min_pressure:,.0f} Pa，"
            f"流量 {flow:.6g} m3/s >= {min_flow:.6g} m3/s"
        ),
    )


class ReliabilityAnalyzer:
    """把求解结果 + 流路结果合成最终判定。"""

    def evaluate(
        self,
        network: Network,
        *,
        pressures: Mapping[str, float | None],
        flows: Mapping[str, float],
        paths: Mapping[str, PathResult],
        topology_supported: bool = True,
        isolated_nodes: set[str] | None = None,
    ) -> dict[str, ReliabilityVerdict]:
        """对网络中每个负载产出可靠性判定。

        ``flows`` 是负载**实际送达**的流量（已计入供液上限），
        ``paths`` 来自 :class:`~fluid_network.paths.FlowPathAnalyzer`。
        """
        isolated_nodes = isolated_nodes or set()
        verdicts: dict[str, ReliabilityVerdict] = {}

        for load in network.loads:
            path = paths.get(load.id)
            reachable = bool(path and path.reachable)
            if load.id in isolated_nodes:
                reachable = False

            verdicts[load.id] = evaluate_load_reliability(
                load=load,
                reachable=reachable,
                pressure=pressures.get(load.id) if reachable else None,
                flow=flows.get(load.id, 0.0) if reachable else 0.0,
                topology_supported=topology_supported,
            )
        return verdicts

    # ------------------------------------------------------------------ #
    @staticmethod
    def to_load_results(
        network: Network,
        verdicts: Mapping[str, ReliabilityVerdict],
        pressures: Mapping[str, float | None],
        flows: Mapping[str, float],
        reachable: Mapping[str, bool],
    ) -> dict[str, LoadResult]:
        """把判定结果打包成 :class:`~fluid_network.models.LoadResult`。

        这是 solver 的产出物 —— 它让 ``SolverResult.load_results`` 同时带上
        数值与状态，使用旧接口的调用方无需改动就能拿到 ``status``。
        """
        results: dict[str, LoadResult] = {}
        for load in network.loads:
            verdict = verdicts[load.id]
            is_reachable = bool(reachable.get(load.id, False))
            results[load.id] = LoadResult(
                load_id=load.id,
                # 不可达时三个数值一律 None —— "没有有效计算值"不是 0。
                pressure=pressures.get(load.id) if is_reachable else None,
                flow=flows.get(load.id) if is_reachable else None,
                functional=verdict.functional,
                status=verdict.status,
                min_pressure=load.min_pressure,
                min_flow=load.min_flow,
                required_flow=load.demand,
                reason=verdict.reason,
            )
        return results
