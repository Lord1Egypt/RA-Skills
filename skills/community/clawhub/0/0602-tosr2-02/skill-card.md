## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection, and rumor or early signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze US stocks and cryptocurrencies, compare tickers, track portfolios and watchlists, review dividends, and scan market, news, and social signals. It is informational only and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanning handles live session cookies.

Mitigation: Run the stock, portfolio, dividend, and hot scanning workflows without social authentication unless the Twitter/X feature has been reviewed.

Risk: The optional social scanner can pass the full process environment to an external CLI.

Mitigation: Keep unrelated secrets out of this skill's .env, avoid granting broad terminal permissions, and use a dedicated low-value Twitter/X account if social scanning is enabled.

Risk: Market, news, social, and rumor signals can be delayed, incomplete, or misleading.

Mitigation: Treat results as informational market research and verify findings with licensed financial advice and primary sources before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0602-tosr2-02)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [Twitter/X](https://x.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON from command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, watchlist, hot scan, and rumor scan JSON state files under the user's ClawHub skill state directory.]

## Skill Version(s):

1.0.1 (source: server release metadata); artifact skill version 6.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
