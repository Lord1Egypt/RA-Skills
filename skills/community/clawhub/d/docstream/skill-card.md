## Description: <br>
Document processing via the DocStream API for text extraction, summarization, format conversion, and PDF parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbennett111](https://clawhub.ai/user/Jbennett111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call DocStream for document text extraction, summarization, PDF parsing, and format conversion. It is suited to workflows that can send document links or content to the DocStream/Voss Consulting Group endpoint under an approved API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents, document links, request metadata, and possibly an email address are sent to the DocStream/Voss Consulting Group endpoint. <br>
Mitigation: Use only with documents approved for that external data sharing, and avoid confidential, regulated, or internal documents unless the sharing is authorized. <br>
Risk: The helper can obtain and print an API key when DOCSTREAM_EMAIL auto-signup is used, which can expose the key in logs. <br>
Mitigation: Prefer setting DOCSTREAM_API_KEY directly, avoid DOCSTREAM_EMAIL auto-signup in logged environments, and rotate any key that has been printed or logged. <br>


## Reference(s): <br>
- [DocStream OpenAPI spec](https://anton.vosscg.com/v1/openapi.json) <br>
- [DocStream ClawHub release page](https://clawhub.ai/Jbennett111/docstream) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DocStream API key and may send document links, document content, request metadata, and email address data to an external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
