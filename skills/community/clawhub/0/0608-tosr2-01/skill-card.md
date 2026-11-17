## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, portfolio and watchlist tools, dividend metrics, multi-source trend scanning, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate stock and cryptocurrency analysis, compare tickers, track portfolios and watchlists, evaluate dividends, and scan market trend or rumor signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X social scanning may use live browser session credentials.

Mitigation: Run trend scans with --no-social unless the Twitter/X setup is isolated, and never place browser session cookies in shared or repository-local .env files.

Risk: The release is finance-related and can produce recommendations or confidence scores that may be mistaken for financial advice.

Mitigation: Treat output as informational analysis only, review the source data and caveats, and consult a licensed financial advisor before making investment decisions.

Risk: Market data, short-interest data, insider filings, and breaking-news signals can be delayed, rate-limited, cached, or incomplete.

Mitigation: Check timestamps and source availability before acting on results, and use fast or no-social modes when external sources are unavailable or credentials are not configured.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/skills/0608-tosr2-01)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [Twitter/X](https://x.com)
- [bird CLI](https://github.com/steipete/bird)
- [Usage Guide](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Hot Scanner](docs/HOT_SCANNER.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Console text and Markdown-style reports with optional JSON output and local portfolio or watchlist JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational market analysis and may include buy, hold, or sell signals, confidence scores, caveats, alerts, trend rankings, and rumor impact scores.]

## Skill Version(s):

6.2.0 (source: artifact frontmatter and artifact _meta.json; ClawHub release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
