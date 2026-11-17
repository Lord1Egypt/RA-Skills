## Description:

Enforce team communication discipline and execution hygiene in shared work channels by detecting repeat messages, routing issues, missing ownership, stale review work, noisy updates, and then producing corrective actions, escalation notes, and manager-ready summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ptaramona](https://clawhub.ai/user/ptaramona)

### License/Terms of Use:

MIT-0

## Use Case:

Team leads, operations managers, and agent operators use this skill to review shared work channels for communication and execution hygiene issues. It produces concise findings, owner-specific corrective actions, escalation notes, and leadership summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reviews team messages and task status, which may include sensitive operational details if the review scope is too broad.

Mitigation: Install only where reviewing team messages and task status is appropriate, and keep outputs scoped to non-sensitive operational summaries.

Risk: Public-ready reports could accidentally include secrets, private endpoints, webhook URLs, or personal identifiers.

Mitigation: Apply the public safety checklist before publishing and replace environment-specific content with generic placeholders.

## Reference(s):

- [Enforcement Checklist](references/enforcement-checklist.md)
- [Message Templates](references/message-templates.md)
- [Public Safety Checklist](references/public-safety-checklist.md)
- [ClawStation](https://clawstation.dev)
- [ClawHub skill page](https://clawhub.ai/ptaramona/skills/drill-sergeant-skill)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with structured findings and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include type, severity, evidence, action, and owner, followed by top actions, escalations, or an all-clear.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
