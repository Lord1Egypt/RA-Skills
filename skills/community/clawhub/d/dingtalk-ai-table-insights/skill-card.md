## Description: <br>
Analyzes DingTalk AI Tables across multiple tables by keyword or topic to surface business insights, data anomalies, risks, and action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomray4ai](https://clawhub.ai/user/tomray4ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business analysts use this skill to analyze DingTalk AI Table data for a specific project, function, or business line. It produces cross-table insight reports, risk warnings, anomaly notes, and action recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive business table data and generated reports, logs, and cache metadata may aggregate information from multiple tables. <br>
Mitigation: Use a least-privilege DingTalk token, prefer keyword-scoped runs, avoid full scans on sensitive workspaces, and treat generated reports, logs, and cache metadata as sensitive. <br>
Risk: Default LLM analysis may send sampled table contents to the configured OpenClaw model or agent context. <br>
Mitigation: Use --no-llm when table contents should not be sent to the configured model or agent context. <br>
Risk: Security evidence reports unsafe shell command construction. <br>
Mitigation: Review or fix shell command construction before installation or production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomray4ai/dingtalk-ai-table-insights) <br>
- [dingtalk-ai-table dependency](https://github.com/aliramw/dingtalk-ai-table) <br>
- [Architecture](references/architecture.md) <br>
- [Configuration](references/configuration.md) <br>
- [Dependencies](references/dependencies.md) <br>
- [LLM Integration](references/llm_integration.md) <br>
- [Examples](references/examples.md) <br>
- [Quickstart](references/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and optional JSON output, with shell commands and configuration guidance in supporting documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include sampled table summaries, anomaly findings, risk prioritization, and recommended actions; local template output is available with --no-llm.] <br>

## Skill Version(s): <br>
1.6.10 (source: frontmatter, server release evidence, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
