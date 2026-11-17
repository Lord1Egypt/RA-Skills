## Description:

global-quotes: free stock quotes and news. Use when: user asks for global stock price, quote, ticker symbol, or company news for US (e.g. AAPL), HK (0700.HK), or China A-shares (000001.SZ, 600000.SS). Uses free sources: Yahoo/Finnhub for US, Tencent/EastMoney/AkShare for CN/HK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antaeus001](https://clawhub.ai/user/antaeus001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent retrieve global stock quotes, basic market data, and company news for US, Hong Kong, and China A-share symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to market-data providers and may use an optional Finnhub API key.

Mitigation: Install only where outbound market-data requests are acceptable, scope FINNHUB_API_KEY to the process or user environment, and avoid exposing it in shared logs or shell history.

Risk: The documented systemd-wide proxy option can route all gateway traffic through the configured proxy.

Mitigation: Prefer process-level HTTPS_PROXY and HTTP_PROXY settings; use service-wide proxy configuration only when an administrator intentionally wants that behavior.

Risk: CN/HK quote data from the Tencent plaintext source can be observed or altered by network intermediaries.

Mitigation: Treat Tencent-sourced CN/HK quote results as unverified market data and cross-check important financial decisions against trusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antaeus001/skills/free-stock-global-quotes-news)
- [Finnhub](https://finnhub.io)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart)
- [Yahoo Finance quote summary endpoint](https://query2.finance.yahoo.com/v10/finance/quoteSummary)
- [EastMoney quote endpoint](https://push2.eastmoney.com/api/qt/stock/get)
- [Tencent quote endpoint](http://qt.gtimg.cn/q={t_code})

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-formatted quote and news summaries, with optional raw JSON from script flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote outputs include symbol, name, currency, price, previous close, change, change percent, volume, and 52-week range when available; news outputs include headline, time, source, summary, and URL when available.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
