## Description:

Place a real phone call paid in USDC over x402. The payphone needs no account: buy minutes, name the number, and stream your own voice over a websocket. Plans lease a number that also receives texts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to place paid, consent-based phone calls, stream their own voice, or lease a number through the Agentgates phone service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone calls and number leases can spend the owner's funds.

Mitigation: Get the owner's authorization before payment or stay within an explicitly set spending limit; check current prices first.

Risk: Phone numbers, task details, and call audio pass through external services, and data retention claims are unverified.

Mitigation: Review the provider's privacy terms before sharing sensitive information, and do not assume call data is not stored.

Risk: Unwanted calls can contact people who have not agreed to receive them.

Mitigation: Call only recipients who have consented to be contacted.

## Reference(s):

- [Phone contract and usage documentation](https://agentgates.ai/api/account/docs/phone)
- [Phone products, plans, and prices](https://agentgates.ai/api/account/catalog)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes phone-call and websocket audio usage guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
