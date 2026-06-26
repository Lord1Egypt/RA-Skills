## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection (Hot Scanner), and rumor/early signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run stock and cryptocurrency analysis, compare tickers, track portfolios and watchlists, review dividend metrics, and scan for trending or rumor-driven market signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X features require sensitive session cookies and may pass broad environment data to an external CLI. <br>
Mitigation: Use --no-social or skip Twitter/X setup unless social sentiment is required; keep .env private, avoid broad filesystem permissions, and use a separate low-risk X account when cookies are needed. <br>
Risk: Market recommendations, trend scans, and rumor signals can be stale, incomplete, or unsuitable as financial advice. <br>
Mitigation: Treat outputs as informational analysis, verify data against current market sources, and consult a licensed financial advisor before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/0605-tosr2-csig-03) <br>
- [Publisher Profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Hot Scanner Guide](docs/HOT_SCANNER.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown command guidance, and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market recommendations, confidence scores, caveats, portfolio summaries, watchlist alerts, dividend metrics, trend scans, and rumor signals.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence); artifact frontmatter reports 6.2.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
