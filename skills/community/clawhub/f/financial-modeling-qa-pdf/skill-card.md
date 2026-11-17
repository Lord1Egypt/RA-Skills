## Description:

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary / Anthropic Terms of Service

## Use Case:

Developers and document automation users use this skill to inspect, transform, generate, split, merge, extract data from, and fill PDF documents. It supports both fillable PDF forms and non-fillable forms that require visual field identification and annotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF processing can expose sensitive document, form, image, and extracted text data.

Mitigation: Use the skill only on PDFs the user is authorized to access, keep intermediate JSON/images/filled PDFs in approved local locations, and delete sensitive intermediates when finished.

Risk: PDF repair or transformation commands may overwrite or alter source files.

Mitigation: Create backups before destructive operations and avoid copying in-place repair commands unless a recoverable copy exists.

Risk: Optional OCR and PDF dependencies may introduce package and execution-environment risk.

Mitigation: Install optional dependencies in an isolated environment using trusted, pinned packages where possible.

Risk: Incorrect field detection or bounding boxes can place form data in the wrong location.

Mitigation: Run the included automated bounding-box checks and visually inspect validation images before producing a filled PDF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/financial-modeling-qa-pdf)
- [PDF form workflow reference](artifact/references/forms.md)
- [PDF processing advanced reference](artifact/references/reference.md)
- [PDF 32000-1:2008 checkbox state reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)
- [Exploring fillable forms with pdfrw](https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, JSON structures, and file-generation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of PDF, PNG, TXT, XLSX, JSON, and image output files during PDF processing workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
