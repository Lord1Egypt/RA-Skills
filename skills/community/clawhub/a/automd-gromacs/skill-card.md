## Description:

AutoMD-GROMACS provides AI-friendly molecular dynamics automation for GROMACS workflows, enhanced sampling, special-system simulation, advanced analysis, publication-ready visualization, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwanttobetop](https://clawhub.ai/user/billwanttobetop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational scientists use this skill to plan, run, troubleshoot, and analyze GROMACS molecular dynamics workflows, including enhanced sampling, special systems, GPU execution, and publication-ready visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe installation and troubleshooting instructions can install unverified code globally or weaken the host environment.

Mitigation: Review commands before execution, prefer a fresh conda environment or disposable container, preinstall pinned dependencies, and avoid persistent shell profile or Docker capability changes unless their host impact is understood.

Risk: Optional auto-install and download paths can fetch dependencies or modify the environment when enabled.

Mitigation: Keep AUTOMD_AUTO_INSTALL and AUTOMD_CG_ALLOW_DOWNLOAD disabled unless the dependency sources are trusted and the commands have been reviewed.

Risk: Molecular dynamics workflows may run for hours or days and produce stateful experiment artifacts.

Mitigation: Create and maintain experiment logs and plans before long-running computation so progress, parameters, failures, and decisions remain auditable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billwanttobetop/skills/automd-gromacs)
- [GROMACS installation guide](https://manual.gromacs.org/current/install-guide/index.html)
- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Workflow index](references/SKILLS_INDEX.yaml)
- [Method selection index](references/METHOD_SELECTION_INDEX.yaml)
- [GPU installation reference](references/gpu/gpu-installation.md)
- [GPU MD execution reference](references/gpu/gpu-md-execution.md)
- [Ligand topology reference](references/gpu/ligand-topology.md)
- [Cross-forcefield system reference](references/gpu/cross-forcefield-system.md)
- [Troubleshoot escalation guide](references/guides/troubleshoot-escalation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration steps, and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gmx and python3; optional workflows may require PLUMED, acpype, martinize2, CP2K, ORCA, or plotting tools.]

## Skill Version(s):

5.3.3 (source: ClawHub release metadata and CHANGELOG, released 2026-06-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
