## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an AI agent shop online, request payments, check wallet status, and make CreditClaw payment-related API calls within owner-managed approvals, limits, and monitoring.

### Deployment Geography for Use:

Global, with US-only support for Amazon shipping workflows.

## Known Risks and Mitigations:

Risk: The skill gives an agent delegated authority to initiate real-money purchases and payment-signing flows.

Mitigation: Keep ask-for-everything approval enabled unless narrow merchant or category limits, low thresholds, strong monitoring, and a wallet freeze path are in place.

Risk: CREDITCLAW_API_KEY functions as a financial credential.

Mitigation: Store it only in a secure secrets manager or environment variable, send it only to creditclaw.com API endpoints, and freeze or rotate access if exposure is suspected.

Risk: Shipping, merchant, wallet, and transaction data may be sent to CreditClaw for fulfillment and approvals.

Mitigation: Review data-sharing expectations before enabling the skill and monitor activity through the owner dashboard.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/triplehippo/skills/card)
- [CreditClaw Skill and API Reference](https://creditclaw.com/creditcard/skill.md)
- [Shopping Guide](https://creditclaw.com/creditcard/shopping.md)
- [Amazon Purchase Guide](https://creditclaw.com/creditcard/amazon.md)
- [Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with bash and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
