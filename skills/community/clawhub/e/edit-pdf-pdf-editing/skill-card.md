## Description:

Complete guide for reading and editing PDF documents with PyMuPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect PDF text, locate text positions, fill form fields, replace visible text, and perform true redaction of sensitive PDF values with PyMuPDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary visual replacement with a white rectangle can leave old PDF text extractable from the saved file.

Mitigation: Use the true redaction workflow with add_redact_annot() and apply_redactions() for confidential values, then verify the original value is not extractable.

Risk: Using image conversion, rasterization, or strikethrough workflows can destroy text-layer fidelity or leave misleading edits.

Mitigation: Use PyMuPDF text extraction, search_for(), draw_rect(), insert_text(), and redaction APIs as appropriate, and inspect the saved PDF after editing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/edit-pdf-pdf-editing)
- [Publisher profile](https://clawhub.ai/user/wu-uk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes preserving the PDF text layer and using true redaction when sensitive values must be removed from the PDF structure.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
