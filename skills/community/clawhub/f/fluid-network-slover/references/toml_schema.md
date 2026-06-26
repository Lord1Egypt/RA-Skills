# TOML Schema Reference

Use this schema to describe a steady incompressible fluid network with scenario-based overrides.

## Top-level sections

- `[system]`: optional system metadata such as `name`, `fluid_density`, or descriptive notes.
- `[[nodes]]`: node list.
- `[[pipes]]`: directed pipe list.
- `[[scenarios]]`: named operating or fault conditions.

## Node fields (`[[nodes]]`)

- `id` (string, required): unique node identifier.
- `type` (string, optional): `source | sink | load | junction` (default `junction`).
- `fixed_pressure` (float, optional): pressure boundary in Pa.
- `min_pressure` (float, optional): minimum acceptable pressure for load nodes.
- `min_flow` (float, optional): minimum acceptable inflow for load nodes in m^3/s.
- `external_flow` (float, optional): external source or sink term added to node continuity, default `0.0`.
- `enabled` (bool, optional): whether the node is active, default `true`.

## Pipe fields (`[[pipes]]`)

- `id` (string, required): unique pipe identifier.
- `source` (string, required): upstream node id.
- `target` (string, required): downstream node id.
- `resistance` (float, required): hydraulic resistance `R`, must be greater than `0`.
- `diameter` (float, optional): pipe diameter in meters, used to compute velocity.
- `valve_open` (bool, optional): whether the pipe is open, default `true`.
- `enabled` (bool, optional): whether the pipe exists in the active network, default `true`.

## Scenario fields (`[[scenarios]]`)

- `name` (string, required): scenario identifier. `base` is reserved.
- `description` (string, optional): human-readable note.
- `[scenarios.overrides.system]` (optional): metadata overrides for the `[system]` table.
- `[scenarios.overrides.nodes]` (optional): per-node field overrides.
- `[scenarios.overrides.pipes]` (optional): per-pipe field overrides.

Supported node override fields:

- `type`
- `fixed_pressure`
- `min_pressure`
- `min_flow`
- `external_flow`
- `enabled`

Supported pipe override fields:

- `resistance`
- `diameter`
- `valve_open`
- `enabled`

## Minimal example

```toml
[system]
name = "demo"

[[nodes]]
id = "src"
type = "source"
fixed_pressure = 250000.0

[[nodes]]
id = "load_a"
type = "load"
min_pressure = 80000.0
min_flow = 0.001

[[nodes]]
id = "ret"
type = "sink"
fixed_pressure = 0.0

[[pipes]]
id = "e1"
source = "src"
target = "load_a"
resistance = 1.5e10
diameter = 0.02

[[pipes]]
id = "e2"
source = "load_a"
target = "ret"
resistance = 1.0e10
diameter = 0.02

[[scenarios]]
name = "fault_close_main"
[scenarios.overrides.pipes]
e1 = { valve_open = false }
```
