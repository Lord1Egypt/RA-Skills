## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, including portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze equities and cryptocurrencies, compare tickers, monitor portfolios and watchlists, inspect dividends, and surface trending or rumor-driven market signals. Its outputs are informational and should be reviewed before investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X scanning may require sensitive session tokens and broad local access. <br>
Mitigation: Use non-social or no-social modes when possible; do not grant Terminal Full Disk Access, and do not store AUTH_TOKEN or CT0 in shared or committed files. <br>
Risk: Market, social, and news signals may be delayed, cached, incomplete, or keyword-based. <br>
Mitigation: Treat outputs as preliminary analysis, review cited caveats, and verify material facts with authoritative market and news sources before acting. <br>
Risk: The skill produces financial recommendations and scores that could be mistaken for professional advice. <br>
Mitigation: Use results for informational purposes only and consult a licensed financial advisor for investment decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/aaaaa) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Hot Scanner](docs/HOT_SCANNER.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown/text summaries with inline shell commands and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local portfolio and watchlist JSON files under ~/.clawdbot/skills/stock-analysis; optional Twitter/X scanning uses AUTH_TOKEN and CT0.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
