## Description:

Analyzes stocks and cryptocurrencies with Yahoo Finance data, portfolio tracking, watchlists, dividend analysis, stock scoring, trend scanning, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run stock and cryptocurrency analysis, monitor portfolios and watchlists, check dividends, and scan for trending or rumor-driven market signals. Outputs are informational and should be verified before making financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional X/Twitter scanning can require live browser session cookies or auth tokens.

Mitigation: Disable social scanning when possible, avoid placing unrelated secrets in the skill's .env file, and only use a pinned, trusted bird CLI in a restricted environment.

Risk: Financial analysis, trending signals, and rumor scores can be stale, incomplete, or misleading.

Mitigation: Treat outputs as informational, confirm current market data with primary sources, and consult a licensed financial advisor before investment decisions.

Risk: Some market data sources may lag, rate-limit requests, or have incomplete non-US coverage.

Mitigation: Use fast or no-social modes for lower-risk runs, account for documented data delays, and verify important findings against authoritative market data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0605-tosr2-csig)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear and Greed Index](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)
- [Usage guide](artifact/docs/USAGE.md)
- [Hot Scanner guide](artifact/docs/HOT_SCANNER.md)
- [Architecture notes](artifact/docs/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or console text, with optional JSON output from supported scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update local portfolio, watchlist, and cache state; financial outputs are informational rather than advice.]

## Skill Version(s):

6.2.0 (source: artifact/SKILL.md frontmatter); ClawHub release 1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
