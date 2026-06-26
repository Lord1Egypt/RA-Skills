## Description: <br>
Data visualization, report generation, SQL queries, and spreadsheet automation. Transform your AI agent into a data-savvy analyst that turns raw data into actionable insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tihuaqin-commits](https://clawhub.ai/user/tihuaqin-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users can use this skill to query databases, analyze spreadsheets, create visualizations, and generate Markdown reports with statistical summaries and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run SQL against configured databases, including statements that may change live data. <br>
Mitigation: Use read-only or least-privilege credentials by default, inspect generated SQL before execution, and require explicit approval plus backups for UPDATE, DELETE, INSERT, DROP, ALTER, or similar commands. <br>
Risk: Database credentials or connection strings could be exposed if placed in shared prompts or configuration files. <br>
Mitigation: Keep secrets out of shared prompt and config files; provide credentials through local environment variables or approved secret-management workflows. <br>
Risk: Reports and visualizations can be misleading if source data is incomplete, stale, or poorly cleaned. <br>
Mitigation: Run data quality checks, document source data and cleaning steps, and review generated findings before using them for decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tihuaqin-commits/fox-data-analyst) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/tihuaqin-commits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL, Python, and shell code blocks; generated workspace files, CSV exports, charts, and reports when scripts are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the user's configured data sources, database permissions, and local analysis environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
