## Description:

文档导航工具包（专业版） helps agents navigate documentation with decision-tree guidance, sitemap generation, full-text search, document change tracking, and reusable configuration snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and enterprise teams use this skill to navigate trusted documentation folders, build sitemaps and full-text indexes, locate relevant content, track document changes, and export configuration snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and package installation behavior.

Mitigation: Require explicit confirmation before running commands or installing packages, and execute only reviewed commands in a trusted workspace.

Risk: The skill advertises broad write, export, deletion, webhook, callback, API, and automation behavior without clear limits.

Mitigation: Limit use to trusted documentation folders, keep docs_root narrowly scoped, and require review before exports, deletions, callbacks, webhooks, or API integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docs-toolkit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON responses, Python examples, YAML configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read documentation folders and propose commands; keep docs_root narrow and review generated actions before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
