## Description:

Bitcoin Lightning wallet for agents — balances, invoices, payments, BTC/USD swaps, QR codes, price conversion, transaction history, non-custodial (Spark) accounts, and L402 auto-pay client via the Blink API. All output is JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pretyflaco](https://clawhub.ai/user/pretyflaco)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use Blink to inspect Lightning wallet balances and transactions, create and monitor invoices, send payments, swap BTC and USD balances, and access Spark wallet and L402 payment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lightning payments and swaps can spend funds and cannot be reversed once completed.

Mitigation: Use Read and Receive scopes where possible; before spending, check the balance, probe fees, and confirm the recipient and amount with the user.

Risk: A Spark seed grants spend authority over a self-custodial wallet.

Mitigation: Keep the seed secret and use it only through the protected environment variable; do not expose it in logs or output.

Risk: L402 auto-pay may reuse cached paid tokens, and satoshi budgets do not cover fees or plain token transfers.

Mitigation: Dry-run first, configure a budget and approved-domain allowlist, check transaction history after errors before retrying, and account separately for fees and token transfers.

## Reference(s):

- [Blink API and Authentication](references/blink-api-and-auth.md)
- [Invoice Lifecycle](references/invoice-lifecycle.md)
- [Payment Operations](references/payment-operations.md)
- [Swap Operations](references/swap-operations.md)
- [Non-custodial Spark Wallets](references/non-custodial.md)
- [Blink Agent Playbook](https://dev.blink.sv/api/agent-playbook)
- [Blink API Documentation](https://dev.blink.sv)
- [Blink Skills Project Homepage](https://github.com/blinkbitcoin/blink-skills)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON objects; some commands emit sequential event objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine-readable results; fields vary by wallet operation.]

## Skill Version(s):

3.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
