## Description:

Analyzes stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlist alerts, dividend analysis, stock scoring, hot-scan trend detection, and early rumor/signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, investors, and analysts use this skill to request stock and cryptocurrency analysis, compare tickers, review dividend metrics, monitor portfolios and watchlists, and surface market trends or early signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanning can expose browser session cookies or broad local privileges through an unpinned third-party CLI.

Mitigation: Run scanners with --no-social unless social data is needed, avoid Terminal Full Disk Access, keep auth_token and ct0 out of the skill directory, and use an isolated environment with only the required credentials.

Risk: Financial analysis outputs may be stale, incomplete, or misread as investment advice.

Mitigation: Treat outputs as informational, verify market data and source links independently, and consult a licensed financial advisor before making investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/skills/0528-tosr2-csig)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text and optional JSON, with markdown documentation and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, watchlist, hot-scan, and rumor-scan JSON files; some social scanning paths require optional Twitter/X credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
