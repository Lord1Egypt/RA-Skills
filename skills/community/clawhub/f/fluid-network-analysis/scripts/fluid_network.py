#!/usr/bin/env python3
"""Dependency-free runtime for the fluid-network-analysis Agent Skill."""

import argparse
import ast
import json
import math
import re
import sys
from collections import Counter, deque
from pathlib import Path

try:
    import tomllib
except ImportError:  # Python 3.9 and 3.10 use the schema-specific fallback below.
    tomllib = None


class NetworkError(Exception):
    pass


def _strip_comment(line):
    quote = None
    escaped = False
    output = []
    for character in line:
        if escaped:
            output.append(character)
            escaped = False
            continue
        if character == "\\" and quote == '"':
            output.append(character)
            escaped = True
            continue
        if character in {'"', "'"}:
            if quote is None:
                quote = character
            elif quote == character:
                quote = None
            output.append(character)
            continue
        if character == "#" and quote is None:
            break
        output.append(character)
    return "".join(output).strip()


def _parse_scalar(text, line_number):
    if text in {"true", "false"}:
        return text == "true"
    if text.startswith(('"', "'")):
        try:
            value = ast.literal_eval(text)
        except (SyntaxError, ValueError) as exc:
            raise NetworkError(f"line {line_number}: invalid string value") from exc
        if not isinstance(value, str):
            raise NetworkError(f"line {line_number}: only string scalar values are supported")
        return value
    normalized = text.replace("_", "")
    try:
        if re.fullmatch(r"[+-]?\d+", normalized):
            return int(normalized)
        if re.fullmatch(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?", normalized):
            return float(normalized)
    except ValueError as exc:
        raise NetworkError(f"line {line_number}: invalid numeric value") from exc
    raise NetworkError(
        f"line {line_number}: unsupported TOML value; use a string, number, or boolean"
    )


def _resolve_table(root, parts, line_number):
    current = root
    for part in parts:
        if not isinstance(current, dict):
            raise NetworkError(f"line {line_number}: invalid nested table path")
        if part not in current:
            current[part] = {}
        value = current[part]
        if isinstance(value, list):
            if not value:
                raise NetworkError(f"line {line_number}: array table {part!r} has no current item")
            current = value[-1]
        elif isinstance(value, dict):
            current = value
        else:
            raise NetworkError(f"line {line_number}: {part!r} is already a scalar")
    return current


def _parse_toml_subset(text):
    """Parse the scalar/table subset used by schema 1.0 on Python before 3.11."""

    root = {}
    current = root
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = _strip_comment(raw_line)
        if not line:
            continue
        if line.startswith("[[") and line.endswith("]]" ):
            path = [part.strip() for part in line[2:-2].split(".")]
            if not all(path):
                raise NetworkError(f"line {line_number}: invalid array table")
            parent = _resolve_table(root, path[:-1], line_number)
            collection = parent.setdefault(path[-1], [])
            if not isinstance(collection, list):
                raise NetworkError(f"line {line_number}: array table conflicts with existing value")
            current = {}
            collection.append(current)
            continue
        if line.startswith("[") and line.endswith("]"):
            path = [part.strip() for part in line[1:-1].split(".")]
            if not all(path):
                raise NetworkError(f"line {line_number}: invalid table")
            current = _resolve_table(root, path, line_number)
            continue
        if "=" not in line:
            raise NetworkError(f"line {line_number}: expected key = value")
        key, value_text = (part.strip() for part in line.split("=", 1))
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key):
            raise NetworkError(f"line {line_number}: unsupported key syntax {key!r}")
        if key in current:
            raise NetworkError(f"line {line_number}: duplicate key {key!r}")
        current[key] = _parse_scalar(value_text, line_number)
    return root


def _read_toml(path):
    try:
        content = Path(path).read_bytes()
    except OSError as exc:
        raise NetworkError(f"cannot read {path}: {exc}") from exc
    try:
        if tomllib is not None:
            return tomllib.loads(content.decode("utf-8"))
        return _parse_toml_subset(content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise NetworkError(f"invalid TOML in {path}: {exc}") from exc


def _unknown(data, allowed, context):
    extras = sorted(set(data) - set(allowed))
    if extras:
        raise NetworkError(f"{context} contains unsupported fields: {', '.join(extras)}")


def _string(data, key, context, required=True, default=None):
    value = data.get(key, default)
    if value is None and not required:
        return None
    if not isinstance(value, str) or not value.strip():
        raise NetworkError(f"{context}.{key} must be a non-empty string")
    return value


def _number(data, key, context, required=True, default=None):
    value = data.get(key, default)
    if value is None and not required:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise NetworkError(f"{context}.{key} must be a finite number")
    return float(value)


def _duplicates(values):
    return sorted(value for value, count in Counter(values).items() if count > 1)


def load_network(path):
    raw = _read_toml(path)
    if not isinstance(raw, dict):
        raise NetworkError("TOML root must be a table")
    _unknown(raw, {"schema_version", "network", "solver", "nodes", "edges", "scenarios"}, "root")
    if raw.get("schema_version") != "1.0":
        raise NetworkError("schema_version must be '1.0'")

    metadata = raw.get("network")
    if not isinstance(metadata, dict):
        raise NetworkError("network must be a table")
    _unknown(metadata, {"id", "name", "pressure_reference", "units_system"}, "network")
    if metadata.get("pressure_reference") != "gauge":
        raise NetworkError("network.pressure_reference must be 'gauge'")
    if metadata.get("units_system") != "SI":
        raise NetworkError("network.units_system must be 'SI'")

    solver_raw = raw.get("solver", {})
    if not isinstance(solver_raw, dict):
        raise NetworkError("solver must be a table")
    _unknown(solver_raw, {"residual_tolerance_m3_s", "max_nfev"}, "solver")
    tolerance = _number(solver_raw, "residual_tolerance_m3_s", "solver", False, 1e-8)
    max_nfev = solver_raw.get("max_nfev", 1000)
    if tolerance <= 0:
        raise NetworkError("solver.residual_tolerance_m3_s must be greater than zero")
    if isinstance(max_nfev, bool) or not isinstance(max_nfev, int) or max_nfev <= 0:
        raise NetworkError("solver.max_nfev must be a positive integer")

    nodes_raw = raw.get("nodes")
    edges_raw = raw.get("edges")
    scenarios_raw = raw.get("scenarios", [])
    if not isinstance(nodes_raw, list) or not nodes_raw:
        raise NetworkError("nodes must be a non-empty array of tables")
    if not isinstance(edges_raw, list):
        raise NetworkError("edges must be an array of tables")
    if not isinstance(scenarios_raw, list):
        raise NetworkError("scenarios must be an array of tables")

    errors = []
    nodes = []
    node_fields = {
        "id", "kind", "pressure_pa", "boundary_role", "function_id",
        "measurement_edge_id", "min_inlet_pressure_pa", "min_flow_m3_s",
    }
    for index, item in enumerate(nodes_raw):
        context = f"nodes[{index}]"
        if not isinstance(item, dict):
            raise NetworkError(f"{context} must be a table")
        _unknown(item, node_fields, context)
        node = {
            "id": _string(item, "id", context),
            "kind": _string(item, "kind", context),
            "pressure_pa": _number(item, "pressure_pa", context, False),
            "boundary_role": _string(item, "boundary_role", context, False),
            "function_id": _string(item, "function_id", context, False),
            "measurement_edge_id": _string(item, "measurement_edge_id", context, False),
            "min_inlet_pressure_pa": _number(item, "min_inlet_pressure_pa", context, False),
            "min_flow_m3_s": _number(item, "min_flow_m3_s", context, False),
        }
        nodes.append(node)

    edges = []
    edge_fields = {
        "id", "from", "to", "kind", "resistance_model", "resistance",
        "diameter_m", "fixed_head_pa", "enabled",
    }
    for index, item in enumerate(edges_raw):
        context = f"edges[{index}]"
        if not isinstance(item, dict):
            raise NetworkError(f"{context} must be a table")
        _unknown(item, edge_fields, context)
        enabled = item.get("enabled", True)
        if not isinstance(enabled, bool):
            raise NetworkError(f"{context}.enabled must be true or false")
        edge = {
            "id": _string(item, "id", context),
            "from": _string(item, "from", context),
            "to": _string(item, "to", context),
            "kind": _string(item, "kind", context),
            "resistance_model": _string(item, "resistance_model", context),
            "resistance": _number(item, "resistance", context),
            "diameter_m": _number(item, "diameter_m", context, False),
            "fixed_head_pa": _number(item, "fixed_head_pa", context, False, 0.0),
            "enabled": enabled,
        }
        edges.append(edge)

    scenarios = []
    for index, item in enumerate(scenarios_raw):
        context = f"scenarios[{index}]"
        if not isinstance(item, dict):
            raise NetworkError(f"{context} must be a table")
        _unknown(item, {"id", "description", "actions"}, context)
        actions_raw = item.get("actions", [])
        if not isinstance(actions_raw, list):
            raise NetworkError(f"{context}.actions must be an array of tables")
        actions = []
        for action_index, action_raw in enumerate(actions_raw):
            action_context = f"{context}.actions[{action_index}]"
            if not isinstance(action_raw, dict):
                raise NetworkError(f"{action_context} must be a table")
            _unknown(action_raw, {"target_type", "target_id", "attribute", "value"}, action_context)
            value = action_raw.get("value")
            if not isinstance(value, bool):
                raise NetworkError(f"{action_context}.value must be true or false")
            actions.append({
                "target_type": _string(action_raw, "target_type", action_context),
                "target_id": _string(action_raw, "target_id", action_context),
                "attribute": _string(action_raw, "attribute", action_context),
                "value": value,
            })
        description = item.get("description", "")
        if not isinstance(description, str):
            raise NetworkError(f"{context}.description must be a string")
        scenarios.append({"id": _string(item, "id", context), "description": description, "actions": actions})

    for duplicate in _duplicates(node["id"] for node in nodes):
        errors.append(f"duplicate node id: {duplicate}")
    for duplicate in _duplicates(edge["id"] for edge in edges):
        errors.append(f"duplicate edge id: {duplicate}")
    for duplicate in _duplicates(scenario["id"] for scenario in scenarios):
        errors.append(f"duplicate scenario id: {duplicate}")
    if any(scenario["id"] == "base" for scenario in scenarios):
        errors.append("scenario id 'base' is reserved")

    node_ids = {node["id"] for node in nodes}
    edge_ids = {edge["id"] for edge in edges}
    edge_by_id = {edge["id"]: edge for edge in edges}
    function_ids = []
    has_source = False
    for node in nodes:
        context = f"node {node['id']!r}"
        if node["kind"] not in {"pressure_boundary", "junction", "load"}:
            errors.append(f"{context} has unsupported kind {node['kind']!r}")
        if node["kind"] == "pressure_boundary":
            if node["pressure_pa"] is None:
                errors.append(f"{context} requires pressure_pa")
            if node["boundary_role"] not in {"source", "sink"}:
                errors.append(f"{context} requires boundary_role 'source' or 'sink'")
            has_source = has_source or node["boundary_role"] == "source"
        elif node["pressure_pa"] is not None or node["boundary_role"] is not None:
            errors.append(f"{context} may not define pressure boundary fields")
        if node["kind"] == "load":
            for field in ("function_id", "measurement_edge_id", "min_inlet_pressure_pa", "min_flow_m3_s"):
                if node[field] is None:
                    errors.append(f"{context} requires {field}")
            if node["function_id"]:
                function_ids.append(node["function_id"])
            if node["min_flow_m3_s"] is not None and node["min_flow_m3_s"] < 0:
                errors.append(f"{context} min_flow_m3_s must be non-negative")
        elif any(node[field] is not None for field in ("function_id", "measurement_edge_id", "min_inlet_pressure_pa", "min_flow_m3_s")):
            errors.append(f"{context} may not define load-only fields")
    if not has_source:
        errors.append("network requires at least one source pressure boundary")
    for duplicate in _duplicates(function_ids):
        errors.append(f"duplicate function_id: {duplicate}")

    for edge in edges:
        context = f"edge {edge['id']!r}"
        if edge["kind"] not in {"pipe", "valve", "pump"}:
            errors.append(f"{context} has unsupported kind {edge['kind']!r}")
        if edge["resistance_model"] not in {"linear", "quadratic"}:
            errors.append(f"{context} has unsupported resistance_model")
        if edge["from"] not in node_ids or edge["to"] not in node_ids:
            errors.append(f"{context} references an unknown node")
        if edge["from"] == edge["to"]:
            errors.append(f"{context} may not be a self-loop")
        if edge["resistance"] <= 0:
            errors.append(f"{context} resistance must be positive")
        if edge["kind"] in {"pipe", "valve"} and (edge["diameter_m"] is None or edge["diameter_m"] <= 0):
            errors.append(f"{context} requires positive diameter_m")
        if edge["kind"] == "pump" and edge["fixed_head_pa"] <= 0:
            errors.append(f"{context} requires positive fixed_head_pa")
        if edge["kind"] != "pump" and edge["fixed_head_pa"] != 0:
            errors.append(f"{context} may define fixed_head_pa only for a pump")

    for node in nodes:
        if node["kind"] != "load" or not node["measurement_edge_id"]:
            continue
        measurement = edge_by_id.get(node["measurement_edge_id"])
        if measurement is None:
            errors.append(f"load {node['id']!r} references an unknown measurement edge")
        elif node["id"] not in {measurement["from"], measurement["to"]}:
            errors.append(f"load {node['id']!r} measurement edge is not incident to the load")

    for scenario in scenarios:
        seen = set()
        for action in scenario["actions"]:
            key = (action["target_type"], action["target_id"], action["attribute"])
            if key in seen:
                errors.append(f"scenario {scenario['id']!r} contains a duplicate action")
            seen.add(key)
            if action["target_type"] != "edge" or action["attribute"] != "enabled":
                errors.append(f"scenario {scenario['id']!r} supports only edge.enabled actions")
            if action["target_id"] not in edge_ids:
                errors.append(f"scenario {scenario['id']!r} references an unknown edge")

    if errors:
        raise NetworkError("network validation failed:\n- " + "\n- ".join(errors))
    return {
        "id": _string(metadata, "id", "network"),
        "name": _string(metadata, "name", "network"),
        "schema_version": "1.0",
        "nodes": {node["id"]: node for node in nodes},
        "edges": {edge["id"]: edge for edge in edges},
        "scenarios": {scenario["id"]: scenario for scenario in scenarios},
        "solver": {"tolerance": tolerance, "max_nfev": max_nfev},
    }


def _scenario(network, scenario_id):
    if scenario_id in {None, "base"}:
        return None
    if scenario_id not in network["scenarios"]:
        known = ", ".join(network["scenarios"]) or "none"
        raise NetworkError(f"unknown scenario {scenario_id!r}; declared scenarios: {known}")
    return network["scenarios"][scenario_id]


def _enabled_state(network, scenario_id):
    state = {edge_id: edge["enabled"] for edge_id, edge in network["edges"].items()}
    selected = _scenario(network, scenario_id)
    if selected:
        for action in selected["actions"]:
            state[action["target_id"]] = action["value"]
    return state


def _adjacency(network, enabled):
    graph = {node_id: set() for node_id in network["nodes"]}
    for edge in network["edges"].values():
        if enabled[edge["id"]]:
            graph[edge["from"]].add(edge["to"])
            graph[edge["to"]].add(edge["from"])
    return graph


def _components(network, enabled):
    graph = _adjacency(network, enabled)
    unseen = set(graph)
    output = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        component = set()
        while queue:
            current = queue.popleft()
            component.add(current)
            for neighbor in graph[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        output.append(component)
    return output


def _edge_flow(edge, from_pressure, to_pressure):
    delta = from_pressure - to_pressure + edge["fixed_head_pa"]
    if edge["resistance_model"] == "linear":
        return delta / edge["resistance"]
    if delta == 0:
        return 0.0
    return math.copysign(math.sqrt(abs(delta) / edge["resistance"]), delta)


def _flow_gradient(edge, from_pressure, to_pressure):
    if edge["resistance_model"] == "linear":
        return 1.0 / edge["resistance"]
    delta = abs(from_pressure - to_pressure + edge["fixed_head_pa"])
    delta = max(delta, 1e-6)
    return 1.0 / (2.0 * math.sqrt(edge["resistance"] * delta))


def _residual_jacobian(network, enabled, pressures, unknown_ids):
    index = {node_id: position for position, node_id in enumerate(unknown_ids)}
    residual = [0.0 for _ in unknown_ids]
    jacobian = [[0.0 for _ in unknown_ids] for _ in unknown_ids]
    for edge in network["edges"].values():
        if not enabled[edge["id"]] or edge["from"] not in pressures or edge["to"] not in pressures:
            continue
        flow = _edge_flow(edge, pressures[edge["from"]], pressures[edge["to"]])
        gradient = _flow_gradient(edge, pressures[edge["from"]], pressures[edge["to"]])
        for node_id, sign in ((edge["from"], 1.0), (edge["to"], -1.0)):
            if node_id not in index:
                continue
            row = index[node_id]
            residual[row] += sign * flow
            if edge["from"] in index:
                jacobian[row][index[edge["from"]]] += sign * gradient
            if edge["to"] in index:
                jacobian[row][index[edge["to"]]] -= sign * gradient
    return residual, jacobian


def _solve_dense(matrix, vector):
    size = len(vector)
    augmented = [list(matrix[row]) + [float(vector[row])] for row in range(size)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-30:
            raise NetworkError("hydraulic Jacobian is singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        for item in range(column, size + 1):
            augmented[column][item] /= pivot_value
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            for item in range(column, size + 1):
                augmented[row][item] -= factor * augmented[column][item]
    return [augmented[row][size] for row in range(size)]


def solve_network(network, scenario_id=None):
    selected_id = scenario_id or "base"
    enabled = _enabled_state(network, scenario_id)
    components = _components(network, enabled)
    anchored = set()
    component_pressure = {}
    for component in components:
        boundaries = [
            network["nodes"][node_id]["pressure_pa"]
            for node_id in component
            if network["nodes"][node_id]["kind"] == "pressure_boundary"
        ]
        if boundaries:
            anchored.update(component)
            average = sum(boundaries) / len(boundaries)
            for node_id in component:
                component_pressure[node_id] = average
    unknown_ids = sorted(
        node_id for node_id in anchored if network["nodes"][node_id]["kind"] != "pressure_boundary"
    )
    pressures = {
        node_id: float(node["pressure_pa"])
        for node_id, node in network["nodes"].items()
        if node_id in anchored and node["kind"] == "pressure_boundary"
    }
    pressures.update({node_id: component_pressure[node_id] for node_id in unknown_ids})
    active_edges = [
        edge for edge in network["edges"].values()
        if enabled[edge["id"]] and edge["from"] in anchored and edge["to"] in anchored
    ]
    linear = all(edge["resistance_model"] == "linear" for edge in active_edges)
    tolerance = network["solver"]["tolerance"]
    converged = not unknown_ids
    message = "no unknown node pressures"
    max_residual = 0.0

    if unknown_ids:
        max_iterations = 1 if linear else min(200, network["solver"]["max_nfev"])
        message = "maximum iterations reached"
        for _ in range(max_iterations):
            residual, jacobian = _residual_jacobian(network, enabled, pressures, unknown_ids)
            max_residual = max(abs(value) for value in residual)
            if max_residual <= tolerance:
                converged = True
                message = "linear solve completed" if linear else "nonlinear solve converged"
                break
            try:
                step = _solve_dense(jacobian, [-value for value in residual])
            except NetworkError as exc:
                message = str(exc)
                break
            baseline = max_residual
            accepted = False
            scale = 1.0
            original = [pressures[node_id] for node_id in unknown_ids]
            for _ in range(24):
                for index, node_id in enumerate(unknown_ids):
                    pressures[node_id] = original[index] + scale * step[index]
                candidate, _ = _residual_jacobian(network, enabled, pressures, unknown_ids)
                candidate_max = max(abs(value) for value in candidate)
                if candidate_max < baseline:
                    accepted = True
                    break
                scale *= 0.5
            if not accepted:
                for index, node_id in enumerate(unknown_ids):
                    pressures[node_id] = original[index]
                message = "nonlinear line search failed"
                break
        residual, _ = _residual_jacobian(network, enabled, pressures, unknown_ids)
        max_residual = max(abs(value) for value in residual)
        if max_residual <= tolerance:
            converged = True
            message = "linear solve completed" if linear else "nonlinear solve converged"

    node_results = {}
    for node_id, node in network["nodes"].items():
        if node_id not in pressures:
            status, pressure = "ISOLATED", None
        elif node["kind"] == "pressure_boundary":
            status, pressure = "FIXED", pressures[node_id]
        elif converged:
            status, pressure = "SOLVED", pressures[node_id]
        else:
            status, pressure = "UNRESOLVED", None
        node_results[node_id] = {"id": node_id, "status": status, "pressure_pa": pressure}

    edge_results = {}
    for edge_id, edge in network["edges"].items():
        if not enabled[edge_id]:
            flow = 0.0
            velocity = 0.0 if edge["diameter_m"] else None
        elif converged and edge["from"] in pressures and edge["to"] in pressures:
            flow = _edge_flow(edge, pressures[edge["from"]], pressures[edge["to"]])
            velocity = None
            if edge["diameter_m"]:
                area = math.pi * edge["diameter_m"] ** 2 / 4.0
                velocity = flow / area
        else:
            flow = velocity = None
        edge_results[edge_id] = {
            "id": edge_id, "enabled": enabled[edge_id], "flow_m3_s": flow, "velocity_m_s": velocity
        }
    return {
        "scenario_id": selected_id,
        "status": "SUCCESS" if converged else "SOLVER_FAILED",
        "converged": converged,
        "message": message,
        "max_residual_m3_s": max_residual,
        "node_results": node_results,
        "edge_results": edge_results,
    }


def analyze_scenario(network, scenario_id=None):
    selected = _scenario(network, scenario_id)
    enabled = _enabled_state(network, scenario_id)
    graph = _adjacency(network, enabled)
    sources = [
        node_id for node_id, node in network["nodes"].items()
        if node["kind"] == "pressure_boundary" and node["boundary_role"] == "source"
    ]
    reached = set(sources)
    queue = deque(sources)
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    solve = solve_network(network, scenario_id)
    functions = {}
    for load in sorted(
        (node for node in network["nodes"].values() if node["kind"] == "load"),
        key=lambda node: node["id"],
    ):
        connected = load["id"] in reached
        pressure = solve["node_results"][load["id"]]["pressure_pa"]
        raw_flow = solve["edge_results"][load["measurement_edge_id"]]["flow_m3_s"]
        measured_flow = None if raw_flow is None else abs(raw_flow)
        reasons = []
        if not solve["converged"]:
            status = "SOLVER_FAILED"
            reasons.append(solve["message"])
        elif not connected:
            status = "UNSERVED"
            reasons.append("load is not connected to an enabled source boundary")
        else:
            if pressure is None or pressure < load["min_inlet_pressure_pa"]:
                reasons.append("inlet pressure is below its threshold")
            if measured_flow is None or measured_flow < load["min_flow_m3_s"]:
                reasons.append("measured flow is below its threshold")
            status = "PASS" if not reasons else "FAIL"
        functions[load["function_id"]] = {
            "function_id": load["function_id"],
            "load_node_id": load["id"],
            "status": status,
            "connected_to_source": connected,
            "inlet_pressure_pa": pressure,
            "measured_flow_m3_s": measured_flow,
            "min_inlet_pressure_pa": load["min_inlet_pressure_pa"],
            "min_flow_m3_s": load["min_flow_m3_s"],
            "reasons": reasons,
        }
    return {
        "scenario_id": scenario_id or "base",
        "description": "base state" if selected is None else selected["description"],
        "solve": solve,
        "functions": functions,
    }


def _format_number(value):
    return "—" if value is None else f"{value:.6g}"


def markdown_report(network, analyses):
    lines = [
        f"# Fluid network report: {network['name']}", "",
        f"- Network ID: `{network['id']}`", "- Pressure: Pa gauge", "- Flow: m3/s", "",
    ]
    for analysis in analyses:
        solve = analysis["solve"]
        lines.extend([
            f"## Scenario `{analysis['scenario_id']}`", "", analysis["description"] or "No description", "",
            f"Solver: **{solve['status']}**; max residual: `{_format_number(solve['max_residual_m3_s'])} m3/s`.", "",
            "| Function | Status | Source connected | Inlet pressure Pa | Flow m3/s | Notes |",
            "|---|---|---:|---:|---:|---|",
        ])
        for function in analysis["functions"].values():
            notes = "; ".join(function["reasons"]) or "all criteria met"
            lines.append(
                f"| `{function['function_id']}` | **{function['status']}** | "
                f"{'yes' if function['connected_to_source'] else 'no'} | "
                f"{_format_number(function['inlet_pressure_pa'])} | "
                f"{_format_number(function['measured_flow_m3_s'])} | {notes} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_parser():
    parser = argparse.ArgumentParser(prog="fluid_network.py")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("file")
    solve = commands.add_parser("solve")
    solve.add_argument("file")
    solve.add_argument("--scenario")
    solve.add_argument("--format", choices=("json", "markdown"), default="json")
    analyze = commands.add_parser("analyze")
    analyze.add_argument("file")
    analyze.add_argument("--scenario")
    analyze.add_argument("--format", choices=("json", "markdown"), default="markdown")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        network = load_network(args.file)
        if args.command == "validate":
            print(f"VALID: {network['id']} (schema {network['schema_version']})")
            return 0
        if args.command == "solve":
            solve = solve_network(network, args.scenario)
            if args.format == "json":
                print(json.dumps(solve, ensure_ascii=False, indent=2))
            else:
                print(markdown_report(network, [analyze_scenario(network, args.scenario)]), end="")
            return 0 if solve["converged"] else 1
        scenario_ids = [args.scenario] if args.scenario else (list(network["scenarios"]) or [None])
        analyses = [analyze_scenario(network, scenario_id) for scenario_id in scenario_ids]
        if args.format == "json":
            payload = {
                "network": {"id": network["id"], "name": network["name"], "schema_version": "1.0"},
                "scenarios": analyses,
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(markdown_report(network, analyses), end="")
        return 0 if all(item["solve"]["converged"] for item in analyses) else 1
    except NetworkError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
