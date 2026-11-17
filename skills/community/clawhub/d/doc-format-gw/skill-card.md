## Description:

公文排版工具 - 根据公文格式规范自动排版Word文档。适用于发送Word文件前进行格式调整。

This skill is ready for commercial/non-commercial use.

## Publisher:

[batduke](https://clawhub.ai/user/batduke)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document-preparation agents use this skill to format Word documents according to Chinese official-document style before sharing or sending them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatting changes may make an official document inaccurate or unsuitable to send.

Mitigation: Run the formatter on a copy or separate output file, then review the resulting Word document before sending.

Risk: Documents with tables may fail during formatting.

Mitigation: Test table-heavy documents before relying on the output, and manually review or adjust table formatting when needed.

Risk: Missing expected Chinese fonts can cause layout differences from the documented format.

Mitigation: Verify the required fonts are installed in the execution environment before formatting final documents.

## Reference(s):

- [Format Rules](references/format-rules.md)
- [ClawHub skill page](https://clawhub.ai/batduke/skills/doc-format-gw)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks; generated Word document file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, python-docx, and the expected Chinese fonts for reliable document formatting.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
