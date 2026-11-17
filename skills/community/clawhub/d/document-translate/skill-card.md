## Description:

Translates and localizes Office documents in PPTX, DOCX, PDF, and XLSX formats while preserving the original document template and formatting where supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexyland](https://clawhub.ai/user/lexyland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document localization users use this skill to translate PPTX, DOCX, XLSX, and PDF files, especially English-to-Chinese office documents, while preserving templates and styles where the file format allows. Use it on trusted documents and review translation quality for specialized content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a general-purpose translator even though the bundled scripts primarily perform fixed replacement mappings.

Mitigation: Treat the skill as a limited English-to-Chinese replacement workflow and require human review for translation quality, especially for specialized terminology.

Risk: The workflow describes downloading, storing, sending, and uploading documents, which can expose sensitive files if used without scoping.

Mitigation: Use only trusted documents in a constrained environment and require explicit user approval before handling or transmitting sensitive files.

Risk: PDF handling has format limitations, including non-editable text and an incomplete direct overlay path.

Mitigation: Prefer the PDF-to-DOCX workflow, verify the converted output manually, and avoid relying on direct overlay for production results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lexyland/skills/document-translate)
- [Publisher profile](https://clawhub.ai/user/lexyland)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts produce translated document files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PPTX, DOCX, XLSX, and PDF inputs; translation behavior is mapping-based unless an agent adds a scoped translation step.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
