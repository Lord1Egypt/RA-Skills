## Description:

Master OpenClaw's timing systems. Use for scheduling reliable reminders, setting up periodic maintenance (janitor jobs), and understanding when to use Cron vs Heartbeat for time-sensitive tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to choose between OpenClaw Cron and Heartbeat timing patterns, create reliable reminders, configure recurring maintenance jobs, and migrate older cron payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example jobs can create persistent schedules that deliver messages to a fixed Telegram recipient.

Mitigation: Replace example recipient identifiers with verified user-owned destinations before creating jobs.

Risk: Scheduled email summaries or other content may be sent to external channels.

Mitigation: Only schedule delivery to external channels after explicit user confirmation of the content source, destination, and cadence.

Risk: Janitor and jobs.json deletion guidance can remove unrelated cron state.

Mitigation: Confirm the target jobs, create backups where possible, and avoid deleting cron state unless recovery or cleanup is clearly intended.

## Reference(s):

- [Cron Examples & Templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reminder, maintenance, recurring job, timezone, and troubleshooting patterns for OpenClaw cron scheduling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
