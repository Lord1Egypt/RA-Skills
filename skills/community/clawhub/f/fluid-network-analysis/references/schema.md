# TOML Schema 1.0 Reference

The bundled runtime uses Python's standard `tomllib` on Python 3.11 and newer. On Python 3.9–3.10 it accepts the schema's required TOML subset: scalar strings, finite numbers, booleans, ordinary tables, arrays of tables, comments, and the nested `scenarios.actions` array. Multiline strings, datetime values, inline tables, and arbitrary arrays are outside schema 1.0 and should not be used.

## Required root tables

```toml
schema_version = "1.0"

[network]
id = "network-id"
name = "Readable name"
pressure_reference = "gauge"
units_system = "SI"

[solver]
residual_tolerance_m3_s = 1.0e-8
max_nfev = 1000
```

`solver` is optional and uses the displayed defaults.

## Nodes

Fixed source or sink:

```toml
[[nodes]]
id = "source"
kind = "pressure_boundary"
pressure_pa = 300000.0
boundary_role = "source" # source | sink
```

Unknown-pressure connection:

```toml
[[nodes]]
id = "manifold"
kind = "junction"
```

Load inlet:

```toml
[[nodes]]
id = "load_inlet"
kind = "load"
function_id = "cooling"
measurement_edge_id = "load_restriction"
min_inlet_pressure_pa = 200000.0
min_flow_m3_s = 0.003
```

The measurement edge must touch the load node. Connect that edge to a separate sink pressure boundary; do not make the load itself the fixed sink.

## Edges

```toml
[[edges]]
id = "pipe_1"
from = "source"
to = "load_inlet"
kind = "pipe" # pipe | valve | pump
resistance_model = "quadratic" # linear | quadratic
resistance = 5.0e9
diameter_m = 0.04
enabled = true
```

`pipe` and `valve` require `diameter_m`. A pump requires positive `fixed_head_pa` and positive internal `resistance`; `diameter_m` is optional for a pump.

Positive flow follows `from` to `to`. A pump raises pressure in this same direction.

## Explicit scenarios

```toml
[[scenarios]]
id = "supply_failure"
description = "Supply path is blocked"

[[scenarios.actions]]
target_type = "edge"
target_id = "pipe_1"
attribute = "enabled"
value = false
```

Version 1.0 supports only boolean overrides of `edge.enabled`. Do not repeat the same target and attribute within one scenario.

## Function statuses

- `PASS`: converged, source-connected, pressure threshold met, flow threshold met.
- `FAIL`: solved and source-connected, but at least one threshold is not met.
- `UNSERVED`: no enabled path from any source boundary to the load.
- `SOLVER_FAILED`: numerical result did not pass convergence and mass-balance checks.
