## Description:

FinClaw is an AI finance assistant for real-time quotes, charts, technical analysis, portfolio tracking, price alerts, watchlists, market briefings, macro indicators, and sentiment analysis across US stocks, BIST, crypto, and forex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salihgun](https://clawhub.ai/user/salihgun)

### License/Terms of Use:


## Use Case:

External users and agents use FinClaw to retrieve market data, generate chart files, run technical and macro analysis, manage local portfolios and watchlists, and create local price alerts. The skill is intended for finance workflow assistance and should be reviewed before acting on market or portfolio outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs Python dependencies for a local finance utility.

Mitigation: Review the dependency list before setup and run the skill in its local virtual environment.

Risk: The skill contacts third-party market-data services for quotes, news, macro indicators, sentiment, crypto, and forex data.

Mitigation: Confirm data against authoritative sources before making financial decisions and configure API keys only when needed.

Risk: Portfolio, alert, watchlist, and cached market data are stored locally.

Mitigation: Avoid entering sensitive notes or holdings on shared machines and protect the skill directory and local database.

Risk: Some portfolio and alert commands mutate or delete local records.

Mitigation: Review remove, sell, and delete commands before execution and keep backups when portfolio history matters.

## Reference(s):

- [FinClaw ClawHub Skill Page](https://clawhub.ai/salihgun/skills/finclaw)
- [API Endpoints Reference](references/api-endpoints.md)
- [Briefing Templates](references/briefing-template.md)
- [FRED Macro Indicators Reference](references/macro-indicators.md)
- [Portfolio Commands Quick Reference](references/portfolio-commands.md)
- [Technical Indicators Reference](references/technical-indicators.md)
- [Ticker Symbols Reference](references/ticker-symbols.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and JSON text output, shell command invocations, configuration snippets, and generated PNG chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional API keys for some data sources, calls third-party market-data services, and stores portfolio, alert, watchlist, and cache data in a local SQLite database.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
