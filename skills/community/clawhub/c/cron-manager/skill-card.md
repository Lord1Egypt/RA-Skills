## Description:

Manage, schedule, monitor, and report on recurring cron tasks with flexible patterns, dependencies, priorities, timezones, and execution logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, pause, resume, manually run, inspect, and remove recurring tasks for autonomous agents. It is suited for workspace-level recurring jobs that need JSON status, execution logs, statistics, and health reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved task commands may execute arbitrary shell commands on the host.

Mitigation: Install and run the skill only in a trusted, low-privilege workspace, and allow task creation only from trusted users or agents.

Risk: Scheduled commands may expose or misuse sensitive environment variables.

Mitigation: Keep sensitive credentials out of the runtime environment used for scheduled tasks and review each command before saving or running it.

Risk: Weak scoping and file-path validation can make task storage and logs harder to isolate.

Mitigation: Use a dedicated data directory with restricted permissions and review stored task definitions and logs during deployment.

## Reference(s):

- [Cron Manager on ClawHub](https://clawhub.ai/indigas/skills/cron-manager)
- [indigas publisher profile](https://clawhub.ai/user/indigas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return standardized JSON with status, data, message, logs, statistics, and health fields depending on the action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
