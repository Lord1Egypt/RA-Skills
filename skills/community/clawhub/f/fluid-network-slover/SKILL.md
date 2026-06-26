---
name: fluid-network-solver
description: Solve and analyze steady incompressible fluid networks from TOML definitions. Use when users ask to design a network template, validate TOML topology data, compute node pressure plus pipe flow/velocity, run named scenarios, and generate reliability reports from pressure and flow thresholds.
---

# Fluid Network Solver

## Overview

Parse a TOML fluid network, apply named scenario overrides, solve hydraulic steady-state variables, and produce reliability analysis outputs.
Use the scripts in this skill for deterministic execution instead of rewriting solver logic each time.

## Workflow

1. Read schema details from `references/toml_schema.md` when defining or checking input.
2. Prepare a TOML file containing `system`, `nodes`, `pipes`, and `scenarios`.
3. Run `scripts/run_fluid_skill.py` with one scenario or all scenarios.
4. Return JSON output, markdown report, or a readable console summary.

## Parameter Entry

Use this command from the skill root:

```bash
python scripts/run_fluid_skill.py --toml <input.toml> [--scenario <name> | --all-scenarios] [--report-out <report.md>] [--json-out <result.json>] [--print-text]
```

Supported parameters:

- `--toml`: required input network file.
- `--scenario`: single scenario name (default `base`).
- `--all-scenarios`: analyze `base` plus all named scenarios.
- `--report-template`: optional template path, default `assets/report_template.md`.
- `--report-out`: optional markdown report output path.
- `--json-out`: optional JSON result output path.
- `--print-text`: print readable scenario analysis to stdout.
- `--generate-template`: optionally write a starter TOML template and exit.

## Outputs

Generate these outputs based on user request:

- Plain text analysis: convergence, pressures, flows, and load pass/fail status.
- JSON payload: machine-readable scenario results.
- Markdown report: rendered from `assets/report_template.md`.

## Report Template

Use `assets/report_template.md` placeholders:

- `{{generated_at_utc}}`
- `{{input_file}}`
- `{{scenario_mode}}`
- `{{scenario_count}}`
- `{{summary_table}}`
- `{{detail_sections}}`

## Files

- `scripts/fluid_solver_core.py`: compatibility shim that re-exports the maintained root implementation.
- `scripts/run_fluid_skill.py`: CLI entry for parameterized execution and report generation.
- `references/toml_schema.md`: authoritative schema and sample.
- `assets/report_template.md`: default report skeleton.
- `assets/sample_network.toml`: runnable demo network.
- `requirements.txt`: runtime dependencies for packaging or local execution.

## Execution Examples

Run one scenario:

```bash
python scripts/run_fluid_skill.py --toml assets/sample_network.toml --scenario Normal_Operation --print-text
```

Run all scenarios and export report + JSON:

```bash
python scripts/run_fluid_skill.py --toml assets/sample_network.toml --all-scenarios --report-out outputs/report.md --json-out outputs/result.json
```

Generate a template:

```bash
python scripts/run_fluid_skill.py --generate-template outputs/template.toml
```
