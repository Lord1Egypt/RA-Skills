## Description:

Compute and analyze technical indicators (MACD, KDJ, RSI, Moving Averages, Bollinger Bands) for Chinese futures markets. Generate buy/sell signals and chart descriptions based on data from china-commodity-quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to calculate common technical indicators for Chinese futures contracts and present concise buy, sell, or neutral signal analysis. It depends on quote data from china-commodity-quotes and should be used as analytical support rather than as a trading system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Technical indicator signals may be mistaken for financial advice or an automated trading decision.

Mitigation: Treat outputs as market-analysis support only; independently verify buy/sell signals and apply separate risk controls before trading.

Risk: Analysis quality depends on the freshness and completeness of quote data from public market APIs.

Mitigation: Check data source, contract symbol, and timestamp before relying on indicator values or generated signals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaocaixia888/skills/china-technical-analysis)
- [china-commodity-quotes dependency](https://clawhub.ai/zhaocaixia888/skills/china-commodity-quotes)
- [Sina Finance daily K-line API example](https://stock2.finance.sina.com.cn/futures/api/jsonp.php/InnerFuturesNewService.getDailyKLine?symbol=IF0&datalen=60)
- [SKILL.md](artifact/SKILL.md)
- [scripts/indicators.py](artifact/scripts/indicators.py)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with technical indicator values, chart descriptions, and buy/sell/neutral signal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses supplied or fetched market quote data; disclosed runtime behavior requires curl and the china-commodity-quotes skill.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
