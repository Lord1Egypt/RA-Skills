## Description: <br>
Automated sales and performance report generator for retail store managers that creates daily, weekly, and monthly reports from POS/ERP data, highlights anomalies, tracks targets, and delivers reports through configured channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store managers and retail operations teams use this skill to generate scheduled or on-demand sales and performance reports from POS/ERP or manually provided data. Reports cover KPIs, product performance, anomalies, staff metrics when available, and recommended actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read retail business data through POS/ERP connections. <br>
Mitigation: Install it where access can be limited to intended store data, preferably with read-only connector permissions. <br>
Risk: Scheduled delivery can send business reports to unintended chat channels or recipients if misconfigured. <br>
Mitigation: Verify the delivery channel, recipient IDs, schedule, and opt-out controls before enabling automatic delivery. <br>
Risk: Connector or report-generation implementation outside this package may add behavior that was not included in the reviewed artifact. <br>
Mitigation: Review any separate connector or report-generation implementation before deployment. <br>


## Reference(s): <br>
- [Metric Definitions](references/metric-definitions.md) <br>
- [ClawHub skill page](https://clawhub.ai/fangwei-frank/frank-report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with KPI tables, alert summaries, recommended actions, optional channel card formatting, and setup guidance when data is unavailable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily, weekly, monthly, and custom reporting periods; output depends on configured POS/ERP, inventory, target, and delivery settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
