from __future__ import annotations

from collections import deque

try:
    import networkx as nx
except ModuleNotFoundError:  # pragma: no cover
    nx = None  # type: ignore[assignment]

try:
    from .models import (
        AnalysisReport,
        ConnectivitySummary,
        LoadAssessment,
        SolverResult,
        SystemConfig,
    )
except ImportError:  # pragma: no cover
    from models import AnalysisReport, ConnectivitySummary, LoadAssessment, SolverResult, SystemConfig


def analyze_solution(
    config: SystemConfig,
    solver_result: SolverResult,
    *,
    scenario_name: str = "base",
    scenario_description: str = "",
) -> AnalysisReport:
    """Analyze topology and functional reliability for a solved network snapshot."""

    topology_graph = _build_topology_graph(config)
    active_pipe_ids = sorted(_iter_active_pipe_ids(config))
    source_ids = _source_ids(config)

    reachable_sources_by_load: dict[str, list[str]] = {}
    disconnected_loads: list[str] = []
    load_assessments: list[LoadAssessment] = []

    for load in config.load_nodes():
        reachable_sources = sorted(
            source_id for source_id in source_ids if _has_path(topology_graph, source_id, load.id)
        )
        reachable_sources_by_load[load.id] = reachable_sources
        if not reachable_sources:
            disconnected_loads.append(load.id)

        topology_path = _find_pipe_path(topology_graph, reachable_sources[0], load.id) if reachable_sources else []
        pressure = solver_result.node_pressures.get(load.id, 0.0)
        inflow = _compute_node_inflow(config, solver_result, load.id)
        pressure_ok = load.min_pressure is None or pressure >= load.min_pressure
        flow_ok = load.min_flow is None or inflow >= load.min_flow

        alarms: list[str] = []
        if not reachable_sources:
            alarms.append("Load is topologically disconnected from all sources.")
        if not pressure_ok:
            alarms.append(
                f"Pressure below threshold: actual={pressure:.6f}, required={load.min_pressure:.6f}."
            )
        if not flow_ok:
            alarms.append(f"Flow below threshold: actual={inflow:.6f}, required={load.min_flow:.6f}.")

        load_assessments.append(
            LoadAssessment(
                node_id=load.id,
                connected_sources=reachable_sources,
                topologically_connected=bool(reachable_sources),
                topology_path_pipe_ids=topology_path,
                pressure=pressure,
                min_pressure=load.min_pressure,
                pressure_ok=pressure_ok,
                inflow=inflow,
                min_flow=load.min_flow,
                flow_ok=flow_ok,
                operational=bool(reachable_sources) and pressure_ok and flow_ok,
                alarms=alarms,
            )
        )

    alarms = []
    if not solver_result.converged:
        alarms.append(f"Solver did not converge cleanly: {solver_result.message}")
    for assessment in load_assessments:
        alarms.extend(f"{assessment.node_id}: {alarm}" for alarm in assessment.alarms)

    connectivity = ConnectivitySummary(
        active_pipe_ids=active_pipe_ids,
        component_count=_component_count(config),
        reachable_sources_by_load=reachable_sources_by_load,
        disconnected_loads=disconnected_loads,
    )
    return AnalysisReport(
        system_name=config.name,
        scenario_name=scenario_name,
        scenario_description=scenario_description,
        solver=solver_result,
        connectivity=connectivity,
        loads=load_assessments,
        alarms=alarms,
    )


def _build_topology_graph(config: SystemConfig):
    if nx is not None:
        graph = nx.MultiDiGraph()
        for node in config.nodes.values():
            if node.enabled:
                graph.add_node(node.id, type=node.type)
        for pipe_id in _iter_active_pipe_ids(config):
            pipe = config.pipes[pipe_id]
            graph.add_edge(pipe.source, pipe.target, key=pipe.id, pipe_id=pipe.id)
        return graph

    graph: dict[str, list[tuple[str, str]]] = {
        node.id: [] for node in config.nodes.values() if node.enabled
    }
    for pipe_id in _iter_active_pipe_ids(config):
        pipe = config.pipes[pipe_id]
        graph[pipe.source].append((pipe.target, pipe.id))
    return graph


def _has_path(graph, source_id: str, target_id: str) -> bool:
    if nx is not None:
        if source_id not in graph or target_id not in graph:
            return False
        return nx.has_path(graph, source_id, target_id)

    queue = deque([source_id])
    seen = {source_id}
    while queue:
        current = queue.popleft()
        if current == target_id:
            return True
        for next_node, _pipe_id in graph.get(current, []):
            if next_node not in seen:
                seen.add(next_node)
                queue.append(next_node)
    return False


def _find_pipe_path(graph, source_id: str, target_id: str) -> list[str]:
    if nx is not None:
        node_path = nx.shortest_path(graph, source_id, target_id)
        pipe_ids: list[str] = []
        for start, end in zip(node_path[:-1], node_path[1:], strict=False):
            edge_bundle = graph.get_edge_data(start, end) or {}
            first_key = next(iter(sorted(edge_bundle)))
            edge_data = edge_bundle[first_key]
            pipe_ids.append(str(edge_data["pipe_id"]))
        return pipe_ids

    queue = deque([source_id])
    parents: dict[str, tuple[str, str]] = {}
    seen = {source_id}
    while queue:
        current = queue.popleft()
        if current == target_id:
            break
        for next_node, pipe_id in graph.get(current, []):
            if next_node in seen:
                continue
            seen.add(next_node)
            parents[next_node] = (current, pipe_id)
            queue.append(next_node)
    if target_id not in seen:
        return []

    pipe_ids: list[str] = []
    current = target_id
    while current in parents:
        previous, pipe_id = parents[current]
        pipe_ids.append(pipe_id)
        current = previous
    pipe_ids.reverse()
    return pipe_ids


def _compute_node_inflow(config: SystemConfig, solver_result: SolverResult, node_id: str) -> float:
    inflow = 0.0
    for pipe_id in _iter_active_pipe_ids(config):
        pipe = config.pipes[pipe_id]
        flow = solver_result.pipe_states[pipe_id].flow
        if pipe.target == node_id:
            inflow += max(flow, 0.0)
        elif pipe.source == node_id:
            inflow += max(-flow, 0.0)
    return inflow


def _source_ids(config: SystemConfig) -> list[str]:
    sources = [node.id for node in config.source_nodes()]
    if sources:
        return sources
    return sorted(node.id for node in config.boundary_nodes())


def _iter_active_pipe_ids(config: SystemConfig):
    for pipe_id, pipe in config.pipes.items():
        if (
            pipe.enabled
            and pipe.valve_open
            and config.nodes[pipe.source].enabled
            and config.nodes[pipe.target].enabled
        ):
            yield pipe_id


def _component_count(config: SystemConfig) -> int:
    adjacency: dict[str, set[str]] = {
        node.id: set()
        for node in config.nodes.values()
        if node.enabled
    }
    for pipe_id in _iter_active_pipe_ids(config):
        pipe = config.pipes[pipe_id]
        adjacency[pipe.source].add(pipe.target)
        adjacency[pipe.target].add(pipe.source)

    components = 0
    seen: set[str] = set()
    for node_id in adjacency:
        if node_id in seen:
            continue
        components += 1
        queue = deque([node_id])
        seen.add(node_id)
        while queue:
            current = queue.popleft()
            for next_node in adjacency[current]:
                if next_node not in seen:
                    seen.add(next_node)
                    queue.append(next_node)
    return components
