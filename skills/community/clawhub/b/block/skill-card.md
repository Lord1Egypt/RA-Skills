## Description:

Lets an OpenClaw agent shop, request payments, and manage guardrailed wallets with owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to let an agent register with CreditClaw, check wallet status and spending permissions, make approved purchases through payment rails, request top-ups, and create payment requests. It is intended for agentic commerce workflows where spending remains subject to owner controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent real spending and payment-request capabilities.

Mitigation: Use a dedicated low-limit wallet or virtual card and keep per-transaction owner approval enabled.

Risk: API keys, card data, or payment details could be exposed during checkout.

Mitigation: Store CREDITCLAW_API_KEY in a secrets manager, send it only to creditclaw.com, and never store, log, or persist decrypted card data.

Risk: Mutable remote companion files or decrypt scripts could change after installation.

Mitigation: Review companion files before installation and do not run remotely delivered decrypt scripts unless independently verified and sandboxed.

Risk: If encrypted-card checkout runs in the main agent, decrypted card data can enter the main context.

Mitigation: Use an ephemeral sub-agent for card decryption and checkout, and do not allow main-agent card decryption.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/jononovo/skills/block)
- [Publisher Profile](https://clawhub.ai/user/jononovo)
- [CreditClaw Main Skill Documentation](https://creditclaw.com/amazon/skill.md)
- [Encrypted Card Guide](https://creditclaw.com/amazon/encrypted-card.md)
- [Crossmint Wallet Guide](https://creditclaw.com/amazon/crossmint-wallet.md)
- [Spending Permissions Guide](https://creditclaw.com/amazon/spending.md)
- [Wallet Management Guide](https://creditclaw.com/amazon/management.md)
- [Heartbeat Guide](https://creditclaw.com/amazon/heartbeat.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with curl examples, configuration notes, and JSON request and response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and uses CreditClaw HTTPS API endpoints.]

## Skill Version(s):

1.0.7 (source: server release metadata, created 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
