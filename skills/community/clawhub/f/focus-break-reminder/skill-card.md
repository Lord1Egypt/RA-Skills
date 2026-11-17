## Description:

Workspace wellness break reminder with configurable work interval, cooldown, idle reset, quiet hours, and per-day caps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxj0276](https://clawhub.ai/user/lxj0276)

### License/Terms of Use:


## Use Case:

OpenClaw users and workspace tool developers use this skill to configure optional break reminders during long work sessions, including reminder timing, quiet hours, snooze behavior, status commands, and minimal restart-safe state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default reminder text and timezone may not match every workspace locale.

Mitigation: Review and adjust the reminder templates and timezone before installation.

Risk: The skill expects a small local JSON state file containing reminder settings and timestamps.

Mitigation: Store only the minimum timing state needed for reminder logic and protect it according to local workspace policy.

Risk: Wellness reminders could be mistaken for medical advice if expanded beyond break prompts.

Mitigation: Keep reminder copy practical and non-medical, and avoid diagnosis or treatment guidance.

## Reference(s):

- [Configuration Example](references/config.example.json)
- [Test Cases](references/test-cases.md)
- [ClawHub Skill Page](https://clawhub.ai/lxj0276/skills/focus-break-reminder)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown guidance with JSON configuration examples and command behavior descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces optional reminder logic and local state guidance; no network or credential behavior is expected.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
