## Description:

AIUSD Core provides structured trading tools and account management for agents that need to buy or sell assets, check balances, stake funds, or manage positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tech-fe-aiusd](https://clawhub.ai/user/tech-fe-aiusd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to manage AIUSD accounts and route trading workflows across spot markets, perpetual futures, prediction markets, staking, withdrawals, market data, and conditional monitors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an npm-distributed CLI for wallet authentication, trading, withdrawals, staking, leveraged positions, and automation workflows.

Mitigation: Install only from a trusted aiusd-core supply chain, prefer a reviewed and pinned local version, and use limited balances.

Risk: Login, wallet restore, and funding flows can expose sensitive account access if URLs, domains, or mnemonic contents are mishandled.

Mitigation: Verify login URLs and domains, never place mnemonic contents in chat, and only restore from an explicitly chosen local backup path.

Risk: Trades, withdrawals, staking, leveraged futures, prediction-market orders, and auto-buy monitors can move real funds or create financial exposure.

Mitigation: Require fresh user confirmation before every trade, withdrawal, stake, leveraged position, prediction order, or auto-buy rule.

Risk: Deposits can be lost when the wrong stablecoin is sent to a chain-specific deposit address.

Mitigation: Confirm the chain and token before deposit; use only USDT on Tron and only USDC on other listed chains.

## Reference(s):

- [AIUSD homepage](https://aiusd.ai)
- [ClawHub skill page](https://clawhub.ai/tech-fe-aiusd/skills/aiusd-core)
- [Publisher profile](https://clawhub.ai/user/tech-fe-aiusd)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 18 and uses the aiusd-core CLI through npx or an installed command.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
