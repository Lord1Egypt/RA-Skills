## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection (Hot Scanner), and rumor/early signal detection. Use for stock analysis, portfolio tracking, earnings reactions, crypto monitoring, trending stocks, or finding rumors before they hit mainstream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate structured stock and cryptocurrency analysis, compare tickers, review dividend metrics, track portfolios and watchlists, and scan for trending or rumor-driven market signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional X/Twitter integration may require live session cookies in a local plaintext .env file.

Mitigation: Prefer running scans with --no-social; if social scanning is needed, avoid using a primary account and store only the required AUTH_TOKEN and CT0 values.

Risk: The optional social integration relies on an external CLI and may receive broad environment secrets.

Mitigation: Review the CLI before use, pin or control the installed version where possible, and keep unrelated secrets out of the skill environment.

Risk: Generated BUY, HOLD, SELL, trend, and rumor outputs could be mistaken for financial advice.

Mitigation: Treat outputs as informational analysis only and review investment decisions with independent research or a licensed financial advisor.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/skills/0605-cisg-tosr2)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear & Greed Index](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)
- [Usage Guide](docs/USAGE.md)
- [Concept and Philosophy](docs/CONCEPT.md)
- [Hot Scanner](docs/HOT_SCANNER.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or console text with optional JSON output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local portfolio and watchlist JSON files under the user's ClawHub skill data directory.]

## Skill Version(s):

6.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
