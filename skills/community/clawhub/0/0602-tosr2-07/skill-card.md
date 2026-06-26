## Description: <br>
Analyzes stocks and cryptocurrencies with Yahoo Finance data, portfolio and watchlist workflows, dividend analysis, stock scoring, trend scanning, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and investors can use this skill to run command-line stock and crypto analysis, manage watchlists and portfolios, inspect dividend metrics, and scan for trending or rumor-driven market signals. Outputs are informational and should be reviewed before any investment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X features may require sensitive browser session credentials such as AUTH_TOKEN and CT0. <br>
Mitigation: Use --no-social or avoid Twitter/X features unless needed; keep tokens out of shared or committed files and rotate them if exposed. <br>
Risk: Twitter/X setup may involve broad local permissions for browser session access. <br>
Mitigation: Do not grant Terminal Full Disk Access unless isolated and necessary for the intended environment. <br>
Risk: Portfolio and watchlist automation can modify or delete local tracking data. <br>
Mitigation: Back up portfolio and watchlist data before using delete, remove, or automation commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/0602-tosr2-07) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Technical Architecture](docs/ARCHITECTURE.md) <br>
- [Hot Scanner](docs/HOT_SCANNER.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Console text, Markdown guidance, and optional JSON from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Portfolio and watchlist commands may write local JSON data files under the user's ClawHub skill data directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata); source skill declares 6.2.0 in SKILL.md frontmatter <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
