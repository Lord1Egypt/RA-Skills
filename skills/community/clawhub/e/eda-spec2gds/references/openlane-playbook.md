# OpenLane Playbook

Use OpenLane only after RTL syntax checks, testbench simulation, and Yosys synthesis have all passed successfully.

## Inputs to Prepare

- Verilog RTL file
- Top module name
- Clock port name
- Clock period
- Minimal OpenLane configuration JSON

## Default Assumptions for MVP

- Single top module
- No macros
- No custom floorplan beyond template defaults
- Focus on obtaining a runnable backend result, not signoff-quality closure

## Common Setup Notes

- Keep OpenLane artifacts isolated under the project tree.
- Save the configuration used for each run.
- Prefer absolute configuration paths when invoking OpenLane from scripts.
- Record the exact command line used for reproducibility.
- In headless or non-interactive shells, prefer `--docker-no-tty --dockerized` flags.
- Be aware that runs may land under `constraints/runs/` depending on the invocation path.
- Capture the latest run directory and final GDS path.

## When Backend Fails

Check issues in the following order:

1. Wrong top module name or missing Verilog file
2. Malformed configuration JSON
3. Invalid clock port name or clock period
4. Design too large for default floorplan
5. Environment, Docker, or tool installation issues

Do not immediately rewrite RTL unless reports indicate an RTL-caused issue.
