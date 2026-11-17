## Description:

A general OpenClaw cron-task skill that extracts conversation context and standardizes scheduled task creation and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonfc888](https://clawhub.ai/user/jasonfc888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create one-time or recurring scheduled reminder tasks and verify that each task uses the expected isolated session, delivery mode, channel, recipient, and schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent outbound scheduled messages without enough scoping or consent.

Mitigation: Require the agent to show the exact schedule, message, channel, and recipient before creating any task.

Risk: Task names, message contents, channel IDs, and user IDs may be retained in agent memory or logs.

Mitigation: Avoid storing raw task names, message contents, channel IDs, or user IDs in memory; use a bounded structured log with only necessary operational details.

## Reference(s):

- [Cron examples reference](references/cron-examples.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw cron command templates, validation commands, and operational guidance for scheduled messages.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
