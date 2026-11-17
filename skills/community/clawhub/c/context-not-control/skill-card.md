## Description:

Enable "Context, not Control" workflow - clarify requirements through multi-turn dialogue, reduce rework, and execute with appropriate permission levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[843645440](https://clawhub.ai/user/843645440)

### License/Terms of Use:


## Use Case:

Developers and AI-assisted builders use this skill to clarify vague project requirements, establish permission boundaries, and maintain project context across iterations. It is intended for workflows where an agent may take more initiative while still confirming higher-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad agent autonomy while permission checks are advisory and can fail open.

Mitigation: Use Assistant Mode or strict custom red lines for sensitive projects, and review actions yourself before deployments, database changes, package installs, scheduled jobs, external messages, credential handling, or spending money.

Risk: The security verdict is suspicious, so users may overestimate the protection provided by the workflow's permission configuration.

Mitigation: Treat permission_check.py as workflow guidance rather than a security control, and apply independent review and deployment safeguards before high-impact actions.

## Reference(s):

- [Requirement Clarification Framework](references/clarification-framework.md)
- [Permission Levels](references/permission-levels.md)
- [Real-World Examples](references/examples.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Example Dialogues](assets/EXAMPLE_DIALOG.md)
- [Project Context Template](assets/PROJECT_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON output, bash commands, generated project context, and YAML permission configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update PROJECT.md and PERMISSION_CONFIG.yaml when its helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
