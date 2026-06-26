## Description: <br>
Automatically generates a daily research progress report from Feishu chat activity and recent OpenClaw memory notes, then prepares it for scheduled Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[databian](https://clawhub.ai/user/databian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to summarize daily research progress, continuing projects, next-day plans, system status, and a recent work heatmap from local session and memory data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report may contain sensitive Feishu chat content or recent memory notes and can be delivered through Feishu on a schedule. <br>
Mitigation: Review the cron job, recipient, push schedule, and memory retention expectations before enabling scheduled delivery. <br>
Risk: The skill writes the generated report back into daily memory, which may preserve sensitive summaries longer than intended. <br>
Mitigation: Confirm the workspace memory location and retention policy before first use, and periodically review generated memory entries. <br>
Risk: Project extraction and next-day plans are generated from heuristic parsing and may omit or misclassify work items. <br>
Mitigation: Review the generated report before relying on it for planning or stakeholder updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/databian/daily-report-bian) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files] <br>
**Output Format:** [Markdown report with Chinese section headings, bullet lists, status fields, and a text heatmap] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends the generated report to the daily memory file and prepares it for Feishu delivery according to the configured schedule.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
