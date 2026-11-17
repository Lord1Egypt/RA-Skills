## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlists and alerts, dividend analysis, stock scoring, trend scanning, and early rumor detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate informational stock and cryptocurrency analysis, compare tickers, track portfolios and watchlists, review dividend metrics, and scan market trend or rumor signals. The outputs are intended as research support, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanner setup uses browser session credentials and a third-party CLI.

Mitigation: Skip social scanning with the documented no-social mode, or use a dedicated low-risk account and limit the environment passed to the CLI to AUTH_TOKEN and CT0.

Risk: External finance, news, crypto, and social requests may disclose searched tickers or portfolio holdings.

Mitigation: Run the skill only with holdings and tickers you are comfortable sending to the configured data sources, and review network behavior before using sensitive portfolios.

Risk: BUY, HOLD, and SELL labels could be mistaken for personalized investment advice.

Mitigation: Present the output as informational research support and keep the documented financial-advice disclaimer visible in user-facing workflows.

Risk: Market data, short interest, insider activity, and breaking-news signals may be delayed or incomplete.

Mitigation: Cross-check time-sensitive results against authoritative market data before acting and avoid relying on cached or lagging signals for trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0602-tosr2-01)
- [Usage Guide](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Hot Scanner](docs/HOT_SCANNER.md)
- [Concept and Philosophy](docs/CONCEPT.md)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style console output, with optional JSON output from supported scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local portfolio and watchlist JSON state files; scanner output depends on external finance, news, crypto, and optional social sources.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
