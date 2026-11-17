## Description:

Converts PDF and image files into Word, Excel, PowerPoint, HTML, image, TXT, JSON, Markdown, RTF, or CSV outputs using the ComPDFKit Conversion SDK with OCR and AI layout analysis support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0; ComPDFKit Conversion SDK Commercial / Proprietary terms apply

## Use Case:

Developers and document-processing agents use this skill to convert PDFs and supported image files into editable documents, structured data, Markdown, text, HTML, and image outputs. It is suited for local conversion workflows that need configurable OCR, page layout, table, image, and output-format settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes potentially private or regulated documents through a proprietary conversion package.

Mitigation: Review before installing, use a sandboxed virtual environment, and only process documents approved for the execution environment.

Risk: The workflow can rely on runtime downloads for license.xml and documentai.model when trusted local files are not already present.

Mitigation: Pre-stage trusted license and model files where possible, restrict network access, and verify downloaded assets before use.

Risk: The ComPDFKitConversion package is a runtime dependency and should not be treated as implicitly trusted.

Mitigation: Pin and verify the ComPDFKitConversion package before deployment, especially for private or regulated document workflows.

Risk: Trial usage is counted locally under the user's home directory and trial conversions are limited.

Mitigation: Confirm license status before production use and provide an approved custom license.xml when a full license is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/compdf-conversion-cli)
- [ComPDF Publisher Profile](https://clawhub.ai/user/compdf-youna)
- [ComPDF Homepage](https://www.compdf.com/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=compdf_pdf_skill_to_word&ref_platform_id=clawhub_skills)
- [ComPDF Conversion SDK Python Overview](https://www.compdf.com/guides/conversion-sdk/python/overview)
- [ComPDF Conversion SDK Python PDF to Word Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-word)
- [ComPDF Conversion SDK Python PDF to Excel Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-excel)
- [ComPDF Conversion SDK Python PDF to PPT Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-ppt)
- [License Notice](artifact/License.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated local document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent may produce conversion commands and, when executed, local output files in DOCX, PPTX, XLSX, HTML, RTF, image, TXT, JSON, Markdown, or CSV-compatible formats.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
