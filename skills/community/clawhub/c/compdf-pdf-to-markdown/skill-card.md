## Description:

Convert PDF files into Markdown with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI agents, and content teams use this skill to prepare ComPDF PDF-to-Markdown requests for knowledge-base ingestion, developer documentation, content repurposing, and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDFs are uploaded to ComPDF for processing.

Mitigation: Confirm affected files and destination before upload, and avoid sending sensitive documents unless the user accepts ComPDF processing.

Risk: The skill stores a ComPDF API key in a local api_key file.

Mitigation: Use a limited or revocable API key where possible, exclude the file from version control, and restrict filesystem permissions.

Risk: The bundled API reference includes ComPDF endpoints outside PDF-to-Markdown.

Mitigation: Use only the documented PDF-to-Markdown operation and avoid deletion, decryption, watermarking, or other unsupported endpoints.

## Reference(s):

- [ComPDF Endpoint Index](references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](references/official-api-reference.md)
- [ComPDF PDF to Markdown API](https://www.compdf.com/guides/api-reference/v2/pdf-to-md)
- [ComPDF Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [ComPDF Portal](https://www.compdf.com/compdf-portal/signin?utm_source=clawhub&utm_medium=referral&utm_campaign=compdf_skills_repo_en&ref_platform_id=clawhub_compdfkit_skills_en)
- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/compdf-pdf-to-markdown)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown with endpoint, method, content type, request fields, expected response fields, and polling or download steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PDF-to-Markdown request plans for ComPDF Server API, including sourceType=5 and skill-local API key handling.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
