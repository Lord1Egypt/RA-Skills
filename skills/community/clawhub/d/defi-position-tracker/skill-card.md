## Description:

Monitor and analyze DeFi positions across protocols and chains, including LP positions, staking rewards, yield farming returns, impermanent loss, and cost basis per position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DeFi operators, DAO contributors, and fund or treasury analysts use this skill to prepare portfolio snapshots, impermanent-loss estimates, staking-reward summaries, and structured exports for tax or dashboard workflows. It is not intended for executing trades, swaps, bridges, staking transactions, payroll, NFT tracking, or generic spot-price alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example API calls can disclose wallet addresses, position identifiers, portfolio details, and API keys to third-party DeFi data providers.

Mitigation: Use read-only API keys where possible, review each provider's terms before querying, and avoid sending unnecessary wallets or position IDs.

Risk: Users may confuse analysis workflows with transaction execution.

Mitigation: Keep usage limited to read-only portfolio analysis and do not provide wallet private keys, seed phrases, signing access, or transaction approval authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/defi-position-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, GraphQL, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API query examples, DeFi portfolio schemas, tax handoff structures, monitoring thresholds, and operational caveats.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
