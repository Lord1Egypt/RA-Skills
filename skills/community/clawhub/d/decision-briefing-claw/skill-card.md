## Description: <br>
决策简报虾 collects daily business metrics from databases, APIs, Excel, and Feishu Bitable, calculates KPI comparisons, generates structured business briefs, and sends them through Feishu, email, or WeCom. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, analysts, and decision makers use this skill to automate daily KPI collection, comparison, briefing, delivery, and archive workflows across common business data sources and communication channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SQL test command can execute unrestricted queries against configured databases. <br>
Mitigation: Use read-only database accounts, avoid the raw SQL test command on production data, and review configured queries before enabling scheduled collection. <br>
Risk: Generated business reports can be sent to external Feishu or email destinations. <br>
Mitigation: Restrict API tokens and webhooks, verify every destination in the channel configuration, and protect the reports directory. <br>
Risk: Scheduled cron execution can repeatedly collect and distribute sensitive business data. <br>
Mitigation: Enable cron only under a least-privilege user after configuration review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/decision-briefing-claw) <br>
- [Data source configuration guide](references/data-sources.md) <br>
- [Metric calculation rules](references/metrics-calculation.md) <br>
- [Report template library](references/report-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON data files, shell command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate archived daily report files and send report content to configured Feishu or email channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
