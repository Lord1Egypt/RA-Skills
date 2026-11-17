## Description:

Standardizes OpenClaw cron job entries to target the current user session and use the expected jobs.json schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegoaldev](https://clawhub.ai/user/thegoaldev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create or update scheduled reminders and recurring checks as OpenClaw cron jobs that deliver messages to the active user session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent persistent automation authority by directing it to create or update OpenClaw cron jobs.

Mitigation: Review each job's schedule, message payload, enabled state, and deletion behavior before activation.

Risk: Restarting the OpenClaw gateway may interrupt local service state.

Mitigation: Confirm that a restart is acceptable and keep a rollback path for the edited jobs.json file before restarting.

Risk: Incorrect schedule math or stale nextRunAtMs values can cause jobs to run at the wrong time or remain frozen.

Mitigation: Validate timestamp calculations, update nextRunAtMs when changing intervals, and run JSON validation before reload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thegoaldev/skills/cron-skills-session)
- [ClawHub publisher profile](https://clawhub.ai/user/thegoaldev)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates OpenClaw cron job entries in ~/.openclaw/cron/jobs.json when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
