## Description:

文档格式刷帮助代理将 Word、Markdown 或纯文本文档按模板或内置 GB/T 9704-2012 公文格式整理为一致的版式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yechao1995](https://clawhub.ai/user/yechao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to format local documents against a template, apply a built-in Chinese official document profile, and convert between Word, Markdown, and plain text outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected documents and writes formatted output files, so an unintended input or output path could expose private content or overwrite expected results.

Mitigation: Run it only on intended local documents, review input and output paths before execution, and use distinct output filenames.

Risk: The Word processing path depends on python-docx and local document parsing, which can produce formatting differences across templates or environments.

Mitigation: Install dependencies in a virtual environment from trusted, preferably pinned sources, and inspect generated documents before sharing or publishing.

## Reference(s):

- [文档格式刷参考手册](artifact/references/format_reference.md)
- [ClawHub skill page](https://clawhub.ai/yechao1995/skills/doc-format-brush)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Text, Configuration]

**Output Format:** [Markdown guidance with bash commands; local scripts can produce .docx, .md, .txt, and JSON format profiles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-selected local documents and python-docx for Word document processing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
