## Description:

Helps users design autonomous yes/no agent loops with triggers, approval gates, output routing, memory choices, templates, and deployment checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flynndavid](https://clawhub.ai/user/flynndavid)

### License/Terms of Use:


## Use Case:

Founders, operators, and developers use this skill to turn repeatable workflows such as standup digests, lead qualification, PR reminders, revenue snapshots, and content intake into agent loop designs with clear trigger, approval, output, and memory decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Templates may encourage automatic sharing or writing of internal, personal, revenue, or private engineering data.

Mitigation: Require human approval before any loop sends or writes outputs containing personnel, customer, revenue, or private engineering data.

Risk: Loops may target the wrong Slack channels, Notion databases, recipients, or connected accounts if configuration is not scoped carefully.

Mitigation: Verify destinations and connected accounts before deployment and use least-privilege credentials for each integration.

Risk: Loop memory may retain data beyond what the workflow actually needs.

Mitigation: Define exactly what memory may store, how long it persists, and when it is deleted before enabling recurring runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flynndavid/skills/agentic-loop-designer)
- [Publisher profile](https://clawhub.ai/user/flynndavid)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with loop templates, decision trees, scoring matrices, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Slack, Notion, GitHub, Linear, Stripe, and webhook setup guidance depending on the selected loop.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
