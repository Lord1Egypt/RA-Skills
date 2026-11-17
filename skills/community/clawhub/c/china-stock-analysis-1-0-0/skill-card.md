## Description:

Analyzes Chinese A-share and Hong Kong stock prices, with optional U.S. tickers, to provide market trend summaries and buy, hold, or sell recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request structured stock analysis for Chinese A-shares, Hong Kong stocks, and supported U.S. tickers. The skill gathers current price and market context through web search, then returns concise trend analysis and informational buy, hold, or sell guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buy, hold, and sell recommendations may be mistaken for personalized financial advice.

Mitigation: Treat outputs as informational only, retain the risk disclaimer, and verify investment decisions with independent financial sources or qualified professionals.

Risk: Current prices, news, and market sentiment depend on web search and may be stale, incomplete, or inconsistent across data providers.

Mitigation: Check timestamps and compare results against authoritative market data sources before acting on the analysis.

Risk: The skill can analyze U.S. tickers even though it is primarily described as Chinese stock analysis.

Mitigation: Confirm the market, ticker, and exchange context before interpreting recommendations.

## Reference(s):

- [Popular Chinese Stocks Reference](references/china-stocks.md)
- [Eastmoney](https://www.eastmoney.com)
- [Xueqiu](https://xueqiu.com)
- [Yahoo Finance](https://finance.yahoo.com)
- [Google Finance](https://www.google.com/finance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables, technical analysis, recommendation rationale, and risk disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces informational financial analysis and may answer in Chinese.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
