## Description:

Daily Recorder Assistant helps a user capture morning feedback, evening reviews, status queries, energy scores, next-day plans, and daily or weekly summaries in OpenClaw notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkctly](https://clawhub.ai/user/tkctly)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to run a structured daily journaling loop with morning check-ins, evening retrospectives, plan capture, progress analysis, and optional recurring reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores daily notes, state, plans, and reflections in the local OpenClaw workspace, which may contain personal routine and productivity data.

Mitigation: Install and run it only in a workspace where local journal storage is acceptable, and manage file permissions for the OpenClaw notes directory and skill state file.

Risk: The optional cron setup can create persistent recurring reminders to the configured user and channel.

Mitigation: Treat setup_cron.py as optional; review the target channel and user, list existing OpenClaw cron jobs, and remove unwanted jobs manually.

Risk: The security summary notes that promised user isolation is not fully reflected in the storage design for shared use.

Mitigation: Use it for single-user workflows unless storage is changed and reviewed to separate notes and state by user and channel.

## Reference(s):

- [Chinese interaction templates](references/interaction-templates-zh.md)
- [English interaction templates](references/interaction-templates-en-full.md)
- [ClawHub skill page](https://clawhub.ai/tkctly/skills/daily-recorder-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with JSON snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local note and state files; optional cron setup can create recurring OpenClaw reminders.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
