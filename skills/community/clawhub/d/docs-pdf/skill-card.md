## Description:

docs-pdf helps agents guide PDF extraction, creation, editing, conversion, OCR, form filling, security, metadata, comparison, repair, and batch workflows with bundled scripts and examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echodjx](https://clawhub.ai/user/echodjx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and document operations users use this skill to choose and run PDF workflows such as extracting text or tables, generating or editing PDFs, converting between images and PDFs, applying OCR, filling forms, and producing comparison or metadata reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may require powerful, unpinned system and package-manager installs.

Mitigation: Install in an isolated virtual environment or container, pin dependencies before use, avoid --break-system-packages where possible, and treat sudo package installation as an administrator setup step.

Risk: PDF batch, OCR, extraction, metadata, and decrypt operations can process sensitive or unauthorized documents.

Mitigation: Run these operations only on PDFs the user owns or is authorized to process, and review any generated text, PDF, report, or metadata outputs before sharing.

Risk: Generated files may be written to task-specific output paths and could expose document contents if saved in the wrong location.

Mitigation: Confirm output paths before execution and inspect saved artifacts after each operation.

## Reference(s):

- [PDF Skill guide](SKILL.md)
- [PDF form filling guide](FORMS.md)
- [Creating PDFs with reportlab](references/create.md)
- [Advanced extraction reference](references/extract.md)
- [OCR reference](references/ocr.md)
- [PDF security reference](references/security.md)
- [ClawHub skill page](https://clawhub.ai/echodjx/skills/docs-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline Python and shell commands; bundled scripts may write PDF, TXT, XLSX, image, JSON, or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local file and document operations whose exact artifacts depend on the selected PDF task.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
