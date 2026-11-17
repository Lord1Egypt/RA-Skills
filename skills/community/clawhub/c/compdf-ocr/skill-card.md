## Description:

Recognize and extract text from scanned PDFs and images with ComPDF OCR workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to prepare ComPDF Server API request plans for OCR, searchable PDF generation, text recognition, table recognition, and scanned-document extraction from PDFs or images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents selected for OCR may be uploaded to ComPDF for processing.

Mitigation: Identify the affected files and destination before upload, obtain user confirmation unless already authorized, and use asynchronous or presigned workflows for large, batch, or security-sensitive uploads.

Risk: The ComPDF API key is stored locally for reuse.

Mitigation: Store the key only in the skill-local api_key file, keep it private, exclude it from commits and backups, and never display it in examples or final output.

Risk: Unsupported endpoint options or OCR parameters could produce incorrect request plans.

Mitigation: Use only operations listed in the skill, read the matching official reference section, and preserve exact endpoint paths, request fields, request modes, and response fields.

## Reference(s):

- [ComPDF Endpoint Index](references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](references/official-api-reference.md)
- [ComPDF API Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [PDF to TXT API](https://www.compdf.com/guides/api-reference/v2/pdf-to-txt)
- [PDF to Editable PDF API](https://www.compdf.com/guides/api-reference/v2/pdf-to-editable-pdf-tool-guide)
- [Image to TXT API](https://www.compdf.com/guides/api-reference/v2/image-to-txt)
- [OCR Language Codes](https://www.compdf.com/guides/api-reference/v2/ocr-languages)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown request plan with endpoint, method, content type, request fields, expected response fields, and polling or download steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ComPDF API request details and curl-style examples; API keys should not be displayed or logged.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
