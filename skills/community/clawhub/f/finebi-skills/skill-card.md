## Description: <br>
FineBI 主技能入口。先识别用户目标，再路由到 dashboard-briefing、report-to-doc、alert-to-task、sync-to-bitable 等子技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsmj1994](https://clawhub.ai/user/zsmj1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and analysts use this skill to route FineBI dashboard, reporting, alerting, and dataset synchronization requests to scenario-specific workflows. It helps agents locate the right FineBI object, use the documented finebi-cli command path, and produce grounded summaries, documents, alerts, or synchronization guidance from real FineBI outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and move business data when FineBI credentials are configured. <br>
Mitigation: Confirm the exact dashboard or dataset and destination before sync, export, group-chat, or scheduled workflows. <br>
Risk: FineBI access tokens grant the agent access to organization data through finebi-cli. <br>
Mitigation: Install only when finebi-cli is trusted and provide credentials only in environments approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zsmj1994/finebi-skills) <br>
- [README](README.md) <br>
- [CLI command map](references/cli-command-map.md) <br>
- [Dashboard question-answer flow](references/dashboard-question-answer-flow.md) <br>
- [Dashboard ID resolution flow](references/dashboard-id-resolution-flow.md) <br>
- [Dashboard widget data flow](references/dashboard-widget-data-flow.md) <br>
- [Dataset search and preview flow](references/dataset-search-and-preview-flow.md) <br>
- [Published subject resource flow](references/published-subject-resource-flow.md) <br>
- [Skill routing](references/skill-routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured business-analysis outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires finebi-cli plus FINEBI_BASE_URL and FINE_ACCESS_TOKEN before workflows can access FineBI data.] <br>

## Skill Version(s): <br>
0.2.33 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
