## Description:

Convert PDF content into structured JSON with ComPDF. Use when PDF text, tables, images, and structured content must feed an AI pipeline, application, or system integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to prepare ComPDF Server API requests that convert PDFs into structured JSON for AI pipelines, applications, and system integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are sent to ComPDF for processing.

Mitigation: Use the skill only with PDFs that are approved for transfer to ComPDF, and obtain confirmation before upload unless the user has already authorized it.

Risk: The skill asks to store an API key in a skill-local plaintext api_key file.

Mitigation: Prefer a protected secret store or one-time key entry, and never display, log, commit, or include the key in examples.

Risk: Bundled reference material includes unrelated destructive and security-changing PDF operations.

Mitigation: Keep use limited to the PDF-to-JSON operation and do not use bundled endpoints for editing, decryption, watermark removal, account browsing, or AI extraction workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/compdf-youna/skills/compdf-pdf-to-json)
- [ComPDF PDF to JSON API](https://www.compdf.com/guides/api-reference/v2/pdf-to-json)
- [ComPDF request workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [ComPDF authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [Endpoint index](artifact/references/endpoint-index.md)
- [Official API reference snapshot](artifact/references/official-api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown request plan with endpoint details, request fields, expected response fields, and optional command examples; the ComPDF API result is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill should stay scoped to PDF-to-JSON and include sourceType=5 in final ComPDF API request details.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
