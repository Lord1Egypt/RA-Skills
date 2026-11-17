## Description:

BigTimer helps agents manage cron-based scheduled tasks and scheduled message pushes across OpenClaw and DSH environments, including task creation, listing, removal, status checks, immediate runs, schedule generation, and Feishu or multi-channel delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users use this skill to create, inspect, run, and install recurring task schedules that execute trusted commands and deliver the results through OpenClaw messaging, Feishu webhooks, or stdout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled tasks can create persistent arbitrary command execution through cron when actions come from untrusted input.

Mitigation: Review commands before installing schedules, use the skill only for trusted tasks, and avoid scheduling free-form shell commands from untrusted input.

Risk: Webhook delivery can send task output to an arbitrary external endpoint.

Mitigation: Prefer stdout or trusted OpenClaw messaging, and use only trusted Feishu webhook URLs when webhook delivery is required.

Risk: Removing a task from the task list may leave scheduler entries that continue to run.

Mitigation: Verify and remove crontab or OpenClaw cron entries manually after deleting scheduled tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kobenfang/skills/bigtimer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create task records, logs, and scheduler entries when the user runs the provided commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
