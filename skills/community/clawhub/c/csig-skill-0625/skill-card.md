## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, including portfolio management, watchlists with alerts, dividend analysis, stock scoring, trend detection, and rumor or early-signal scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate stock, crypto, portfolio, watchlist, dividend, trend, and rumor analysis from finance and market data sources. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X features may expose session cookies through the external bird CLI.

Mitigation: Run scanners with social media disabled unless credentials can be isolated and the bird executable is trusted.

Risk: Live browser session cookies stored near the skill can increase credential exposure.

Mitigation: Do not place live browser session cookies in the skill directory, and avoid granting Full Disk Access.

Risk: Unpinned or unreviewed dependencies can change the behavior of market-data scanners.

Mitigation: Pin or review dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/csig-skill-0625)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear & Greed Index](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [X](https://x.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with optional JSON output from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio and watchlist JSON files under the user's skill data directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
