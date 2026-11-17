## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection (Hot Scanner), and rumor/early signal detection. Use for stock analysis, portfolio tracking, earnings reactions, crypto monitoring, trending stocks, or finding rumors before they hit mainstream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to analyze US stocks and supported cryptocurrencies, compare tickers, track portfolios and watchlists, review dividends, and scan for trending or rumor-driven market signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Hot Scanner and Rumor Scanner workflows rely on Twitter/X session-token handling and a third-party CLI.

Mitigation: Use the social scanners only in an isolated environment without unrelated API keys or cloud credentials, and skip social scanning when it is not required.

Risk: Twitter/X cookie tokens stored in a project .env can expose account access if the file is shared or mishandled.

Mitigation: Do not store Twitter/X session cookies in a project .env; prefer ephemeral environment variables or a dedicated, access-limited environment.

Risk: Granting Terminal Full Disk Access for browser-cookie extraction broadens local data exposure.

Mitigation: Do not grant Terminal Full Disk Access unless the operator understands and accepts the risk.

Risk: Financial analyses, rumor signals, and trend scores can be delayed, incomplete, or misleading.

Mitigation: Treat outputs as informational, verify market data and sources independently, and consult a licensed financial advisor before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0608-tosr2-02)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with optional JSON output from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce stock and crypto analysis, portfolio summaries, watchlist alerts, dividend reports, hot-scanner results, rumor-scanner results, and commands for local execution.]

## Skill Version(s):

6.2.0 (source: frontmatter); ClawHub release version 1.0.1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
