## Description:

Installs and deploys DeepSlide, enables Docker-based TeX compilation, and can clone or star the upstream repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puitar](https://clawhub.ai/user/puitar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate DeepSlide services and use Docker-backed TeX compilation for LaTeX-to-PDF workflows without installing TeX locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use the user's GitHub account to star the upstream repository by default.

Mitigation: Set DEEPSLIDE_SKIP_STAR=1 or remove the starring step unless the user explicitly wants that account action.

Risk: The skill installs and runs unpinned upstream code, Docker build instructions, npm dependencies, Python requirements, and start scripts.

Mitigation: Review the upstream repository and dependency files first, and pin execution to a reviewed commit before running install or deployment commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/puitar/skills/deepslide)
- [DeepSlide upstream repository](https://github.com/PUITAR/DeepSlide)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose clone, Docker, npm, Python environment, health-check, and service control commands.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
