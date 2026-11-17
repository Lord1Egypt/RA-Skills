## Description:

Add or remove text and image watermarks in PDFs with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operations teams use this skill to prepare ComPDF Server API request plans for adding or removing PDF watermarks in branding, draft review, document control, cleanup, and final delivery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDFs are sent to ComPDF for processing.

Mitigation: Use the skill only for documents your organization permits ComPDF to process, and confirm affected files and destination before upload.

Risk: The skill stores a ComPDF API key locally in skill runtime state.

Mitigation: Protect shared workspaces and rotate the API key if access may have been exposed.

Risk: Watermark removal or replacement can affect document control, branding, or review status.

Mitigation: Confirm authorization before removing or replacing watermarks and preserve original files unless replacement is explicitly requested.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/compdf-youna/skills/compdf-add-watermark-remover-watermark)
- [ComPDF add watermark API reference](https://www.compdf.com/guides/api-reference/v2/watermark-guides)
- [ComPDF remove watermark API reference](https://www.compdf.com/guides/api-reference/v2/del-watermark-guides)
- [ComPDF authentication API reference](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF request workflow API reference](https://www.compdf.com/guides/api-reference/v2/request-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint, method, content type, request fields, expected response fields, and follow-up polling or download steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill prepares request plans for ComPDF watermark endpoints and requires user confirmation before uploads or destructive document operations.]

## Skill Version(s):

1.0.4 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
