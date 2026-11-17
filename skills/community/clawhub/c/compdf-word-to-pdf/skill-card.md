## Description:

Convert Word documents into polished PDFs with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare official ComPDF Server API requests that convert Word files to PDF for contracts, reports, proposals, manuals, approvals, and formal delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected Word documents are uploaded to ComPDF for conversion.

Mitigation: Confirm affected files and destination before upload; use asynchronous or secure request modes for large or security-sensitive files.

Risk: A ComPDF API key is stored locally in a skill-local api_key file.

Mitigation: Use a limited key when possible; keep the file private and out of backups, publishing, logs, examples, and commits.

Risk: Generated requests require the extra sourceType=5 field.

Mitigation: Review request details before execution and include sourceType=5 in final ComPDF API requests.

## Reference(s):

- [ComPDF Word to PDF Skill on ClawHub](https://clawhub.ai/compdf-youna/skills/compdf-word-to-pdf)
- [ComPDF Endpoint Index](references/endpoint-index.md)
- [ComPDF Official API Reference](references/official-api-reference.md)
- [ComPDF Word to PDF API](https://www.compdf.com/guides/api-reference/v2/word-to-pdf)
- [ComPDF API Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint, request fields, response fields, and next polling or download steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepares ComPDF API request plans; it does not convert files locally and asks for confirmation before uploads.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
