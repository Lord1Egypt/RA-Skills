## Description:

Run a fail-closed governance preflight before consequential AI-agent actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentnomos](https://clawhub.ai/user/agentnomos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and governance reviewers use this skill to check whether consequential agent actions are authorized, scoped, reviewable, and supported by evidence before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may hold or block consequential tasks when authority, scope, approval, or evidence is missing.

Mitigation: Use it where fail-closed governance review is expected, and provide explicit current authority, scope, approvals, and required evidence when an action should proceed.

Risk: Requests may contain secrets or sensitive raw data.

Mitigation: Do not repeat sensitive values; redact them with neutral placeholders and return BLOCK when secret exposure is detected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentnomos/skills/agentnomos-governance-preflight)
- [AgentNOMOS](https://agentnomos.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Concise explanation followed by structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only advisory result; sensitive values are redacted and not_executed remains true.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
