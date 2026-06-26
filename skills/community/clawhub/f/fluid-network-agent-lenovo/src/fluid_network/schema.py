from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple


NodeKind = Literal["junction", "reservoir"]
ResistanceKind = Literal["linear", "quadratic"]
GateMode = Literal["all", "any"]
ScenarioVarValue = str
FlowMetric = Literal["abs", "inflow"]
FunctionCriteriaMode = Literal["all", "any"]


@dataclass(frozen=True)
class GatingCondition:
    variable: str
    equals: ScenarioVarValue


@dataclass(frozen=True)
class Gating:
    # If enabled_when_mode == "all": all conditions must match to enable.
    # If enabled_when_mode == "any": any condition matches to enable.
    enabled_when_mode: GateMode = "all"
    conditions: Tuple[GatingCondition, ...] = ()
    # If disabled, multiply the base resistance by this factor.
    disabled_resistance_multiplier: float = 1e12

    def is_enabled(self, variables: Dict[str, ScenarioVarValue]) -> bool:
        if not self.conditions:
            return True
        matched = []
        for c in self.conditions:
            matched.append(variables.get(c.variable) == c.equals)
        if self.enabled_when_mode == "all":
            return all(matched)
        return any(matched)


@dataclass(frozen=True)
class ResistanceModel:
    kind: ResistanceKind
    # Linear: dP = R * Q  => Q = dP / R
    # Quadratic: dP = R * Q^2  => Q = sign(dP) * sqrt(|dP|/R)
    # Units: R should be consistent with flow unit used in TOML.
    R: float


@dataclass(frozen=True)
class Node:
    id: str
    kind: NodeKind
    # For reservoir nodes, pressure is fixed.
    pressure_pa: Optional[float] = None

    # Optional role for analysis.
    role: Optional[Literal["source", "load"]] = None

    # Load thresholds (only meaningful when role == "load").
    min_flow_m3s: Optional[float] = None
    min_pressure_pa: Optional[float] = None


@dataclass(frozen=True)
class Edge:
    id: str
    from_node: str
    to_node: str
    resistance: ResistanceModel
    gating: Optional[Gating] = None

    # Optional geometry for velocity estimation.
    area_m2: Optional[float] = None
    diameter_m: Optional[float] = None

    def cross_section_area_m2(self) -> Optional[float]:
        if self.area_m2 is not None:
            return self.area_m2
        if self.diameter_m is not None:
            # area = pi*d^2/4
            from math import pi

            return pi * (self.diameter_m ** 2) / 4.0
        return None


@dataclass(frozen=True)
class Scenario:
    id: str
    # Variable values (switches, faults, valve states, etc.)
    variables: Dict[str, ScenarioVarValue] = field(default_factory=dict)
    # Optional pressure overrides for reservoir nodes.
    reservoir_pressure_overrides_pa: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class FunctionSpec:
    id: str
    # Load nodes that must succeed for this function.
    load_node_ids: Tuple[str, ...]
    criteria_mode: FunctionCriteriaMode = "all"  # "all" or "any"


@dataclass(frozen=True)
class AnalysisConfig:
    # How to treat computed load flow for threshold checking.
    flow_metric: FlowMetric = "abs"
    # Paths: edge connectivity uses only "enabled" edges from scenario gating.
    topology_direction: Literal["undirected", "from_to"] = "undirected"

    # For reporting purposes only; solver computes flows regardless of this.
    flow_abs_threshold_m3s_for_path: float = 0.0


@dataclass(frozen=True)
class NetworkSpec:
    nodes: Dict[str, Node]
    edges: Dict[str, Edge]
    scenarios: List[Scenario] = field(default_factory=list)
    functions: List[FunctionSpec] = field(default_factory=list)
    analysis: AnalysisConfig = AnalysisConfig()
    # If not provided, defaults to all nodes with role == "source".
    source_node_ids: Tuple[str, ...] = ()

    def load_nodes(self) -> List[Node]:
        return [n for n in self.nodes.values() if n.role == "load"]

    def reservoir_pressure_pa(self, node_id: str, scenario: Optional[Scenario] = None) -> float:
        node = self.nodes[node_id]
        if node.kind != "reservoir" or node.pressure_pa is None:
            raise ValueError(f"Node {node_id!r} is not a reservoir with a fixed pressure")
        if scenario and node_id in scenario.reservoir_pressure_overrides_pa:
            return scenario.reservoir_pressure_overrides_pa[node_id]
        return node.pressure_pa


def _require(d: Dict[str, Any], key: str, ctx: str) -> Any:
    if key not in d:
        raise ValueError(f"Missing required key {key!r} in {ctx}")
    return d[key]


def parse_toml_network(toml_data: Dict[str, Any]) -> NetworkSpec:
    # Expected top-level keys:
    # - nodes: array of tables
    # - edges: array of tables
    # - scenarios: array of tables (optional)
    # - functions: array of tables (optional)
    # - analysis: object (optional)
    # - source_node_ids: array (optional)
    nodes_raw = _require(toml_data, "nodes", "root")
    edges_raw = _require(toml_data, "edges", "root")

    nodes: Dict[str, Node] = {}
    for nd in nodes_raw:
        node_id = _require(nd, "id", "nodes[]")
        kind = _require(nd, "kind", f"nodes[{node_id!r}]")
        if kind not in ("junction", "reservoir"):
            raise ValueError(f"nodes[{node_id!r}].kind must be 'junction' or 'reservoir'")
        pressure_pa = nd.get("pressure_pa")
        role = nd.get("role")
        if role is not None and role not in ("source", "load"):
            raise ValueError(f"nodes[{node_id!r}].role must be 'source'/'load' or omitted")
        min_flow_m3s = nd.get("min_flow_m3s")
        min_pressure_pa = nd.get("min_pressure_pa")
        if kind == "reservoir":
            if pressure_pa is None:
                raise ValueError(f"Reservoir node {node_id!r} must define pressure_pa")
        else:
            if pressure_pa is not None:
                raise ValueError(f"Junction node {node_id!r} must not define pressure_pa")
        if role == "load":
            if min_flow_m3s is None or min_pressure_pa is None:
                raise ValueError(f"Load node {node_id!r} must define min_flow_m3s and min_pressure_pa")
        nodes[node_id] = Node(
            id=node_id,
            kind=kind,
            pressure_pa=pressure_pa,
            role=role,
            min_flow_m3s=min_flow_m3s,
            min_pressure_pa=min_pressure_pa,
        )

    edges: Dict[str, Edge] = {}
    for ed in edges_raw:
        eid = _require(ed, "id", "edges[]")
        from_node = _require(ed, "from", f"edges[{eid!r}]")
        to_node = _require(ed, "to", f"edges[{eid!r}]")
        if from_node not in nodes:
            raise ValueError(f"edges[{eid!r}].from references unknown node {from_node!r}")
        if to_node not in nodes:
            raise ValueError(f"edges[{eid!r}].to references unknown node {to_node!r}")

        res_raw = _require(ed, "resistance_model", f"edges[{eid!r}]")
        kind = _require(res_raw, "kind", f"edges[{eid!r}].resistance_model")
        R = float(_require(res_raw, "R", f"edges[{eid!r}].resistance_model"))
        if R <= 0:
            raise ValueError(f"edges[{eid!r}].resistance_model.R must be > 0")
        resistance = ResistanceModel(kind=kind, R=R)

        gating: Optional[Gating] = None
        gating_raw = ed.get("gating")
        if gating_raw is not None:
            enabled_when_mode = gating_raw.get("enabled_when_mode", "all")
            if enabled_when_mode not in ("all", "any"):
                raise ValueError(
                    f"edges[{eid!r}].gating.enabled_when_mode must be 'all' or 'any'"
                )
            disabled_multiplier = float(gating_raw.get("disabled_resistance_multiplier", 1e12))
            conditions_raw = gating_raw.get("conditions", [])
            conditions: List[GatingCondition] = []
            for c in conditions_raw:
                var = _require(c, "variable", f"edges[{eid!r}].gating.conditions[]")
                eq = _require(c, "equals", f"edges[{eid!r}].gating.conditions[]")
                conditions.append(GatingCondition(variable=var, equals=str(eq)))
            gating = Gating(
                enabled_when_mode=enabled_when_mode,  # type: ignore[arg-type]
                conditions=tuple(conditions),
                disabled_resistance_multiplier=disabled_multiplier,
            )

        area_m2 = ed.get("area_m2")
        diameter_m = ed.get("diameter_m")
        if area_m2 is not None and float(area_m2) <= 0:
            raise ValueError(f"edges[{eid!r}].area_m2 must be > 0")
        if diameter_m is not None and float(diameter_m) <= 0:
            raise ValueError(f"edges[{eid!r}].diameter_m must be > 0")
        edges[eid] = Edge(
            id=eid,
            from_node=from_node,
            to_node=to_node,
            resistance=resistance,
            gating=gating,
            area_m2=float(area_m2) if area_m2 is not None else None,
            diameter_m=float(diameter_m) if diameter_m is not None else None,
        )

    scenarios: List[Scenario] = []
    for sc in toml_data.get("scenarios", []) or []:
        sid = _require(sc, "id", "scenarios[]")
        variables = dict(sc.get("variables", {}) or {})
        overrides_raw = sc.get("reservoir_pressure_overrides_pa", {}) or {}
        overrides: Dict[str, float] = {k: float(v) for k, v in overrides_raw.items()}
        scenarios.append(
            Scenario(
                id=str(sid),
                variables={str(k): str(v) for k, v in variables.items()},
                reservoir_pressure_overrides_pa=overrides,
            )
        )

    functions: List[FunctionSpec] = []
    for fn in toml_data.get("functions", []) or []:
        fid = _require(fn, "id", "functions[]")
        load_node_ids = tuple(fn.get("load_node_ids", []) or [])
        if not load_node_ids:
            raise ValueError(f"functions[{fid!r}] must define non-empty load_node_ids")
        criteria_mode = fn.get("criteria_mode", "all")
        if criteria_mode not in ("all", "any"):
            raise ValueError(f"functions[{fid!r}].criteria_mode must be 'all' or 'any'")
        functions.append(
            FunctionSpec(
                id=str(fid),
                load_node_ids=load_node_ids,
                criteria_mode=criteria_mode,  # type: ignore[arg-type]
            )
        )

    analysis_raw = toml_data.get("analysis", {}) or {}
    analysis = AnalysisConfig(
        flow_metric=analysis_raw.get("flow_metric", "abs"),
        topology_direction=analysis_raw.get("topology_direction", "undirected"),
        flow_abs_threshold_m3s_for_path=float(
            analysis_raw.get("flow_abs_threshold_m3s_for_path", 0.0)
        ),
    )
    source_node_ids = tuple(toml_data.get("source_node_ids", []) or [])
    # If analysis config doesn't set, NetworkSpec can infer later.
    return NetworkSpec(
        nodes=nodes,
        edges=edges,
        scenarios=scenarios,
        functions=functions,
        analysis=analysis,
        source_node_ids=source_node_ids,
    )


