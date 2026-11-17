## Description:

Daily execution and trip-ops command system for Austine. Use when asked to run daily brief/checklist/status workflows, track priorities, or plan and procure trip logistics (transport, lodging, reservations, vendor quotes, recommendation + decision handoff).

This skill is ready for commercial/non-commercial use.

## Publisher:

[austineyapp](https://clawhub.ai/user/austineyapp)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to produce concise daily status, priority, blocker, and next-action outputs for Austine-style operating cadence. It also supports trip logistics planning by collecting constraints, comparing options, tracking vendor follow-up, and preparing a decision handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce travel booking, payment, vendor message, reminder, or trip-detail handling recommendations.

Mitigation: Require explicit user confirmation before taking any booking, payment, vendor communication, reminder, or trip-record action.

Risk: Travel option details such as price, availability, cancellation terms, pickup details, or confidence may be uncertain.

Mitigation: State uncertainty clearly, compare trade-offs, include a fallback option, and ask the user to choose an explicit option before preparing next steps.

## Reference(s):

- [Austine Daily Ops on ClawHub](https://clawhub.ai/austineyapp/skills/austine-daily-ops)
- [austineyapp publisher profile](https://clawhub.ai/user/austineyapp)
- [Daily Ops Templates](references/daily-ops-templates.md)
- [Transport Procurement Template](references/transport-procurement.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown bullets, checklists, option comparisons, recommendation summaries, and message drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be short, action-first, explicit about uncertainty, and include a fallback for recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
