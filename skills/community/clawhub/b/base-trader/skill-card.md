## Description:

Autonomous crypto trading on Base via Bankr. Use for trading tokens, monitoring launches, executing strategies, or managing a trading portfolio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sp0oby](https://clawhub.ai/user/sp0oby)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to guide Base-chain crypto trading through Bankr, including portfolio checks, token research, trade execution, stop-loss planning, automation, and trade journaling. It is intended for users who understand the financial risk of live crypto trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct real crypto trades, cancellations, leverage, DCA, and recurring orders using a funded Bankr wallet.

Mitigation: Require explicit user confirmation before every buy, sell, cancellation, leverage trade, DCA, or recurring order.

Risk: Broad trading triggers and autonomous cron or heartbeat mode can cause trading actions to be proposed outside a user's immediate review.

Mitigation: Avoid autonomous execution until an enforceable policy wrapper blocks unapproved trades and order changes.

Risk: Documented safety limits and journals are advisory and may not reliably enforce loss limits or stop trading.

Mitigation: Treat stop-loss, daily-loss, and journal checks as review aids, and enforce portfolio limits outside the skill before deployment.

## Reference(s):

- [Trading Strategies Deep Dive](references/strategies.md)
- [Token Analysis Framework](references/token-analysis.md)
- [Risk Management](references/risk-management.md)
- [Market Analysis](references/market-analysis.md)
- [Market Research via Bankr](references/market-research-bankr.md)
- [Trade Execution](references/execution.md)
- [Automation Strategies](references/automation-strategies.md)
- [Launch Sniping Guide](references/launch-sniping.md)
- [Leverage Trading Guide](references/leverage-guide.md)
- [Basescan Contract Lookup](https://basescan.org/address/CONTRACT)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON data, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON trade or performance records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose live Bankr trading commands and update local trade journal or performance JSON files.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
