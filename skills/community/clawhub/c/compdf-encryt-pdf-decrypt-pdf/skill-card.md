## Description:

Encrypt PDFs with AES-128, AES-256, or RC4 options and decrypt authorized PDFs with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to prepare ComPDF Server API requests for PDF encryption, permission controls, and authorized PDF decryption. It helps select supported endpoints, request fields, and follow-up polling or download steps while handling document passwords as sensitive data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF files and document passwords may be sent to ComPDF during encryption or decryption workflows.

Mitigation: Confirm affected files and destinations before upload, avoid repeating passwords in output, and use asynchronous or presigned workflows for large or security-sensitive documents.

Risk: The ComPDF API key is stored in a local plaintext skill file.

Mitigation: Keep the key only in the skill-local api_key file, exclude it from version control and publishing, and rotate or protect the key if the directory may be synced or shared.

Risk: RC4 is available as an encryption option and may be inappropriate for new protection workflows.

Mitigation: Prefer AES-256 for new encryption unless a narrow legacy compatibility requirement justifies RC4.

## Reference(s):

- [ComPDF Endpoint Index](references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](references/official-api-reference.md)
- [ComPDF PDF Encryption API](https://www.compdf.com/guides/api-reference/v2/pdf-encrypt)
- [ComPDF PDF Decryption API](https://www.compdf.com/guides/api-reference/v2/pdf-decrypt)
- [ComPDF API Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/compdf-encryt-pdf-decrypt-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint details, request fields, and next-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include request plans, API field summaries, polling or download steps, and credential handling guidance.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
