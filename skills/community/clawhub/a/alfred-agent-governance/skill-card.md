## Description:

Enforces YAML-based runtime policies to intercept, audit, rate-limit, and stop AI agent tool calls for secure governance in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabatech-dev](https://clawhub.ai/user/sabatech-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent platform operators use this skill to define runtime governance rules, audit tool calls, and stop active agent sessions in OpenClaw. Review the implementation before relying on it as an approval, rate-limiting, resource-limit, or audit-integrity control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents governance controls that may be incomplete or sample-level.

Mitigation: Review and test the actual implementation before relying on it for approvals, rate limiting, resource limits, or enforcement.

Risk: Audit logging may not provide tamper-evident records or operational retention controls.

Mitigation: Use controlled log storage with retention, access control, and integrity protections before using the logs for compliance or incident review.

Risk: Users may treat roadmap items such as permission rings and trust scoring as available controls.

Mitigation: Document which controls are implemented before deployment and avoid depending on planned phases for security decisions.

## Reference(s):

- [Alfred Agent Governance on ClawHub](https://clawhub.ai/sabatech-dev/skills/alfred-agent-governance)
- [Publisher profile: sabatech-dev](https://clawhub.ai/user/sabatech-dev)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes policy examples, audit-log examples, session kill commands, OWASP mapping, and a phased roadmap.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
