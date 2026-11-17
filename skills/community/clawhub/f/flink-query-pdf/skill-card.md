## Description:

A PDF manipulation toolkit for extracting text and tables, creating, merging, splitting, rotating, protecting, watermarking, and filling PDF documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to inspect, transform, generate, and fill PDF documents with Python libraries, command-line tools, and bundled validation utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs can contain sensitive personal, legal, or business data that may be extracted, logged, or copied into local outputs.

Mitigation: Use copies of important documents, restrict access to generated outputs, and avoid logging or sharing extracted sensitive text.

Risk: PDF transformation and form-filling utilities create local files and may overwrite or misplace important outputs if paths are reused.

Mitigation: Choose unique output paths, review generated files before use, and keep original PDFs unchanged.

Risk: Password-removal examples can be misused on documents the user is not authorized to decrypt.

Mitigation: Only remove PDF passwords when the user has explicit authorization for the document.

Risk: Non-fillable PDF form completion depends on accurate visual bounding boxes and can place text in the wrong area.

Mitigation: Generate and inspect validation images, correct bounding boxes, and verify the completed PDF before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/flink-query-pdf)
- [PDF forms guide](artifact/forms.md)
- [PDF processing advanced reference](artifact/reference.md)
- [Adobe PDF 32000:2008 field state reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python, JavaScript, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PDFs, page images, JSON field maps, and validation images when the agent runs bundled utilities.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
