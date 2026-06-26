## Description: <br>
商业数据洞察连接业务数据源，帮助用户查询数据并生成分析报告和可视化看板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, operators, and data-facing teams use this skill to connect configured business data sources, ask natural-language analytics questions, and produce recurring Markdown reports with tables, summaries, and Mermaid charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read rows from configured databases or local files, including sensitive business, financial, or personal data. <br>
Mitigation: Use read-only, least-privilege credentials or sanitized reporting views, and avoid broad production datasets unless the data is approved for analysis. <br>
Risk: Generated SQL may select more data than the user intended. <br>
Mitigation: Review the SQL before confirming execution and keep result limits appropriate for the subscription tier and data sensitivity. <br>
Risk: Database credentials or datasource URIs may expose sensitive access details. <br>
Mitigation: Provide passwords through environment variables, avoid sharing secrets in chat, and rotate credentials if they are accidentally disclosed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanjing5024064/biz-data-insight) <br>
- [Publisher profile](https://clawhub.ai/user/hanjing5024064) <br>
- [Report templates](references/report-templates.md) <br>
- [Mermaid chart guide](references/mermaid-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, Mermaid code blocks, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may vary by subscription tier; paid workflows add deeper analysis, anomaly notes, and larger result limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
