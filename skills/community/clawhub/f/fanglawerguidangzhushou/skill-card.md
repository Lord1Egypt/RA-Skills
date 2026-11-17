## Description:

自动识别律师案件图片或PDF，生成民事归档卷宗和办案小结文档，并支持PDF转换与备份功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fong12368](https://clawhub.ai/user/fong12368)

### License/Terms of Use:

MIT-0

## Use Case:

Legal practitioners and support staff use this skill to organize case folders by extracting case information from PDFs or images, generating civil archive volumes and case summary documents, converting outputs to PDF, and backing up skill files. It is intended for local workflows that handle confidential legal records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes confidential legal case files and writes OCR text, DOCX, PDF, and backup copies that may contain sensitive information.

Mitigation: Run it only on a dedicated local copy of case files, keep generated outputs in approved confidential storage, and review output paths before sharing or backing up.

Risk: The security evidence reports unsafe PowerShell document conversion when case or template paths can be influenced by untrusted parties.

Mitigation: Avoid untrusted case and template paths until the conversion flow is fixed, and execute the skill only inside an isolated Python environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fong12368/skills/fanglawerguidangzhushou)
- [Publisher profile](https://clawhub.ai/user/fong12368)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime outputs include DOCX, PDF, OCR text, and backup files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents and OCR text may contain confidential legal information and should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
