## Description:

China Doc OCR helps agents recognize and structure content from documents, PDFs, scanned images, photos, invoices, receipts, ID cards, tables, and charts using SiliconFlow-hosted OCR models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to convert Chinese and mixed-language document images, PDFs, invoices, IDs, tables, and charts into editable text, Markdown, or structured extraction results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends documents to a third-party OCR API, which can expose sensitive personal, financial, legal, or regulated business information.

Mitigation: Use it only for documents the user is permitted to upload, and redact or avoid IDs, bank statements, contracts, invoices, and regulated records unless upload is approved.

Risk: OCR results and temporary outputs may remain in the workspace after processing.

Mitigation: Delete retained workspace outputs and temporary files when the task is finished, especially after handling private documents.

Risk: The skill requires a SiliconFlow API key for network calls.

Mitigation: Keep the API key in the environment, avoid pasting it into prompts or files, and rotate it if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-doc-ocr)
- [Model selection reference](references/models.md)
- [OCR prompt templates](references/prompts.md)
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1/chat/completions)
- [SiliconFlow console](https://cloud.siliconflow.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, structured text, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save OCR results in the workspace; the helper supports image, PDF, or URL input and defaults to 4096 response tokens.]

## Skill Version(s):

1.2.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
