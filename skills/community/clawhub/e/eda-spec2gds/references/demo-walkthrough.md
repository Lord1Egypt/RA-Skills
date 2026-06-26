# Demo Walkthrough

Use `assets/examples/simple-fifo/` as the canonical first demonstration.

## Goal

Demonstrate that the skill can manage a staged EDA flow:

1. Create a run directory
2. Save raw specification
3. Normalize specification
4. Place RTL and testbench
5. Run lint checks
6. Run simulation
7. Run synthesis
8. Prepare backend configuration
9. Summarize artifacts

## Suggested Commands

From the skill directory:

```bash
python3 scripts/init_project.py simple_fifo_demo
cp assets/examples/simple-fifo/input/raw-spec.md eda-runs/simple_fifo_demo/input/raw-spec.md
python3 scripts/normalize_spec.py \
  eda-runs/simple_fifo_demo/input/raw-spec.md \
  eda-runs/simple_fifo_demo/input/normalized-spec.yaml
cp assets/examples/simple-fifo/rtl/design.v eda-runs/simple_fifo_demo/rtl/design.v
cp assets/examples/simple-fifo/tb/testbench.v eda-runs/simple_fifo_demo/tb/testbench.v
cp assets/examples/simple-fifo/constraints/config.json eda-runs/simple_fifo_demo/constraints/config.json
./scripts/check_env.sh
./scripts/run_lint.sh eda-runs/simple_fifo_demo/rtl/design.v eda-runs/simple_fifo_demo/lint/lint.log
./scripts/run_sim.sh eda-runs/simple_fifo_demo/rtl/design.v eda-runs/simple_fifo_demo/tb/testbench.v eda-runs/simple_fifo_demo/sim
./scripts/run_synth.sh eda-runs/simple_fifo_demo/rtl/design.v simple_fifo eda-runs/simple_fifo_demo/synth
python3 scripts/collect_reports.py eda-runs/simple_fifo_demo > eda-runs/simple_fifo_demo/reports/artifacts.json
python3 scripts/summarize_run.py eda-runs/simple_fifo_demo > eda-runs/simple_fifo_demo/reports/run-summary.json
```

Run OpenLane only after the environment is ready and the earlier steps pass successfully.

```bash
source ~/.venvs/openlane/bin/activate
./scripts/run_openlane.sh eda-runs/simple_fifo_demo constraints/config.json
python3 scripts/collect_openlane_results.py eda-runs/simple_fifo_demo > eda-runs/simple_fifo_demo/reports/openlane-results.json
python3 scripts/render_gds_preview.py \
  eda-runs/simple_fifo_demo/constraints/runs/RUN_*/final/gds/simple_fifo.gds \
  eda-runs/simple_fifo_demo/reports/simple_fifo_preview.png
python3 scripts/write_success_summary.py \
  eda-runs/simple_fifo_demo/reports/openlane-results.json \
  eda-runs/simple_fifo_demo/reports/demo-summary.md
python3 scripts/serve_multi_project_dashboard.py 8765
# Port 8765 now serves the multi-project homepage. Click into each project for details.
```

## Demo Talking Points

- The skill is artifact-first, not GUI-first.
- The agent can stop early when dependencies are missing.
- The same project layout can later support report-driven iteration.
- `normalized-spec.yaml` serves as the contract between natural language specifications and EDA execution.
