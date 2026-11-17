## Description:

Aurora Norfolk produces a practical 3-day northern lights planning and live-update workflow for Tim in Dereham, Norfolk, including North Norfolk coast comparisons and conservative go or no-go decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timcoy47](https://clawhub.ai/user/timcoy47)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal automation agents use this skill to maintain a Norfolk aurora watch, compare Dereham with the North Norfolk coast, and decide whether to stand down, watch, go local, or go coast.

### Deployment Geography for Use:

Norfolk, United Kingdom

## Known Risks and Mitigations:

Risk: Recurring checks or scheduler entries could produce stale or poorly timed alerts if configured casually.

Mitigation: Configure cron or scheduler entries deliberately, keep the workflow on Europe/London time, and adjust timezone behavior only when adapting the skill outside the UK.

Risk: A persistent state file could retain more context than needed for alert suppression.

Mitigation: Limit stored state to the listed aurora fields such as prior outlook, action, viewing window, chance values, notification status, and timestamps.

Risk: Stale, unavailable, or conflicting aurora and weather feeds can make travel guidance overconfident.

Mitigation: State unavailable or stale feeds, reduce confidence when authoritative sources disagree, and prefer watch or stand_down unless conditions clearly justify action.

## Reference(s):

- [Message rules](references/message-rules.md)
- [OpenClaw setup notes](references/openclaw-setup.md)
- [Source checklist](references/source-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown tables and concise text alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Europe/London local time and percentages for Dereham and the North Norfolk coast.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
