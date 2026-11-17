## Description:

商业数据洞察 — 连接业务数据源，自动生成数据分析报告和看板.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, analysts, and developers use this skill to connect local business data sources, ask natural-language analytics questions, and generate recurring Markdown reports with tables, Mermaid charts, anomaly notes, and business recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose database credentials through connection strings or command-line arguments.

Mitigation: Use least-privileged read-only datasource accounts and pass passwords through protected environment variables instead of chat text, command lines, or connection URIs.

Risk: Exploration and query outputs may contain raw or sensitive business records.

Mitigation: Limit query scope, review outputs before sharing, and redact sensitive fields in reports or interactive results.

Risk: Reports generated from untrusted or incomplete data can produce misleading business conclusions.

Mitigation: Review generated reports and anomaly explanations before using them for operational decisions or external distribution.

## Reference(s):

- [Report Templates](artifact/references/report-templates.md)
- [Mermaid Chart Guide](artifact/references/mermaid-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/hanjing5024064/skills/biz-data-insight)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables and Mermaid chart blocks, JSON command results, and guided shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language interaction by default; output may include raw query rows, aggregate statistics, anomaly summaries, and environment-variable setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
