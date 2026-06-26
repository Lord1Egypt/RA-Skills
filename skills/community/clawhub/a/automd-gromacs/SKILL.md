---
name: automd-gromacs
description: "AutoMD-GROMACS: AI-friendly molecular dynamics automation for GROMACS with workflow, enhanced sampling, special-system simulation, advanced analysis, and publication-ready visualization. Built-in troubleshooting and token-optimized execution. Part of the AutoMD series."
metadata:
  openclaw:
    emoji: "🧬"
    category: science
    requires:
      bins:
        - gmx
        - python3
    install:
      - id: conda
        kind: conda
        channel: conda-forge
        package: gromacs
        bins:
          - gmx
        label: Install GROMACS via conda
      - id: manual
        kind: manual
        url: https://manual.gromacs.org/current/install-guide/index.html
        label: Install GROMACS from source
      - id: pyyaml
        kind: manual
        url: https://pyyaml.org/wiki/PyYAMLDocumentation
        label: Install PyYAML for the decision layer (`pip install pyyaml`)
---

# AutoMD-GROMACS

AutoMD-GROMACS is an AI-oriented automation toolkit for GROMACS. It packages decision-layer routing, end-to-end simulation workflows, enhanced sampling, special-system simulation, advanced analysis, and publication-ready visualization into a public OpenClaw skill with troubleshooting references.

Project metadata:
- Version: 5.3.2
- Author: Guo Xuan
- Organization: Hong Kong University of Science and Technology (Guangzhou)
- Contributors: 实验室小精灵 (GPU installation, ligand topology, cross-forcefield workflow)
- Homepage: https://github.com/Billwanttobetop/automd-gromacs

## ⚠️ AI Assistant Rules — MUST READ BEFORE ANY WORK

**All AI assistants using this skill MUST follow these rules before executing any computation:**

1. **Create experiment log FIRST** — Before running any simulation (MD, QM, etc.), create or append to an experiment log file (`EXPT_LOG.md`) in the working directory. Record:
   - Date, time, and purpose of the experiment
   - Key parameters and settings
   - Expected duration and output

2. **Create experiment plan FIRST** — Before starting any long-running task (>1 hour), create a `PLAN.md` with:
   - Clear objectives and phases
   - Timeline estimates
   - Risk assessment and fallback strategies
   - Expected deliverables

3. **Update logs after EVERY significant event** — Record completion, failure, parameter changes, and decisions.

4. **Why this matters:** MD/QM calculations run for hours to days. AI session context gets cleared between sessions. Without proper experiment logs, progress is lost and work is duplicated. The experiment log is the single source of truth.

5. **File naming convention:**
   - `EXPT_LOG.md` — chronological experiment log
   - `PLAN.md` — experiment plan and timeline (update status: ✅/🔄/⏳/❌)

## Scope

- Decision layer: method routing before execution via `method-selector`
- Core workflow: setup, equilibration, production, preprocessing, utilities
- **GPU acceleration:** source-build installation, GPU MD execution, performance tuning, CUDA setup
- **Ligand topology:** acpype + GAFF2 workflow, cross-forcefield system construction (AMBER protein + GAFF ligand)
- Enhanced sampling: umbrella, free energy, replica exchange, metadynamics, steered MD, enhanced sampling, accelerated MD
- Special systems: membrane, ligand, coarse-grained, electric field, non-equilibrium, QM/MM
- Validation and analysis: trajectory, binding, property, membrane, scattering, free-energy, protein-focused analyses
- Visualization: publication-ready plotting and structure/trajectory rendering

## Quick Start

1. Read `references/SKILLS_INDEX.yaml` — structured index of all workflows
2. If the target method is unclear, run the decision layer:
   ```bash
   python3 scripts/decision/method-selector.py --goal "..." --system-type "..." --target-observable "..." --pretty
   ```
3. Execute the recommended script (e.g. `bash scripts/advanced/freeenergy.sh --input ...`)
4. On failure: look up the error code in the matching file under `references/troubleshoot/`
   (e.g. freeenergy errors → `references/troubleshoot/freeenergy-errors.md`)

## Design

- Decision -> execution -> validation as the public product stack
- Executable workflows over tutorial prose
- Layered disclosure for low token overhead
- Embedded domain knowledge from GROMACS practice
- Auto-repair and troubleshooting guidance by default
- Reusable MDP templates in `references/templates/` (em, nvt, npt, production, membrane, freeenergy)

## Project Info

- Version: 5.2.0
- Based on: GROMACS 2025.4 - 2026.1
- Runtime needs: `python3`, `PyYAML`, `gmx`
- License: MIT
- Homepage: https://github.com/Billwanttobetop/automd-gromacs

## GPU, Ligand & ORCA Quick References

- **GPU 源码编译安装:** `read references/gpu/gpu-installation.md`
- **GPU MD 运行避坑:** `read references/gpu/gpu-md-execution.md`
- **配体 GAFF2 拓扑生成:** `read references/gpu/ligand-topology.md`
- **跨力场体系构建:** `read references/gpu/cross-forcefield-system.md`
- **ORCA 多核并行 (OpenMPI):** `read references/troubleshoot/qmmm-errors.md` → ERROR-011

**Get started:** `read references/SKILLS_INDEX.yaml`
