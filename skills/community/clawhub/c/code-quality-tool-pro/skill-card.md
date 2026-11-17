## Description:

代码质量检查专业版 helps engineering teams perform code quality and security audits with OWASP Top 10 checks, batch project analysis, custom rules, CI/CD integration, and multi-format reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect codebases for quality, security, compliance, and CI/CD readiness issues, then generate review guidance, reports, and configuration examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to read, write, edit, and execute audit commands across a project.

Mitigation: Use it only on trusted repositories, review proposed commands before execution, and review generated file changes before keeping them.

Risk: Broad activation language may cause the skill to be used for normal coding tasks where a code-audit workflow is not intended.

Mitigation: Enable it only for explicit code quality, security audit, reporting, or CI/CD integration requests.

Risk: External scanner integrations may require credentials or send project data to third-party services.

Mitigation: Keep external scanner settings disabled unless needed, store credentials in environment variables, and confirm data-handling requirements before enabling integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-quality-tool-pro)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, YAML, Python, JSON, and CI configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or generate audit reports in JSON, SARIF, HTML, or summary formats when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
