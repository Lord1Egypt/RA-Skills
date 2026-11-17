## Description:

Easy-to-use agentic wallets powered by Stripe for agent purchases, top-ups, checkout pages, and A2A payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to give an agent a CreditClaw payment wallet, request owner-approved spending, monitor balance and permissions, create checkout pages, and receive or send payments through supported rails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend real money through CreditClaw payment rails.

Mitigation: Keep approval_mode set to ask_for_everything unless clear spending limits are configured, check spending permissions before purchases, and rely on owner approval for higher-risk transactions.

Risk: The skill uses CREDITCLAW_API_KEY as payment authority.

Mitigation: Store CREDITCLAW_API_KEY only in a secure secrets manager or environment variable and send it only to creditclaw.com API endpoints.

Risk: Encrypted-card checkout can expose decrypted card details if handled in the main agent context.

Mitigation: Use the ephemeral sub-agent checkout flow for each transaction, do not store or log decrypted card data, and delete checkout context after confirmation.

Risk: Checkout may involve server-delivered scripts or remote instructions.

Mitigation: Validate delivered decrypt scripts and checkout instructions before execution and run them in a tightly controlled sandbox.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jononovo/skills/cash)
- [CreditClaw main skill documentation](https://creditclaw.com/stripe/skill.md)
- [CreditClaw checkout guide](https://creditclaw.com/stripe/checkout.md)
- [CreditClaw encrypted card guide](https://creditclaw.com/stripe/encrypted-card.md)
- [CreditClaw spending permissions guide](https://creditclaw.com/stripe/spending.md)
- [CreditClaw wallet management guide](https://creditclaw.com/stripe/management.md)
- [CreditClaw heartbeat guide](https://creditclaw.com/stripe/heartbeat.md)
- [CreditClaw Crossmint wallet guide](https://creditclaw.com/stripe/crossmint-wallet.md)
- [CreditClaw skill metadata](https://creditclaw.com/stripe/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, JSON examples, endpoint tables, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API requests.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact skill metadata reports 2.3.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
