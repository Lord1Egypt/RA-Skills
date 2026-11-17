## Description:

Merge, split, rotate, insert, delete, and extract PDF pages with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation users use this skill to prepare ComPDF Server API request plans for PDF page-management tasks such as merging, splitting, rotating, inserting, deleting, and extracting pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDFs may be uploaded to ComPDF for page editing.

Mitigation: Confirm the affected files and destination before upload, and use the skill only when sending those documents to ComPDF is acceptable.

Risk: The ComPDF API key is stored in a local plaintext api_key file.

Mitigation: Exclude api_key from version control and packaging, keep the key low-privilege where possible, and rotate it if exposed.

Risk: The bundled API reference includes broader ComPDF capabilities beyond page management.

Mitigation: Limit use to merge, split, rotate, insert, delete, and extract operations unless broader ComPDF use is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/compdf-youna/skills/compdf-page-editor)
- [ComPDF Endpoint Index](references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](references/official-api-reference.md)
- [ComPDF PDF API catalog](https://www.compdf.com/guides/api-reference/v2/api-overview-pdf)
- [ComPDF request workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [ComPDF authentication](https://www.compdf.com/guides/api-reference/v2/authentication)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown with endpoint, method, content type, request fields, expected response fields, and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ComPDF request details and polling or download steps; does not include stored API keys.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
