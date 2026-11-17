## Description:

Convert image files into Word, Excel, PPT, PDF, HTML, RTF, CSV, TXT, or JSON with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare ComPDF Server API request plans for converting image sources such as scans, screenshots, receipts, forms, and photos into editable or structured document formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected image documents are sent to ComPDF for processing.

Mitigation: Confirm the affected files and destination before upload, and use asynchronous or presigned workflows for large, batch, or security-sensitive files.

Risk: The ComPDF API key is stored in a local plaintext api_key file.

Mitigation: Use scoped or low-quota keys where possible, keep the key out of examples and final output, and exclude the api_key file from version control and publishing.

Risk: Generated request details may include an incorrect endpoint, mode, or parameter if unsupported options are inferred.

Mitigation: Use only the matching documented endpoint section and preserve exact request fields, response fields, and sourceType=5 routing in the final request plan.

## Reference(s):

- [ComPDF Convert Images to Documents on ClawHub](https://clawhub.ai/compdf-youna/skills/compdf-convert-images-to-documents)
- [ComPDF Endpoint Index](artifact/references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](artifact/references/official-api-reference.md)
- [ComPDF API Overview](https://www.compdf.com/guides/api-reference/v2/api-overview)
- [ComPDF Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint, method, content type, request fields, expected response fields, and polling or download next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Request plans include sourceType=5 and must not expose API keys.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
