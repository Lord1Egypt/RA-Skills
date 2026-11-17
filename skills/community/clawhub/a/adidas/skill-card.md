## Description:

Lets an agent shop online with CreditClaw guardrailed wallets, owner approval, and payment rails for Amazon, Shopify, SaaS, online merchants, and x402 services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent make online purchases, request payment signatures, monitor wallet status, and work within owner-defined spending guardrails.

### Deployment Geography for Use:

Global; Amazon and pre-paid wallet shipping flows document US-only shipping addresses.

## Known Risks and Mitigations:

Risk: The skill can exercise real spending authority through CreditClaw.

Mitigation: Start with strict approval mode, low per-transaction and daily limits, and merchant or category restrictions.

Risk: CREDITCLAW_API_KEY is a spending credential.

Mitigation: Store it in a secrets manager, avoid logging it, and send it only to CreditClaw API endpoints.

Risk: Purchase flows may handle sensitive shipping addresses and checkout details.

Mitigation: Avoid logging full addresses, headers, payment responses, or other sensitive purchase data.

Risk: The artifact documents curl-based remote installation paths.

Mitigation: Prefer a packaged or verified release before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jononovo/skills/adidas)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw Stripe skill](https://creditclaw.com/stripe/skill.md)
- [Shopping guide](https://creditclaw.com/stripe/shopping.md)
- [Amazon purchase guide](https://creditclaw.com/stripe/amazon.md)
- [Pre-paid wallet guide](https://creditclaw.com/stripe/prepaid-wallet.md)
- [Self-hosted card guide](https://creditclaw.com/stripe/self-hosted-card.md)
- [Stripe x402 wallet guide](https://creditclaw.com/stripe/stripe-x402-wallet.md)
- [Heartbeat guide](https://creditclaw.com/stripe/heartbeat.md)
- [Skill metadata](https://creditclaw.com/stripe/skill.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with JSON examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter reports 2.3.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
