## Description:

Convert PDF files into reusable HTML with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and operations teams use this skill to plan ComPDF Server API requests that convert PDF reports, manuals, brochures, or archived documents into browser-friendly HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF content may be uploaded to ComPDF for processing.

Mitigation: Confirm affected files and destination before upload, and avoid highly sensitive documents unless the ComPDF account, region, and retention requirements are acceptable.

Risk: The skill uses a locally stored ComPDF API key.

Mitigation: Store only the current skill's key in the skill-local api_key file, do not display or log it, and rotate the key if exposure is suspected.

## Reference(s):

- [ComPDF Endpoint Index](artifact/references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](artifact/references/official-api-reference.md)
- [ComPDF PDF to HTML API](https://www.compdf.com/guides/api-reference/v2/pdf-to-html)
- [ComPDF Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/compdf-pdf-to-html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown request plan with endpoint, method, content type, request fields, expected response fields, and polling or download steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ComPDF API request details, credential setup guidance, and confirmation prompts before document upload.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
