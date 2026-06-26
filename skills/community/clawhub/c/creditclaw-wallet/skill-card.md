## Description: <br>
Give your agent spending power. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creditclaw](https://clawhub.ai/user/creditclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to let an agent register a CreditClaw wallet, request owner-approved purchases, complete supported merchant checkouts, manage wallet state, and receive payments through checkout pages or x402 flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad real-money checkout authority and can involve raw payment-card handling. <br>
Mitigation: Install only when this spending behavior is intended; keep ask-for-everything enabled unless transaction limits, merchant or domain rules, and monitoring are in place. <br>
Risk: A checkout could submit the wrong merchant, item, total, shipping address, or payment method. <br>
Mitigation: Require a fresh final review of merchant, item, total, shipping address, and payment method before any order or x402 payment is submitted. <br>
Risk: Credential or card data exposure could allow unauthorized spending. <br>
Mitigation: Keep CREDITCLAW_API_KEY limited to creditclaw.com API requests, use secure secret storage, avoid unrelated merchant accounts or saved-payment sessions, and discard decrypted card data immediately after checkout. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/creditclaw/creditclaw-wallet) <br>
- [CreditClaw Publisher Profile](https://clawhub.ai/user/creditclaw) <br>
- [CreditClaw Homepage](https://creditclaw.com) <br>
- [CreditClaw API Base](https://creditclaw.com/api/v1) <br>
- [Main Skill Instructions](SKILL.md) <br>
- [Checkout Guide](CHECKOUT-GUIDE.md) <br>
- [OpenClaw Sub-Agent Checkout Guide](agents/OPENCLAW.md) <br>
- [Stripe x402 Wallet Guide](STRIPE-X402-WALLET.md) <br>
- [Shopping Guide](SHOPPING-GUIDE.md) <br>
- [Store and Payments Guide](MY-STORE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and user-confirmed invocation; checkout behavior can involve real-money purchases.] <br>

## Skill Version(s): <br>
2.9.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
