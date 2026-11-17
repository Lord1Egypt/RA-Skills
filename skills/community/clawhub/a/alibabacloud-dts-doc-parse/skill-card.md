## Description:

Use Alibaba Cloud DTS-AI to parse local PDF, DOCX, PPTX, JPEG, JPG, and PNG files into Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can convert specified local documents and images into Markdown for downstream reading or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious, citing an unverified remote installer, automatic updates to the CLI and other skills, and a command it considers mismatched with the document-parsing purpose.

Mitigation: Before use, independently verify installer and update sources and review whether automatic changes to other installed skills are acceptable.

Risk: The workflow uploads specified documents for cloud processing.

Mitigation: Use it only for documents the user explicitly selected or authorized for cloud processing.

Risk: Scan coverage was partial because one local reference could not be resolved.

Mitigation: Review the unresolved reference and remaining skill materials before relying on the release.

## Reference(s):

- [Alibaba Cloud DTS-AI document parsing use case](https://help.aliyun.com/en/dts/use-cases/use-dtsai-api-to-parse-documents)
- [CreateDocParserJob API reference](https://help.aliyun.com/en/dts/developer-reference/api-dtsai-2026-04-01-createdocparserjob)
- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-dts-doc-parse)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One Markdown file per input document.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
