---
name: fluid-network-analysis
description: Design, validate, solve, and analyze schema 1.0 steady-state incompressible fluid networks from TOML or natural-language requirements. Use for pressure, flow, velocity, explicit operating-scenario, and deterministic function-availability analysis; do not use for transient, compressible, thermal, or probabilistic reliability simulation.
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    emoji: "💧"
---

# Fluid Network Analysis

Use the bundled runtime and schema instead of calculating nontrivial networks informally. The runtime requires Python 3.9 or newer and does not require the source repository or third-party Python packages.

## Workflow

1. Read [references/schema.md](references/schema.md) when creating or modifying TOML.
2. Preserve the distinction between a load inlet and its downstream sink boundary. Measure inlet pressure at the load node and flow on its declared measurement edge.
3. Convert user units to SI before writing TOML and retain the original values in explanatory text when useful.
4. Represent only explicitly requested operating conditions. Apply scenario actions as state overrides; never generate a Cartesian product of all failures unless the user asks for it.
5. Resolve `<skill-folder>` to the directory containing this `SKILL.md`, then validate before solving:

   ```text
   python <skill-folder>/scripts/fluid_network.py validate <network.toml>
   ```

6. Analyze all declared scenarios or one selected scenario:

   ```text
   python <skill-folder>/scripts/fluid_network.py analyze <network.toml> --format markdown
   python <skill-folder>/scripts/fluid_network.py analyze <network.toml> --scenario <scenario-id> --format json
   ```

7. Report assumptions, validation errors, solver convergence and mass-balance residuals. Do not present unresolved pressures or flows as physical results.

## Modeling decisions

- Use `pressure_boundary` with role `source` for supplies and role `sink` for ambient or return pressure.
- Use `junction` for ordinary unknown-pressure nodes.
- Use `load` only at the load inlet and provide both pressure and flow thresholds.
- Use `ΔP = RQ` for linear resistance and `ΔP = RQ|Q|` for quadratic resistance.
- Model a pump as fixed pressure rise plus positive internal resistance. Do not silently approximate a supplied pump curve as fixed head.
- Treat reliability results as deterministic availability within the named scenario, not as failure probability.

If topology, source pressure, sink pressure, resistance data, or load thresholds are absent, state the minimum assumptions required for a runnable model. Do not hide those assumptions inside generated values.

Use [assets/simple_network.toml](assets/simple_network.toml) as a minimal starting template and [assets/redundant_supply.toml](assets/redundant_supply.toml) for main/backup path analysis. Copy an asset to the user's workspace before modifying it; do not edit the installed asset in place.
