## Description:

Master OpenClaw's timing systems. Use for scheduling reliable reminders, setting up periodic maintenance (janitor jobs), and understanding when to use Cron vs Heartbeat for time-sensitive tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wt865143010](https://clawhub.ai/user/wt865143010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose precise cron scheduling over drifting heartbeat checks, create reliable reminders, configure maintenance jobs, and migrate older scheduling patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can route reminders and email summaries to a fixed Telegram recipient.

Mitigation: Replace the recipient with a verified user-controlled destination or disable external delivery before using the examples.

Risk: Cleanup guidance may remove the cron jobs state file and cause loss of scheduled jobs.

Mitigation: Back up the cron jobs state file and confirm that losing scheduled jobs is acceptable before deleting it.

Risk: Email-summary workflows may read email and send summaries externally.

Mitigation: Review data access and destination settings before enabling email summaries or other external delivery workflows.

## Reference(s):

- [Cron Examples & Templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reminder, maintenance, recurring task, timezone, and troubleshooting guidance.]

## Skill Version(s):

1.0.3 (source: artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
