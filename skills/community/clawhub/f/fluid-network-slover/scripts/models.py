from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Mapping

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


NodeType = Literal["source", "junction", "load", "sink"]

_ALLOWED_NODE_TYPES = {"source", "junction", "load", "sink"}
_ALLOWED_NODE_OVERRIDE_FIELDS = {
    "enabled",
    "external_flow",
    "fixed_pressure",
    "min_flow",
    "min_pressure",
    "type",
}
_ALLOWED_PIPE_OVERRIDE_FIELDS = {"diameter", "enabled", "resistance", "valve_open"}


class ConfigError(ValueError):
    """Raised when the TOML schema or scenario overrides are invalid."""


class ScenarioError(KeyError):
    """Raised when a requested scenario is not defined."""


@dataclass(slots=True)
class Node:
    """A network node."""

    id: str
    type: NodeType = "junction"
    fixed_pressure: float | None = None
    min_pressure: float | None = None
    min_flow: float | None = None
    external_flow: float = 0.0
    enabled: bool = True

    def __post_init__(self) -> None:
        self.id = _normalize_id(self.id, "node")
        if self.type not in _ALLOWED_NODE_TYPES:
            raise ConfigError(f"Unsupported node type '{self.type}' for node '{self.id}'.")
        self.fixed_pressure = _optional_float(self.fixed_pressure, "fixed_pressure", self.id)
        self.min_pressure = _optional_non_negative_float(self.min_pressure, "min_pressure", self.id)
        self.min_flow = _optional_non_negative_float(self.min_flow, "min_flow", self.id)
        self.external_flow = _coerce_float(self.external_flow, "external_flow", self.id)
        self.enabled = bool(self.enabled)


@dataclass(slots=True)
class Pipe:
    """A directed pipe between two nodes."""

    id: str
    source: str
    target: str
    resistance: float
    valve_open: bool = True
    diameter: float | None = None
    enabled: bool = True

    def __post_init__(self) -> None:
        self.id = _normalize_id(self.id, "pipe")
        self.source = _normalize_id(self.source, "pipe.source")
        self.target = _normalize_id(self.target, "pipe.target")
        if self.source == self.target:
            raise ConfigError(f"Pipe '{self.id}' must connect two distinct nodes.")
        self.resistance = _positive_float(self.resistance, "resistance", self.id)
        self.diameter = _optional_positive_float(self.diameter, "diameter", self.id)
        self.valve_open = bool(self.valve_open)
        self.enabled = bool(self.enabled)

    @property
    def is_active(self) -> bool:
        """Whether the pipe is enabled and its valve is open."""

        return self.enabled and self.valve_open


@dataclass(slots=True)
class ScenarioOverrides:
    """Incremental field overrides for a scenario."""

    system: dict[str, Any] = field(default_factory=dict)
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    pipes: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass(slots=True)
class Scenario:
    """A named operating scenario."""

    name: str
    description: str = ""
    overrides: ScenarioOverrides = field(default_factory=ScenarioOverrides)

    def __post_init__(self) -> None:
        self.name = _normalize_id(self.name, "scenario")
        self.description = str(self.description)


@dataclass(slots=True)
class SystemConfig:
    """In-memory representation of the TOML network definition."""

    system: dict[str, Any]
    nodes: dict[str, Node]
    pipes: dict[str, Pipe]
    scenarios: dict[str, Scenario] = field(default_factory=dict)
    source_path: str | None = None

    @property
    def name(self) -> str:
        return str(self.system.get("name", "Unnamed Fluid Network"))

    def source_nodes(self) -> list[Node]:
        return [node for node in self.nodes.values() if node.enabled and node.type == "source"]

    def load_nodes(self) -> list[Node]:
        return [node for node in self.nodes.values() if node.enabled and node.type == "load"]

    def boundary_nodes(self) -> list[Node]:
        return [node for node in self.nodes.values() if node.enabled and node.fixed_pressure is not None]

    def scenario_names(self, include_base: bool = True) -> list[str]:
        names = sorted(self.scenarios)
        return (["base"] + names) if include_base else names


@dataclass(slots=True)
class PipeState:
    """Solved pipe state for one operating scenario."""

    flow: float
    velocity: float | None
    pressure_drop: float
    active: bool


@dataclass(slots=True)
class SolverResult:
    """Numerical solver output."""

    scenario_name: str
    converged: bool
    method: str
    message: str
    iterations: int
    residual_norm: float
    node_pressures: dict[str, float]
    pipe_states: dict[str, PipeState]


@dataclass(slots=True)
class ConnectivitySummary:
    """Topological connectivity summary for active pipes."""

    active_pipe_ids: list[str]
    component_count: int
    reachable_sources_by_load: dict[str, list[str]]
    disconnected_loads: list[str]


@dataclass(slots=True)
class LoadAssessment:
    """Reliability assessment for a load node."""

    node_id: str
    connected_sources: list[str]
    topologically_connected: bool
    topology_path_pipe_ids: list[str]
    pressure: float
    min_pressure: float | None
    pressure_ok: bool
    inflow: float
    min_flow: float | None
    flow_ok: bool
    operational: bool
    alarms: list[str] = field(default_factory=list)


@dataclass(slots=True)
class AnalysisReport:
    """Combined solver and topology analysis report."""

    system_name: str
    scenario_name: str
    scenario_description: str
    solver: SolverResult
    connectivity: ConnectivitySummary
    loads: list[LoadAssessment]
    alarms: list[str]


def load_system_config(filepath: str | Path) -> SystemConfig:
    """Load and validate a TOML fluid network configuration file."""

    path = Path(filepath).resolve()
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    config = system_config_from_dict(data)
    config.source_path = str(path)
    return config


def system_config_from_dict(data: Mapping[str, Any]) -> SystemConfig:
    """Build a validated ``SystemConfig`` instance from parsed TOML content."""

    if not isinstance(data, Mapping):
        raise ConfigError("The root TOML document must be a table.")

    raw_system = data.get("system", {})
    if raw_system and not isinstance(raw_system, Mapping):
        raise ConfigError("[system] must be a TOML table.")
    system = dict(raw_system)

    raw_nodes = data.get("nodes", [])
    raw_pipes = data.get("pipes", [])
    raw_scenarios = data.get("scenarios", [])

    if not isinstance(raw_nodes, list) or not raw_nodes:
        raise ConfigError("At least one [[nodes]] entry is required.")
    if not isinstance(raw_pipes, list) or not raw_pipes:
        raise ConfigError("At least one [[pipes]] entry is required.")
    if raw_scenarios and not isinstance(raw_scenarios, list):
        raise ConfigError("[[scenarios]] must be declared as an array of tables.")

    nodes: dict[str, Node] = {}
    pipes: dict[str, Pipe] = {}
    scenarios: dict[str, Scenario] = {}

    for raw_node in raw_nodes:
        if not isinstance(raw_node, Mapping):
            raise ConfigError("Each [[nodes]] entry must be a table.")
        node = Node(
            id=raw_node["id"],
            type=str(raw_node.get("type", "junction")),
            fixed_pressure=raw_node.get("fixed_pressure"),
            min_pressure=raw_node.get("min_pressure"),
            min_flow=raw_node.get("min_flow"),
            external_flow=raw_node.get("external_flow", 0.0),
            enabled=raw_node.get("enabled", True),
        )
        if node.id in nodes:
            raise ConfigError(f"Duplicate node id '{node.id}'.")
        nodes[node.id] = node

    for raw_pipe in raw_pipes:
        if not isinstance(raw_pipe, Mapping):
            raise ConfigError("Each [[pipes]] entry must be a table.")
        pipe = Pipe(
            id=raw_pipe["id"],
            source=raw_pipe["source"],
            target=raw_pipe["target"],
            resistance=raw_pipe["resistance"],
            valve_open=raw_pipe.get("valve_open", True),
            diameter=raw_pipe.get("diameter"),
            enabled=raw_pipe.get("enabled", True),
        )
        if pipe.id in pipes:
            raise ConfigError(f"Duplicate pipe id '{pipe.id}'.")
        pipes[pipe.id] = pipe

    for raw_scenario in raw_scenarios:
        if not isinstance(raw_scenario, Mapping):
            raise ConfigError("Each [[scenarios]] entry must be a table.")
        scenario = _parse_scenario(raw_scenario)
        if scenario.name == "base":
            raise ConfigError("Scenario name 'base' is reserved.")
        if scenario.name in scenarios:
            raise ConfigError(f"Duplicate scenario name '{scenario.name}'.")
        scenarios[scenario.name] = scenario

    config = SystemConfig(system=system, nodes=nodes, pipes=pipes, scenarios=scenarios)
    _validate_config(config)
    return config


def apply_scenario(base_system: SystemConfig, scenario_name: str = "base") -> SystemConfig:
    """Deep copy a base config and apply a named scenario override."""

    scoped = copy.deepcopy(base_system)
    if scenario_name == "base":
        scoped.system["active_scenario"] = "base"
        return scoped
    if scenario_name not in base_system.scenarios:
        raise ScenarioError(f"Unknown scenario '{scenario_name}'.")

    scenario = base_system.scenarios[scenario_name]
    if scenario.overrides.system:
        scoped.system.update(copy.deepcopy(scenario.overrides.system))

    for node_id, fields in scenario.overrides.nodes.items():
        if node_id not in scoped.nodes:
            raise ConfigError(f"Scenario '{scenario_name}' references unknown node '{node_id}'.")
        node = scoped.nodes[node_id]
        for key, value in fields.items():
            if key not in _ALLOWED_NODE_OVERRIDE_FIELDS:
                raise ConfigError(
                    f"Scenario '{scenario_name}' uses unsupported node override field '{key}' on '{node_id}'."
                )
            setattr(node, key, value)
        node.__post_init__()

    for pipe_id, fields in scenario.overrides.pipes.items():
        if pipe_id not in scoped.pipes:
            raise ConfigError(f"Scenario '{scenario_name}' references unknown pipe '{pipe_id}'.")
        pipe = scoped.pipes[pipe_id]
        for key, value in fields.items():
            if key not in _ALLOWED_PIPE_OVERRIDE_FIELDS:
                raise ConfigError(
                    f"Scenario '{scenario_name}' uses unsupported pipe override field '{key}' on '{pipe_id}'."
                )
            setattr(pipe, key, value)
        pipe.__post_init__()

    scoped.system["active_scenario"] = scenario_name
    _validate_config(scoped, validate_scenarios=False)
    return scoped


def _parse_scenario(raw_scenario: Mapping[str, Any]) -> Scenario:
    overrides = raw_scenario.get("overrides", {})
    if overrides is None:
        overrides = {}
    if not isinstance(overrides, Mapping):
        raise ConfigError("Scenario overrides must be declared as a TOML table.")

    node_overrides = overrides.get("nodes", {})
    pipe_overrides = overrides.get("pipes", {})
    system_overrides = overrides.get("system", {})

    if node_overrides and not isinstance(node_overrides, Mapping):
        raise ConfigError("Scenario overrides.nodes must be a TOML table.")
    if pipe_overrides and not isinstance(pipe_overrides, Mapping):
        raise ConfigError("Scenario overrides.pipes must be a TOML table.")
    if system_overrides and not isinstance(system_overrides, Mapping):
        raise ConfigError("Scenario overrides.system must be a TOML table.")

    normalized_node_overrides: dict[str, dict[str, Any]] = {}
    for node_id, fields in dict(node_overrides).items():
        if not isinstance(fields, Mapping):
            raise ConfigError(f"Override for node '{node_id}' must be an inline TOML table.")
        normalized_node_overrides[_normalize_id(node_id, "scenario.node")] = dict(fields)

    normalized_pipe_overrides: dict[str, dict[str, Any]] = {}
    for pipe_id, fields in dict(pipe_overrides).items():
        if not isinstance(fields, Mapping):
            raise ConfigError(f"Override for pipe '{pipe_id}' must be an inline TOML table.")
        normalized_pipe_overrides[_normalize_id(pipe_id, "scenario.pipe")] = dict(fields)

    return Scenario(
        name=raw_scenario["name"],
        description=str(raw_scenario.get("description", "")),
        overrides=ScenarioOverrides(
            system=dict(system_overrides),
            nodes=normalized_node_overrides,
            pipes=normalized_pipe_overrides,
        ),
    )


def _validate_config(config: SystemConfig, *, validate_scenarios: bool = True) -> None:
    if not config.boundary_nodes():
        raise ConfigError("At least one enabled node must define fixed_pressure as a pressure boundary.")

    for pipe in config.pipes.values():
        if pipe.source not in config.nodes:
            raise ConfigError(f"Pipe '{pipe.id}' references unknown source node '{pipe.source}'.")
        if pipe.target not in config.nodes:
            raise ConfigError(f"Pipe '{pipe.id}' references unknown target node '{pipe.target}'.")

    if validate_scenarios:
        for scenario in config.scenarios.values():
            for node_id, fields in scenario.overrides.nodes.items():
                if node_id not in config.nodes:
                    raise ConfigError(f"Scenario '{scenario.name}' references unknown node '{node_id}'.")
                for key in fields:
                    if key not in _ALLOWED_NODE_OVERRIDE_FIELDS:
                        raise ConfigError(
                            f"Scenario '{scenario.name}' uses unsupported node override field '{key}'."
                        )
            for pipe_id, fields in scenario.overrides.pipes.items():
                if pipe_id not in config.pipes:
                    raise ConfigError(f"Scenario '{scenario.name}' references unknown pipe '{pipe_id}'.")
                for key in fields:
                    if key not in _ALLOWED_PIPE_OVERRIDE_FIELDS:
                        raise ConfigError(
                            f"Scenario '{scenario.name}' uses unsupported pipe override field '{key}'."
                        )


def _normalize_id(value: Any, label: str) -> str:
    text = str(value).strip()
    if not text:
        raise ConfigError(f"{label} id cannot be empty.")
    return text


def _coerce_float(value: Any, field_name: str, owner_id: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"Field '{field_name}' for '{owner_id}' must be numeric.") from exc


def _positive_float(value: Any, field_name: str, owner_id: str) -> float:
    number = _coerce_float(value, field_name, owner_id)
    if number <= 0.0:
        raise ConfigError(f"Field '{field_name}' for '{owner_id}' must be greater than 0.")
    return number


def _optional_float(value: Any, field_name: str, owner_id: str) -> float | None:
    if value is None:
        return None
    return _coerce_float(value, field_name, owner_id)


def _optional_positive_float(value: Any, field_name: str, owner_id: str) -> float | None:
    if value is None:
        return None
    return _positive_float(value, field_name, owner_id)


def _optional_non_negative_float(value: Any, field_name: str, owner_id: str) -> float | None:
    if value is None:
        return None
    number = _coerce_float(value, field_name, owner_id)
    if number < 0.0:
        raise ConfigError(f"Field '{field_name}' for '{owner_id}' must be non-negative.")
    return number
