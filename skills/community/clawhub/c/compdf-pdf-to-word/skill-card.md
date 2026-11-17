## Description:

Convert PDF files into editable Word documents with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to prepare accurate ComPDF PDF-to-Word API requests for contracts, reports, forms, proposals, review, revision, localization, and business reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF files are uploaded to ComPDF for processing.

Mitigation: Confirm the affected files and destination before upload, and use the skill only when sending the document to ComPDF is acceptable.

Risk: The ComPDF API key is stored in a plaintext skill-local api_key file after user confirmation.

Mitigation: Keep the api_key file private, exclude it from publishing and backups, and avoid displaying or logging the key.

Risk: Generated requests include sourceType=5 as an integration routing parameter.

Mitigation: Verify the parameter against compliance or attribution requirements before using the generated request.

## Reference(s):

- [ComPDF Endpoint Index](artifact/references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](artifact/references/official-api-reference.md)
- [ComPDF PDF to Word API](https://www.compdf.com/guides/api-reference/v2/pdf-to-word)
- [ComPDF Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with endpoint, method, content type, request fields, expected response fields, and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cURL or code-oriented request examples and ComPDF task polling or download steps.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
