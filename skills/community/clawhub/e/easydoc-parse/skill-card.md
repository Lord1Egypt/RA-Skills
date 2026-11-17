## Description:

Converts unstructured documents through EasyDoc CN and Global REST APIs into normalized JSON or markdown, with task polling and RAG-safe retrieval guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sycamore792](https://clawhub.ai/user/sycamore792)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to submit documents to EasyDoc, poll asynchronous parse jobs, normalize parse responses, and retrieve relevant content from large parsed JSON outputs without loading full files by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper can send uploaded documents and API keys to an arbitrary user-supplied base URL.

Mitigation: Use only the documented EasyLink and EasyDoc HTTPS endpoints unless the alternate endpoint is fully controlled and trusted.

Risk: Document parsing may transfer confidential or regulated document contents to an external service.

Mitigation: Avoid uploading confidential, medical, legal, financial, or regulated documents unless the service and data-transfer policy are approved.

## Reference(s):

- [EasyDoc REST API Reference](references/easydoc-rest-api.md)
- [ClawHub Skill Page](https://clawhub.ai/sycamore792/skills/easydoc-parse)
- [Sycamore Publisher Profile](https://clawhub.ai/user/sycamore792)
- [EasyLink Platform](https://platform.easylink-ai.com)
- [EasyDoc Platform](https://platform.easydoc.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell examples and a normalized JSON output contract.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The normalized parse envelope contains task_id, status, files, and raw response data.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
