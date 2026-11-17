## Description:

Manage OpenClaw agent configurations, update model assignments, modify bindings, and test configuration changes with validation, backup, restore, and rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheben77](https://clawhub.ai/user/cheben77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw agents, update their model assignments, validate configuration structure, and prepare configuration changes before applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change OpenClaw agent behavior by modifying local agent configuration.

Mitigation: Review proposed model and binding changes before applying them, run validation or dry-run checks first, and keep a known-good configuration backup for rollback.

Risk: Configuration backups may include sensitive API-key-bearing content and may be written under shared temporary paths.

Mitigation: Use the skill only in a trusted local environment, restrict access to generated backups, and prefer secure temporary files or protected backup locations before relying on it.

## Reference(s):

- [Agent Config Manager on ClawHub](https://clawhub.ai/cheben77/skills/agent-config-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local OpenClaw configuration workflows and may include commands that read or modify /data/.openclaw/openclaw.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
