## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, including portfolio management, watchlists with alerts, dividend analysis, stock scoring, viral trend detection, and rumor or early signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze stocks and cryptocurrencies, compare tickers, manage portfolios and watchlists, monitor dividends, and scan for trending or rumored market signals. Outputs should be treated as informational market analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional X/Twitter scanning can use live session credentials.

Mitigation: Prefer --no-social unless X/Twitter scanning is required, avoid placing live X cookies in the skill directory, and run the skill in an environment without unrelated secrets.

Risk: Portfolio and watchlist data are stored locally as JSON.

Mitigation: Do not store sensitive or regulated account information in these files, and review local file permissions before use.

Risk: Financial outputs may be mistaken for trading instructions.

Mitigation: Treat recommendations, trend signals, and rumor scores as informational analysis and verify decisions with independent sources or licensed financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0602-tosr2-07)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [Twitter/X](https://x.com)
- [bird CLI](https://github.com/steipete/bird)
- [Usage guide](artifact/docs/USAGE.md)
- [Hot Scanner documentation](artifact/docs/HOT_SCANNER.md)
- [Concept and limitations](artifact/docs/CONCEPT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON state for portfolios, watchlists, hot scans, and rumor scans.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
