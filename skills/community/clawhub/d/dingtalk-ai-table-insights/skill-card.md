## Description:

Analyzes DingTalk AI Tables across multiple tables by keyword or topic to identify risks, anomalies, cross-table relationships, and actionable business insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomray4ai](https://clawhub.ai/user/tomray4ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, analysts, and developers use this skill to scan DingTalk AI Tables for a business line, project, or function and generate cross-table insight reports with risks, anomalies, trends, and recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive DingTalk table data may be included in broad scans or LLM analysis.

Mitigation: Review usage with the DingTalk workspace owner or security admin, use a narrow read-only token, avoid all-table scans unless intended, and prefer --no-llm for sensitive data.

Risk: Unsafe command construction, temporary-file handling, and unpinned dependencies require review before broad use.

Mitigation: Review and fix command construction and temporary-file behavior, then pin dependencies before deployment.

Risk: Access tokens may be exposed if handled carelessly.

Mitigation: Do not print tokens or store them in shell startup files; keep tokens least-privileged and rotate them according to workspace policy.

## Reference(s):

- [dingtalk-ai-table dependency](https://github.com/aliramw/dingtalk-ai-table)
- [Architecture](references/architecture.md)
- [Configuration](references/configuration.md)
- [Dependencies](references/dependencies.md)
- [Examples](references/examples.md)
- [LLM Integration](references/llm_integration.md)
- [Prompt Design](references/prompt_design.md)
- [Quickstart](references/quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON insight reports, with shell commands and concise operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may use LLM analysis by default and can fall back to local templates; table reads are sampled and configurable with command-line limits.]

## Skill Version(s):

1.6.10 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
