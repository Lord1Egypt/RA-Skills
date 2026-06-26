# Simple FIFO Demo

This example serves as the first smoke-test design for the `eda-spec2gds` skill.

## Contents

- `input/raw-spec.md`: Free-form design request
- `input/normalized-spec.yaml`: Structured specification contract
- `rtl/design.v`: Synchronous FIFO RTL implementation
- `tb/testbench.v`: Minimal simulation testbench
- `constraints/config.json`: Starter OpenLane configuration

## Intended Usage

Copy these files into a fresh run directory, then execute the following steps in order:
1. Lint checks
2. Simulation
3. Synthesis
4. Backend (OpenLane)

This demo is intentionally minimal:

- Single clock domain
- Active-low reset
- No macros
- No CDC (Clock Domain Crossing)
- OpenLane-friendly MVP assumptions
