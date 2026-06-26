## Description: <br>
Extract text from PDF files using PyMuPDF. Parse tables, forms, and complex layouts. Supports OCR for scanned documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to extract text, metadata, tables, and OCR text from PDFs using local Python tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing Python and OCR dependencies can introduce package-source and environment risk. <br>
Mitigation: Use a virtual environment, install packages only from trusted sources, and run OCR system-package commands only when OCR is needed. <br>
Risk: Example code includes placeholder password handling for protected PDFs. <br>
Mitigation: Replace example passwords with prompted or otherwise protected credential handling in production code. <br>
Risk: OCR or complex PDF layout extraction can produce incomplete or incorrectly ordered text. <br>
Mitigation: Check whether pages need OCR, use sorted or structured extraction for complex layouts, and review OCR results before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/extract-pdf-text) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Code examples](examples.md) <br>
- [OCR setup](ocr.md) <br>
- [Troubleshooting](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local PDF extraction, OCR setup, structured text output, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
