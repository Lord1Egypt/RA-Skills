## Description:

Automates topic-neutral COMSOL Multiphysics optical, semiconductor, thermal, and coupled optoelectronic simulations through Python/mph for environment discovery, project configuration, parameter sweeps, solver diagnostics, and post-processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leima-max](https://clawhub.ai/user/leima-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and run COMSOL optical, semiconductor, thermal, and coupled simulations, including sweeps, diagnostics, and post-processing. It is intended for user-supplied COMSOL installations and project-specific material, boundary-condition, and validation inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic or repair scripts can rerun studies or overwrite simulation model files.

Mitigation: Run the skill in a disposable workspace or on copied .mph files, and review diagnostic or repair scripts before allowing them to modify models.

Risk: Dependency installation changes the local skill environment.

Mitigation: Approve dependency installation deliberately and keep installed Python bridge packages scoped to the skill-local vendor directory.

Risk: Unconfigured templates or missing material, boundary-condition, and validation data can produce misleading quantitative simulation results.

Mitigation: Replace placeholders with project-specific values, record sources for parameters, and validate outputs against measured data or accepted criteria before relying on results.

## Reference(s):

- [COMSOL Skill Input Schema](references/input-schema.md)
- [Generic Material Parameter Template](references/material-database.md)
- [COMSOL API Patterns via MPh](references/comsol-api-patterns.md)
- [COMSOL Documentation and Java API Playbook](references/comsol-docs-java-playbook.md)
- [COMSOL Official Learning Roadmap](references/comsol-official-learning-roadmap.md)
- [COMSOL Convergence Diagnostics](references/comsol-convergence-diagnostics.md)
- [Official Photogeneration Coupling Template](references/comsol-official-photogeneration-template.md)
- [Thermal And Multiphysics Coupling Guide](references/thermal-coupling-guide.md)
- [Parameter Sweep Guide](references/parameter-sweep-guide.md)
- [MPh documentation](https://mph.readthedocs.io)
- [COMSOL API overview](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_intro.46.01.html)
- [COMSOL Programming Reference Manual](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/COMSOL_ProgrammingReferenceManual.pdf)
- [COMSOL Application Programming Guide](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/ApplicationProgrammingGuide.pdf)
- [COMSOL Java API package documentation](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/api/com/comsol/model/package-summary.html)
- [COMSOL Semiconductor Module User's Guide](https://doc.comsol.com/6.4/doc/com.comsol.help.semicond/SemiconductorModuleUsersGuide.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration templates, and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce COMSOL model artifacts, exported plots, CSV files, and JSON summaries when the referenced scripts are executed in a configured COMSOL environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
