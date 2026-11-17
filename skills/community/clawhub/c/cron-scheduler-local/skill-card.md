## Description:

Local-first recurring schedule engine for reminders, repeated tasks, and time-based execution plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture recurring reminders, repeated tasks, and future execution plans as local schedules. It helps agents add, inspect, pause, resume, and list daily, weekly, monthly, or interval-based jobs while keeping schedule data on the user's machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Schedule state is persisted locally under the user's OpenClaw memory directory.

Mitigation: Review create, pause, and resume actions before execution, and inspect stored jobs when schedule state matters.

Risk: Upcoming run times may be wrong if a job is created with an unintended timezone.

Mitigation: Specify the timezone explicitly when adding jobs and verify the computed next run time.

## Reference(s):

- [Cron Philosophy](references/philosophy.md)
- [ClawHub skill page](https://clawhub.ai/panchenbo/skills/cron-scheduler-local)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists schedule state in local JSON files under the OpenClaw memory directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
