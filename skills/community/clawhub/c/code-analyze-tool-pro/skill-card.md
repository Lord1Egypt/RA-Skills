## Description:

代码分析工具专业版 helps developers and teams perform structured code, data, text, decision, visualization, and architecture analysis, including batch reviews, cross-validation, custom frameworks, and history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, and security reviewers use this skill to analyze codebases and technical plans, generate structured findings, compare perspectives, and track remediation trends. It is intended for repository and workflow analysis where users explicitly want the agent to inspect files, run approved commands, and produce review artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad repository analysis and agent powers, including file reads, writes, edits, and shell command execution.

Mitigation: Review before installing in repositories with proprietary code or secrets, limit work to intended paths, and require explicit approval for commands or edits that affect source files.

Risk: Analysis reports and history can retain sensitive code, security findings, or operational details.

Mitigation: Store reports only in approved locations, avoid including secrets in outputs, and periodically purge .code-analyze history when reports may contain sensitive information.

Risk: Optional callback and external API behavior can send repository-derived data outside the local environment.

Mitigation: Keep network, API, and callback features disabled unless needed, verify destination URLs and environment variables, and use HTTPS endpoints controlled by the user or organization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-analyze-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with code blocks, JSON configuration examples, and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local report, framework, and history files under .code-analyze when the user directs the agent to persist analysis output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
