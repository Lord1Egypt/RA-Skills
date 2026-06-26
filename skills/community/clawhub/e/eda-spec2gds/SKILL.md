---
name: eda-spec2gds
description: Drive an open-source EDA workflow from spec to GDS using OpenClaw skills, workspace files, and CLI tools. Use when the user wants to turn a hardware spec into RTL, testbenches, synthesis results, OpenLane backend runs, GDS output, or report summaries; also use when creating, iterating, or auditing an AgentSkill for AI-driven chip design workflows.
metadata:
  requires:
    bins: [python3, yosys, iverilog, vvp, docker]
    optional_bins: [verilator, klayout, gtkwave]
    network: true  # For Docker image pulls and package installation
    permissions:
      - sudo_access  # Required only for initial toolchain installation
      - docker_group  # Required for OpenLane backend runs
    install_script: scripts/install_ubuntu_24_mvp.sh  # Optional, requires sudo
  warnings:
    - This skill includes optional installation scripts that modify system state (apt packages, Docker group, pip virtualenvs)
    - Run installation scripts only in isolated environments (VM, container, or development machine)
    - Core skill operations are file-based and safe; system modifications are limited to optional setup scripts
    - OpenLane requires Docker daemon and pulls images from Docker Hub (~2-3GB)
---

# eda-spec2gds Skill

> **⚠️ Security Notice:** This skill includes optional system installation scripts (`scripts/install_ubuntu_24_mvp.sh`, `scripts/bootstrap_eda_demo.sh`) that require sudo access and modify system state. These scripts should only be run in isolated development environments (VM, container, or dedicated workstation), not production systems. Core skill operations (RTL generation, file management, report collection) are file-based and safe.

Execute a staged, artifact-first open-source EDA flow within the workspace. Prefer deterministic scripts for execution, keeping the agent focused on planning, generation, diagnosis, and iteration.

## Workflow

### 1. Normalize the Specification First
- Convert free-form requirements into a structured specification before writing RTL.
- Read `references/spec-template.md` and produce `input/normalized-spec.yaml`.
- If clock/reset, IO, target flow, or timing targets are missing, stop and ask the user or record explicit assumptions.

### 2. Initialize a Project Directory
- Create a run folder under `eda-runs/<design-name>/` using the layout in `references/workflow.md`.
- Copy or generate starter files from `assets/project-template/` when useful.

### 3. Generate RTL and Testbench Separately
- Write RTL to `rtl/design.v`.
- Write testbench to `tb/testbench.v`.
- Keep assumptions and design notes in `reports/rtl-notes.md`.

### 4. Run Validation in Strict Order
- Run lint/syntax checks before simulation.
- Run simulation before synthesis.
- Run synthesis before OpenLane.
- Do not skip failed stages unless the user explicitly requests it.

### 5. Treat Artifacts as Source of Truth
- Save logs, reports, VCD waveforms, netlists, configurations, and summary files.
- Prefer file outputs over GUI tools. GUI viewers like GTKWave/KLayout are optional helpers, not required steps.

### 6. Diagnose Before Editing
- For failures, read `references/failure-patterns.md`.
- Classify the failure: specification gap, RTL bug, testbench bug, synthesis issue, or backend/configuration issue.
- Fix the smallest plausible cause first.

### 7. Summarize Each Stage Clearly
- State pass/fail status.
- List key artifact paths.
- Record assumptions, blockers, and next recommended actions.

## Hard Rules

- Do not start backend if simulation is failing.
- Do not start OpenLane if synthesis failed or the top module is unclear.
- Do not silently invent missing interfaces, clocks, resets, or timing targets without documenting assumptions.
- Prefer single-clock, no-macro, no-CDC MVP flows unless the user explicitly requests advanced features.
- Use the scripts in `scripts/` for repeatable operations instead of re-inventing shell commands each time.

## Default Project Layout

Use this layout unless the user already has an existing project structure:

```text
eda-runs/<design-name>/
├── input/
│   ├── raw-spec.md
│   └── normalized-spec.yaml
├── rtl/
│   └── design.v
├── tb/
│   └── testbench.v
├── constraints/
│   └── config.json
├── lint/
│   └── lint.log
├── sim/
│   ├── compile.log
│   ├── sim.log
│   └── output.vcd
├── synth/
│   ├── synth.ys
│   ├── synth.log
│   ├── synth_output.v
│   └── stat.rpt
├── backend/
│   └── openlane_project/
├── reports/
│   ├── summary.md
│   ├── risks.md
│   ├── next-steps.md
│   └── ppa.json
└── metadata.json
```

## Resource Map

- Read `references/spec-template.md` when the specification is incomplete or ambiguous.
- Read `references/workflow.md` when you need the phase-by-phase execution order.
- Read `references/openlane-playbook.md` before setting up or debugging OpenLane.
- Read `references/failure-patterns.md` when a run fails and you need a triage path.
- Read `references/ppa-report-guide.md` when summarizing synthesis/backend reports.
- Read `references/ubuntu-24-setup.md` when preparing an Ubuntu host for this workflow.
- Read `references/demo-walkthrough.md` when you want a concrete first-run example.
- Read `references/dashboard-plan.md` when you want a web view for progress and artifacts.
- Use scripts in `scripts/` for initialization, spec normalization, environment checks, installation, lint, simulation, synthesis, OpenLane, backend result collection, GDS preview rendering, artifact web serving, report collection, and run summaries.
- Use `assets/examples/simple-fifo/` as the first smoke-test case.
- Use `assets/openlane-config-template.json` as the default backend configuration template.

## Quick Start

### Prerequisites

Before using this skill, ensure your environment has:

**Required Tools:**
- `python3` (3.8+)
- `yosys` (synthesis)
- `iverilog` + `vvp` (simulation)
- `docker` (OpenLane backend)

**Optional Tools:**
- `verilator` (faster simulation)
- `klayout` (GDS visualization)
- `gtkwave` (waveform viewing)

### Option A: Environment Already Prepared

If your system already has the EDA toolchain installed:

1. Initialize a run directory with `scripts/init_project.py <design-name>`.
2. Save user requirements to `input/raw-spec.md`.
3. Normalize them into `input/normalized-spec.yaml` using `scripts/normalize_spec.py` along with `references/spec-template.md`.
4. Write or copy `rtl/design.v` and `tb/testbench.v`.
5. Run `scripts/check_env.sh` to verify tool availability.
6. Run `scripts/run_lint.sh`, then `scripts/run_sim.sh`, then `scripts/run_synth.sh`.
7. Only after those pass, prepare `constraints/config.json` and run `scripts/run_openlane.sh`.
8. Collect artifacts with `scripts/collect_reports.py` and summarize with `scripts/summarize_run.py`.

### Option B: Fresh Environment Setup

**⚠️ Run only in isolated/development environments!**

1. Review `scripts/install_ubuntu_24_mvp.sh` to understand system changes
2. Run the installation script (requires sudo): `bash scripts/install_ubuntu_24_mvp.sh`
3. Re-login or run `newgrp docker` to apply Docker group changes
4. Pull OpenLane image: `docker pull efabless/openlane:latest`
5. Verify installation: `scripts/check_env.sh`
6. Proceed with Quick Start Option A

## MVP Scope

Default to an MVP flow that supports:

- Single module or small design
- Single clock domain
- Simple reset behavior
- Generated or hand-authored Verilog RTL
- Testbench-driven simulation
- Yosys synthesis
- OpenLane backend run with template configuration
- Report collection and summary

Escalate to the user before attempting advanced topics like CDC, SRAM/macros, multi-clock constraints, DFT, or signoff-quality closure.

## Security and Isolation

### What This Skill Does

**Safe, File-Based Operations (Core Skill):**
- Generate RTL and testbench code
- Manage project directory structures
- Run local EDA tools (yosys, iverilog)
- Collect and summarize reports
- Serve local dashboards

**System-Modifying Operations (Optional Setup Scripts Only):**
- Install system packages via apt (`scripts/install_ubuntu_24_mvp.sh`)
- Modify Docker group membership (`usermod -aG docker`)
- Create Python virtual environments
- Pull Docker images from Docker Hub

### Recommended Deployment

- ✅ **Development workstation** with sudo access
- ✅ **Isolated VM** (recommended for production evaluation)
- ✅ **Docker-in-Docker** container environments
- ⚠️ **Shared production systems** - review scripts first
- ❌ **Unreviewed execution** on critical infrastructure

### Script Audit Checklist

Before running installation scripts:

1. Review `scripts/install_ubuntu_24_mvp.sh` for apt/pip/docker commands
2. Review `scripts/bootstrap_eda_demo.sh` for demo setup steps
3. Understand that `usermod -aG docker` grants container escape potential
4. Verify network destinations (apt archives, PyPI, Docker Hub)
5. Consider running in a disposable VM or container

See `references/SECURITY.md` for detailed security guidance.
