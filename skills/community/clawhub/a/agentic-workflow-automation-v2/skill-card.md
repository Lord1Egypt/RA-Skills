## Description:

Generate reusable multi-step agent workflow blueprints for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to define workflow names, triggers, ordered steps, dependencies, and fallback behavior for reusable automation blueprints. The output can be handed off for implementation in n8n or internal orchestrators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled generator writes to a caller-selected output path and can overwrite files, including when run with --dry-run.

Mitigation: Run the skill only in a constrained workspace, choose a dedicated new output path, and review generated files before using them.

## Reference(s):

- [Workflow Blueprint Guide](artifact/references/workflow-blueprint-guide.md)
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/skills/agentic-workflow-automation-v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, CSV, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled generator normalizes workflow steps and can write caller-selected output files.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
