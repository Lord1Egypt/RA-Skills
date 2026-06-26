# TOML Schema (Steady Incompressible Fluid Network)

TOML 文件需要包含下面信息：

1. Nodes (junctions + fixed-pressure reservoirs)
2. Edges (pipes/links with a resistance model)
3. Scenarios (finite switch/fault variable assignments)
4. Functions (how to judge reliability at one or more load nodes)

## Units

All pressure values use `Pa`, flow uses `m3/s`, and resistance coefficients must be consistent with the chosen flow/pressure relationship:

- `linear`: `dP = R * Q`
- `quadratic`: `dP = R * Q^2`

Velocity is computed only when an edge provides `area_m2` or `diameter_m`.

## Top-level keys

- `nodes`: `[[nodes]]` array of node objects
- `edges`: `[[edges]]` array of edge objects
- `scenarios`: optional `[[scenarios]]` array
- `functions`: optional `[[functions]]` array
- `analysis`: optional object
- `source_node_ids`: optional array of node ids used for connectivity BFS

## Nodes

### Junction (unknown pressure)

```toml
[[nodes]]
id = "J1"
kind = "junction"
role = "load" # optional: only meaningful for reliability checks
min_flow_m3s = 0.01 # required when role == "load"
min_pressure_pa = 2.0e5 # required when role == "load"
```

### Reservoir (fixed pressure)

```toml
[[nodes]]
id = "S"
kind = "reservoir"
role = "source" # optional
pressure_pa = 3.0e6
```

## Edges

Edges connect `from` -> `to` node ids and carry resistance.

### Simple pipe (always enabled)

```toml
[[edges]]
id = "E1"
from = "S"
to = "J1"

[edges.resistance_model]
kind = "linear" # or "quadratic"
R = 1.25e7

diameter_m = 0.02 # optional (for velocity)
```

### Scenario-gated edge (switch/fault dependent)

If `gating` disables an edge, the solver multiplies resistance by `disabled_resistance_multiplier`
to emulate a blocked path.

```toml
[[edges]]
id = "V1"
from = "J1"
to = "L1"

[edges.resistance_model]
kind = "quadratic"
R = 8.0e10

[edges.gating]
enabled_when_mode = "all"
disabled_resistance_multiplier = 1e12

[[edges.gating.conditions]]
variable = "valve_v1"
equals = "open"
```

## Scenarios

Scenarios are finite combinations of variables (switch states, fault flags, etc.).

```toml
[[scenarios]]
id = "normal"

[scenarios.variables]
valve_v1 = "open"
```

Optional pressure overrides per scenario:

```toml
[[scenarios]]
id = "leak_case"

[scenarios.variables]
valve_v1 = "open"

[scenarios.reservoir_pressure_overrides_pa]
S = 2.8e6
```

## Functions (reliability criteria)

Each function is defined as a set of load nodes and whether all or any of them must pass.

```toml
[[functions]]
id = "cooling_loop"
load_node_ids = ["L1", "L2"]
criteria_mode = "all" # or "any"
```

If `functions` is omitted, each load node becomes its own function automatically.

## analysis

```toml
[analysis]
flow_metric = "abs" # abs or inflow
topology_direction = "undirected" # or "from_to"
```

## Minimal complete example

See `examples/example_network.toml`.

