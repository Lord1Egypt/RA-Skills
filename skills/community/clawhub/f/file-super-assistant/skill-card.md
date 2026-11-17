## Description:

文件创建与 AI 降味助手。支持 docx/xlsx/pptx/pdf 文件创建和编辑，提供 AI 内容改写为人类风格功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to create Word, Excel, PowerPoint, and PDF files and to rewrite AI-generated Chinese text into a more natural human style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports under-disclosed writes to a hard-coded OneDrive/Desktop path.

Mitigation: Run only in workspaces where document creation is intended, verify output paths before execution, and avoid sensitive content unless local persistence is acceptable.

Risk: The security guidance reports unsafe sudo/npm registry installation commands in generated documents.

Mitigation: Do not follow generated installation commands without independently verifying package provenance and using least-privilege installation methods.

Risk: Generated or rewritten documents may contain misleading edits or unintended content changes.

Mitigation: Review generated files and humanized text before sharing or using them in production workflows.

## Reference(s):

- [AI 内容特征与降味规则](references/ai-flavor-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown responses with inline shell commands and generated local document or text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write docx, xlsx, pptx, pdf, text, and JSON metadata files depending on the selected script and output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
