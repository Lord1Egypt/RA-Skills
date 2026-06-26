from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from .schema import AnalysisConfig, FunctionSpec, NetworkSpec, Node, Scenario
from .solver import Solution


@dataclass(frozen=True)
class LoadAssessment:
    load_node_id: str
    connected: bool
    pass_threshold: bool
    pressure_pa: float
    flow_m3s: float


@dataclass(frozen=True)
class FunctionAssessment:
    function_id: str
    loads: Tuple[LoadAssessment, ...]
    function_pass: bool


@dataclass(frozen=True)
class ScenarioAssessment:
    scenario_id: str
    # BFS reachability from sources.
    reachable_node_ids: Tuple[str, ...]
    functions: Tuple[FunctionAssessment, ...]


def _net_inflow_to_node(sol: Solution, network: NetworkSpec, node_id: str) -> float:
    # Using edge flow sign convention: positive flow is from edge.from_node -> edge.to_node.
    # net_inflow = sum(inflow) - sum(outflow)
    # For a node:
    # - if node is edge.to_node => +flow contributes to inflow
    # - if node is edge.from_node => flow leaves node => -flow contributes to inflow
    total = 0.0
    for eid, edge_res in sol.edge_results.items():
        # Need edge definition to know endpoints.
        edge_def = network.edges[eid]
        if edge_def.to_node == node_id:
            total += edge_res.flow_m3s
        elif edge_def.from_node == node_id:
            total -= edge_res.flow_m3s
    return total


def _build_adjacency(network: NetworkSpec, scenario: Scenario, sol: Solution) -> Dict[str, List[str]]:
    cfg = network.analysis
    adjacency: Dict[str, List[str]] = {nid: [] for nid in network.nodes.keys()}
    for eid, edge_def in network.edges.items():
        er = sol.edge_results[eid]
        if not er.enabled:
            continue
        u = edge_def.from_node
        v = edge_def.to_node
        if cfg.topology_direction == "undirected":
            adjacency[u].append(v)
            adjacency[v].append(u)
        else:
            adjacency[u].append(v)
    return adjacency


def _bfs_reachable(
    adjacency: Dict[str, List[str]], source_ids: List[str]
) -> Tuple[Set[str], Dict[str, Optional[str]]]:
    from collections import deque

    seen: Set[str] = set()
    parent: Dict[str, Optional[str]] = {s: None for s in source_ids}
    q = deque(source_ids)
    for s in source_ids:
        seen.add(s)
    while q:
        x = q.popleft()
        for y in adjacency.get(x, []):
            if y in seen:
                continue
            seen.add(y)
            parent[y] = x
            q.append(y)
    return seen, parent


def _choose_sources(network: NetworkSpec) -> List[str]:
    if network.source_node_ids:
        return list(network.source_node_ids)
    return [nid for nid, n in network.nodes.items() if n.role == "source"]


def assess_connectivity_and_reliability(network: NetworkSpec, scenario: Scenario, sol: Solution) -> ScenarioAssessment:
    sources = _choose_sources(network)
    if not sources:
        raise ValueError("No source_node_ids defined and no nodes with role == 'source' found")

    adjacency = _build_adjacency(network, scenario, sol)
    reachable, _parent = _bfs_reachable(adjacency, sources)

    functions = network.functions
    if not functions:
        # Default: each load node is its own function.
        functions = [
            FunctionSpec(
                id=f"function_for_{load.id}",
                load_node_ids=(load.id,),
                criteria_mode="all",
            )
            for load in network.load_nodes()
        ]

    assessments: List[FunctionAssessment] = []
    for fn in functions:
        loads: List[LoadAssessment] = []
        for load_id in fn.load_node_ids:
            load_node = network.nodes[load_id]
            if load_node.role != "load":
                raise ValueError(f"functions[{fn.id!r}].load_node_ids includes non-load node {load_id!r}")
            connected = load_id in reachable
            p = sol.node_pressures_pa[load_id]
            net_inflow = _net_inflow_to_node(sol, network, load_id)
            cfg = network.analysis
            if cfg.flow_metric == "abs":
                flow_metric = abs(net_inflow)
            else:
                # inflow metric: only count positive inflow
                flow_metric = net_inflow if net_inflow > 0 else 0.0

            pass_threshold = (p >= (load_node.min_pressure_pa or float("inf"))) and (
                flow_metric >= (load_node.min_flow_m3s or float("inf"))
            )
            loads.append(
                LoadAssessment(
                    load_node_id=load_id,
                    connected=connected,
                    pass_threshold=pass_threshold,
                    pressure_pa=p,
                    flow_m3s=flow_metric,
                )
            )
        if fn.criteria_mode == "all":
            function_pass = all(l.connected and l.pass_threshold for l in loads)
        else:
            function_pass = any(l.connected and l.pass_threshold for l in loads)

        assessments.append(
            FunctionAssessment(
                function_id=fn.id,
                loads=tuple(loads),
                function_pass=function_pass,
            )
        )

    return ScenarioAssessment(
        scenario_id=scenario.id,
        reachable_node_ids=tuple(sorted(reachable)),
        functions=tuple(assessments),
    )

