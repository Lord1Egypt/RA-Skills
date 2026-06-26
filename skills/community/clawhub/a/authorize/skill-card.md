## Description: <br>
Authorize.net is a payments provider; this CreditClaw skill helps agents use owner-approved payment cards, wallets, checkout pages, invoices, and storefront payment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to CreditClaw payment rails for controlled spending, x402 wallet payments, checkout pages, invoices, storefronts, balance checks, and owner approval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real-money payment and wallet operations. <br>
Mitigation: Keep ask-for-everything approval enabled, use low limits or dedicated funding, and verify each recipient, merchant, amount, and shipping detail before sending payment requests. <br>
Risk: The release branding may look like an Authorize.net integration while the artifact primarily describes CreditClaw payment rails. <br>
Mitigation: Install only when the intended dependency is CreditClaw, and review the release page, skill files, and payment provider assumptions before deployment. <br>
Risk: A leaked CreditClaw API key or webhook secret could expose payment authority. <br>
Mitigation: Store secrets in a secure secret manager, send the API key only to creditclaw.com API endpoints, and rotate or revoke credentials immediately if exposure is suspected. <br>
Risk: The Crossmint purchase flow is present in artifact documentation but is not declared in the manifest and was called out by security guidance. <br>
Mitigation: Avoid the Crossmint flow until it is fully declared in the manifest and separately reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/codejika/authorize) <br>
- [CreditClaw skill documentation](https://creditclaw.com/skill.md) <br>
- [Encrypted card guide](https://creditclaw.com/encrypted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [Checkout guide](https://creditclaw.com/checkout.md) <br>
- [Wallet management guide](https://creditclaw.com/management.md) <br>
- [Heartbeat guide](https://creditclaw.com/heartbeat.md) <br>
- [Machine-readable skill metadata](https://creditclaw.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with curl examples, JSON request and response examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
