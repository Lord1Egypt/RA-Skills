## Description:

Convert office documents (DOCX, DOC, PPT, PPTX, XLS, XLSX, CSV, TXT, ODT, RTF) to PDF via the PDFAPIHub cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow builders use this skill to convert Word, spreadsheet, presentation, and text documents to PDF through the PDFAPIHub hosted API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and the API key are sent to PDFAPIHub for conversion.

Mitigation: Use the skill only when the document contents and credential handling are acceptable for PDFAPIHub; avoid confidential, regulated, or proprietary files unless the provider's handling and retention practices have been independently accepted.

Risk: Converted files are handled by a third-party cloud service and the artifact notes a 30-day auto-deletion period.

Mitigation: Review retention requirements before use and avoid uploading files that require stricter deletion, residency, or confidentiality controls.

## Reference(s):

- [PDFAPIHub Documentation](https://pdfapihub.com/docs)
- [PDFAPIHub API](https://pdfapihub.com/api)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header. Documents may be provided by public URL, base64 payload, or multipart upload, and responses can include a PDF URL, base64 content, or file output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
