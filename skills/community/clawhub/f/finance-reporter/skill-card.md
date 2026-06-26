## Description: <br>
Fetches real-time market data from Yahoo Finance for major global stocks, indexes, foreign exchange, commodities, and cryptocurrency, with optional scheduled DingTalk or WeChat delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfstylejf](https://clawhub.ai/user/jfstylejf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to generate current finance reports for selected market symbols and optionally schedule recurring delivery through configured OpenClaw messaging integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends outbound requests to Yahoo Finance for the configured market symbols. <br>
Mitigation: Install only where those outbound market-data queries are acceptable, and review the configured symbols before use. <br>
Risk: Optional cron scheduling and DingTalk or WeChat bindings can repeatedly publish generated reports. <br>
Mitigation: Enable scheduled jobs and messaging bindings only after confirming the intended cadence and destination channels. <br>
Risk: The skill requires installing and running the Python requests dependency. <br>
Mitigation: Install dependencies in an environment you control and review dependency installation before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jfstylejf/finance-reporter) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain-text finance report with markdown-style command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, the requests package, network access to Yahoo Finance, and optional OpenClaw scheduling or messaging integrations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
