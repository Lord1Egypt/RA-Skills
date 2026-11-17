# -*- coding: utf-8 -*-
"""求解结果的分析与展示。

:sclass:`~fluid_network.solver.Solver` 只产出结构化的 :class:`SolverResult`；
把结果渲染成人能读的表格、或做跨工况对比，是这一层的职责。求解逻辑与展示
逻辑分离，互不污染。

**输出一律 ASCII**：``[PASS] / [FAIL] / [WARNING]`` 之类的标记不使用
``✓``/``✗``/``³`` 等字符。原因是 Windows 的 cmd/PowerShell 默认使用 GBK
代码页，非 ASCII 符号会直接抛 :class:`UnicodeEncodeError` 中断程序 ——
一个物理计算问题不该因为终端字体而失败。

关于守恒自检
------------
节点流量守恒 ``ΣQ_in = ΣQ_out + demand`` 对**内部节点**成立。
泵节点是**压力边界**：它不参与守恒，而是主动向网络补流，其残差恰好等于泵的
输出流量。因此自检会单独统计泵的供液量，并验证它等于全网负载需求之和。
"""

from __future__ import annotations

import unicodedata
from typing import Mapping, Sequence

from .models import (
    LoadStatus,
    Network,
    NodeType,
    Scenario,
    SolverResult,
)

# 判定守恒是否自洽的容差。整条链路只做加减乘除，误差应当接近浮点精度
# （实测约 1e-19），这里的阈值留了足够余量以容忍不同平台的浮点差异。
_CONSERVATION_TOL = 1e-12

_LEFT, _RIGHT = "l", "r"


# --------------------------------------------------------------------------- #
# 表格渲染（正确处理中日韩全角字符的显示宽度）
# --------------------------------------------------------------------------- #
def _display_width(text: str) -> int:
    """文本在等宽终端里占用的列数。"""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def _pad(text: str, width: int, align: str) -> str:
    """按**显示宽度**而不是字符数补齐。

    ``str.rjust`` 数的是字符个数，而中日韩字符在终端里占 2 列 ——
    直接用会得到参差不齐的表格。这里先算出需要补的空格数再手工拼接。
    """
    spaces = " " * max(0, width - _display_width(text))
    return spaces + text if align == _RIGHT else text + spaces


def _num(value: float | None, digits: int, scale: float = 1.0) -> str:
    """把可能为 ``None`` 的数值格式化进表格。

    ``None`` 表示"没有有效计算值"（例如管路被切断），渲染成 ``-``
    而不是 ``0`` —— 后者在物理上是误导性的。
    """
    if value is None:
        return "-"
    return f"{value * scale:.{digits}f}"


def _table(header: Sequence[str], rows: Sequence[Sequence[str]], aligns: Sequence[str]) -> list[str]:
    widths = [_display_width(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], _display_width(cell))

    def line(cells: Sequence[str]) -> str:
        return "  " + "  ".join(_pad(c, w, a) for c, w, a in zip(cells, widths, aligns))

    out = [line(header), "  " + "-" * (sum(widths) + 2 * (len(widths) - 1))]
    out.extend(line(r) for r in rows)
    return out


# 状态 -> 报告标记（纯 ASCII）
_STATUS_MARK: dict[LoadStatus, str] = {
    LoadStatus.HEALTHY: "[PASS]",
    LoadStatus.ISOLATED: "[FAIL]",
    LoadStatus.LOW_PRESSURE: "[FAIL]",
    LoadStatus.LOW_FLOW: "[FAIL]",
    LoadStatus.UNSUPPORTED: "[SKIP]",
    LoadStatus.FAILED: "[FAIL]",
}


# --------------------------------------------------------------------------- #
class Analyzer:
    """把 :class:`SolverResult` 变成可读报告 / 结构化摘要。"""

    # -- 结构化摘要 ------------------------------------------------------ #
    def summary(self, result: SolverResult) -> dict:
        """适合做断言或序列化的摘要。"""
        loads = list(result.load_results.values())
        main_pipe_id = self.main_pipe_id(result)
        return {
            "network_id": result.network_id,
            "scenario_id": result.scenario_id,
            "scenario_name": result.scenario_name,
            "loads_total": len(loads),
            "loads_functional": sum(1 for r in loads if r.functional),
            "all_loads_functional": result.all_loads_functional(),
            # 主干管流量即"泵出口总流量"，是系统总需求是否被满足的最直接指标。
            "main_pipe_id": main_pipe_id,
            "system_flow": result.pipe_results[main_pipe_id].flow if main_pipe_id else 0.0,
            "total_supply": self.total_supply(result),
            "max_conservation_residual": result.max_conservation_residual(),
            "status_counts": _status_counts(loads),
            "warnings": list(result.warnings),
        }

    @staticmethod
    def main_pipe_id(result: SolverResult) -> str:
        """流量最大的那条管路（本例中即主干管），仅用于摘要展示。"""
        if not result.pipe_results:
            return ""
        return max(result.pipe_results.values(), key=lambda p: p.flow).pipe_id

    # -- 守恒自检 -------------------------------------------------------- #
    @staticmethod
    def total_supply(result: SolverResult) -> float:
        """泵向网络补充的总流量（m³/s）。"""
        return result.supply_flow()

    def check_conservation(self, result: SolverResult, tol: float = _CONSERVATION_TOL) -> list[str]:
        """检查每个**内部节点**的 ``ΣQ_in = ΣQ_out + demand``。

        泵节点作为压力边界被排除（其残差是供液量，不是不守恒）。
        返回违规描述列表；空列表表示全部通过。
        """
        violations: list[str] = []
        for nr in result.node_results.values():
            if nr.is_isolated or nr.node_type is NodeType.PUMP:
                continue
            if abs(nr.residual) > tol:
                violations.append(
                    f"节点 '{nr.node_id}' 流量不守恒："
                    f"流入 {nr.inflow:.9g} - 流出 {nr.outflow:.9g} "
                    f"- 需求 {nr.demand:.9g} = {nr.residual:.3g}（容差 {tol:g}）"
                )
        return violations

    # -- 文本报告 -------------------------------------------------------- #
    def render(self, network: Network, scenario: Scenario, result: SolverResult) -> str:
        lines: list[str] = []
        add = lines.append

        bar = "=" * 78
        add(bar)
        add(f"Network : {network.name}  ({network.id})")
        add(f"Scenario: {scenario.display_name}  ({scenario.id})")
        add(bar)

        # -- 节点 -------------------------------------------------------- #
        add("")
        add("[Nodes]")
        node_rows = []
        for node in network.nodes:
            nr = result.node_results[node.id]
            pressure = f"{nr.pressure / 1000:,.2f}" if nr.pressure is not None else "-"
            if nr.is_isolated:
                residual = "-"
            elif nr.node_type is NodeType.PUMP:
                residual = "boundary"
            else:
                residual = f"{nr.residual:.2e}"
            node_rows.append([node.id, node.type.value, pressure, nr.status, residual])
        lines += _table(
            ["node", "type", "pressure(kPa)", "status", "residual(m3/s)"],
            node_rows,
            [_LEFT, _LEFT, _RIGHT, _LEFT, _RIGHT],
        )

        # -- 管路 / 阀门 -------------------------------------------------- #
        add("")
        add("[Pipes and Valves]")
        element_rows = []
        for pipe in network.pipes:
            pr = result.pipe_results.get(pipe.id)
            if pr is None:
                element_rows.append([
                    pipe.id, "pipe", f"{pipe.from_node} -> {pipe.to_node}",
                    "-", "-", "-", f"{pipe.resistance:.4g}", "-",
                ])
                continue
            element_rows.append([
                pr.pipe_id, "pipe", f"{pr.from_node} -> {pr.to_node}",
                _num(pr.flow, 6), _num(pr.velocity, 4),
                _num(pr.pressure_drop, 2, scale=1e-3), f"{pipe.resistance:.4g}", "-",
            ])
        for valve in network.valves:
            vr = result.valve_results[valve.id]
            state = "OPEN" if vr.is_open else "CLOSED"
            element_rows.append([
                vr.valve_id, "valve", f"{valve.from_node} -> {valve.to_node}",
                _num(vr.flow, 6), "-", f"{vr.pressure_drop / 1000:,.2f}", "-", state,
            ])
        lines += _table(
            ["element", "kind", "route", "flow(m3/s)", "vel(m/s)",
             "dP(kPa)", "R(Pa.s2/m6)", "valve"],
            element_rows,
            [_LEFT, _LEFT, _LEFT, _RIGHT, _RIGHT, _RIGHT, _RIGHT, _LEFT],
        )

        # -- 流路 -------------------------------------------------------- #
        add("")
        add("[Flow Paths]")
        for load in network.loads:
            path = result.paths.get(load.id)
            if path is None:
                add(f"  {load.id}: (no path information)")
                continue
            if path.reachable:
                add(f"  {load.id}: {' -> '.join(path.path)}")
            else:
                add(f"  {load.id}: UNREACHABLE")
                if path.isolation_point:
                    add(f"        cut at: {path.isolation_point}")
                add(f"        reason: {path.reason}")

        # -- 可靠性 ------------------------------------------------------ #
        add("")
        add("[Reliability]")
        for load in network.loads:
            lr = result.load_results[load.id]
            mark = _STATUS_MARK.get(lr.status, "[FAIL]")
            add(f"  {mark} {load.id}  status={lr.status.value}")
            p_txt = f"{lr.pressure / 1000:,.2f} kPa" if lr.pressure is not None else "n/a"
            flow_txt = f"{lr.flow:.6g} m3/s" if lr.flow is not None else "n/a"
            add(f"        pressure {p_txt}   required >= {lr.min_pressure / 1000:,.2f} kPa")
            add(f"        flow {flow_txt}   required >= {lr.min_flow:.6g} m3/s"
                f"   demand {lr.demanded:.6g} m3/s")
            add(f"        reason: {lr.reason}")

        # -- 自检 -------------------------------------------------------- #
        add("")
        add("[Conservation Check]")
        violations = self.check_conservation(result)
        internal_nodes = result.internal_nodes()
        if violations:
            for v in violations:
                add(f"  [FAIL] {v}")
        else:
            add(
                f"  [PASS] {len(internal_nodes)} internal nodes satisfy "
                f"sum(Q_in) = sum(Q_out) + demand "
                f"(max residual {result.max_conservation_residual():.3e} m3/s)"
            )

        supply = self.total_supply(result)
        demand = result.demand_flow()
        if abs(supply - demand) <= _CONSERVATION_TOL:
            add(f"  [PASS] pump output {supply:.6f} m3/s = sum of delivered load flow {demand:.6f} m3/s")
        else:
            add(f"  [FAIL] pump output {supply:.6f} m3/s != sum of delivered load flow {demand:.6f} m3/s")

        if result.warnings:
            add("")
            add("[Warnings]")
            for w in result.warnings:
                add(f"  [WARNING] {w}")

        add("")
        return "\n".join(lines)

    # -- 跨工况对比 ------------------------------------------------------ #
    def compare(self, network: Network, results: Mapping[str, SolverResult]) -> str:
        lines: list[str] = []
        add = lines.append

        load_ids = [load.id for load in network.loads]

        add("=" * 78)
        add("Scenario Comparison")
        add("=" * 78)

        add("")
        add("[Load Pressure (kPa)]")
        rows = []
        for scenario_id, result in results.items():
            row = [scenario_id]
            for lid in load_ids:
                lr = result.load_results[lid]
                row.append(f"{lr.pressure / 1000:,.2f}" if lr.pressure is not None else "no supply")
            rows.append(row)
        lines += _table(["scenario"] + load_ids, rows, [_LEFT] + [_RIGHT] * len(load_ids))

        add("")
        add("[Load Status]")
        rows = []
        for scenario_id, result in results.items():
            row = [scenario_id]
            for lid in load_ids:
                row.append(result.load_results[lid].status.value)
            rows.append(row)
        lines += _table(["scenario"] + load_ids, rows, [_LEFT] + [_RIGHT] * len(load_ids))

        add("")
        add("[System Flow (m3/s)]")
        rows = []
        for scenario_id, result in results.items():
            mp = self.main_pipe_id(result)
            rows.append([scenario_id, mp or "-", f"{result.pipe_results[mp].flow:.6f}" if mp else "-"])
        lines += _table(["scenario", "main pipe", "total flow"], rows, [_LEFT, _LEFT, _RIGHT])

        add("")
        return "\n".join(lines)


def _status_counts(loads) -> dict[str, int]:
    counts: dict[str, int] = {}
    for lr in loads:
        counts[lr.status.value] = counts.get(lr.status.value, 0) + 1
    return counts


__all__ = ["Analyzer"]
