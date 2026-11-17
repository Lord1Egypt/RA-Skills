## Description:

Manages OpenClaw cron jobs by listing jobs, changing models, enabling or disabling jobs, manually running jobs, and deleting jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect and manage scheduled OpenClaw cron jobs through CLI commands, including model changes and controlled state changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage OpenClaw scheduled jobs with state-changing commands, including model changes, enable or disable operations, manual runs, and deletion.

Mitigation: Require explicit user confirmation before any enable, disable, run, delete, or model-change action.

Risk: The skill can automatically edit persistent OpenClaw configuration when repairing an unsupported toolCall key.

Mitigation: Make a backup before the repair and validate the JSON configuration afterward; avoid the automatic repair if those checks cannot be performed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lgugeng/skills/cron-model-manager)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing actions require user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
