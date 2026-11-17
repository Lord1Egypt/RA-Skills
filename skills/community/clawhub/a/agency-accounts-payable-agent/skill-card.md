## Description:

Expert AI agent specializing in accounts payable agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouqkt](https://clawhub.ai/user/zhouqkt)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations teams use this skill to process vendor, contractor, recurring, and inter-agent payment requests while maintaining idempotency checks, approval thresholds, audit logs, and escalation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to move real funds across high-risk payment rails.

Mitigation: Use only in a payment environment with human approval, authenticated callers, vendor allowlists, immutable idempotency keys, cumulative limits, audit logs, and reconciliation before retry or rail failover.

Risk: Unrestricted access to live payment, crypto, stablecoin, wire, payroll, or vendor-payment tools could enable unauthorized or duplicate transfers.

Mitigation: Do not grant unrestricted live payment access; require scoped credentials, approval thresholds, spend limits, and human review for exceptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouqkt/skills/agency-accounts-payable-agent)
- [Publisher profile](https://clawhub.ai/user/zhouqkt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline code examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce payment status messages, audit summaries, escalation notes, and example tool-call code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
