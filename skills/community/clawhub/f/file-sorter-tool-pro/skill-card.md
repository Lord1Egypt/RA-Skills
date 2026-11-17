## Description:

视觉文件整理专业版 helps agents organize local files with custom classification rules, batch and recursive processing, rename templates, operation history rollback, shared configuration, and Markdown, PDF, or CSV reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, finance teams, and enterprise file-governance teams use this skill to preview and apply rule-based file organization, renaming, deduplication, rollback, and reporting workflows for local directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive organization and scheduled cleanup can move or rename many local files if targets or rules are wrong.

Mitigation: Review before installing, use only explicit target directories, run dry-run previews first, and keep important folders backed up before batch rename or move operations.

Risk: Scheduled cleanup and history behavior may affect files repeatedly unless paths, rules, and rollback expectations are confirmed.

Mitigation: Avoid enabling scheduled cleanup until paths and rules are confirmed, and verify history settings before relying on rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/file-sorter-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML configuration examples, and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include dry-run guidance, operation reports, history and rollback commands, and exported report formats.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
