## Description: <br>
Provides agent-facing guidance for CreditClaw payment workflows published as an Adyen release, including owner-approved card spending, x402/USDC wallet payments, checkout pages, invoices, and wallet management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to CreditClaw financial workflows for owner-approved purchases, wallet balance checks, x402 payments, checkout pages, invoices, and payment status monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is branded as Adyen while the artifact behavior centers on CreditClaw financial and commerce workflows. <br>
Mitigation: Install only when the intended integration is CreditClaw payment management, and review the publisher page and documentation before enabling credentials. <br>
Risk: The skill can guide agents through broad money-moving actions such as purchases, wallet spending, checkout pages, invoices, and top-up requests. <br>
Mitigation: Use strict per-purchase approval, low spending limits, scoped and rotated credentials, and regular transaction review. <br>
Risk: Payment workflows may expose card data, buyer PII, invoice emails, shipping addresses, or webhook event data. <br>
Mitigation: Use secure secret storage, verify webhooks, minimize logs, avoid persisting decrypted card details, and limit access to payment-related records. <br>
Risk: Public shop publishing and invoice sending can create external-facing payment surfaces. <br>
Mitigation: Require human review before publishing shop pages, sending invoices, or exposing payment links. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codejika/adyen) <br>
- [Publisher Profile](https://clawhub.ai/user/codejika) <br>
- [CreditClaw Skill Documentation](https://creditclaw.com/skill.md) <br>
- [CreditClaw Encrypted Card Guide](https://creditclaw.com/encrypted-card.md) <br>
- [CreditClaw x402 Wallet Guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [CreditClaw Checkout Guide](https://creditclaw.com/checkout.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with HTTP examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and covers payment, wallet, checkout, invoice, webhook, and approval workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
