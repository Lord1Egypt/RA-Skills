## Description:

飞书文档翻译助手在飞书文档之间进行中英文互译，支持全文翻译、段落翻译和双语对照文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[young-joey](https://clawhub.ai/user/young-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and documentation teams use this skill to translate Feishu documents between Chinese and English while preserving Markdown structure. It can create translated copies, translate selected sections, or produce bilingual comparison documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads source Feishu documents and may write translated content to a new or existing document.

Mitigation: Confirm the source document and destination before translation, especially for confidential documents or append operations.

Risk: Translation quality depends on the underlying AI model and may be weaker for long documents, unsupported formatting, or text embedded in images.

Mitigation: Review translated output before relying on it, split very long documents into sections, and handle image text with OCR before translation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown document content and Feishu document updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a new Feishu document or append translated content to an existing document.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
