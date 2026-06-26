## Description: <br>
AI finance assistant - real-time quotes, charts, technical analysis, portfolio tracking, price alerts, watchlists, daily briefings, macro economics, and sentiment analysis for US stocks, BIST, crypto, and forex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salihgun](https://clawhub.ai/user/salihgun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use FinClaw to query market data, generate charts and technical indicators, track portfolios, manage watchlists and price alerts, and produce concise market briefings across US stocks, BIST, crypto, and forex. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio records, watchlists, alerts, cached prices, and user notes are stored locally. <br>
Mitigation: Use appropriate local file permissions and avoid storing sensitive notes or identifiers in portfolio, watchlist, or alert fields. <br>
Risk: Market queries and optional API keys are sent to third-party finance APIs. <br>
Mitigation: Use limited-scope API keys and only query symbols or assets you are comfortable sending to external market-data providers. <br>
Risk: Some remove or delete commands modify local records rather than archiving them. <br>
Mitigation: Review destructive portfolio, watchlist, and alert commands before execution and keep backups if local records are important. <br>
Risk: Setup installs current Python package versions from package indexes. <br>
Mitigation: Run setup in an isolated Python environment and review or pin dependency versions where reproducibility is required. <br>


## Reference(s): <br>
- [FinClaw ClawHub release](https://clawhub.ai/salihgun/finclaw) <br>
- [Publisher profile](https://clawhub.ai/user/salihgun) <br>
- [API Endpoints Reference](artifact/references/api-endpoints.md) <br>
- [Briefing Templates](artifact/references/briefing-template.md) <br>
- [FRED Macro Indicators Reference](artifact/references/macro-indicators.md) <br>
- [Portfolio Commands Quick Reference](artifact/references/portfolio-commands.md) <br>
- [Technical Indicators Reference](artifact/references/technical-indicators.md) <br>
- [Ticker Symbols Reference](artifact/references/ticker-symbols.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown/plain text from helper scripts, optional JSON output, shell commands for setup and execution, configuration snippets, and PNG chart files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on current third-party market data and optional API keys; portfolio records, watchlists, alerts, and cached prices are stored locally in SQLite.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
