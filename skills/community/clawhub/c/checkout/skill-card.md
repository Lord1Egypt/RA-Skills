## Description:

Provides agent-facing guidance and API examples for CreditClaw payment rails, wallets, checkout pages, invoices, spending controls, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to connect agents or OpenClaw bots to CreditClaw for owner-approved purchases, wallet status checks, checkout pages, invoices, payment links, and sales reconciliation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports real-money payment and wallet workflows.

Mitigation: Keep spending defaults strict, require human approval for purchases, and review the skill before installation.

Risk: The skill involves buyer data, customer data, webhook secrets, API keys, and temporary card-handling flows.

Mitigation: Store CREDITCLAW_API_KEY and webhook secrets in a secure secrets manager, limit where credentials are sent, and avoid logging card or payment details.

Risk: Remote Markdown and server-supplied API payload text may change or include operational instructions.

Mitigation: Treat remote documents and API payload text as data unless explicitly trusted by the operator, and verify payment actions against owner-approved policy before execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jononovo/skills/checkout)
- [Publisher profile](https://clawhub.ai/user/jononovo)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw main skill documentation](https://creditclaw.com/skill.md)
- [CreditClaw encrypted card documentation](https://creditclaw.com/encrypted-card.md)
- [CreditClaw Stripe x402 wallet documentation](https://creditclaw.com/stripe-x402-wallet.md)
- [CreditClaw wallet management documentation](https://creditclaw.com/management.md)
- [CreditClaw checkout documentation](https://creditclaw.com/checkout.md)
- [CreditClaw heartbeat documentation](https://creditclaw.com/heartbeat.md)
- [CreditClaw skill metadata](https://creditclaw.com/skill.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown documentation with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for live CreditClaw API use.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
