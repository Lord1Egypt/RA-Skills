## Description:

Helps developers refactor research Python or R scripts into publication-ready, reproducible projects with documentation, environment specifications, error handling, and validation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewankeynes](https://clawhub.ai/user/ewankeynes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research engineers use this skill to turn existing analysis scripts into reproducible research workflows for publication or collaboration. It guides analysis, refactoring, environment capture, documentation, and validation of unchanged behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled requirements.txt includes an ambiguous unpinned src dependency.

Mitigation: Review or replace requirements.txt before installing dependencies, and install only inside an isolated project environment.

Risk: The generator can replace README, requirements, CI, Docker, and source template files in the selected output path.

Mitigation: Run it against a fresh output directory or a backed-up project, then review generated files before merging them into existing work.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and optional generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate README, requirements, environment, CI, Docker, test, and source template files under a selected output directory.]

## Skill Version(s):

0.1.0 (source: server release and tile.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
