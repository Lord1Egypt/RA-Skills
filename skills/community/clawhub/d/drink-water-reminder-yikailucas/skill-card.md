## Description:

Create, manage, and remove periodic hydration reminders via OpenClaw cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:


## Use Case:

External OpenClaw users can ask an agent to create, list, or remove recurring hydration reminders delivered to the current session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reminder cron job persists until it is removed.

Mitigation: Use the remove script or OpenClaw cron management to disable the reminder when it is no longer wanted.

Risk: Adding a reminder may replace an existing OpenClaw cron job named drink-water-reminder.

Mitigation: List current reminders before adding a new one when preserving an existing hydration reminder matters.

Risk: Removing reminders deletes all OpenClaw cron jobs with the exact drink-water-reminder name.

Mitigation: Reserve that job name for this hydration reminder and list matching jobs before removal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yikailucas/skills/drink-water-reminder-yikailucas)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Text with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, replace, list, or remove a persistent OpenClaw cron job named drink-water-reminder.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
