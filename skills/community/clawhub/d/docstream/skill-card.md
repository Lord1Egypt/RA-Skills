## Description:

DocStream helps agents process documents through the DocStream API for text extraction, summarization, format conversion, and PDF parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill when an agent needs to extract, summarize, convert, or parse documents through the DocStream API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document URLs, payloads, and document contents may be sent to the DocStream service.

Mitigation: Use the skill only with documents approved for external processing, and avoid confidential or regulated documents unless an appropriate review has approved the service.

Risk: Auto-signup with DOCSTREAM_EMAIL can print a newly created API key into logs or terminal history.

Mitigation: Set DOCSTREAM_API_KEY securely through the agent runtime or secret manager instead of relying on auto-signup in logged environments.

Risk: Changing DOCSTREAM_API_URL can redirect document data and credentials to a different endpoint.

Mitigation: Leave DOCSTREAM_API_URL unset unless the endpoint is explicitly trusted and approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jbennett111/skills/docstream)
- [Publisher Profile](https://clawhub.ai/user/jbennett111)
- [DocStream Key Endpoint](https://anton.vosscg.com/v1/keys)
- [DocStream Process Endpoint](https://anton.vosscg.com/v1/documents/process)
- [DocStream API Base](https://anton.vosscg.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DocStream API key and may return API response content from submitted document processing requests.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
