from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

try:
    from scipy.optimize import fsolve
except ModuleNotFoundError:  # pragma: no cover
    fsolve = None  # type: ignore[assignment]

try:
    from .models import PipeState, SolverResult, SystemConfig
except ImportError:  # pragma: no cover
    from models import PipeState, SolverResult, SystemConfig


EPS = 1e-12
PRESSURE_ZERO_TOLERANCE = 1e-5
FLOW_ZERO_TOLERANCE = 1e-12


class SolveError(RuntimeError):
    """Raised when the nonlinear hydraulic equations cannot be solved."""


@dataclass(slots=True)
class _VariableLayout:
    variable_node_ids: list[str]
    active_pipe_ids: list[str]
    fixed_pressures: dict[str, float]


def solve_system(
    config: SystemConfig,
    *,
    scenario_name: str = "base",
    tolerance: float = 1e-8,
    max_iterations: int = 400,
) -> SolverResult:
    """Solve the steady-state pressure and flow field for a network snapshot."""

    layout = _build_variable_layout(config)
    _validate_pressure_boundaries(config, layout)

    x0 = _build_initial_guess(config, layout)
    residual_fn = _make_residual_function(config, layout)

    if not x0:
        solution = []
        converged = True
        method = "trivial"
        message = "No unknown variables remained after boundary conditions were applied."
        iterations = 0
    elif fsolve is not None:
        solution, converged, message, iterations = _solve_with_fsolve(
            residual_fn,
            x0,
            tolerance=tolerance,
            max_iterations=max_iterations,
        )
        method = "scipy.optimize.fsolve"
        if not converged:
            solution, converged, message, iterations = _solve_with_damped_newton(
                residual_fn,
                x0,
                tolerance=tolerance,
                max_iterations=max_iterations,
            )
            method = "damped_newton_fallback"
    else:
        solution, converged, message, iterations = _solve_with_damped_newton(
            residual_fn,
            x0,
            tolerance=tolerance,
            max_iterations=max_iterations,
        )
        method = "damped_newton_fallback"

    node_pressures, pipe_flows = _decode_state(solution, config, layout)
    residual_norm = _compute_residual_norm(residual_fn(solution))
    pipe_states = _build_pipe_states(config, node_pressures, pipe_flows)

    if not converged and residual_norm > max(tolerance * 10.0, 1e-6):
        raise SolveError(f"Solver failed to converge for scenario '{scenario_name}': {message}")

    return SolverResult(
        scenario_name=scenario_name,
        converged=converged,
        method=method,
        message=message,
        iterations=iterations,
        residual_norm=residual_norm,
        node_pressures=node_pressures,
        pipe_states=pipe_states,
    )


def _build_variable_layout(config: SystemConfig) -> _VariableLayout:
    variable_node_ids: list[str] = []
    active_pipe_ids: list[str] = []
    fixed_pressures: dict[str, float] = {}

    for node in config.nodes.values():
        if not node.enabled:
            continue
        if node.fixed_pressure is None:
            variable_node_ids.append(node.id)
        else:
            fixed_pressures[node.id] = float(node.fixed_pressure)

    for pipe_id in config.pipes:
        if _pipe_is_active(pipe_id, config):
            active_pipe_ids.append(pipe_id)

    return _VariableLayout(
        variable_node_ids=variable_node_ids,
        active_pipe_ids=active_pipe_ids,
        fixed_pressures=fixed_pressures,
    )


def _validate_pressure_boundaries(config: SystemConfig, layout: _VariableLayout) -> None:
    if not layout.fixed_pressures:
        raise SolveError("At least one enabled node must define fixed_pressure.")

    adjacency: dict[str, set[str]] = {
        node_id: set()
        for node_id, node in config.nodes.items()
        if node.enabled
    }
    for pipe_id in layout.active_pipe_ids:
        pipe = config.pipes[pipe_id]
        adjacency[pipe.source].add(pipe.target)
        adjacency[pipe.target].add(pipe.source)

    visited: set[str] = set()
    for node_id in adjacency:
        if node_id in visited:
            continue
        stack = [node_id]
        component: set[str] = set()
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            component.add(current)
            stack.extend(adjacency[current] - visited)

        has_variable = any(current in layout.variable_node_ids for current in component)
        has_boundary = any(current in layout.fixed_pressures for current in component)
        if has_variable and not has_boundary:
            raise SolveError(
                "Each enabled connected component must contain at least one fixed-pressure boundary. "
                f"Component without boundary: {sorted(component)}"
            )


def _build_initial_guess(config: SystemConfig, layout: _VariableLayout) -> list[float]:
    if not layout.variable_node_ids and not layout.active_pipe_ids:
        return []

    average_pressure = sum(layout.fixed_pressures.values()) / len(layout.fixed_pressures)
    node_guess = [average_pressure for _ in layout.variable_node_ids]
    pressures = dict(layout.fixed_pressures)
    pressures.update(dict(zip(layout.variable_node_ids, node_guess, strict=False)))

    flow_guess: list[float] = []
    for pipe_id in layout.active_pipe_ids:
        pipe = config.pipes[pipe_id]
        source_pressure = pressures.get(pipe.source, average_pressure)
        target_pressure = pressures.get(pipe.target, average_pressure)
        delta_p = source_pressure - target_pressure
        if abs(delta_p) < EPS:
            flow_guess.append(0.0)
        else:
            flow_guess.append(math.copysign(math.sqrt(abs(delta_p) / pipe.resistance), delta_p))

    return node_guess + flow_guess


def _make_residual_function(
    config: SystemConfig,
    layout: _VariableLayout,
) -> Callable[[list[float]], list[float]]:
    active_pipe_ids = layout.active_pipe_ids
    variable_node_ids = layout.variable_node_ids
    pressure_scale = max((abs(value) for value in layout.fixed_pressures.values()), default=1.0)
    pressure_scale = max(pressure_scale, 1.0)
    flow_scale = max((_estimate_pipe_flow_scale(config, pipe_id) for pipe_id in active_pipe_ids), default=1e-3)
    flow_scale = max(flow_scale, 1e-3)

    def residuals(vector: list[float]) -> list[float]:
        node_pressures, pipe_flows = _decode_state(vector, config, layout)
        residual_values: list[float] = []

        for pipe_id in active_pipe_ids:
            pipe = config.pipes[pipe_id]
            source_pressure = node_pressures[pipe.source]
            target_pressure = node_pressures[pipe.target]
            flow = pipe_flows[pipe_id]
            residual_values.append(
                (source_pressure - target_pressure - pipe.resistance * flow * abs(flow)) / pressure_scale
            )

        for node_id in variable_node_ids:
            node = config.nodes[node_id]
            inflow = 0.0
            outflow = 0.0
            for pipe_id in active_pipe_ids:
                pipe = config.pipes[pipe_id]
                flow = pipe_flows[pipe_id]
                if pipe.target == node_id:
                    inflow += flow
                if pipe.source == node_id:
                    outflow += flow
            residual_values.append((inflow - outflow + node.external_flow) / flow_scale)

        return residual_values

    return residuals


def _decode_state(
    vector: list[float],
    config: SystemConfig,
    layout: _VariableLayout,
) -> tuple[dict[str, float], dict[str, float]]:
    node_pressures = {node_id: 0.0 for node_id in config.nodes}
    node_pressures.update(layout.fixed_pressures)

    node_count = len(layout.variable_node_ids)
    pressure_values = vector[:node_count]
    flow_values = vector[node_count:]

    for node_id, pressure in zip(layout.variable_node_ids, pressure_values, strict=False):
        node_pressures[node_id] = _cleanup_small_value(float(pressure), PRESSURE_ZERO_TOLERANCE)

    pipe_flows = {pipe_id: 0.0 for pipe_id in config.pipes}
    for pipe_id, flow in zip(layout.active_pipe_ids, flow_values, strict=False):
        pipe_flows[pipe_id] = _cleanup_small_value(float(flow), FLOW_ZERO_TOLERANCE)

    return node_pressures, pipe_flows


def _build_pipe_states(
    config: SystemConfig,
    node_pressures: dict[str, float],
    pipe_flows: dict[str, float],
) -> dict[str, PipeState]:
    pipe_states: dict[str, PipeState] = {}
    for pipe_id, pipe in config.pipes.items():
        active = _pipe_is_active(pipe_id, config)
        flow = pipe_flows.get(pipe_id, 0.0) if active else 0.0
        pressure_drop = node_pressures[pipe.source] - node_pressures[pipe.target]
        velocity = None
        if pipe.diameter is not None:
            area = math.pi * (pipe.diameter ** 2) / 4.0
            velocity = flow / area
        pipe_states[pipe_id] = PipeState(
            flow=flow,
            velocity=velocity,
            pressure_drop=pressure_drop,
            active=active,
        )
    return pipe_states


def _solve_with_fsolve(
    residual_fn: Callable[[list[float]], list[float]],
    x0: list[float],
    *,
    tolerance: float,
    max_iterations: int,
) -> tuple[list[float], bool, str, int]:
    solution, info, ier, message = fsolve(  # type: ignore[misc]
        func=residual_fn,
        x0=x0,
        full_output=True,
        xtol=tolerance,
        maxfev=max_iterations,
    )
    return list(solution), ier == 1, str(message), int(info.get("nfev", 0))


def _solve_with_damped_newton(
    residual_fn: Callable[[list[float]], list[float]],
    x0: list[float],
    *,
    tolerance: float,
    max_iterations: int,
) -> tuple[list[float], bool, str, int]:
    x = list(x0)
    for iteration in range(1, max_iterations + 1):
        residual = residual_fn(x)
        current_norm = _compute_residual_norm(residual)
        if current_norm < tolerance:
            return x, True, "Damped Newton converged.", iteration

        jacobian = _finite_difference_jacobian(residual_fn, x)
        try:
            step = _solve_linear_system(jacobian, [-value for value in residual])
        except SolveError as exc:
            return x, False, str(exc), iteration

        damping = 1.0
        accepted = False
        while damping >= 1e-4:
            trial = [value + damping * delta for value, delta in zip(x, step, strict=False)]
            trial_norm = _compute_residual_norm(residual_fn(trial))
            if trial_norm < current_norm:
                x = trial
                accepted = True
                break
            damping *= 0.5
        if not accepted:
            x = [value + delta for value, delta in zip(x, step, strict=False)]

    return x, False, "Damped Newton reached the iteration limit.", max_iterations


def _finite_difference_jacobian(
    residual_fn: Callable[[list[float]], list[float]],
    x: list[float],
) -> list[list[float]]:
    if not x:
        return []

    base_length = len(x)
    jacobian = [[0.0 for _ in range(base_length)] for _ in range(base_length)]
    for column in range(base_length):
        step = 1e-6 * max(1.0, abs(x[column]))
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[column] += step
        x_minus[column] -= step
        residual_plus = residual_fn(x_plus)
        residual_minus = residual_fn(x_minus)
        for row in range(base_length):
            jacobian[row][column] = (residual_plus[row] - residual_minus[row]) / (2.0 * step)
    return jacobian


def _solve_linear_system(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    size = len(rhs)
    if size == 0:
        return []

    a = [row[:] for row in matrix]
    b = rhs[:]

    for column in range(size):
        pivot = max(range(column, size), key=lambda index: abs(a[index][column]))
        if abs(a[pivot][column]) < EPS:
            raise SolveError("Encountered a singular Jacobian matrix.")
        if pivot != column:
            a[column], a[pivot] = a[pivot], a[column]
            b[column], b[pivot] = b[pivot], b[column]

        pivot_value = a[column][column]
        for row in range(column + 1, size):
            factor = a[row][column] / pivot_value
            if abs(factor) < EPS:
                continue
            for inner in range(column, size):
                a[row][inner] -= factor * a[column][inner]
            b[row] -= factor * b[column]

    solution = [0.0 for _ in range(size)]
    for row in range(size - 1, -1, -1):
        accumulator = b[row]
        for column in range(row + 1, size):
            accumulator -= a[row][column] * solution[column]
        solution[row] = accumulator / a[row][row]
    return solution


def _pipe_is_active(pipe_id: str, config: SystemConfig) -> bool:
    pipe = config.pipes[pipe_id]
    return (
        pipe.enabled
        and pipe.valve_open
        and config.nodes[pipe.source].enabled
        and config.nodes[pipe.target].enabled
    )


def _compute_residual_norm(values: list[float]) -> float:
    return max((abs(value) for value in values), default=0.0)


def _estimate_pipe_flow_scale(config: SystemConfig, pipe_id: str) -> float:
    pipe = config.pipes[pipe_id]
    source_node = config.nodes[pipe.source]
    target_node = config.nodes[pipe.target]
    delta_p = 0.0
    if source_node.fixed_pressure is not None and target_node.fixed_pressure is not None:
        delta_p = source_node.fixed_pressure - target_node.fixed_pressure
    elif source_node.fixed_pressure is not None:
        delta_p = source_node.fixed_pressure
    elif target_node.fixed_pressure is not None:
        delta_p = -target_node.fixed_pressure
    if abs(delta_p) < EPS:
        return 1e-3
    return math.sqrt(abs(delta_p) / pipe.resistance)


def _cleanup_small_value(value: float, zero_tolerance: float) -> float:
    if abs(value) < zero_tolerance:
        return 0.0
    return value
