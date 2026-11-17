## Description:

Extract text and structured data from PDFs, images, scanned documents, handwriting, tables, forms, and common business documents using Azure Document Intelligence REST API v4.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-hongmin](https://clawhub.ai/user/li-hongmin)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to run single-file or batch OCR on PDFs, images, and document URLs. It produces extracted text, structured markdown, or raw JSON for review, document processing, and downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and the Azure Document Intelligence API key may be sent to network destinations during OCR processing.

Mitigation: Use only a trusted HTTPS Azure endpoint and review the endpoint and polling URL handling before deploying the scripts.

Risk: OCR inputs may contain sensitive identity, tax, health, financial, or regulated data.

Mitigation: Process sensitive documents only with appropriate approval and data handling controls for Azure Document Intelligence.

Risk: Batch processing can submit multiple documents concurrently, increasing exposure and rate-limit impact.

Mitigation: Tune worker counts for the Azure resource, monitor failures, and limit batches to approved document sets.

## Reference(s):

- [Azure Document Intelligence Prebuilt Models](references/models.md)
- [ClawHub skill page](https://clawhub.ai/li-hongmin/skills/azure-doc-ocr)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration instructions]

**Output Format:** [Plain text, Markdown, or JSON files; guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports stdout or file output for single documents and per-document output files for batch processing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
