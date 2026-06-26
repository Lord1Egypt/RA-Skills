## Description: <br>
Automates weekly competitor monitoring by collecting competitor updates, analyzing trends, generating structured reports, and distributing them to team channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, marketing, and competitive intelligence teams use this skill to collect public competitor activity each week, summarize important updates and trends, and distribute Markdown reports to configured team channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Competitor monitoring can collect public or business intelligence from sources that may not be approved for monitoring. <br>
Mitigation: Limit monitoring to authorized sources and review the dependent skills before installation. <br>
Risk: Reports and alerts can disclose collected intelligence to configured recipients, webhooks, or n8n routes. <br>
Mitigation: Store webhook values as secrets and verify every recipient, route, and delivery channel before enabling distribution. <br>
Risk: Automatic weekly delivery, instant alerts, and 90-day report retention may conflict with an organization's data policy. <br>
Mitigation: Confirm scheduling, alerting, and retention settings against the organization's data policy before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/competitor-monitor-weekly) <br>
- [Workflow definition](artifact/workflow.json) <br>
- [Configuration example](artifact/config.yaml) <br>
- [Weekly report template](artifact/templates/weekly-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown weekly reports, JSON data files, and configured delivery actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be sent through configured Feishu, email, DingTalk, or n8n channels and retained locally when history is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; workflow.json also declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
