from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .schema import (
    Edge,
    NetworkSpec,
    ResistanceKind,
    Scenario,
    Node,
)


@dataclass(frozen=True)
class EdgeResult:
    id: str
    enabled: bool
    effective_R: float
    # Positive flow means from edge.from_node -> edge.to_node
    flow_m3s: float
    velocity_m_per_s: Optional[float] = None
    # Pressure drop aligned with flow sign:
    # dP = p_from - p_to
    delta_p_pa: float = 0.0


@dataclass(frozen=True)
class Solution:
    scenario_id: str
    node_pressures_pa: Dict[str, float]
    edge_results: Dict[str, EdgeResult]


def _gaussian_solve(A: List[List[float]], b: List[float]) -> List[float]:
    # Simple Gaussian elimination with partial pivoting.
    n = len(A)
    M = [row[:] + [b_i] for row, b_i in zip(A, b)]
    for col in range(n):
        # Find pivot.
        pivot = col
        max_abs = abs(M[col][col])
        for r in range(col + 1, n):
            v = abs(M[r][col])
            if v > max_abs:
                pivot = r
                max_abs = v
        if max_abs == 0:
            raise ValueError("Singular matrix while solving linear system")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        # Normalize pivot row.
        pivot_val = M[col][col]
        for k in range(col, n + 1):
            M[col][k] /= pivot_val
        # Eliminate other rows.
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if factor == 0:
                continue
            for k in range(col, n + 1):
                M[r][k] -= factor * M[col][k]
    return [M[i][n] for i in range(n)]


def _effective_edge_R_and_enabled(edge: Edge, scenario: Scenario) -> Tuple[bool, float]:
    if edge.gating is None:
        return True, edge.resistance.R
    enabled = edge.gating.is_enabled(scenario.variables)
    if enabled:
        return True, edge.resistance.R
    return False, edge.resistance.R * edge.gating.disabled_resistance_multiplier


def _compute_edge_flow_pa_delta(
    edge: Edge, effective_R: float, delta_p_pa: float
) -> float:
    kind = edge.resistance.kind
    if effective_R <= 0:
        raise ValueError("effective_R must be > 0")
    if kind == "linear":
        # delta_p = R * Q
        return delta_p_pa / effective_R
    if kind == "quadratic":
        # delta_p = R * Q^2
        if delta_p_pa == 0:
            return 0.0
        return math.copysign(math.sqrt(abs(delta_p_pa) / effective_R), delta_p_pa)
    raise ValueError(f"Unsupported resistance kind: {kind}")


def solve_linear(network: NetworkSpec, scenario: Scenario) -> Solution:
    # Linear system: all edges must be linear.
    unknown_nodes = [n for n in network.nodes.values() if n.kind != "reservoir"]
    if not unknown_nodes:
        # Everything is a reservoir => pressures known; flows can be computed directly.
        node_pressures = {
            nid: network.reservoir_pressure_pa(nid, scenario) for nid, n in network.nodes.items()
        }
        edge_results: Dict[str, EdgeResult] = {}
        for eid, edge in network.edges.items():
            enabled, eff_R = _effective_edge_R_and_enabled(edge, scenario)
            p_from = node_pressures[edge.from_node]
            p_to = node_pressures[edge.to_node]
            dp = p_from - p_to
            flow = _compute_edge_flow_pa_delta(edge, eff_R, dp)
            area = edge.cross_section_area_m2()
            vel = flow / area if area and area > 0 else None
            edge_results[eid] = EdgeResult(
                id=eid,
                enabled=enabled,
                effective_R=eff_R,
                flow_m3s=flow,
                velocity_m_per_s=vel,
                delta_p_pa=dp,
            )
        return Solution(scenario_id=scenario.id, node_pressures_pa=node_pressures, edge_results=edge_results)

    # Build coefficient matrix A and RHS b for unknown pressures.
    idx = {n.id: i for i, n in enumerate(unknown_nodes)}
    n = len(unknown_nodes)
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    b = [0.0 for _ in range(n)]

    # Validate all edges are linear.
    for edge in network.edges.values():
        if edge.resistance.kind != "linear":
            raise ValueError("solve_linear called with non-linear edge models")

    # Each edge contributes conductance (1/R) terms to the mass balance equations.
    for edge in network.edges.values():
        enabled, eff_R = _effective_edge_R_and_enabled(edge, scenario)
        g = 1.0 / eff_R  # conductance
        u, v = edge.from_node, edge.to_node
        if u in idx:
            iu = idx[u]
            A[iu][iu] += g
            if v in idx:
                A[iu][idx[v]] -= g
            else:
                # v is reservoir (known pressure)
                b[iu] += g * network.reservoir_pressure_pa(v, scenario)
        if v in idx:
            iv = idx[v]
            A[iv][iv] += g
            if u in idx:
                A[iv][idx[u]] -= g
            else:
                b[iv] += g * network.reservoir_pressure_pa(u, scenario)

    p_unknown = _gaussian_solve(A, b)
    node_pressures = {n.id: p_unknown[idx[n.id]] for n in unknown_nodes}
    # add reservoir pressures
    for nid, node in network.nodes.items():
        if node.kind == "reservoir":
            node_pressures[nid] = network.reservoir_pressure_pa(nid, scenario)

    edge_results: Dict[str, EdgeResult] = {}
    for eid, edge in network.edges.items():
        enabled, eff_R = _effective_edge_R_and_enabled(edge, scenario)
        p_from = node_pressures[edge.from_node]
        p_to = node_pressures[edge.to_node]
        dp = p_from - p_to
        flow = _compute_edge_flow_pa_delta(edge, eff_R, dp)
        area = edge.cross_section_area_m2()
        vel = flow / area if area and area > 0 else None
        edge_results[eid] = EdgeResult(
            id=eid,
            enabled=enabled,
            effective_R=eff_R,
            flow_m3s=flow,
            velocity_m_per_s=vel,
            delta_p_pa=dp,
        )

    return Solution(scenario_id=scenario.id, node_pressures_pa=node_pressures, edge_results=edge_results)


def solve_nonlinear_newton(network: NetworkSpec, scenario: Scenario) -> Solution:
    # Newton solve for general mixed models (linear/quadratic).
    unknown_nodes = [n for n in network.nodes.values() if n.kind != "reservoir"]
    idx = {n.id: i for i, n in enumerate(unknown_nodes)}

    if not unknown_nodes:
        # Same as linear path.
        return solve_linear(network, scenario)

    # If any quadratic edges exist, treat as non-linear. We just always run Newton here
    # to support mixed models.
    reservoir_pressures = [
        network.reservoir_pressure_pa(nid, scenario)
        for nid, node in network.nodes.items()
        if node.kind == "reservoir"
    ]
    p0 = sum(reservoir_pressures) / len(reservoir_pressures) if reservoir_pressures else 0.0

    p_guess = [p0 for _ in unknown_nodes]
    max_iter = 50
    tol = 1e-7
    damping = 0.7

    # Pre-compute incident lists for faster residual evaluation.
    incident_edges: Dict[str, List[Edge]] = {n.id: [] for n in unknown_nodes}
    for edge in network.edges.values():
        if edge.from_node in incident_edges:
            incident_edges[edge.from_node].append(edge)
        if edge.to_node in incident_edges:
            incident_edges[edge.to_node].append(edge)

    def residual(p_vec: List[float]) -> List[float]:
        node_press = {nid: p_vec[idx[nid]] for nid in idx.keys()}
        # reservoir pressures
        for nid, node in network.nodes.items():
            if node.kind == "reservoir":
                node_press[nid] = network.reservoir_pressure_pa(nid, scenario)

        res: List[float] = [0.0 for _ in unknown_nodes]
        for n in unknown_nodes:
            total_outflow = 0.0
            nid = n.id
            for edge in incident_edges[nid]:
                enabled, eff_R = _effective_edge_R_and_enabled(edge, scenario)
                p_from = node_press[edge.from_node]
                p_to = node_press[edge.to_node]
                dp = p_from - p_to
                flow = _compute_edge_flow_pa_delta(edge, eff_R, dp)
                # outflow convention: positive out of the node.
                if edge.from_node == nid:
                    total_outflow += flow
                else:
                    # nid is edge.to_node => flow is entering nid when flow>0
                    total_outflow -= flow
            res[idx[nid]] = total_outflow
        return res

    def norm(v: List[float]) -> float:
        return math.sqrt(sum(x * x for x in v))

    for it in range(max_iter):
        f0 = residual(p_guess)
        if norm(f0) < tol:
            break

        # Numerical Jacobian.
        m = len(p_guess)
        J = [[0.0 for _ in range(m)] for _ in range(m)]
        for j in range(m):
            scale = max(1.0, abs(p_guess[j]))
            delta = 1e-4 * scale
            p2 = p_guess[:]
            p2[j] += delta
            f2 = residual(p2)
            for i in range(m):
                J[i][j] = (f2[i] - f0[i]) / delta

        dx = _gaussian_solve(J, [-x for x in f0])
        # Damped update for stability.
        for j in range(m):
            p_guess[j] += damping * dx[j]

    node_pressures = {n.id: p_guess[idx[n.id]] for n in unknown_nodes}
    for nid, node in network.nodes.items():
        if node.kind == "reservoir":
            node_pressures[nid] = network.reservoir_pressure_pa(nid, scenario)

    edge_results: Dict[str, EdgeResult] = {}
    for eid, edge in network.edges.items():
        enabled, eff_R = _effective_edge_R_and_enabled(edge, scenario)
        p_from = node_pressures[edge.from_node]
        p_to = node_pressures[edge.to_node]
        dp = p_from - p_to
        flow = _compute_edge_flow_pa_delta(edge, eff_R, dp)
        area = edge.cross_section_area_m2()
        vel = flow / area if area and area > 0 else None
        edge_results[eid] = EdgeResult(
            id=eid,
            enabled=enabled,
            effective_R=eff_R,
            flow_m3s=flow,
            velocity_m_per_s=vel,
            delta_p_pa=dp,
        )
    return Solution(scenario_id=scenario.id, node_pressures_pa=node_pressures, edge_results=edge_results)


class FluidNetworkSolver:
    def __init__(self, network: NetworkSpec):
        self.network = network

    def solve(self, scenario: Scenario) -> Solution:
        has_quadratic = any(e.resistance.kind == "quadratic" for e in self.network.edges.values())
        if not has_quadratic:
            return solve_linear(self.network, scenario)
        return solve_nonlinear_newton(self.network, scenario)

