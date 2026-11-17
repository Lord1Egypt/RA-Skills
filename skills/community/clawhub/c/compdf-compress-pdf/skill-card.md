## Description:

Compress PDF files with ComPDF while balancing file size and readable visual quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to prepare ComPDF Server API request plans for PDF compression, including compression flags, resolution settings, request fields, and follow-up download or polling steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled API reference includes broad ComPDF documentation outside the compression scope.

Mitigation: Use only the compression endpoints and compression-flag sections listed by the skill, and reject unrelated ComPDF endpoint requests.

Risk: The skill stores the ComPDF API key in a persistent plaintext skill-local credential file.

Mitigation: Use the skill only where local plaintext credential storage is acceptable, exclude the key file from publishing, and rotate the key if the file is exposed.

Risk: Compressing PDFs may require uploading sensitive documents to ComPDF.

Mitigation: Identify affected files and destinations before upload, obtain confirmation unless already authorized, and use the documented asynchronous or presigned workflow for large or security-sensitive uploads.

## Reference(s):

- [ComPDF Endpoint Index](references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](references/official-api-reference.md)
- [ComPDF PDF Compression API](https://www.compdf.com/guides/api-reference/v2/compress-guides)
- [ComPDF Compression Parameters](https://www.compdf.com/guides/api-reference/v2/optimization-flags)
- [ComPDF Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with endpoint details, request fields, expected response fields, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request plans and next-step instructions; does not include stored API keys in examples or final output.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
