## Description:

财经监控 helps users query real-time prices and concise trend reports for stocks, indices, precious metals, futures, and commodities, then optionally send the report to a configured channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and retail finance watchers use this skill to check market prices during work hours and generate concise reports for stocks, precious metals, futures, commodities, and indices. Outputs are informational and should be reviewed before automated outbound delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports are configured to be sent to a fixed embedded WeChat recipient.

Mitigation: Confirm the destination belongs to the installing user, or remove the push step and require explicit confirmation before each send.

Risk: Market data can be delayed or stale, and generated commentary may be mistaken for trading advice.

Mitigation: Treat outputs as informational only and verify prices against authoritative market sources before making financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/finance-watch)
- [Publisher profile](https://clawhub.ai/user/fslong520)
- [Eastmoney Quotes](https://quote.eastmoney.com/)
- [TradingEconomics commodities](https://zh.tradingeconomics.com/commodities)
- [Sina Finance](https://finance.sina.com.cn/)
- [Stock code quick reference](artifact/stock_codes.md)
- [Futures code quick reference](artifact/futures_codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown market reports with optional browser/API lookup steps and channel send commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include live prices, intraday ranges, volume, brief analysis, timestamps, and outbound channel delivery details.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
