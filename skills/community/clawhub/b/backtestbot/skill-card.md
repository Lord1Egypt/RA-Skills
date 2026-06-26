## Description: <br>
Backtest trading strategies against historical market data with performance analytics and risk metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CollierKing](https://clawhub.ai/user/CollierKing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External traders, quantitative researchers, and developers use BacktestBot to ask an agent to backtest trading strategies against historical market data and compare performance, risk, and strategy variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest requests may submit proprietary trading strategies or sensitive assumptions to the BacktestBot service. <br>
Mitigation: Use a dedicated or scoped API key if available and avoid submitting proprietary strategies unless you are comfortable sharing them with the provider. <br>
Risk: Historical data caching may consume disk space or leave stale local data. <br>
Mitigation: Review and manage the BACKTESTBOT_DATA_DIR cache location when disk use or data freshness matters. <br>


## Reference(s): <br>
- [BacktestBot on ClawHub](https://clawhub.ai/CollierKing/backtestbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or text responses with backtest requests, analytics summaries, and risk metrics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BACKTESTBOT_API_KEY for authenticated BacktestBot requests; BACKTESTBOT_DATA_DIR is an optional local cache directory.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
