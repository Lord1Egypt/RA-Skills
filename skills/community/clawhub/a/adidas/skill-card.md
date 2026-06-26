## Description: <br>
This skill helps an agent shop online with CreditClaw wallets, owner approval, and payment rails for Amazon, Shopify, SaaS, online merchant, and x402 purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to configure CreditClaw wallets, check spending permissions, and make owner-controlled online purchases or x402 payments. <br>

### Deployment Geography for Use: <br>
Global, with US-only shipping for Amazon purchase flows described in the artifact guidance. <br>

## Known Risks and Mitigations: <br>
Risk: The marketplace title suggests Adidas shopping, while the artifact grants broader CreditClaw shopping and payment authority. <br>
Mitigation: Install only when broad CreditClaw payment authority is intended, and restrict merchants, categories, and spending limits before use. <br>
Risk: CREDITCLAW_API_KEY is a spending credential that can authorize purchases and payment requests. <br>
Mitigation: Store the key in a secrets manager, use it only with creditclaw.com API endpoints, and rotate or revoke it if exposure is suspected. <br>
Risk: The skill can submit real-money purchases, payment links, and x402 payment-signing requests. <br>
Mitigation: Prefer approval for every purchase and review the merchant, amount, shipping address, payment link, or x402 recipient before allowing transactions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jononovo/adidas) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw Stripe skill and API reference](https://creditclaw.com/stripe/skill.md) <br>
- [CreditClaw shopping guide](https://creditclaw.com/stripe/shopping.md) <br>
- [CreditClaw Amazon purchase guide](https://creditclaw.com/stripe/amazon.md) <br>
- [CreditClaw pre-paid wallet guide](https://creditclaw.com/stripe/prepaid-wallet.md) <br>
- [CreditClaw self-hosted card guide](https://creditclaw.com/stripe/self-hosted-card.md) <br>
- [CreditClaw Stripe x402 wallet guide](https://creditclaw.com/stripe/stripe-x402-wallet.md) <br>
- [CreditClaw heartbeat guide](https://creditclaw.com/stripe/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and may initiate real-money shopping or payment workflows through CreditClaw APIs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter and package metadata report 2.3.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
