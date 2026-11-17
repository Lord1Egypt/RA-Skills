## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists, alerts, dividend analysis, stock scoring, viral trend detection, and rumor or early signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze public stock and cryptocurrency market data, compare tickers, manage watchlists and portfolios, evaluate dividends, and surface trending or rumor-driven market signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanning can expose active browser session credentials and pass broad environment data to a third-party CLI.

Mitigation: Avoid enabling Twitter/X scanning as written; do not paste primary X/Twitter session cookies, do not grant Terminal Full Disk Access, and run the bird integration only if the CLI is pinned, trusted, and given minimum required environment variables.

Risk: Market data, social signals, rumors, and generated recommendations can be delayed, incomplete, or misleading.

Mitigation: Treat outputs as informational only, verify material signals against primary sources, and consult a licensed financial advisor before making investment decisions.

Risk: External market data sources may be rate-limited or unavailable, which can reduce output quality.

Mitigation: Use fast or no-social modes when appropriate, cache repeated checks, and confirm critical results outside the skill before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/skills/0602-tosr2-06)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)
- [Usage Guide](docs/USAGE.md)
- [Hot Scanner](docs/HOT_SCANNER.md)
- [Architecture](docs/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with optional JSON output and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, watchlist, hot-scan, or rumor-scan JSON files when the corresponding scripts are run.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter version: 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
