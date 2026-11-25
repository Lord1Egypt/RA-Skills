## Description:

Use to run supervised autopilot cycles under a bounded, revocable session grant: intents, policy checks, approvals, receipts, and zero-custody local signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain FarmDash sessions, coordinate DeFi intent workflows, and run supervised or bounded autonomous cycles with execution authority checked against policy and user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner judged the package benign with medium confidence, but its inspection was partial because four local references could not be verified.

Mitigation: Review the referenced targets and scan the complete package when those files are available.

Risk: Incorrect plans or stale authority checks could lead to unintended DeFi actions.

Mitigation: Check current domain readiness and scoped execution authority, follow policy and approval gates, and stop when status or settlement is unclear.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical Autonomous Operator skill manual](https://www.farmdash.one/agents/skills/farmdash-autonomous-operator)
- [FarmDash security and authority boundaries](https://www.farmdash.one/security)
- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-autonomous-operator)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Natural-language guidance and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session and execution results depend on current service status, policy checks, and valid user authorization.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
