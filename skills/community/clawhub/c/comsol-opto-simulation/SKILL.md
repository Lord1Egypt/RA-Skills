---
name: comsol-opto-simulation
description: >
  Automate topic-neutral COMSOL Multiphysics optical, semiconductor,
  thermal, and coupled optoelectronic simulations through Python/mph.
  Use when a user needs COMSOL environment discovery, project configuration,
  parameter sweeps, solver diagnostics, or simulation post-processing.
homepage: https://github.com/leima-max/comsol-opto-simulation-skill
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python"] },
      },
  }
---

# COMSOL Optical / Optoelectronic Simulation

Automate COMSOL Multiphysics simulations through the `mph` Python interface for user-configured optical, semiconductor, thermal, or coupled multiphysics projects.

This skill is topic-neutral. It does not assume a material stack, device type, measured benchmark, local COMSOL path, or default parameter set.

## OpenClaw / ClawHub Quick Start

Install from ClawHub:

```powershell
openclaw skills install comsol-opto-simulation
```

After installation, verify the offline helpers before any license-consuming COMSOL run:

```powershell
python scripts/test_sweep_offline.py
python scripts/discover_comsol_environment.py --pretty
```

Run `python scripts/install_mph.py` only when the user approves dependency installation. It installs Python bridge packages into a skill-local `vendor/site-packages` directory and does not install COMSOL or provide a license.

## Scope

Use this skill for:

- optical absorption and field-distribution models
- semiconductor or transport models
- thermal-electrical coupled models
- parameter sweeps and batch studies
- post-processing of simulated device or sample metrics
- convergence diagnostics and solver fallback planning

Do not use this skill to invent missing material parameters, boundary conditions, or validation data. Ask the user to configure those values first.

## Required User Configuration

Before running COMSOL automation, collect or confirm:

- COMSOL installation path and available modules
- geometry dimension and domain/layer list
- material parameters and their sources
- optical constants or source/excitation terms
- electrical/thermal/mechanical boundary conditions as relevant
- solver strategy and sweep variables
- output metrics and validation criteria

Use:

- `templates/device_stack.json`
- `templates/config_sweep.json`
- `templates/config_thermal.json`
- `templates/official_photogeneration_coupling.json`
- `references/script-map.md`
- `references/material-database.md`
- `references/input-schema.md`

as generic templates only.

## Workflow

1. Discover local COMSOL:
   ```bash
   python scripts/discover_comsol_environment.py --pretty
   ```
2. Check official resources and licenses when the user permits a license-consuming check:
   ```bash
   python scripts/probe_application_library_examples.py --pretty
   python scripts/check_comsol_products.py --skip-start --pretty
   ```
3. Install or verify the workspace-local Python bridge:
   ```bash
   python scripts/install_mph.py
   ```
4. Create a project-specific config by copying a template and replacing all `<UNCONFIGURED>` values.
5. Run the appropriate script:
   ```bash
   python scripts/run_optoelectronic_sim.py --config <project_config.json>
   python scripts/run_parameter_sweep.py --config <project_sweep_config.json>
   ```
   If unsure which script to use, read `references/script-map.md` first.
6. Inspect exported plots, CSV files, JSON summaries, and COMSOL model artifacts under `output/`.
7. Report assumptions, fitted parameters, solver settings, convergence status, and validation gaps.

## Prerequisites

- COMSOL Multiphysics compatible with the selected physics
- Required COMSOL modules for the selected model
- Python 3.10+
- Java runtime compatible with COMSOL/mph

## Escalation

- If COMSOL is not installed, ask the user to provide the installation path or install COMSOL.
- If a required module is missing, report the missing module and suggest a reduced model if possible.
- If a simulation diverges, reduce step size, simplify physics, inspect material parameters, adjust scaling, and add continuation or fallback strategies.
- If a parameter sweep fails mid-way, use checkpoint/resume behavior where configured.

## References

- `references/input-schema.md`
- `references/material-database.md`
- `references/comsol-api-patterns.md`
- `references/comsol-docs-java-playbook.md`
- `references/comsol-official-learning-roadmap.md`
- `references/comsol-convergence-diagnostics.md`
- `references/comsol-official-photogeneration-template.md`
- `references/thermal-coupling-guide.md`
- `references/parameter-sweep-guide.md`
