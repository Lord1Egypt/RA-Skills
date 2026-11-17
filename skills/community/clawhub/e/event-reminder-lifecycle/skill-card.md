## Description:

Plan, create when authorized, reconcile and retire finite event reminders for RSVPs, shopping, prep, gifts and cleanup. Use for event-bound automation, not indefinite background monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjhenriksen](https://clawhub.ai/user/jjjhenriksen)

### License/Terms of Use:

MIT

## Use Case:

External users can use this skill to plan and manage finite reminders for event tasks such as RSVPs, shopping, preparation, gifts and cleanup. It guides reconciliation when event details change and retirement when an event closes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence is incomplete because one reference could not be resolved, despite no issues being found by the reported checks.

Mitigation: Review the skill and its references before relying on its guidance, and assess whether the unresolved reference matters for the intended use.

Risk: An eligibility result could be mistaken for permission to send or proof of delivery, and concurrent runs can both see an unsent state.

Mitigation: Require scoped authorization, serialize send ownership or reconcile before retrying, and verify scheduler state and delivery receipts.

## Reference(s):

- [ClawHub release](https://clawhub.ai/jjjhenriksen/skills/event-reminder-lifecycle)
- [OpenClaw cron job schedules](https://docs.openclaw.ai/automation/cron-jobs/schedules.md)
- [Offline helper contract](references/input.md)
- [Sources and scope](references/sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, JSON]

**Output Format:** [Markdown guidance, Python helper, shell invocation, and JSON eligibility result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The offline helper reports local eligibility only; it does not authorize or send reminders.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
