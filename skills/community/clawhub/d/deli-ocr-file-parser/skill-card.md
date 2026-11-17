## Description:

将扫描版 PDF、图片、OFD、票据、合同扫描件和法院文书等文件解析为可继续分析的 Markdown 或文本，并仅在原生解析失败、结果不可用或用户明确要求时调用得理 OCR。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent cannot directly read scanned PDFs, images, OFD files, receipts, contracts, court documents, or other files that need OCR conversion into Markdown or text. It supports document parsing workflows while requiring native parsing to be attempted first and OCR results to be reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send sensitive documents such as contracts, IDs, receipts, court records, or other confidential files to an external OCR service.

Mitigation: Get explicit user approval before OCR processing, share only the files needed for the task, and avoid pasting full private OCR output back into the conversation.

Risk: The workflow invokes a mutable npm CLI package using latest-version commands.

Mitigation: Prefer a pinned and reviewed CLI version before installation or execution, and use the command discovery output from the current run instead of assuming fixed commands.

Risk: API credentials may be stored locally or exposed through shell command history if handled carelessly.

Mitigation: Protect ~/.deli/cli/config.json and avoid placing API keys directly in shell commands when configuring the CLI.

Risk: OCR can misread critical fields such as amounts, dates, names, case numbers, invoice numbers, bank accounts, seals, signatures, or handwriting.

Mitigation: Mark OCR output as requiring human review and call out uncertain or incomplete fields in the final parsing summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolalam/skills/deli-ocr-file-parser)
- [deli-cli common prerequisites](references/cli-common.md)
- [OCR file parsing CLI guide](references/ocr-cli-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text file paths, concise Markdown status summaries, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify source files, generated Markdown or text paths, whether raw responses were saved, parsing completeness, and fields requiring human review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
