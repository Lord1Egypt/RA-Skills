# EDA Workflow

## Phase 0: Environment Check

1. Run `scripts/check_env.sh`.
2. Verify at minimum that `python3`, `yosys`, `iverilog`/`verilator`, `vvp`, and `docker` are available.
3. If any tools are missing, stop early and report exactly which ones are absent.

## Phase 1: Intake

1. Save raw user requirements to `input/raw-spec.md`.
2. Convert them into `input/normalized-spec.yaml`.
3. Record missing fields and document assumptions.

## Phase 2: RTL Drafting

1. Generate `rtl/design.v`.
2. Keep module names aligned with `top_module`.
3. Record design intent and shortcuts in `reports/rtl-notes.md`.

## Phase 3: Verification

1. Generate `tb/testbench.v`.
2. Run lint checks first.
3. Run simulation and require an explicit pass signal in logs.
4. Save VCD waveforms if possible.

## Phase 4: Synthesis

1. Create `synth/synth.ys` synthesis script.
2. Run Yosys and collect `synth/stat.rpt`.
3. Save synthesized netlist and logs.

## Phase 5: Backend

1. Build `constraints/config.json` for OpenLane.
2. Activate the OpenLane virtualenv if needed.
3. Run OpenLane in a dedicated backend directory.
4. Collect final GDS path, latest run directory, run logs, and report excerpts using `scripts/collect_openlane_results.py`.

## Phase 6: Summary

Always produce the following:

- Overall status
- Artifact paths
- Assumptions made
- Blockers encountered
- Next action recommendation
