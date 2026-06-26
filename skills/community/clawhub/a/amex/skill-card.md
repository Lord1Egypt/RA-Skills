## Description: <br>
Provides agents with CreditClaw payment wallets, encrypted-card checkout, spending controls, and selling workflows for online purchases and payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent register with CreditClaw, check wallet status and spending rules, request or execute approved purchases, manage top-ups, and create checkout pages, invoices, or payment links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable agents to make real purchases, request top-ups, create payment links, publish shops, and send invoices. <br>
Mitigation: Keep approval-required spending limits enabled and manually review any invoice, payment-link, shop-publishing, top-up, or real-purchase action before execution. <br>
Risk: The skill handles real card data through encrypted-card checkout flows. <br>
Mitigation: Prefer a low-limit virtual card, use the ephemeral sub-agent checkout flow, and avoid the main-agent card-decryption fallback. <br>
Risk: Delivered decrypt scripts and card files could expose sensitive payment data if handled unsafely. <br>
Mitigation: Do not run delivered decrypt scripts outside a sandbox, never store or log decrypted card data, and remove temporary checkout artifacts after use. <br>
Risk: The API key authorizes CreditClaw actions on behalf of the agent. <br>
Mitigation: Store CREDITCLAW_API_KEY in a secret manager and send it only to CreditClaw API endpoints. <br>
Risk: The AMEX-branded listing may imply an affiliation not proven by the server evidence. <br>
Mitigation: Verify the listing is not implying an unsupported American Express affiliation before publication or use. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/TripleHippo/amex) <br>
- [CreditClaw Shopping Skill](https://creditclaw.com/shopping/skill.md) <br>
- [CreditClaw Encrypted Card Guide](https://creditclaw.com/shopping/encrypted-card.md) <br>
- [CreditClaw Spending Permissions](https://creditclaw.com/shopping/spending.md) <br>
- [CreditClaw Checkout Guide](https://creditclaw.com/shopping/checkout.md) <br>
- [CreditClaw Stripe x402 Wallet Guide](https://creditclaw.com/shopping/stripe-x402-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
