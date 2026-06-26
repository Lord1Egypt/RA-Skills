## Description: <br>
Extract text and structured data from PDFs, images, scanned documents, and document URLs using Azure Document Intelligence prebuilt OCR and document analysis models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Li-Hongmin](https://clawhub.ai/user/Li-Hongmin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing teams use this skill to run single-file or batch OCR over PDFs and images, choose Azure Document Intelligence prebuilt models, and produce text, Markdown, or JSON extraction results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, document URLs, and extracted OCR outputs may contain sensitive information. <br>
Mitigation: Only process documents intended for Azure Document Intelligence, use a trusted Azure resource, and handle generated text or JSON outputs with the same sensitivity as the source documents. <br>
Risk: The Azure Document Intelligence API key could be exposed if stored in source control or logs. <br>
Mitigation: Provide the key through environment variables, keep it out of source control and logs, and rotate it if exposure is suspected. <br>
Risk: Broad batch runs over mixed folders may send unintended private files for OCR. <br>
Mitigation: Review input folders and file-extension filters before running batch processing, especially on shared or mixed-content directories. <br>


## Reference(s): <br>
- [Azure Document Intelligence Prebuilt Models](references/models.md) <br>
- [ClawHub skill release page](https://clawhub.ai/Li-Hongmin/azure-doc-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, plus generated text, Markdown, or JSON OCR output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Azure Document Intelligence endpoint and API key environment variables; batch processing can write extracted files to an output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
