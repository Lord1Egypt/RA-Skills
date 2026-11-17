## Description:

Excel大师 helps agents handle batch Excel and CSV work, including large-file processing, format-preserving edits, long-number preservation, formula-cache handling, conversion, filtering, merging, validation, and report-style output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and automation users use this skill to guide agents through spreadsheet processing tasks such as reading, transforming, validating, merging, splitting, converting, and writing Excel or CSV files. It is intended for explicit spreadsheet workflows, not encrypted-file bypass or complex human judgment tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read, write, and command execution authority for spreadsheet tasks.

Mitigation: Restrict agent access to named input and output files, review proposed commands before execution, and keep backups before any write operation.

Risk: Spreadsheet transformations can corrupt data through precision loss, formula-cache assumptions, encoding errors, or unintended format changes.

Mitigation: Require explicit task scope, preserve originals, validate row counts and key columns, and inspect outputs before replacing source files.

Risk: The artifact includes broad API key and OAuth guidance outside the core local-spreadsheet workflow.

Mitigation: Do not provide credentials unless an online-Excel workflow is explicitly required, and then use least-privilege credentials through environment variables or the platform's secure secret store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/excel-maestro)
- [Skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus optional JSON-style result structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce spreadsheet-processing plans, command examples, Python snippets, validation steps, and output-file recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
