## Description:

Changshu Dev Assistant supports Dameng database development, SQL Server-to-Dameng migration, code security and quality scanning, local knowledge search, LLM chat, model monitoring, and prompt template management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze, optimize, format, and convert SQL for Dameng database workflows, scan source code for security and quality issues, search local knowledge bases, and manage LLM prompts and usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured LLM integrations may transmit SQL, source code, or chat content outside the local machine.

Mitigation: Use only approved HTTPS LLM endpoints and avoid submitting sensitive content unless that data transfer is approved.

Risk: Database credentials can be supplied on command lines for connection testing, which may expose secrets in shell history or process listings.

Mitigation: Avoid placing database passwords on the command line; use controlled secret handling before running database connection workflows.

Risk: SQL conversion and diagnostics can depend on an external dm_converter path outside this skill.

Mitigation: Review or remove the dm_converter dependency path before using SQL conversion or diagnostics.

Risk: High-impact external integrations are under-scoped for an unreviewed installation.

Mitigation: Review and control external integrations before installing or running the skill.

## Reference(s):

- [Changshu Dev Assistant on ClawHub](https://clawhub.ai/fish1981bimmer/skills/changshu-dev-assistant)
- [fish1981bimmer Publisher Profile](https://clawhub.ai/user/fish1981bimmer)
- [Dameng Database Guide](references/dameng_database_guide.md)
- [Hardcoding Audit & Fix - 2026-06-20](references/hardcoding-audit-2026-06-20.md)
- [Script Audit Report - 2026-06-06](references/audit-2026-06-06.md)
- [Optimization Suggestions](references/optimization-suggestions.md)
- [Test Automation Guide](references/test_automation_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SQL conversion guidance, scan reports, prompt templates, model usage summaries, and configuration instructions.]

## Skill Version(s):

3.0.2 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
