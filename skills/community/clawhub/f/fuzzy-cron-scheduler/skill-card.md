## Description:

Helps agents configure OpenClaw cron schedules for one-shot reminders, recurring background tasks, session targeting, delivery modes, failure alerting, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to schedule recurring checks, reminders, background jobs, webhook notifications, and cron job management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background jobs can continue running after they are no longer needed.

Mitigation: Periodically review scheduled jobs with cron_list and cron_runs, then disable or remove obsolete jobs.

Risk: Webhook delivery can send generated results or sensitive context to an external URL.

Mitigation: Use webhook delivery only with trusted URLs and minimize sensitive content in scheduled job outputs.

Risk: Using main or current sessions for recurring jobs can increase context exposure, cost, or stale session bindings.

Mitigation: Prefer isolated sessions unless the job explicitly requires main-session context or a named persistent session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/fuzzy-cron-scheduler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with cron schedule examples and JSON-like command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include schedule expressions, session targets, delivery configuration, failure alert settings, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
