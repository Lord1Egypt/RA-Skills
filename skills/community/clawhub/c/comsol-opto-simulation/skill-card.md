## Description: <br>
Automates topic-neutral COMSOL Multiphysics optical, semiconductor, thermal, and coupled optoelectronic simulations through Python/mph for environment discovery, project configuration, parameter sweeps, solver diagnostics, and post-processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leima-max](https://clawhub.ai/user/leima-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and simulation engineers use this skill to configure and run COMSOL optical, semiconductor, thermal, and coupled optoelectronic workflows, then inspect generated model artifacts, CSV outputs, JSON summaries, and solver diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic and repair scripts may overwrite COMSOL .mph models or solver state. <br>
Mitigation: Run those scripts only on copied models or backed-up workspaces, and confirm the target model path before execution. <br>
Risk: COMSOL automation can consume local COMSOL licenses and compute resources. <br>
Mitigation: Use offline helpers first, then run license-consuming product checks or solves only after the user approves the environment and module requirements. <br>
Risk: Template outputs and placeholder metric CSVs can be mistaken for validated simulation results. <br>
Mitigation: Replace all placeholders with project-specific measured or literature-supported values and report assumptions, solver settings, convergence status, and validation gaps with results. <br>
Risk: Dependency installation modifies a skill-local vendor directory. <br>
Mitigation: Review dependency-install commands before running them and keep installed Python bridge packages isolated from project source files. <br>


## Reference(s): <br>
- [COMSOL Simulation ClawHub page](https://clawhub.ai/leima-max/comsol-opto-simulation) <br>
- [COMSOL Skill Input Schema](references/input-schema.md) <br>
- [COMSOL Script Map](references/script-map.md) <br>
- [COMSOL API Patterns via MPh](references/comsol-api-patterns.md) <br>
- [COMSOL Java API Cheat Sheet for MPh / Python Bridge](references/comsol-api-cheatsheet.md) <br>
- [COMSOL Convergence Diagnostics](references/comsol-convergence-diagnostics.md) <br>
- [Generic Material Parameter Template](references/material-database.md) <br>
- [COMSOL API Introduction](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_intro.46.01.html) <br>
- [COMSOL Programming Reference Manual](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/COMSOL_ProgrammingReferenceManual.pdf) <br>
- [COMSOL Semiconductor Module User's Guide](https://doc.comsol.com/6.4/doc/com.comsol.help.semicond/SemiconductorModuleUsersGuide.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration guidance, and code-oriented script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide generation of COMSOL model artifacts, CSV files, JSON summaries, and diagnostic logs under user-selected output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
