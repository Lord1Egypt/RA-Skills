## Description: <br>
Guides agents through CreditClaw-powered checkout pages, wallet payments, encrypted-card purchases, spending checks, invoices, and payment links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to connect a CreditClaw bot, manage spending permissions, create payment collection surfaces, request wallet or card payments, and monitor balances and approvals. <br>

### Deployment Geography for Use: <br>
Global; Crossmint physical-goods purchase examples state US shipping addresses only. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real spending, card checkout, wallet payments, invoicing, and payment-link creation. <br>
Mitigation: Install only for intentional payment workflows, keep ask-for-everything approvals enabled, and set low transaction, daily, and monthly limits. <br>
Risk: A leaked CREDITCLAW_API_KEY could authorize wallet, payment, or card-related operations. <br>
Mitigation: Store the key in a secrets manager, rotate it when exposed, and send it only to CreditClaw API endpoints. <br>
Risk: Decrypted card data, buyer emails, and shipping addresses are sensitive financial or personal data. <br>
Mitigation: Do not log or persist decrypted card data, avoid delegating it to secondary agents, and minimize handling of buyer and shipping data. <br>
Risk: Provider identity and some money-moving/card-handling capabilities are under-disclosed in the security evidence. <br>
Mitigation: Review the publisher, service terms, payment rails, approval model, and operational controls before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jononovo/checkout) <br>
- [CreditClaw Main Skill Documentation](https://creditclaw.com/skill.md) <br>
- [CreditClaw Encrypted Card Documentation](https://creditclaw.com/encrypted-card.md) <br>
- [CreditClaw Stripe x402 Wallet Documentation](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [CreditClaw Checkout Documentation](https://creditclaw.com/checkout.md) <br>
- [CreditClaw Management Documentation](https://creditclaw.com/management.md) <br>
- [CreditClaw Heartbeat Documentation](https://creditclaw.com/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with curl examples and JSON request/response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
