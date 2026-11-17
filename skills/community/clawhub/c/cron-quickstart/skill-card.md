## Description:

Use the OpenClaw cron tool for scheduling reminders, delayed follow-ups, and recurring periodic checks. Covers one-shot and recurring schedules, session targeting, delivery modes, and wake events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create one-shot reminders, recurring checks, deferred follow-ups, and session wake events with the OpenClaw cron tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron jobs can execute later or recur unexpectedly if schedules, timezones, session targets, or cleanup settings are copied without review.

Mitigation: Replace example times and timezones with deployment-specific values, prefer isolated sessions for autonomous checks, use deleteAfterRun for one-time reminders, and review recurring jobs periodically.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/terrycarter1985/skills/cron-quickstart)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides schedule patterns, payload constraints, delivery mode guidance, and job-management commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
