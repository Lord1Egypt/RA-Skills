## Description: <br>
Track, analyze, and report business KPIs with targets, status flags, trend analysis, and root cause prompts using configurable JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Business operators, founders, and teams use this skill to define KPIs, record metric values, generate weekly or monthly status reports, and identify off-track metrics that need investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KPI configuration, historical data, and saved reports can contain sensitive business records. <br>
Mitigation: Install only in workspaces where KPI data should be stored, and review access to kpi-config.json, kpi-data.json, and saved reports. <br>
Risk: Scheduled delivery or messaging integrations could distribute KPI summaries beyond the intended audience. <br>
Mitigation: Review any cron, Slack, Telegram, or other automation integration before enabling scheduled reports. <br>


## Reference(s): <br>
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown reports and JSON configuration or data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write kpi-config.json, kpi-data.json, and optional reports/kpi-YYYY-MM-DD.md files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
