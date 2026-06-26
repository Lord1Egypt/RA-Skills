## Description: <br>
Cost Guardian tracks, analyzes, and optimizes AI and infrastructure costs with budgets, token usage scans, forecasts, subscription tracking, and optimization recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor AI model usage, infrastructure expenses, subscriptions, and budget status from local cost records and gateway logs. It helps produce spend reports, forecasts, and recommendations for reducing recurring costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local cost summaries, model names, usage patterns, and subscription records may be sensitive. <br>
Mitigation: Review the configured gateway log directory, protect or periodically clean ~/.openclaw/workspace/costs/, and enable recurring cron scans only when ongoing local collection is intended. <br>
Risk: Token cost estimates depend on local logs and the script's built-in model pricing table, so reports may diverge from provider billing. <br>
Mitigation: Treat reports and forecasts as operational estimates and confirm material spending decisions against provider invoices or account dashboards. <br>


## Reference(s): <br>
- [Cost Guardian on ClawHub](https://clawhub.ai/mariusfit/cost-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and optional JSON reports with command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local configuration and SQLite cost data under ~/.openclaw/workspace/costs/ by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
