## Description:

G2量化交易策略 provides a China A-share quantitative screening workflow using multi-factor scoring, volume-ratio filtering, and fixed stop-loss and take-profit rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austin0208](https://clawhub.ai/user/austin0208)

### License/Terms of Use:

MIT-0

## Use Case:

External traders, analysts, and developers can use this skill to inspect a China A-share screening strategy, run local analysis code, and review configured risk controls before simulated or independently validated trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading and backtest claims may be misleading if treated as proof of future performance.

Mitigation: Use the skill for review or simulation first, and require independent validation before applying any recommendation to real trading.

Risk: The local database helper can drop and recreate its target watchlist table at a hard-coded database path.

Mitigation: Run in an isolated, nonprivileged environment and review the database path and table-writing behavior before allowing writes to any important database.

Risk: The analysis code performs market-data network requests during operation.

Mitigation: Review outbound data access and run with only the network permissions needed for the intended market-data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/austin0208/skills/g2-trading-strategy)
- [TradingAgents framework reference](https://github.com/TauricResearch/TradingAgents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trading strategy parameters and local analysis outputs; generated recommendations require independent validation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
