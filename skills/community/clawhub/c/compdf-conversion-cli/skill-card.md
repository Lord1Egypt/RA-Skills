## Description: <br>
ComPDF Conversion CLI converts PDF and image files to Word, Excel, PowerPoint, HTML, image, text, JSON, Markdown, RTF, and CSV using the ComPDFKit Conversion SDK with OCR and AI layout analysis on Windows and macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compdf-youna](https://clawhub.ai/user/compdf-youna) <br>

### License/Terms of Use: <br>
Commercial / Proprietary <br>


## Use Case: <br>
Developers and document automation users use this skill to run local PDF or image conversions from an agent workflow or shell command, with OCR, layout, and output-format options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download vendor license and model files on first use. <br>
Mitigation: Pre-provision license.xml and documentai.model for confidential, regulated, or offline environments, and install only where expected network access is acceptable. <br>
Risk: Trial-license conversions are tracked in a local usage counter. <br>
Mitigation: Confirm local persistence is acceptable before use and provide a full ComPDF license for production workflows. <br>
Risk: The ComPDFKit Conversion SDK is commercial/proprietary and the bundled trial license is limited. <br>
Mitigation: Review the vendor terms and obtain a valid license before production use. <br>


## Reference(s): <br>
- [ComPDF Conversion SDK Python Overview](https://www.compdf.com/guides/conversion-sdk/python/overview) <br>
- [ComPDF Conversion SDK Python PDF to Word](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-word) <br>
- [ComPDF Conversion SDK Python PDF to Excel](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-excel) <br>
- [ComPDF Conversion SDK Python PDF to PPT](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-ppt) <br>
- [ComPDF Conversion SDK Python Apply License](https://www.compdf.com/guides/conversion-sdk/python/apply-license) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the requested conversion target and may include DOCX, PPTX, XLSX, HTML, image, TXT, JSON, Markdown, RTF, or CSV files.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
