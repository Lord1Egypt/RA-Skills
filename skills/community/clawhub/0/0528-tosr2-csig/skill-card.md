## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlists and alerts, dividend analysis, stock scoring, Hot Scanner trend detection, and rumor or early-signal scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run stock and cryptocurrency analysis, compare tickers, track portfolios and watchlists, inspect dividends, and scan for trending or rumor-driven market signals. Outputs are informational and should be reviewed before making financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional social scanners use sensitive X/Twitter session credentials and an external bird CLI. <br>
Mitigation: Avoid the optional X/Twitter setup unless needed, keep AUTH_TOKEN and CT0 scoped to the skill, do not place unrelated secrets in the skill .env, and prefer --no-social or --fast modes for routine use. <br>
Risk: The skill produces finance-oriented recommendations, trend scores, and rumor signals that may be delayed, incomplete, or misleading. <br>
Mitigation: Treat outputs as informational, review underlying sources and timestamps, and consult qualified financial advice before acting on investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/0528-tosr2-csig) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Hot Scanner](docs/HOT_SCANNER.md) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Console text, Markdown guidance, local JSON files, and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces financial analysis summaries, ticker comparisons, portfolio/watchlist state, dividend metrics, trend scans, rumor scans, and warnings; some commands write local JSON state or cache files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports stock-analysis 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
