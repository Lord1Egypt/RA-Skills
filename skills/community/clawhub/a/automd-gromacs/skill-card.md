## Description: <br>
AutoMD-GROMACS helps agents plan, run, troubleshoot, analyze, and visualize GROMACS molecular dynamics workflows, including enhanced sampling, special systems, and publication-ready reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational scientists, and agent operators use this skill to select and execute GROMACS molecular dynamics workflows, manage setup through production runs, and generate analysis or visualization outputs. It is most useful when an agent needs structured guidance, shell workflows, and troubleshooting references for MD projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GROMACS workflows can be long-running and resource intensive. <br>
Mitigation: Use a project directory, conda environment, container, or HPC job sandbox; create experiment plans and logs before starting extended runs. <br>
Risk: The skill includes optional installation and download paths that can change the local environment or fetch external assets. <br>
Mitigation: Review commands before execution and enable AUTOMD_AUTO_INSTALL=1 or AUTOMD_CG_ALLOW_DOWNLOAD=1 only when those package or network changes are intended. <br>
Risk: Molecular structures or trajectories may contain proprietary or sensitive research data. <br>
Mitigation: Avoid uploading proprietary structures to external services unless the user has approval. <br>


## Reference(s): <br>
- [GROMACS installation guide](https://manual.gromacs.org/current/install-guide/index.html) <br>
- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) <br>
- [AutoMD-GROMACS on ClawHub](https://clawhub.ai/billwanttobetop/automd-gromacs) <br>
- [Skill index](references/SKILLS_INDEX.yaml) <br>
- [Method selection index](references/METHOD_SELECTION_INDEX.yaml) <br>
- [Installation reference](references/tools/INSTALLATION.md) <br>
- [Troubleshoot escalation guide](references/guides/troubleshoot-escalation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, script selections, configuration notes, and generated analysis/report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run long-running GROMACS workflows and create experiment logs, plans, simulation outputs, and analysis reports.] <br>

## Skill Version(s): <br>
5.3.3 (source: server release evidence, released 2026-06-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
