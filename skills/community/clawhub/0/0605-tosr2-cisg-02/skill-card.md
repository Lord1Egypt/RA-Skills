## Description:

Analyzes stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists, dividend analysis, stock scoring, trend detection, and rumor scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate informational stock and cryptocurrency analyses, compare tickers, track portfolios and watchlists, inspect dividends, and scan trending or rumored market signals. Outputs should be treated as informational analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanning handles live session cookies and exposes the full environment to an external CLI.

Mitigation: Review the optional Twitter/X features before installation; avoid placing live X cookies in the skill directory and run hot scans with --no-social unless the bird executable is trusted and credentials are isolated.

Risk: Portfolio and watchlist files can contain sensitive local financial data.

Mitigation: Store these files with appropriate local access controls and avoid committing or sharing them.

Risk: Market analysis, rumor signals, and recommendations may be incomplete, stale, or unsuitable for investment decisions.

Mitigation: Treat outputs as informational only and verify material decisions with current market sources and a licensed financial advisor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0605-tosr2-cisg-02)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)
- [Yahoo Finance](https://finance.yahoo.com)
- [Usage guide](artifact/docs/USAGE.md)
- [Hot Scanner documentation](artifact/docs/HOT_SCANNER.md)
- [Architecture documentation](artifact/docs/ARCHITECTURE.md)
- [Concept documentation](artifact/docs/CONCEPT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands plus plain-text or JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read market data from third-party services and store local portfolio and watchlist JSON files.]

## Skill Version(s):

6.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
