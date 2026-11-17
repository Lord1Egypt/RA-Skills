## Description:

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to inspect, create, merge, split, rotate, OCR, and extract data from PDFs. It also supports filling court or administrative PDF forms by checking fillable fields, generating field JSON, validating bounding boxes, and writing completed PDF outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PDFs, JSON, and page images can create additional copies of sensitive document contents.

Mitigation: Use the skill only on documents the user is authorized to process, keep generated files in approved locations, and delete intermediate files when finished.

Risk: PDF repair or replacement workflows may overwrite or alter source documents.

Mitigation: Avoid in-place repair commands; write repaired or transformed PDFs to a separate output path and preserve the original document.

Risk: OCR and PDF tooling may depend on local binaries or libraries with environment-specific behavior.

Mitigation: Run with pinned dependencies in an isolated environment and review outputs before relying on filled forms or extracted data.

## Reference(s):

- [PDF Form Filling Workflow](artifact/forms.md)
- [PDF Processing Advanced Reference](artifact/reference.md)
- [Adobe PDF 32000-1:2008 field state reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline code and shell commands; helper scripts produce JSON, PDF, and PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PDFs, extracted text, table data, form-field JSON, validation images, and page images may contain sensitive document data.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
