## Description:

Provides a unified API for AI agents to create, query, refund, and cancel multi-currency payments through Stripe and other payment providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building commerce, subscription, billing, or refund workflows use this skill to expose payment creation, transaction lookup, refund, and cancellation capabilities to agent applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes real money-moving actions such as payment creation, refunds, and cancellations without enough documented confirmation or limits.

Mitigation: Require explicit human approval for payment creation, refunds, and cancellations, and use least-privilege payment-provider credentials.

Risk: Installation and package-use safeguards are not documented enough for a payment workflow.

Mitigation: Use sandbox or test keys first, pin and verify the npm package version, and avoid global installation where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/agent-payment-rail)
- [GitHub Repository](https://github.com/ZhenRobotics/openclaw-agent-payment-rail)
- [npm Package](https://www.npmjs.com/package/openclaw-agent-payment-rail)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, JavaScript, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment tool descriptions, setup steps, provider configuration, and usage examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
