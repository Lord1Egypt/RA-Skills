## Description:

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging and splitting documents, and handling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidaiangel](https://clawhub.ai/user/kidaiangel)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document-processing agents use this skill to inspect, extract, transform, create, merge, split, render, and fill PDF documents using Python libraries and command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs and form data may contain sensitive information, including passwords or personal data.

Mitigation: Process only PDFs the user is authorized to use, prefer copied inputs or new output filenames, and treat PDF passwords as sensitive.

Risk: PDF modification, decryption, form filling, and annotation workflows can overwrite or create derived local files.

Mitigation: Use explicit user-selected output paths, keep originals unchanged, and visually review generated PDFs when form placement matters.

Risk: Optional OCR and PDF tooling dependencies add supply-chain and environment risk.

Mitigation: Install optional OCR dependencies in a virtual environment with reviewed package versions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kidaiangel/skills/document-pdf)
- [PDF Forms Guide](artifact/forms.md)
- [PDF Processing Advanced Reference](artifact/reference.md)
- [Adobe PDF 32000:2008 Specification](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)
- [Exploring Fillable Forms with pdfrw](https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python, JavaScript, shell command, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local PDF, image, JSON, text, and spreadsheet files at user-selected paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
