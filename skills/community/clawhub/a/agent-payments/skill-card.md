## Description:

Unified payment skill for AI agents across Stripe for fiat and card payments, Coinbase Commerce for crypto checkout, Coinbase CDP for wallets and transfers, and the Spraay x402 gateway for batch payments, payroll, invoices, and token price lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent prepare payment, invoice, checkout, wallet, transfer, payroll, and batch payout workflows across supported payment rails. It is intended for real payment operations that require explicit user review before funds move.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help an agent initiate real payment operations, including charges, refunds, subscriptions, wallets, transfers, payroll, and batch payouts.

Mitigation: Require explicit user confirmation of recipient, amount, currency, fee, cadence, and refund details before execution.

Risk: Crypto transfers may be irreversible and may expose high-value wallets if overly broad credentials or balances are used.

Mitigation: Use least-privilege API keys, keep agent-managed wallets low-balance, and verify crypto recipient addresses before signing or sending.

Risk: A misconfigured Spraay gateway could route payment requests or x402 proofs to an unintended endpoint.

Mitigation: Use the official HTTPS Spraay gateway by default and require explicit user confirmation before using a controlled alternative gateway.

Risk: Unsigned transaction data returned by a gateway could differ from the user-approved payment request.

Mitigation: Decode and verify transaction calldata locally against the confirmed recipients, amounts, token, chain, contract, and allowance bounds before requesting any signature.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plagtech/skills/agent-payments)
- [Spraay](https://spraay.app)
- [Spraay gateway catalog](https://gateway.spraay.app/.well-known/x402.json)
- [Spraay docs](https://docs.spraay.app)
- [BPA 1.0 spec](https://docs.spraay.app/bpa/1.0/)
- [Stripe docs](https://docs.stripe.com)
- [Coinbase Commerce docs](https://docs.cdp.coinbase.com/commerce)
- [Coinbase CDP docs](https://docs.cdp.coinbase.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces provider-specific command examples and verification guidance; payment execution requires user confirmation and configured provider credentials.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
