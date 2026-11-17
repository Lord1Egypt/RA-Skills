## Description:

Uses the EasyLink EasyDoc masking API to redact selected sensitive fields from medical records or other supported documents and return masked-file results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sycamore792](https://clawhub.ai/user/sycamore792)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to submit EMR or other supported files to EasyLink, poll asynchronous masking jobs, and retrieve normalized masked-document results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper accepts a base URL override that could send medical records and the API key to an unintended endpoint.

Mitigation: Use the documented EasyLink HTTPS host for real records, and allow --base-url only after independently verifying the destination and credential handling.

Risk: The skill processes sensitive medical documents through an external API.

Mitigation: Use it only when the operator has authority to upload the documents and trusts EasyLink for the intended data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sycamore792/skills/easydoc-mask)
- [EasyDoc Mask API reference](references/easydoc-mask-api.md)
- [EasyLink platform](https://platform.easylink-ai.com)
- [EasyLink EasyDoc Mask endpoint](https://api.easylink-ai.com/v1/easydoc/mask)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized results include task_id, status, result URLs, masked fields, page counts, and raw API response data.]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
