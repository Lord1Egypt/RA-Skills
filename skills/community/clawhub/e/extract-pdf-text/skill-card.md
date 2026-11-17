## Description:

Extract text from PDF files using PyMuPDF. Parse tables, forms, and complex layouts. Supports OCR for scanned documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract text, metadata, tables, and structured content from local PDF files, with OCR setup guidance for scanned documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential PDF text or metadata may appear in local output when files are printed, logged, or batch processed.

Mitigation: Process sensitive PDFs only when that local output is intended, and control where extracted text and metadata are displayed or stored.

Risk: Dependency installation and OCR setup may require system-level package managers or sudo.

Mitigation: Install dependencies in a dedicated environment when possible, and review package sources before authorizing sudo or system-wide installs.

Risk: OCR and complex-layout extraction can produce incomplete, out-of-order, or inaccurate text.

Mitigation: Check extracted results, use PyMuPDF options such as sorted text or table extraction when appropriate, and apply OCR only when native text extraction is insufficient.

## Reference(s):

- [Extract PDF Text on ClawHub](https://clawhub.ai/ivangdavila/skills/extract-pdf-text)
- [Skill homepage](https://clawic.com/skills/extract-pdf-text)
- [Code examples](examples.md)
- [OCR setup](ocr.md)
- [Troubleshooting](troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of extracted text, structured dictionaries, JSON strings, PDF metadata, and OCR setup steps.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
