## Description:

Excel 全栈处理技能 helps agents create, read, edit, format, convert, merge, and report on Excel workbooks, including CSV/JSON/PDF conversion and optional Feishu cloud spreadsheet operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linlannet](https://clawhub.ai/user/linlannet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to generate, inspect, clean, merge, convert, and style Excel outputs in agent workflows. It is useful for xlsx report generation, batch data exports, PDF table extraction, and controlled Feishu sheet read/write tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included test script imports from a hard-coded external Windows path.

Mitigation: Remove the hard-coded sys.path entry before running tests and import the local artifact script instead.

Risk: Dependency installation uses an unpinned package command and a trusted mirror flag.

Mitigation: Install dependencies in an isolated environment with pinned versions from a trusted index.

Risk: Generated spreadsheets from untrusted inputs may contain formulas or unsafe content.

Mitigation: Treat generated XLSX files from untrusted CSV, JSON, or PDF inputs as potentially formula-bearing and review before sharing or opening.

Risk: Feishu cloud spreadsheet operations can read, write, or append remote data.

Mitigation: Require explicit confirmation before any Feishu read, write, or append operation and verify target spreadsheet tokens and ranges.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linlannet/skills/excel-skills)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell code examples; scripts can produce XLSX, CSV, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local XLSX, CSV, JSON, and PDF inputs and write converted or formatted spreadsheet outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
