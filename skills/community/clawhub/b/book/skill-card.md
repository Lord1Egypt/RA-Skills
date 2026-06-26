## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent make approved purchases, manage wallet balances, request top-ups, and create checkout or payment flows through CreditClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate real spending or payment collection to an agent. <br>
Mitigation: Install only for intended commerce use, keep approval mode set to ask for every purchase unless strict limits are configured, and use a dedicated low-balance wallet or card. <br>
Risk: Credentials and webhook secrets can authorize sensitive wallet or commerce actions. <br>
Mitigation: Store CREDITCLAW_API_KEY and webhook secrets in a secrets manager and avoid exposing them outside approved CreditClaw API calls. <br>
Risk: Delivered card files or bot-message payloads may contain sensitive payment workflow data. <br>
Mitigation: Treat delivered files and bot messages as sensitive, avoid logging decrypted card data, and review payment-link or shop features before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TripleHippo/book) <br>
- [Publisher profile](https://clawhub.ai/user/TripleHippo) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill metadata](https://creditclaw.com/stripe/skill.json) <br>
- [CreditClaw skill guide](https://creditclaw.com/stripe/skill.md) <br>
- [Checkout guide](https://creditclaw.com/stripe/checkout.md) <br>
- [Encrypted card guide](https://creditclaw.com/stripe/encrypted-card.md) <br>
- [Spending permissions guide](https://creditclaw.com/stripe/spending.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/stripe/stripe-x402-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
