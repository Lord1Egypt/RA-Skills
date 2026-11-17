## Description:

代码解释工具专业版 helps engineering teams analyze project architecture, generate code documentation, create Mermaid/UML diagrams, and extract API documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to understand larger codebases, onboard new contributors, document APIs and modules, and prepare architecture or legacy-system review materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local read, command, and write authority for project-wide analysis and generated documentation.

Mitigation: Use it only on repositories where project-wide reading and documentation writes are acceptable, and review generated files before committing or publishing them.

Risk: Unattended automation such as cron jobs, Git hooks, auto-update, or search-index features can repeatedly modify project documentation or expose unintended content.

Mitigation: Avoid enabling unattended automation unless outputs are constrained to reviewed documentation or wiki paths and sensitive directories are excluded.

Risk: Generated architecture, API, and complexity documentation may be incomplete or misleading if scanner outputs or examples are applied without review.

Mitigation: Treat outputs as drafts and validate them against the source repository before using them for onboarding, architecture review, or external documentation.

## Reference(s):

- [Detailed reference](references/detail.md)
- [ClawHub release page](https://clawhub.ai/thcjp/skills/explain-code-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Mermaid diagrams, JSON or OpenAPI files, YAML configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated documentation, diagrams, reports, and wiki-style files to project documentation paths.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
