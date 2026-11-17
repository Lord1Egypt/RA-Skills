## Description:

Lightweight watchdog for daily report cron failures that checks OpenClaw cron status and daily report files, then sends independent Feishu alerts with a 4-hour cooldown and 36-hour error window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colbertlee](https://clawhub.ai/user/colbertlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor an important daily-report cron workflow and receive independent Feishu alerts when the scheduled job or expected report file indicates a silent failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends operational details to a hard-coded Feishu recipient and account.

Mitigation: Before installing, confirm the recipient and sender account belong to the intended environment, and prefer moving them into explicit per-install configuration.

Risk: The skill is tied to a hard-coded workspace path and cron job ID.

Mitigation: Update the workspace and job ID for the target installation, then run dry-run and check-only validation before scheduling recurring execution.

Risk: The skill stores alert cooldown state in a shared temporary file.

Mitigation: Use a per-install state file with appropriate filesystem permissions on shared or production machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colbertlee/skills/daily-report-watcher)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation, command-line status text, exit codes, and Feishu alert content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The watcher supports normal, dry-run, and check-only modes.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
