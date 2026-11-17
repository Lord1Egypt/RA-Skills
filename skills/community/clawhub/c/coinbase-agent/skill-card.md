## Description:

Autonomous Coinbase integration for portfolio tracking, trading, and on-chain payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stienski](https://clawhub.ai/user/stienski)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review Coinbase balances, request trades, and initiate on-chain payments through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act on live Coinbase trading and crypto transfer workflows without enough confirmation or safety scoping.

Mitigation: Use tightly scoped Coinbase API keys, disable withdrawals or transfers unless required, and require per-transaction confirmation for every trade, swap, or crypto transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stienski/skills/coinbase-agent)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown or plain text with balance reports, trade confirmations, and transaction hashes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Coinbase account, portfolio, and transaction data when authenticated.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
