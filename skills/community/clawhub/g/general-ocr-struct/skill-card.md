## Description:

General-purpose offline OCR and post-processing for Chinese/English screenshots, scanned images, receipts, tables, chat screenshots, statement screenshots, and other text-heavy images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[9penny](https://clawhub.ai/user/9penny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local OCR on text-heavy images, review raw recognized text, and structure clear transaction-like screenshots into rows and fields before downstream table entry, summaries, or document drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipts, card statements, chat screenshots, and similar images can contain sensitive personal or financial information.

Mitigation: Process only files the user intentionally provides for local OCR and avoid sharing the extracted text beyond the intended workflow.

Risk: OCR quality or fixed transaction heuristics can produce incorrect grouping, merchant spillover, or ambiguous fields.

Mitigation: Show raw OCR text for verification, mark uncertain fields as needing confirmation, and request a higher-resolution source image when recognition quality is weak.

## Reference(s):

- [Structuring notes](artifact/references.md)
- [ClawHub skill page](https://clawhub.ai/9penny/skills/general-ocr-struct)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and optional JSON OCR results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw OCR text should be shown before interpretation when accuracy matters; uncertain structured fields should be marked for confirmation.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
