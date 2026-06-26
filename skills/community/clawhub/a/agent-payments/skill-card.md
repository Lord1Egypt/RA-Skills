## Description: <br>
x402 Agent Payments helps AI agents accept fiat and crypto payments, manage wallets and transfers, and run batch payment or payroll workflows across Stripe, Coinbase Commerce, Coinbase CDP, and Spraay x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let agents prepare payment, invoicing, wallet, transfer, payroll, and batch payment workflows while requiring user confirmation before any real-money action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent initiate workflows involving real funds, including charges, refunds, wallet transfers, payroll batches, and invoices. <br>
Mitigation: Require explicit user confirmation of the exact amount, currency, recipient, provider, and action before any payment-related request is executed. <br>
Risk: Provider credentials can authorize sensitive payment or transfer operations. <br>
Mitigation: Use test mode and least-privilege API keys where possible, and avoid granting production transfer authority unless it is required. <br>
Risk: Crypto transfers may be irreversible after confirmation. <br>
Mitigation: Verify destination addresses, network, asset, and amount with the user before sending transfer or batch payment requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/plagtech/agent-payments) <br>
- [Spraay Docs](https://docs.spraay.app) <br>
- [Spraay x402 Gateway](https://gateway.spraay.app) <br>
- [Stripe Docs](https://docs.stripe.com) <br>
- [Coinbase Commerce Docs](https://docs.cdp.coinbase.com/commerce) <br>
- [Coinbase CDP Docs](https://docs.cdp.coinbase.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires provider environment variables for enabled payment rails; payment actions should be confirmed with exact amount, currency, recipient, provider, and action before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
