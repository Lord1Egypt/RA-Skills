## Description:

Provides agent payment wallets and spending controls for online purchases, checkout pages, invoices, and payment collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let agents register CreditClaw wallets, check spending permissions, request or execute approved purchases, manage balances, and create payment collection flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live financial authority through CreditClaw wallets or payment-card workflows.

Mitigation: Keep approval mode set to ask for every purchase unless strong per-transaction, daily, monthly, category, and domain limits are configured.

Risk: CREDITCLAW_API_KEY and webhook secrets authorize sensitive wallet operations if exposed.

Mitigation: Store secrets in a secure secrets manager and send the API key only to CreditClaw API endpoints.

Risk: Encrypted card checkout can expose plaintext card details if the main agent performs checkout directly.

Mitigation: Use the documented ephemeral sub-agent checkout flow, and never store, log, or persist decrypted card data.

Risk: Downloaded or delivered card files and curl-based install/update flows can affect the agent's payment behavior.

Mitigation: Review delivered card files before use and do not run curl-based installation or updates without independent checksum or signature controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triplehippo/skills/amex)
- [Publisher profile](https://clawhub.ai/user/triplehippo)
- [CreditClaw Shopping Skill](https://creditclaw.com/shopping/skill.md)
- [CreditClaw Checkout Guide](https://creditclaw.com/shopping/checkout.md)
- [Encrypted Card Guide](https://creditclaw.com/shopping/encrypted-card.md)
- [Spending Permissions Guide](https://creditclaw.com/shopping/spending.md)
- [Stripe x402 Wallet Guide](https://creditclaw.com/shopping/stripe-x402-wallet.md)
- [Machine-readable skill metadata](https://creditclaw.com/shopping/skill.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown instructions with curl commands, JSON request examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and may handle payment authority or card material depending on the enabled payment rail.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
