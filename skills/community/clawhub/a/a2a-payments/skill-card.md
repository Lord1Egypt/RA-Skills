## Description:

Blockchain USDC payments via APay - pay services, manage budgets, open streaming channels, and handle x402 protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paparusi](https://clawhub.ai/user/paparusi)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let agents check USDC balances, manage spending budgets, pay APay services, open streaming payment channels, and handle x402 payment flows on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned executable payment tooling.

Mitigation: Use a version-pinned, provenance-verified plugin release before installing or deploying the skill.

Risk: The skill describes automatic USDC spending through payment and x402 flows.

Mitigation: Require strict wallet spending limits, trusted services, and independent confirmation of each payment.

Risk: Automatic x402 payment against untrusted URLs can trigger unintended spending.

Mitigation: Avoid automatic x402 payment for untrusted URLs and verify the payment destination and maximum amount first.

## Reference(s):

- [A2A Payments ClawHub Skill Page](https://clawhub.ai/paparusi/skills/a2a-payments)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with tool-call examples and configuration metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides payment, budget, streaming channel, and x402 workflows for APay tools.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
