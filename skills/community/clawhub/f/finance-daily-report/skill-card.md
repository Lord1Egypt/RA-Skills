## Description: <br>
Generates a modular, configurable global finance daily report with external LLM data collectors, chat delivery, scheduled setup, and module management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyangryr-cyber](https://clawhub.ai/user/xyangryr-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate a daily global finance briefing, configure scheduled delivery, and manage report modules. It is not intended for real-time trading, individual stock analysis, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may store DashScope or Doubao API keys in shell startup files. <br>
Mitigation: Use platform secrets or temporary environment variables for API keys, and review shell profile changes after setup. <br>
Risk: Setup can create a persistent scheduled OpenClaw cron job for daily report generation. <br>
Mitigation: Inspect cron entries after setup and remove or adjust the finance-daily-report job if it is not wanted. <br>
Risk: The skill performs outbound calls to finance websites and DashScope or Volcengine LLM APIs. <br>
Mitigation: Deploy only in environments where these network calls are permitted and where generated reports are reviewed before business use. <br>
Risk: Generated finance briefings could be mistaken for trading or investment advice. <br>
Mitigation: Keep the report positioned as a market briefing and preserve the stated exclusion for real-time trading, individual stock picks, and investment advice. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Report Template](references/template.md) <br>
- [Module Schema](references/module-schema.md) <br>
- [Module Management](references/module-mgmt.md) <br>
- [Verification](references/verification.md) <br>
- [Data Sources](references/sources.md) <br>
- [Collector Prompts](references/collector-prompts.md) <br>
- [Trading Economics Stocks](https://tradingeconomics.com/stocks) <br>
- [Trading Economics Currencies](https://tradingeconomics.com/currencies) <br>
- [Trading Economics Commodities](https://tradingeconomics.com/commodities) <br>
- [Jin10](https://www.jin10.com/) <br>
- [CLS](https://www.cls.cn/) <br>
- [Eastmoney](https://www.eastmoney.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report text with inline links, optional shell commands, and YAML-backed configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save dated report Markdown and optional evidence JSON under the OpenClaw workspace; chat output may be auto-chunked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
