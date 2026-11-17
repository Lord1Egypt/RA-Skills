## Description:

A skill for OpenClaw to research crypto market trends (technical & sentiment) and trade ETH on Binance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dymx101](https://clawhub.ai/user/dymx101)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to gather ETH/USDT market indicators, summarize crypto news sentiment, log trading rationale, and optionally place Binance trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent authority to place real-money Binance trades.

Mitigation: Use restricted Binance API keys with withdrawals disabled, keep dry-run as the default, and require manual review before live orders.

Risk: Trading behavior has weak built-in guardrails for symbols, order sizes, and loss exposure.

Mitigation: Add explicit symbol allowlists, maximum order sizes, and loss limits before enabling live execution.

Risk: Market and sentiment outputs can be incomplete or misleading when used as trading signals.

Mitigation: Treat generated analyses as decision support only and verify market conditions independently before placing orders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dymx101/skills/clap-trader)
- [Cointelegraph RSS feed](https://cointelegraph.com/rss)
- [CoinDesk RSS feed](https://www.coindesk.com/arc/outboundfeeds/rss/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON market and sentiment outputs, and local log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market analysis logs are appended to Markdown; trade execution records are appended to CSV.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
