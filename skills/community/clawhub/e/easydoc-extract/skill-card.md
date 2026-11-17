## Description:

Use when tasks need EasyLink extraction API to extract structured fields from documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sycamore792](https://clawhub.ai/user/sycamore792)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to submit PDFs or images to EasyLink, choose an extraction mode, poll asynchronous jobs, and receive normalized structured field data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send documents and the API key to an arbitrary base URL when that option is used.

Mitigation: Use only documents authorized for EasyLink processing, keep EASYLINK_API_KEY in a secure environment variable, avoid custom base URLs except in controlled testing, and restrict outbound access to api.easylink-ai.com when possible.

Risk: Document extraction uploads user-provided files to an external service.

Mitigation: Review data handling requirements before use and avoid submitting sensitive or unauthorized documents.

## Reference(s):

- [EasyLink EasyDoc Extract API Reference](artifact/references/easydoc-extract-api.md)
- [EasyLink Platform](https://platform.easylink-ai.com)
- [EasyLink EasyDoc Extract API](https://api.easylink-ai.com/v1/easydoc/extract)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and normalized JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EASYLINK_API_KEY and can save normalized or raw API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
