## Description:

Provides DeFi analytics and on-chain execution support through Spraay x402, including token prices, swap quotes, wallet and portfolio profiling, DeFi positions, gas data, ENS resolution, contract reads, swap execution, and contract writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and DeFi operators use this skill to retrieve token prices, wallet and portfolio analytics, gas and FX data, swap quotes, and contract-read data. The skill can also help prepare human-approved swap execution and contract-write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid x402 endpoint calls debit USDC, and write operations can submit irreversible on-chain transactions.

Mitigation: Use a limited-purpose wallet, require explicit human approval for write operations, and manually verify transaction details before approving execution.

Risk: Wallet addresses, portfolio data, and contract call details are sent to gateway.spraay.app.

Mitigation: Install only when the gateway is trusted and avoid sending sensitive wallet data that should not leave the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plagtech/skills/defi-intelligence-x402)
- [Spraay x402 gateway](https://gateway.spraay.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON endpoint parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and curl; endpoint calls may create paid x402 requests and may return wallet, portfolio, market, contract, or transaction data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
