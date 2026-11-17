## Description:

Binance DCA Test helps agents plan recurring crypto purchases, check Binance spot prices and balances, place buy orders, review trade history, and manage DCA schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fpsjago](https://clawhub.ai/user/fpsjago)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan Binance dollar-cost averaging strategies, inspect balances and trade history, and prepare manual or scheduled spot buy commands. It is especially relevant when an agent must compare DCA scenarios before a user decides whether to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact live crypto trades or scheduled buys without enough safeguards.

Mitigation: Use Binance testnet first and require explicit confirmation of exchange, pair, amount, order type, and live-vs-testnet status before placing any buy order.

Risk: Binance API credentials could be over-permissioned or exposed in scheduled command entries.

Mitigation: Restrict API keys to the minimum permissions needed, disable withdrawals, and avoid putting secrets directly in cron entries.

## Reference(s):

- [Binance API endpoint](https://api.binance.com)
- [Binance Spot Testnet endpoint](https://testnet.binance.vision)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Binance API credentials, a selected trading pair, quote amount, order type, and live or testnet endpoint selection.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
