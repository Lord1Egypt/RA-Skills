## Description:

Local-first recurring schedule engine for reminders, repeated tasks, and time-based execution plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morrison230](https://clawhub.ai/user/morrison230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture recurring reminders, repeated tasks, and time-based execution plans as local schedules that can be added, inspected, paused, resumed, and listed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder titles, notes, and tags are stored locally under the user's home directory and may contain sensitive personal or work details.

Mitigation: Avoid placing highly sensitive details in job notes unless the local account and home directory permissions are protected.

Risk: New or modified recurring jobs could create unwanted reminders or time-based execution plans if accepted without review.

Mitigation: Confirm schedule details before allowing the agent to create or modify jobs, and use pause or resume controls to manage active schedules.

Risk: The add-job script defaults to the Asia/Tokyo timezone when no timezone is supplied.

Mitigation: Override the timezone when Asia/Tokyo is not the intended schedule timezone.

## Reference(s):

- [Cron Philosophy](references/philosophy.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local JSON schedule state under ~/.openclaw/workspace/memory/cron.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
