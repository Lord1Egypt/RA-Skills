## Description:

Monitor all OpenClaw cron jobs for failures and auto-fix common errors (model-not-allowed, timeouts). Posts to Slack only when issues are found. Runs every 6 hours. Use when you need automated cron health monitoring and self-healing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpbshhx](https://clawhub.ai/user/mpbshhx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw cron jobs, identify failed or degraded scheduled runs, apply common fixes for model and timeout errors, and send Slack alerts only when action is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change and force-run visible cron jobs.

Mitigation: Limit the skill to approved jobs and safe fields, require explicit approval for force-runs, and review proposed updates before execution in sensitive environments.

Risk: Timeout changes may grow operational limits without a stated cap.

Mitigation: Set an administrator-approved maximum timeout increase and require review when a job would exceed that cap.

Risk: Operational failure details may be sent to a fixed Slack destination.

Mitigation: Use an administrator-configured Slack destination and redact sensitive job names, payloads, and error details before sending alerts.

## Reference(s):

- [Cron Watchdog on ClawHub](https://clawhub.ai/mpbshhx/skills/cron-watchdog)
- [mpbshhx ClawHub profile](https://clawhub.ai/user/mpbshhx)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with tool-call examples and operational alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cron update guidance and conditional Slack alert content; no output is expected when all monitored jobs are healthy.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
